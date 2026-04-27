---
title: snaptag
description: >-
  Lokalny backend do indeksowania i przeszukiwania zrzutów ekranu.
full_description: >-
  SnapTag to eksperymentalny backend do budowania lokalnej pamięci ze zrzutów ekranu. Obecny zakres obejmuje import plików, OCR, deduplikację, indeksowanie i wyszukiwanie pełnotekstowe. Usługa jest napisana w FastAPI i korzysta z lokalnej bazy SQLite. Repozytorium zawiera też narzędzia do benchmarkingu OCR, między innymi dla Tesseract, PaddleOCR, Ollama, llama.cpp i vLLM. Projekt nie ma jeszcze pełnego interfejsu użytkownika ani aplikacji mobilnej.
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
summary_en: >-
  SnapTag is an experimental local-first screenshot memory system for a single user, aiming to turn screenshots into searchable, structured memory and action suggestions. This repository contains the backend service (codename: snapgit) and OCR benchmarking tooling. The project is in an active experimental phase with a working local core flow for ingestion, OCR, indexing, and search. It implements a FastAPI service with local SQLite storage, blob deduplication, and FTS-style querying. OCR benchmark runners are provided for Tesseract, PaddleOCR, Ollama, llama.cpp, and vLLM. The system supports filesystem backfill ingestion and screenshot categorization. Mobile app and full product UI are not yet implemented. Requirements include Python 3.13+ and uv. The project is licensed under CC0 1.0 Universal.
generated: true
listed: true
draft: false
weight: 60
---

## Opis

**SnapTag** to eksperymentalny backend do budowania lokalnej pamięci ze zrzutów ekranu. Obecny zakres obejmuje import plików, OCR, deduplikację, indeksowanie i wyszukiwanie pełnotekstowe. Usługa jest napisana w FastAPI i korzysta z lokalnej bazy SQLite. Repozytorium zawiera też narzędzia do benchmarkingu OCR, między innymi dla Tesseract, PaddleOCR, Ollama, llama.cpp i vLLM. Projekt nie ma jeszcze pełnego interfejsu użytkownika ani aplikacji mobilnej.

## Linki

- [GitHub](https://github.com/hipotures/snaptag)
