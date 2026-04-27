#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import re
import shutil
import subprocess
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
LOCAL_REPO_ALIASES = {
    "tklivetracker": ("ttracker", "ttracker-selenium", "ttracker-gemini"),
}


def build_date() -> str:
    return datetime.now(timezone.utc).date().isoformat()


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
        "--refresh-github",
        action="store_true",
        help="Refresh visible project metadata from GitHub before generating pages.",
    )
    parser.add_argument(
        "--translate-abouts",
        action="store_true",
        help="Translate all project about fields to Polish in one LLM request.",
    )
    parser.add_argument(
        "--no-summary-llm",
        action="store_true",
        help="Do not call the LLM for per-project README summaries; use only matching cache.",
    )
    parser.add_argument(
        "--no-llm",
        action="store_true",
        help="Only for structural tests: use CV about fields and mark pages as draft.",
    )
    parser.add_argument("--force", action="store_true", help="Regenerate cached summaries.")
    parser.add_argument("--limit", type=int, default=0, help="Limit generated projects for tests.")
    parser.add_argument(
        "--only-slugs",
        default="",
        help="Comma-separated project slugs to generate, after applying show_in_terminal filtering.",
    )
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


def parse_slug_filter(value: str) -> set[str]:
    return {slugify(item) for item in value.split(",") if item.strip()}


def filter_projects_by_slug(projects: list[dict[str, Any]], slugs: set[str]) -> list[dict[str, Any]]:
    if not slugs:
        return projects
    selected = [project for project in projects if project_slug(project) in slugs]
    selected_slugs = {project_slug(project) for project in selected}
    missing = sorted(slugs - selected_slugs)
    if missing:
        raise ValueError(f"Unknown or hidden project slugs: {', '.join(missing)}")
    return selected


