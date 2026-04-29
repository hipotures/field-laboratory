# Repository Guidelines

## Project Structure & Module Organization

This repository is a Hugo static site for `armum.eu`, configured in `hugo.toml` and based on the `hugo-coder` theme. Source content lives under `content/`: use `content/posts/<slug>/index.md` for articles and `content/projects/<slug>/index.md` for project pages. Site-specific templates and partial overrides belong in `layouts/`; custom styles belong in `assets/scss/custom.scss`; static files such as favicons, manifests, JavaScript, and standalone CSS belong in `static/`. Keep architecture notes in `docs/` and helper automation in `scripts/`. Do not edit `themes/hugo-coder/` directly; override theme behavior locally instead.

## Build, Test, and Development Commands

- `hugo server -D`: run the local development server, including draft content.
- `hugo --minify --gc --cleanDestinationDir`: build the production site into `public/`, matching the GitHub Actions deploy step.
- `python3 scripts/generate_projects.py --dry-run --no-llm`: validate project-page generation without writing files or calling the local LLM.
- `python3 scripts/generate_projects.py --only-slugs <slug>`: regenerate selected project pages from the configured CV data.

Generated output in `public/`, `resources/_gen/`, `.cache/`, and `tmp/` is ignored and should not be committed.

## Coding Style & Naming Conventions

Use Markdown with YAML front matter for content bundles. Prefer Polish copy for public site content, matching the existing posts. Use lowercase, hyphenated slugs for bundle directories. Declare image resources in front matter when images may matter for galleries; screenshots and diagrams should not be marked as gallery photos. Python scripts use 4-space indentation, type hints where practical, and small functions. Hugo templates use the existing Go-template style in `layouts/`.

## Testing Guidelines

There is no separate test suite. Treat a clean Hugo production build as the main validation gate. For generator changes, run the dry-run command above and, when writing content, inspect the generated `content/projects/<slug>/index.md` diff. For visual or layout changes, also run `hugo server -D` and check the affected page locally.

## Commit & Pull Request Guidelines

Recent commits use short, imperative, sentence-case messages such as `Improve Kempner math formatting` and `Use relative links in local UI`. Keep commits focused: separate content changes, generator changes, and layout changes when practical. Pull requests should describe the visible site change, list validation commands run, link related issues when available, and include screenshots for UI/layout changes.

## Agent-Specific Instructions

Avoid command pipelines that can buffer indefinitely. Do not use `head`, `tail`, `less`, or `more` to truncate output; prefer direct commands or command-specific limits such as `git log -n 10`.
