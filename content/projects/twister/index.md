---
title: twister
description: Twister to modularny monolit MVP służący do zbierania tweetów z sekcji „For You” na platformie X/Twitter. Aplikacja wykorzystuje bezpośrednie połączenie CDP z przeglądarką lub Selenium do scrapowania treści bez użycia oficjalnego API. Zbierane dane są deduplikowane za pomocą bazy SQLite oraz wektorowej bazy Qdrant. System oferuje interfejs HTTP do przeglądania tweetów po jednym, z możliwością oceniania ich. Ocenianie wpływa na wagę tagów, co dynamicznie dostosowuje ranking przyszłych tweetów. Aplikacja działa lokalnie, nie wymaga autoryzacji i obsługuje tryb offline dla modeli embeddingów. Domyślnie uruchamia zadania planowane do zbierania danych oraz zarządzania retencją.
date: '2026-04-27'
repo: hipotures/twister
repo_url: https://github.com/hipotures/twister
homepage: ''
topics:
- twitter-scraper
- web-scraping
- deduplication
- semantic-search
- fastapi
- sqlite
- qdrant
- content-curation
project_type: tool
summary_en: Twister is a modular monolith MVP designed to collect tweets from the X/Twitter 'For You' feed. It uses direct CDP browser attachment or Selenium for scraping, bypassing the official API. Collected tweets are deduplicated using SQLite and the vector database Qdrant. The system provides an HTTP interface for reviewing tweets one by one, allowing users to rate them. These ratings dynamically adjust tag weights, influencing the ranking of future collected tweets. The application runs locally without authentication and supports offline embedding models. It automatically starts background scheduler jobs for data collection and retention management upon startup.
generated: true
draft: false
weight: 90
---

## Opis

Twister to modularny monolit MVP służący do zbierania tweetów z sekcji „For You” na platformie X/Twitter. Aplikacja wykorzystuje bezpośrednie połączenie CDP z przeglądarką lub Selenium do scrapowania treści bez użycia oficjalnego API. Zbierane dane są deduplikowane za pomocą bazy SQLite oraz wektorowej bazy Qdrant. System oferuje interfejs HTTP do przeglądania tweetów po jednym, z możliwością oceniania ich. Ocenianie wpływa na wagę tagów, co dynamicznie dostosowuje ranking przyszłych tweetów. Aplikacja działa lokalnie, nie wymaga autoryzacji i obsługuje tryb offline dla modeli embeddingów. Domyślnie uruchamia zadania planowane do zbierania danych oraz zarządzania retencją.

## Linki

- [GitHub](https://github.com/hipotures/twister)