def normalize_topics(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    topics: list[str] = []
    for item in value:
        if isinstance(item, dict):
            name = str(item.get("name") or item.get("topic", {}).get("name") or "").strip()
        else:
            name = str(item).strip()
        if name:
            topics.append(name)
    return topics


def gh_repo_metadata(repo: str) -> dict[str, Any]:
    result = subprocess.run(
        [
            "gh",
            "repo",
            "view",
            repo,
            "--json",
            "name,description,homepageUrl,repositoryTopics,url",
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    payload = json.loads(result.stdout)
    if not isinstance(payload, dict):
        raise ValueError(f"GitHub metadata for {repo} is not an object")
    return payload


def refresh_projects_from_github(projects: list[dict[str, Any]]) -> list[dict[str, Any]]:
    refreshed: list[dict[str, Any]] = []
    for project in projects:
        repo = str(project.get("repo") or "").strip()
        if not repo:
            continue
        fresh = gh_repo_metadata(repo)
        merged = dict(project)
        merged.update(
            {
                "title": str(fresh.get("name") or project.get("title") or project_slug(project)).strip(),
                "about": str(fresh.get("description") or "").strip(),
                "homepage": str(fresh.get("homepageUrl") or "").strip(),
                "url": str(fresh.get("url") or f"https://github.com/{repo}").strip(),
                "topics": normalize_topics(fresh.get("repositoryTopics")),
            }
        )
        refreshed.append(merged)
    return refreshed


def find_readme(project: dict[str, Any], readme_root: Path) -> Path | None:
    candidates: list[Path] = []
    slug = str(project.get("slug") or "").strip()
    repo_name = str(project.get("repo") or "").rsplit("/", 1)[-1].strip()
    aliases = LOCAL_REPO_ALIASES.get(project_slug(project), ())
    for name in dict.fromkeys([slug, repo_name, project_slug(project), *aliases]):
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


def fetch_github_readme(repo: str) -> str:
    repo = repo.strip()
    if "/" not in repo:
        return ""
    request = urllib.request.Request(
        f"https://api.github.com/repos/{repo}/readme",
        headers={
            "Accept": "application/vnd.github.raw",
            "User-Agent": "field-laboratory-project-generator",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return ""
        raise


def project_readme(project: dict[str, Any], readme_root: Path) -> tuple[str, str]:
    readme_path = find_readme(project, readme_root)
    if readme_path is not None:
        return read_readme(readme_path), str(readme_path)
    repo = str(project.get("repo") or "").strip()
    readme = fetch_github_readme(repo)
    if readme.strip():
        return readme, f"github:{repo}"
    return "", ""


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
  "about_pl": "Polish translation of project about, max 1 sentence",
  "summary_pl": "Polish summary, max 10 sentences",
  "summary_en": "English summary, max 10 sentences",
  "topics": ["3-8 short tags"],
  "project_type": "tool|library|app|game|research|config|other"
}}

Rules:
- Be concrete.
- Do not invent features.
- Use README as the only source for summary_pl, summary_en, topics, and project_type.
- Use project about only to produce about_pl.
- Translate project about into Polish for about_pl.
- Preserve technical terms, product names, library names, protocols, and acronyms in their original form.
- If project about is already Polish, keep it Polish and only clean wording lightly.
- If project about is empty, return an empty string for about_pl.
- No markdown outside JSON.

Project title: {title}
Project about: {about}

README:
{readme[:max_readme_chars]}
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


def request_llm_json(
    *,
    llm_url: str,
    model: str,
    prompt: str,
    max_tokens: int,
    timeout: int,
) -> dict[str, Any]:
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
        raise ValueError(f"LLM response had empty message.content; finish_reason={reason}")
    return extract_json_object(content)


def translate_abouts_with_llm(
    *,
    projects: list[dict[str, Any]],
    llm_url: str,
    model: str,
    max_tokens: int,
    timeout: int,
) -> dict[str, str]:
    payload = [
        {
            "slug": project_slug(project),
            "title": str(project.get("title") or project_slug(project)).strip(),
            "about": " ".join(str(project.get("about") or "").split()),
        }
        for project in projects
        if str(project.get("about") or "").strip()
    ]
    if not payload:
        return {}
    prompt = f"""Translate project descriptions to Polish. Return STRICT JSON only.

Schema:
{{
  "translations": {{
    "project-slug": "Polish translation"
  }}
}}

Rules:
- Translate only the "about" field.
- Keep the translation short: one sentence if possible.
- Preserve technical terms, product names, library names, protocols, and acronyms in their original form.
- Do not invent features.
- If text is already Polish, keep it Polish and only clean wording lightly.
- Return every input slug exactly once.

Projects:
{json.dumps(payload, ensure_ascii=False, indent=2)}
"""
    parsed = request_llm_json(
        llm_url=llm_url,
        model=model,
        prompt=prompt,
        max_tokens=max_tokens,
        timeout=timeout,
    )
    translations = parsed.get("translations")
    if not isinstance(translations, dict):
        raise ValueError('LLM response must contain object field "translations"')
    return {
        str(slug): " ".join(str(text).split())
        for slug, text in translations.items()
        if str(slug).strip() and str(text).strip()
    }


def short_lead(text: str, max_sentences: int = 2, max_chars: int = 260) -> str:
    text = " ".join(str(text).split())
    if not text:
        return ""
    sentences = re.split(r"(?<=[.!?])\s+", text)
    lead = " ".join(sentence for sentence in sentences[:max_sentences] if sentence).strip()
    if not lead:
        lead = text
    if len(lead) <= max_chars:
        return lead
    truncated = lead[: max_chars + 1].rsplit(" ", 1)[0].rstrip(".,;:")
    return f"{truncated}..."


def project_name_variants(project: dict[str, Any]) -> list[str]:
    raw_values = [
        str(project.get("title") or ""),
        str(project.get("slug") or ""),
        str(project.get("repo") or "").rsplit("/", 1)[-1],
        project_slug(project),
    ]
    variants: set[str] = set()
    for raw in raw_values:
        raw = raw.strip()
        if not raw:
            continue
        variants.add(raw)
        parts = [part for part in re.split(r"[-_\s]+", raw) if part]
        if len(parts) > 1:
            variants.add(" ".join(parts))
            variants.add("".join(parts))
            variants.add("".join(part[:1].upper() + part[1:] for part in parts))
    return sorted(variants, key=len, reverse=True)


def highlight_project_names(text: str, project: dict[str, Any]) -> str:
    highlighted = text
    for name in project_name_variants(project):
        if len(name) < 3:
            continue
        pattern = re.compile(rf"(?<![\w*])({re.escape(name)})(?![\w*])", flags=re.IGNORECASE)
        highlighted = pattern.sub(lambda match: f"**{match.group(1)}**", highlighted)
    return highlighted


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
    no_summary_llm: bool,
) -> dict[str, Any]:
    repo = str(project.get("repo") or "").strip()
    about = str(project.get("about") or "").strip()
    title = str(project.get("title") or project_slug(project)).strip()
    empty_summary: dict[str, Any] = {
        "about_pl": "",
        "summary_pl": "",
        "summary_en": "",
        "topics": [],
        "project_type": "",
    }
    if not readme.strip():
        return empty_summary
    digest = sha256_text("\n".join([repo, title, about, readme, model]))
    cache_path = cache_dir / f"{project_slug(project)}.json"
    if not no_llm and cache_path.exists() and not force:
        cached = json.loads(cache_path.read_text(encoding="utf-8"))
        if cached.get("digest") == digest and isinstance(cached.get("summary"), dict):
            return dict(cached["summary"])
    if no_summary_llm and cache_path.exists():
        cached = json.loads(cache_path.read_text(encoding="utf-8"))
        if cached.get("digest") == digest and isinstance(cached.get("summary"), dict):
            return dict(cached["summary"])
    if no_llm:
        return empty_summary
    elif no_summary_llm:
        return empty_summary
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
    translated_about = " ".join(str(project.get("about_pl") or "").split())
    topics = summary.get("topics") if isinstance(summary.get("topics"), list) else []
    topics = [str(topic).strip() for topic in topics if str(topic).strip()]
    summary_pl = str(summary.get("summary_pl") or "").strip()
    summary_en = str(summary.get("summary_en") or "").strip()
    about_pl = translated_about or " ".join(str(summary.get("about_pl") or "").split())
    project_type = str(summary.get("project_type") or "").strip()
    if project_type == "other":
        project_type = ""
    front = {
        "title": title,
        "description": about_pl,
        "full_description": summary_pl,
        "date": build_date(),
        "repo": repo,
        "repo_url": url,
        "homepage": homepage,
        "topics": topics,
        "project_type": project_type,
        "summary_en": summary_en,
        "generated": True,
        "listed": bool(about_pl),
        "draft": draft or not bool(summary_pl),
        "weight": index * 10,
    }
    links = [f"- [GitHub]({url})"]
    if homepage:
        links.append(f"- [Strona projektu]({homepage})")
    body_summary = highlight_project_names(summary_pl, project)
    body_parts = [f"""## Opis

{body_summary}
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
        "date": build_date(),
    }
    body = "Wybrane projekty generowane z lokalnego CV i opisów repozytoriów.\n"
    (output / "_index.md").write_text(front_matter(data) + body, encoding="utf-8")


def remove_legacy_projects_page(output: Path) -> None:
    legacy = output.with_suffix(".md")
    if legacy.exists():
        legacy.unlink()


def prune_stale_generated_projects(output: Path, active_slugs: set[str]) -> None:
    if not output.exists():
        return
    for child in output.iterdir():
        if not child.is_dir() or child.name in active_slugs:
            continue
        index = child / "index.md"
        if not index.exists():
            continue
        content = index.read_text(encoding="utf-8", errors="replace")
        if "generated: true" in content:
            shutil.rmtree(child)


def main() -> int:
    args = parse_args()
    try:
        data = load_yaml(args.cv.expanduser())
        slug_filter = parse_slug_filter(args.only_slugs)
        projects = visible_projects(data)
        projects = filter_projects_by_slug(projects, slug_filter)
        if args.refresh_github:
            projects = refresh_projects_from_github(projects)
        if args.limit > 0:
            projects = projects[: args.limit]
        if args.dry_run:
            for project in projects:
                print(f"{project_slug(project)}\t{project.get('repo')}\t{project.get('title')}")
            return 0
        model = args.model
        if not args.no_llm and model == "auto":
            model = get_auto_model(args.llm_url)
        if args.translate_abouts:
            translations = translate_abouts_with_llm(
                projects=projects,
                llm_url=args.llm_url,
                model=model,
                max_tokens=args.max_tokens,
                timeout=args.timeout,
            )
            for project in projects:
                translated = translations.get(project_slug(project), "")
                if translated:
                    project["about_pl"] = translated
        output = args.output.expanduser()
        if not slug_filter:
            remove_legacy_projects_page(output)
            prune_stale_generated_projects(output, {project_slug(project) for project in projects})
            write_index(output)
        for index, project in enumerate(projects, start=1):
            readme, readme_source = project_readme(project, args.readme_root.expanduser())
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
                no_summary_llm=args.no_summary_llm,
            )
            write_project(output, project_slug(project), project_markdown(project, summary, index, draft=args.no_llm))
            if readme_source:
                print(f"generated {project_slug(project)} from {readme_source}")
            else:
                print(f"generated {project_slug(project)} without README")
    except (
        OSError,
        subprocess.CalledProcessError,
        ValueError,
        yaml.YAMLError,
        urllib.error.URLError,
        json.JSONDecodeError,
    ) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
