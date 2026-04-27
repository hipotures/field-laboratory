#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import date
import hashlib
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

import yaml


DEFAULT_CV = Path("~/DEV/config-priv/LifeJourney/cv.yaml").expanduser()
DEFAULT_OUTPUT = Path("content/projects")
DEFAULT_CACHE = Path(".cache/project-summaries")
DEFAULT_LLM_URL = "http://127.0.0.1:8877/v1/chat/completions"
README_NAMES = ("README.md", "Readme.md", "readme.md", "README.MD")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate Hugo project pages from LifeJourney CV project metadata."
    )
    parser.add_argument("--cv", type=Path, default=DEFAULT_CV, help="Path to LifeJourney cv.yaml.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Hugo projects output dir.")
    parser.add_argument("--readme-root", type=Path, default=Path("~/DEV").expanduser())
    parser.add_argument("--cache-dir", type=Path, default=DEFAULT_CACHE)
    parser.add_argument("--llm-url", default=DEFAULT_LLM_URL)
    parser.add_argument("--model", default="auto", help='Model name, or "auto" for first /v1/models entry.')
    parser.add_argument("--max-readme-chars", type=int, default=12000)
    parser.add_argument("--max-tokens", type=int, default=1800)
    parser.add_argument("--timeout", type=int, default=240)
    parser.add_argument(
        "--no-llm",
        action="store_true",
        help="Only for structural tests: use CV about fields and mark pages as draft.",
    )
    parser.add_argument("--force", action="store_true", help="Regenerate cached summaries.")
    parser.add_argument("--limit", type=int, default=0, help="Limit generated projects for tests.")
    parser.add_argument("--dry-run", action="store_true", help="Print selected projects; do not write files.")
    return parser.parse_args()


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing CV YAML: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"CV YAML root must be a mapping: {path}")
    return data


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "project"


def yaml_string(value: Any) -> str:
    return yaml.safe_dump(value, allow_unicode=True, sort_keys=False, width=1000).strip()


def front_matter(data: dict[str, Any]) -> str:
    return "---\n" + yaml_string(data) + "\n---\n\n"


def project_slug(project: dict[str, Any]) -> str:
    slug = str(project.get("slug") or "").strip()
    if slug:
        return slugify(slug)
    repo = str(project.get("repo") or "").strip()
    if repo:
        return slugify(repo.rsplit("/", 1)[-1])
    return slugify(str(project.get("title") or "project"))


def visible_projects(data: dict[str, Any]) -> list[dict[str, Any]]:
    projects = data.get("projects") or []
    if not isinstance(projects, list):
        raise ValueError('CV field "projects" must be a list')
    visible: list[dict[str, Any]] = []
    for raw in projects:
        if not isinstance(raw, dict):
            continue
        if raw.get("show_in_terminal", True) is False:
            continue
        repo = str(raw.get("repo") or "").strip()
        if not repo:
            continue
        visible.append(dict(raw))
    return visible


def find_readme(project: dict[str, Any], readme_root: Path) -> Path | None:
    candidates: list[Path] = []
    slug = str(project.get("slug") or "").strip()
    repo_name = str(project.get("repo") or "").rsplit("/", 1)[-1].strip()
    for name in dict.fromkeys([slug, repo_name, project_slug(project)]):
        if not name:
            continue
        for readme_name in README_NAMES:
            candidates.append(readme_root / name / readme_name)
    for candidate in candidates:
        if candidate.exists() and candidate.is_file():
            return candidate
    return None


def read_readme(path: Path | None) -> str:
    if path is None:
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8", errors="replace")).hexdigest()


def get_auto_model(llm_url: str) -> str:
    models_url = llm_url.rsplit("/", 2)[0] + "/models"
    with urllib.request.urlopen(models_url, timeout=20) as response:
        payload = json.loads(response.read().decode("utf-8"))
    models = payload.get("data") or payload.get("models") or []
    if not models:
        raise ValueError(f"No models returned from {models_url}")
    first = models[0]
    return str(first.get("id") or first.get("model") or first.get("name") or "").strip()


def extract_json_object(raw: str) -> dict[str, Any]:
    raw = raw.strip()
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", raw, flags=re.DOTALL)
        if not match:
            raise
        parsed = json.loads(match.group(0))
    if not isinstance(parsed, dict):
        raise ValueError("LLM response JSON must be an object")
    return parsed


