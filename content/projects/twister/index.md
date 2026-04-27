---
title: twister
description: >-
  Lokalny prototyp do zbierania i oceniania tweetów z X/Twitter.
full_description: >-
  Twister to lokalny prototyp do zbierania tweetów z feedu „For You” na X/Twitterze. Pobieranie treści odbywa się przez połączenie CDP z przeglądarką albo przez Selenium, bez użycia oficjalnego API. Dane są deduplikowane w SQLite i mogą być uzupełniane o embeddingi w Qdrant. Interfejs HTTP pozwala przeglądać tweety pojedynczo i oceniać je, a oceny wpływają na wagi tagów używane przy dalszej selekcji. Aplikacja działa lokalnie i może korzystać z modeli embeddingów offline.
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
summary_en: >-
  Twister is a modular monolith MVP designed to collect tweets from the X/Twitter 'For You' feed. It uses direct CDP browser attachment or Selenium for scraping, bypassing the official API. Collected tweets are deduplicated using SQLite and the vector database Qdrant. The system provides an HTTP interface for reviewing tweets one by one, allowing users to rate them. These ratings dynamically adjust tag weights, influencing the ranking of future collected tweets. The application runs locally without authentication and supports offline embedding models. It automatically starts background scheduler jobs for data collection and retention management upon startup.
generated: true
listed: true
draft: false
weight: 90
---

## Opis

**Twister** to lokalny prototyp do zbierania tweetów z feedu „For You” na X/Twitterze. Pobieranie treści odbywa się przez połączenie CDP z przeglądarką albo przez Selenium, bez użycia oficjalnego API. Dane są deduplikowane w SQLite i mogą być uzupełniane o embeddingi w Qdrant. Interfejs HTTP pozwala przeglądać tweety pojedynczo i oceniać je, a oceny wpływają na wagi tagów używane przy dalszej selekcji. Aplikacja działa lokalnie i może korzystać z modeli embeddingów offline.

## Linki

- [GitHub](https://github.com/hipotures/twister)
