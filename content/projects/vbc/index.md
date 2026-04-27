---
title: vbc
description: >-
  Narzędzie CLI/TUI do wsadowej kompresji wideo do AV1.
full_description: >-
  VBC służy do wsadowej kompresji bibliotek wideo do AV1 z zachowaniem metadanych. Obsługuje enkodowanie przez NVENC albo SVT-AV1, profile jakości dla konkretnych kamer, kolejkę zadań i wznawianie przerwanego procesu. Interfejs TUI pokazuje stan kolejki, użycie GPU i podstawowe statystyki. Narzędzie zachowuje metadane EXIF/XMP/GPS i dopisuje własne tagi VBC. Projekt wymaga Pythona, FFmpeg oraz ExifTool.
date: '2026-04-27'
repo: hipotures/vbc
repo_url: https://github.com/hipotures/vbc
homepage: ''
topics:
- video-compression
- av1
- batch-processing
- python
- tui
- ffmpeg
- metadata
- gpu-acceleration
project_type: tool
summary_en: >-
  VBC is an event-driven batch video compression tool designed for content creators and photographers. It compresses video libraries to the AV1 codec using GPU (NVENC) or CPU (SVT-AV1) acceleration. The tool features intelligent queue management, camera-specific quality presets, and automatic file rotation. It preserves EXIF/XMP/GPS metadata and adds custom VBC tags. VBC includes an interactive terminal user interface (TUI) with a real-time dashboard, GPU monitoring, and dynamic thread control. The architecture follows clean architecture principles with event-driven communication. It supports resuming interrupted processes, file filtering, and a demo mode for testing. The tool requires Python 3.12+, FFmpeg 6.0+, and ExifTool. Error files are logged to a separate directory for easy debugging.
generated: true
listed: true
draft: false
weight: 120
---

## Opis

**VBC** służy do wsadowej kompresji bibliotek wideo do AV1 z zachowaniem metadanych. Obsługuje enkodowanie przez NVENC albo SVT-AV1, profile jakości dla konkretnych kamer, kolejkę zadań i wznawianie przerwanego procesu. Interfejs TUI pokazuje stan kolejki, użycie GPU i podstawowe statystyki. Narzędzie zachowuje metadane EXIF/XMP/GPS i dopisuje własne tagi VBC. Projekt wymaga Pythona, FFmpeg oraz ExifTool.

## Linki

- [GitHub](https://github.com/hipotures/vbc)