def summarize_with_llm(
    *,
    llm_url: str,
    model: str,
    title: str,
    about: str,
    readme: str,
    max_readme_chars: int,
    max_tokens: int,
    timeout: int,
) -> dict[str, Any]:
    prompt = f"""Read this project metadata and README. Return STRICT JSON only.

Schema:
{{
  "summary_pl": "Polish summary, max 10 sentences",
  "summary_en": "English summary, max 10 sentences",
  "topics": ["3-8 short tags"],
  "project_type": "tool|library|app|game|research|config|other"
}}

Rules:
- Be concrete.
- Do not invent features.
- Use README as primary source and about as fallback.
- No markdown outside JSON.

Project title: {title}
Project about: {about}

README:
{readme[:max_readme_chars] if readme.strip() else "(no README available; use project about as source)"}
"""
    payload = {
        "model": model,
        "temperature": 0,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }
    request = urllib.request.Request(
        llm_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        data = json.loads(response.read().decode("utf-8"))
    message = data["choices"][0]["message"]
    content = str(message.get("content") or "").strip()
    if not content:
        reason = data["choices"][0].get("finish_reason", "unknown")
        raise ValueError(
            f"LLM response had empty message.content; finish_reason={reason}. "
            "If reasoning is enabled, raise --max-tokens or disable reasoning on the server."
        )
    return extract_json_object(content)


def fallback_summary(project: dict[str, Any]) -> dict[str, Any]:
    about = str(project.get("about") or "").strip()
    title = str(project.get("title") or project_slug(project)).strip()
    text = about or title
    topics = project.get("topics") if isinstance(project.get("topics"), list) else []
    return {
        "summary_pl": text,
        "summary_en": "",
        "topics": [str(topic) for topic in topics if str(topic).strip()],
        "project_type": "",
    }


def cached_summary(
    *,
    project: dict[str, Any],
    readme: str,
    cache_dir: Path,
    llm_url: str,
    model: str,
    no_llm: bool,
    force: bool,
    max_readme_chars: int,
    max_tokens: int,
    timeout: int,
) -> dict[str, Any]:
    repo = str(project.get("repo") or "").strip()
    about = str(project.get("about") or "").strip()
    title = str(project.get("title") or project_slug(project)).strip()
    digest = sha256_text("\n".join([repo, title, about, readme, model]))
    cache_path = cache_dir / f"{project_slug(project)}.json"
    if not no_llm and cache_path.exists() and not force:
        cached = json.loads(cache_path.read_text(encoding="utf-8"))
        if cached.get("digest") == digest and isinstance(cached.get("summary"), dict):
            return dict(cached["summary"])
    if no_llm:
        summary = fallback_summary(project)
    else:
        summary = summarize_with_llm(
            llm_url=llm_url,
            model=model,
            title=title,
            about=about,
            readme=readme,
            max_readme_chars=max_readme_chars,
            max_tokens=max_tokens,
            timeout=timeout,
        )
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(
        json.dumps({"digest": digest, "model": model, "summary": summary}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return summary


def project_markdown(project: dict[str, Any], summary: dict[str, Any], index: int, *, draft: bool) -> str:
    title = str(project.get("title") or project_slug(project)).strip()
    repo = str(project.get("repo") or "").strip()
    url = str(project.get("url") or f"https://github.com/{repo}").strip()
    homepage = str(project.get("homepage") or "").strip()
    topics = summary.get("topics") if isinstance(summary.get("topics"), list) else []
    topics = [str(topic).strip() for topic in topics if str(topic).strip()]
    summary_pl = str(summary.get("summary_pl") or project.get("about") or "").strip()
    summary_en = str(summary.get("summary_en") or "").strip()
    project_type = str(summary.get("project_type") or "").strip()
    if project_type == "other":
        project_type = ""
    front = {
        "title": title,
        "description": summary_pl,
        "date": date.today().isoformat(),
        "repo": repo,
        "repo_url": url,
        "homepage": homepage,
        "topics": topics,
        "project_type": project_type,
        "summary_en": summary_en,
        "generated": True,
        "draft": draft,
        "weight": index * 10,
    }
    links = [f"- [GitHub]({url})"]
    if homepage:
        links.append(f"- [Strona projektu]({homepage})")
    body_parts = [f"""## Opis

{summary_pl}
"""]

    body_parts.append(f"""## Linki

{chr(10).join(links)}
""")
    body = "\n".join(body_parts)
    return front_matter(front) + body


def write_project(output: Path, slug: str, content: str) -> None:
    target_dir = output / slug
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "index.md"
    if target.exists() and "generated: true" not in target.read_text(encoding="utf-8", errors="replace"):
        raise ValueError(f"Refusing to overwrite non-generated project page: {target}")
    target.write_text(content, encoding="utf-8")


def write_index(output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    data = {
        "title": "Projekty",
        "description": "Wybrane projekty techniczne i eksperymenty.",
        "date": date.today().isoformat(),
    }
    body = "Wybrane projekty generowane z lokalnego CV i opisów repozytoriów.\n"
    (output / "_index.md").write_text(front_matter(data) + body, encoding="utf-8")


def remove_legacy_projects_page(output: Path) -> None:
    legacy = output.with_suffix(".md")
    if legacy.exists():
        legacy.unlink()


def main() -> int:
    args = parse_args()
    try:
        data = load_yaml(args.cv.expanduser())
        projects = visible_projects(data)
        if args.limit > 0:
            projects = projects[: args.limit]
        if args.dry_run:
            for project in projects:
                print(f"{project_slug(project)}\t{project.get('repo')}\t{project.get('title')}")
            return 0
        model = args.model
        if not args.no_llm and model == "auto":
            model = get_auto_model(args.llm_url)
        output = args.output.expanduser()
        remove_legacy_projects_page(output)
        write_index(output)
        for index, project in enumerate(projects, start=1):
            readme_path = find_readme(project, args.readme_root.expanduser())
            readme = read_readme(readme_path)
            summary = cached_summary(
                project=project,
                readme=readme,
                cache_dir=args.cache_dir,
                llm_url=args.llm_url,
                model=model,
                no_llm=args.no_llm,
                force=args.force,
                max_readme_chars=args.max_readme_chars,
                max_tokens=args.max_tokens,
                timeout=args.timeout,
            )
            write_project(output, project_slug(project), project_markdown(project, summary, index, draft=args.no_llm))
            print(f"generated {project_slug(project)}")
    except (OSError, ValueError, yaml.YAMLError, urllib.error.URLError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
