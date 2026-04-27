---
title: snaptag
description: 'SnapTag to eksperymentalny system pamięci oparty na zrzutach ekranu, działający lokalnie dla pojedynczego użytkownika. Głównym celem jest przekształcanie strumienia zrzutów ekranu w przeszukiwalną, ustrukturyzowaną pamięć oraz sugestie działań. Repozytorium zawiera backend (kodowa nazwa: snapgit) oraz narzędzia do benchmarkingu OCR. Projekt znajduje się w fazie eksperymentalnej, z działającym lokalnie przepływem: pobieranie, OCR, indeksowanie i wyszukiwanie. Backend jest zbudowany w FastAPI z lokalową bazą SQLite. Obsługuje deduplikację plików oraz wyszukiwanie pełnotekstowe. Zawiera skrypty do benchmarkingu modeli OCR, takich jak Tesseract, PaddleOCR oraz modele LLM przez Ollama. Nie zawiera jeszcze aplikacji mobilnej ani pełnego interfejsu użytkownika. API i schemat danych ewoluują, a zmiany mogą być breaking. Projekt wymaga Pythona 3.13+ i menedżera uv.'
date: '2026-04-27'
repo: hipotures/snaptag
repo_url: https://github.com/hipotures/snaptag
homepage: ''
topics:
- screenshot-memory
- ocr
- backend
- fastapi
- local-first
- search-indexing
- python
project_type: tool
summary_en: 'SnapTag is an experimental, local-first screenshot memory system designed for a single user. Its goal is to convert a stream of screenshots into searchable, structured memory and action suggestions. This repository hosts the backend service (codenamed snapgit) and OCR benchmarking tooling. The project is in an active experimental phase with a working local core flow: ingest, OCR, index, and search. The backend is built using FastAPI with local SQLite storage. It features blob deduplication via SHA256 and FTS-style querying. The repo includes benchmark runners for various OCR engines like Tesseract, PaddleOCR, and LLM-based models via Ollama. Mobile app and full product UI are not yet implemented. The API and schema are still evolving, so breaking changes are expected. It requires Python 3.13+ and the uv package manager.'
generated: true
draft: false
weight: 60
---

## Opis

SnapTag to eksperymentalny system pamięci oparty na zrzutach ekranu, działający lokalnie dla pojedynczego użytkownika. Głównym celem jest przekształcanie strumienia zrzutów ekranu w przeszukiwalną, ustrukturyzowaną pamięć oraz sugestie działań. Repozytorium zawiera backend (kodowa nazwa: snapgit) oraz narzędzia do benchmarkingu OCR. Projekt znajduje się w fazie eksperymentalnej, z działającym lokalnie przepływem: pobieranie, OCR, indeksowanie i wyszukiwanie. Backend jest zbudowany w FastAPI z lokalową bazą SQLite. Obsługuje deduplikację plików oraz wyszukiwanie pełnotekstowe. Zawiera skrypty do benchmarkingu modeli OCR, takich jak Tesseract, PaddleOCR oraz modele LLM przez Ollama. Nie zawiera jeszcze aplikacji mobilnej ani pełnego interfejsu użytkownika. API i schemat danych ewoluują, a zmiany mogą być breaking. Projekt wymaga Pythona 3.13+ i menedżera uv.

## Linki

- [GitHub](https://github.com/hipotures/snaptag)
