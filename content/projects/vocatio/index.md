---
title: vocatio
description: Przepływ pracy CLI dla mediów z wydarzeń, skupiony na synchronizacji strumieni (zdjęcia, wideo) i wykrywaniu zestawów.
full_description: 'Vocatio to narzędzie CLI do zarządzania mediami z wydarzeń, koncentrujące się na synchronizacji strumieni wideo i wykrywaniu zestawów zdjęć. Oferuje dwa równoległe potoki przetwarzania dziennego: asystowany audio (z transkrypcją) oraz tylko obrazowy. Potok audio wykorzystuje synchronizację wideo i transkrypcję do budowania granic wystąpień, podczas gdy potok obrazowy opiera się na zdjęciach, jakości i osadzeniach DINOv2. Oba potoki generują artefakty w katalogu _workspace i łączą się z tym samym interfejsem GUI do przeglądu. Projekt wymaga Pythona 3.10+, ffmpeg, exiftool oraz opcjonalnie whisperx lub lokalnych modeli VLM. Obsługuje eksport mediów, mapowanie synchronizacji, transkrypcję i przypisywanie zdjęć do odcinków czasu. Użytkownicy mogą przeglądać i eksportować wybrane zestawy zdjęć za pomocą dedykowanego GUI. Struktura danych opiera się na katalogach dziennych z prefiksami strumieni p-* (zdjęcia) i v-* (wideo).'
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
summary_en: 'Vocatio is a CLI tool for event media workflows, focusing on stream synchronization and set detection for photos and videos. It provides two parallel per-day pipelines: an audio-assisted pipeline using video sync and transcription, and an image-only pipeline relying on photos and embeddings. The audio-assisted mode builds performance boundaries from synced video and transcripts, while the image-only mode uses DINOv2 embeddings and quality signals. Both pipelines output artifacts to a workspace directory and feed a unified review GUI. Requirements include Python 3.10+, ffmpeg, exiftool, and optional dependencies like whisperx or local VLM backends. The tool supports media export, sync estimation, transcription, and photo assignment to timeline intervals. Users can review and export selected photo sets via the GUI. Data is organized in daily directories with specific prefixes for photo (p-*) and video (v-*) streams.'
generated: true
listed: true
draft: false
weight: 30
---

## Opis

**Vocatio** to narzędzie CLI do zarządzania mediami z wydarzeń, koncentrujące się na synchronizacji strumieni wideo i wykrywaniu zestawów zdjęć. Oferuje dwa równoległe potoki przetwarzania dziennego: asystowany audio (z transkrypcją) oraz tylko obrazowy. Potok audio wykorzystuje synchronizację wideo i transkrypcję do budowania granic wystąpień, podczas gdy potok obrazowy opiera się na zdjęciach, jakości i osadzeniach DINOv2. Oba potoki generują artefakty w katalogu _workspace i łączą się z tym samym interfejsem GUI do przeglądu. Projekt wymaga Pythona 3.10+, ffmpeg, exiftool oraz opcjonalnie whisperx lub lokalnych modeli VLM. Obsługuje eksport mediów, mapowanie synchronizacji, transkrypcję i przypisywanie zdjęć do odcinków czasu. Użytkownicy mogą przeglądać i eksportować wybrane zestawy zdjęć za pomocą dedykowanego GUI. Struktura danych opiera się na katalogach dziennych z prefiksami strumieni p-* (zdjęcia) i v-* (wideo).

## Linki

- [GitHub](https://github.com/hipotures/vocatio)
