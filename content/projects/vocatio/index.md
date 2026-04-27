---
title: vocatio
description: >-
  CLI do synchronizacji zdjęć i wideo z wydarzeń oraz wyboru zestawów zdjęć.
full_description: >-
  Vocatio wspiera pracę z materiałem z wydarzeń: zdjęciami, wideo, transkrypcją i eksportem wybranych zestawów. Ma dwa tryby przetwarzania dziennego. Pierwszy wykorzystuje synchronizację wideo i transkrypcję do wyznaczania odcinków czasu. Drugi działa tylko na obrazach, jakości zdjęć i embeddingach DINOv2. Oba tryby zapisują artefakty w katalogu _workspace i prowadzą do tego samego GUI do przeglądu oraz eksportu. Projekt wymaga Pythona, ffmpeg i exiftool, a opcjonalnie korzysta z whisperx albo lokalnych modeli VLM.
date: '2026-04-27'
repo: hipotures/vocatio
repo_url: https://github.com/hipotures/vocatio
homepage: ''
topics:
- media-processing
- cli-tool
- video-sync
- photo-management
- event-workflow
- transcription
- computer-vision
project_type: tool
summary_en: >-
  Vocatio is a CLI tool for event media workflows, focusing on stream synchronization and set detection for photos and videos. It provides two parallel per-day pipelines: an audio-assisted pipeline using video sync and transcription, and an image-only pipeline relying on photos and embeddings. The audio-assisted mode builds performance boundaries from synced video and transcripts, while the image-only mode uses DINOv2 embeddings and quality signals. Both pipelines output artifacts to a workspace directory and feed a unified review GUI. Requirements include Python 3.10+, ffmpeg, exiftool, and optional dependencies like whisperx or local VLM backends. The tool supports media export, sync estimation, transcription, and photo assignment to timeline intervals. Users can review and export selected photo sets via the GUI. Data is organized in daily directories with specific prefixes for photo (p-*) and video (v-*) streams.
generated: true
listed: true
draft: false
weight: 30
---

## Opis

**Vocatio** wspiera pracę z materiałem z wydarzeń: zdjęciami, wideo, transkrypcją i eksportem wybranych zestawów. Ma dwa tryby przetwarzania dziennego. Pierwszy wykorzystuje synchronizację wideo i transkrypcję do wyznaczania odcinków czasu. Drugi działa tylko na obrazach, jakości zdjęć i embeddingach DINOv2. Oba tryby zapisują artefakty w katalogu _workspace i prowadzą do tego samego GUI do przeglądu oraz eksportu. Projekt wymaga Pythona, ffmpeg i exiftool, a opcjonalnie korzysta z whisperx albo lokalnych modeli VLM.

## Linki

- [GitHub](https://github.com/hipotures/vocatio)
