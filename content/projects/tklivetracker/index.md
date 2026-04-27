---
title: tklivetracker
description: >-
  Aplikacja do monitorowania transmisji live na TikToku i nagrywania ich przez FFmpeg.
full_description: >-
  tklivetracker monitoruje wybranych użytkowników TikToka i uruchamia nagrywanie, gdy pojawi się transmisja live. Wykrywanie stanu transmisji opiera się na Selenium, a nagrywanie realizuje FFmpeg. Aplikacja ma nadzorcę procesów, limity równoległych nagrań, czyszczenie procesów po awariach i prosty panel webowy we Flasku. Stan nagrań jest synchronizowany z bazą SQLite. Konfiguracja wymaga cookies TikToka, pobieranych z pliku JSON albo z profilu Firefoksa.
date: '2026-04-27'
repo: hipotures/tklivetracker
repo_url: https://github.com/hipotures/tklivetracker
homepage: ''
topics:
- tiktok
- live-stream-recording
- python
- selenium
- ffmpeg
- flask
- automation
- monitoring
project_type: app
summary_en: >-
  Automated Python application that monitors specified TikTok users and records their live streams using Selenium-based detection. It features persistent process management, health monitoring, and a web interface for real-time oversight. The system efficiently manages resources with capacity limits and ensures reliability through automatic restarts and zombie process cleanup. It supports a read-only mode for safe external access and demonstrations. The architecture includes a production supervisor, an FFmpeg-based recording engine, and a Flask web interface. Configuration requires TikTok cookies for authentication, supporting JSON files or Firefox browser extraction. The system synchronizes a SQLite database with active recording processes and handles user states dynamically. It provides comprehensive monitoring capabilities including analytics and historical activity visualization.
generated: true
listed: true
draft: false
weight: 20
---

## Opis

tklivetracker monitoruje wybranych użytkowników TikToka i uruchamia nagrywanie, gdy pojawi się transmisja live. Wykrywanie stanu transmisji opiera się na Selenium, a nagrywanie realizuje FFmpeg. Aplikacja ma nadzorcę procesów, limity równoległych nagrań, czyszczenie procesów po awariach i prosty panel webowy we Flasku. Stan nagrań jest synchronizowany z bazą SQLite. Konfiguracja wymaga cookies TikToka, pobieranych z pliku JSON albo z profilu Firefoksa.

## Linki

- [GitHub](https://github.com/hipotures/tklivetracker)
