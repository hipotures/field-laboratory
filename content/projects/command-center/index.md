---
title: command-center
description: >-
  Lokalna analityka użycia Claude Code oparta na SQLite.
full_description: >-
  Command Center analizuje lokalne logi JSONL z Claude Code i zapisuje metryki w SQLite. Generuje raporty o aktywności, zużyciu tokenów, kosztach modeli i skuteczności cache. Dane można przeglądać w terminalu albo eksportować do PNG. Aktualizacje są przyrostowe, więc kolejne raporty nie wymagają pełnego przetwarzania historii. Projekt korzysta z Pythona, Rich i Pillow, a treści promptów i odpowiedzi nie są wysyłane do zewnętrznych API.
date: '2026-04-27'
repo: hipotures/command-center
repo_url: https://github.com/hipotures/command-center
homepage: ''
topics:
- claude-code
- analytics
- sqlite
- cli-tool
- python
- visualization
- productivity
project_type: tool
summary_en: >-
  Command Center is a modern analytics tool for monitoring Claude Code usage, built on SQLite. It generates visual reports including activity heatmaps, token consumption statistics, and cache efficiency metrics. The application operates locally, processing JSONL logs from Claude configuration directories. It supports incremental updates, ensuring fast report generation on subsequent runs. The tool fetches model pricing data from LiteLLM and tracks current usage streaks. CLI options allow filtering by date, rebuilding the database, and updating project metadata. Results are displayed in the terminal or exported as PNG images. The project uses Python with Pillow and Rich libraries for visualization. It ensures data privacy by not sending prompt or response content to external APIs. Optional features include Telegram integration and a Tauri-based interface.
generated: true
listed: true
draft: false
weight: 100
---

## Opis

**Command Center** analizuje lokalne logi JSONL z Claude Code i zapisuje metryki w SQLite. Generuje raporty o aktywności, zużyciu tokenów, kosztach modeli i skuteczności cache. Dane można przeglądać w terminalu albo eksportować do PNG. Aktualizacje są przyrostowe, więc kolejne raporty nie wymagają pełnego przetwarzania historii. Projekt korzysta z Pythona, Rich i Pillow, a treści promptów i odpowiedzi nie są wysyłane do zewnętrznych API.

## Linki

- [GitHub](https://github.com/hipotures/command-center)
