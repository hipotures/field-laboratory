---
title: snaptag
description: SnapTag to lokalny system pamięci zrzutów ekranu przeznaczony dla pojedynczego użytkownika.
full_description: 'SnapTag to eksperymentalny system lokalnej pamięci zrzutów ekranu dla jednego użytkownika, którego celem jest zamiana strumienia zrzutów w przeszukiwalną, ustrukturyzowaną pamięć i sugestie działań. Repozytorium zawiera backend (kodowa nazwa: snapgit) oraz narzędzia do benchmarkingu OCR. Projekt znajduje się w fazie eksperymentalnej, gdzie działa lokalnie przepływ ingestii, OCR, indeksowania i wyszukiwania. Zaimplementowano usługę FastAPI z lokalną bazą SQLite, deduplikację blobów oraz pipeline wyszukiwania. Dostępne są skrypty do benchmarkingu modeli OCR, takich jak Tesseract, PaddleOCR, Ollama, llama.cpp i vLLM. System obsługuje ingestję z systemu plików oraz wyszukiwanie pełnotekstowe. Nie zaimplementowano jeszcze aplikacji mobilnej ani pełnego interfejsu użytkownika. Wymagania to Python 3.13+ oraz menedżer uv. Projekt jest licencjonowany na CC0 1.0 Universal.'
date: '2026-04-27'
repo: hipotures/snaptag
repo_url: https://github.com/hipotures/snaptag
homepage: ''
topics:
- screenshot-memory
- local-first
- ocr
- fastapi
- search-indexing
- python
- sqlite
project_type: tool
summary_en: 'SnapTag is an experimental local-first screenshot memory system for a single user, aiming to turn screenshots into searchable, structured memory and action suggestions. This repository contains the backend service (codename: snapgit) and OCR benchmarking tooling. The project is in an active experimental phase with a working local core flow for ingestion, OCR, indexing, and search. It implements a FastAPI service with local SQLite storage, blob deduplication, and FTS-style querying. OCR benchmark runners are provided for Tesseract, PaddleOCR, Ollama, llama.cpp, and vLLM. The system supports filesystem backfill ingestion and screenshot categorization. Mobile app and full product UI are not yet implemented. Requirements include Python 3.13+ and uv. The project is licensed under CC0 1.0 Universal.'
generated: true
listed: true
draft: false
weight: 60
---

## Opis

**SnapTag** to eksperymentalny system lokalnej pamięci zrzutów ekranu dla jednego użytkownika, którego celem jest zamiana strumienia zrzutów w przeszukiwalną, ustrukturyzowaną pamięć i sugestie działań. Repozytorium zawiera backend (kodowa nazwa: snapgit) oraz narzędzia do benchmarkingu OCR. Projekt znajduje się w fazie eksperymentalnej, gdzie działa lokalnie przepływ ingestii, OCR, indeksowania i wyszukiwania. Zaimplementowano usługę FastAPI z lokalną bazą SQLite, deduplikację blobów oraz pipeline wyszukiwania. Dostępne są skrypty do benchmarkingu modeli OCR, takich jak Tesseract, PaddleOCR, Ollama, llama.cpp i vLLM. System obsługuje ingestję z systemu plików oraz wyszukiwanie pełnotekstowe. Nie zaimplementowano jeszcze aplikacji mobilnej ani pełnego interfejsu użytkownika. Wymagania to Python 3.13+ oraz menedżer uv. Projekt jest licencjonowany na CC0 1.0 Universal.

## Linki

- [GitHub](https://github.com/hipotures/snaptag)
