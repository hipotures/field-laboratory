---
title: gitiary
description: >-
  Lokalny panel aktywności commitów z wielu repozytoriów GitHuba.
full_description: >-
  Gitiary wizualizuje aktywność commitów z wielu repozytoriów GitHuba. Pokazuje wykresy dzienne, heatmapy, regularność pracy, przerwy oraz zmiany w liczbie dodanych i usuniętych linii. Dane są pobierane przez GitHub CLI i zapisywane w SQLite. Interfejs powstał w SvelteKit i TypeScript, a wykresy są renderowane przez Apache ECharts. Projekt wspiera eksport statyczny oraz automatyczne generowanie zrzutów ekranu.
date: '2026-04-27'
repo: hipotures/gitiary
repo_url: https://github.com/hipotures/gitiary
homepage: ''
topics:
- github
- dashboard
- visualization
- sveltekit
- sqlite
- typescript
- analytics
project_type: app
summary_en: >-
  Gitiary is a personal dashboard for visualizing GitHub commit activity across multiple repositories. It provides repository overviews with time range selectors and detailed pages featuring daily charts and calendar heatmaps. The tool enables cross-repository comparison regarding regularity, streaks, and gaps, along with impact analytics for additions, deletions, and file changes. It includes a narrative story view and a settings UI for repository synchronization and activation. Built with SvelteKit, TypeScript, SQLite, and Apache ECharts, it uses the GitHub CLI for data access. Indexing can be automated via CLI commands or systemd timers. The application supports static export and automated screenshot generation for documentation. Repository configuration is stored in a local SQLite database, and API endpoints require protection for secure deployment.
generated: true
listed: true
draft: false
weight: 110
---

## Opis

**Gitiary** wizualizuje aktywność commitów z wielu repozytoriów GitHuba. Pokazuje wykresy dzienne, heatmapy, regularność pracy, przerwy oraz zmiany w liczbie dodanych i usuniętych linii. Dane są pobierane przez GitHub CLI i zapisywane w SQLite. Interfejs powstał w SvelteKit i TypeScript, a wykresy są renderowane przez Apache ECharts. Projekt wspiera eksport statyczny oraz automatyczne generowanie zrzutów ekranu.

## Linki

- [GitHub](https://github.com/hipotures/gitiary)
