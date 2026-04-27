---
title: tklivetracker
description: Aplikacja Python do monitorowania wybranych użytkowników TikTok, nagrywania ich transmisji na żywo oraz zarządzania procesami z kontrolami stanu przez interfejs webowy.
full_description: Automatyzowana aplikacja Python monitorująca wybranych użytkowników TikToka i nagrywająca ich transmisje na żywo. System wykorzystuje wykrywanie oparte na Selenium, trwałe zarządzanie procesami oraz monitorowanie stanu. Zapewnia efektywne zarządzanie zasobami z limitami pojemności i interfejsem webowym do monitorowania w czasie rzeczywistym. Gwarantuje niezawodność dzięki automatycznemu restartowi, czyszczeniu procesów zombie i odzyskiwaniu po awariach. Obsługuje tryb tylko do odczytu dla bezpiecznego dostępu zewnętrznego. Architektura obejmuje głównego nadzorcy, silnik nagrywania FFmpeg oraz interfejs webowy Flask. Konfiguracja wymaga pliku cookies z TikTok dla uwierzytelnienia. System synchronizuje bazę danych SQLite z aktywnymi procesami nagrywania. Obsługuje różne źródła cookies, w tym pliki JSON i przeglądarkę Firefox.
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
summary_en: Automated Python application that monitors specified TikTok users and records their live streams using Selenium-based detection. It features persistent process management, health monitoring, and a web interface for real-time oversight. The system efficiently manages resources with capacity limits and ensures reliability through automatic restarts and zombie process cleanup. It supports a read-only mode for safe external access and demonstrations. The architecture includes a production supervisor, an FFmpeg-based recording engine, and a Flask web interface. Configuration requires TikTok cookies for authentication, supporting JSON files or Firefox browser extraction. The system synchronizes a SQLite database with active recording processes and handles user states dynamically. It provides comprehensive monitoring capabilities including analytics and historical activity visualization.
generated: true
listed: true
draft: false
weight: 20
---

## Opis

Automatyzowana aplikacja Python monitorująca wybranych użytkowników TikToka i nagrywająca ich transmisje na żywo. System wykorzystuje wykrywanie oparte na Selenium, trwałe zarządzanie procesami oraz monitorowanie stanu. Zapewnia efektywne zarządzanie zasobami z limitami pojemności i interfejsem webowym do monitorowania w czasie rzeczywistym. Gwarantuje niezawodność dzięki automatycznemu restartowi, czyszczeniu procesów zombie i odzyskiwaniu po awariach. Obsługuje tryb tylko do odczytu dla bezpiecznego dostępu zewnętrznego. Architektura obejmuje głównego nadzorcy, silnik nagrywania FFmpeg oraz interfejs webowy Flask. Konfiguracja wymaga pliku cookies z TikTok dla uwierzytelnienia. System synchronizuje bazę danych SQLite z aktywnymi procesami nagrywania. Obsługuje różne źródła cookies, w tym pliki JSON i przeglądarkę Firefox.

## Linki

- [GitHub](https://github.com/hipotures/tklivetracker)
