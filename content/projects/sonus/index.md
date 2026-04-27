---
title: sonus
description: Sonus to skalowalny, chmurowy system automatycznej transkrypcji i diarizacji zbudowany na Google Cloud Platform (GCP), wykorzystujący WhisperX do wysokiej precyzji konwersji mowy na tekst z identyfikacją mówcy.
full_description: 'Sonus to skalowalny, chmurowy system automatycznej transkrypcji i diarizacji zbudowany na Google Cloud Platform. Wykorzystuje WhisperX do precyzyjnej konwersji mowy na tekst oraz identyfikacji mówców. Architektura opiera się na Cloud Run Jobs i Pub/Sub do asynchronicznego przetwarzania zadań. System skanuje źródła, takie jak Google Drive, w poszukiwaniu nowych plików audio i wideo. Obsługuje formaty mp3, wav, m4a, flac, mp4, mov, avi oraz mkv. Infrastruktura jest zarządzana za pomocą Terraform lub OpenTofu. Projekt składa się z dwóch głównych komponentów: aktywatora i transkrybera. Kod źródłowy jest napisany w Pythonie i testowany przy użyciu pytest. Wymaga konta GCP, Dockera oraz Pythona 3.11+. Licencja CC0 1.0 Universal pozwala na swobodne wykorzystanie projektu.'
date: '2026-04-27'
repo: hipotures/sonus
repo_url: https://github.com/hipotures/sonus
homepage: ''
topics:
- transcription
- diarization
- whisperx
- google-cloud-platform
- terraform
- python
- cloud-run
- pub-sub
project_type: tool
summary_en: Sonus is a scalable, cloud-native automated transcription and diarization system built on Google Cloud Platform. It leverages WhisperX for high-accuracy speech-to-text conversion and speaker identification. The architecture uses Cloud Run Jobs and Pub/Sub for asynchronous task processing. An activator component scans sources like Google Drive for new audio and video files. Supported formats include mp3, wav, m4a, flac, mp4, mov, avi, and mkv. Infrastructure is managed as code using Terraform or OpenTofu. The system consists of an activator service and a transcriber worker. The codebase is written in Python and tested with pytest. Prerequisites include a GCP account, Docker, and Python 3.11+. The project is released under the CC0 1.0 Universal license.
generated: true
listed: true
draft: false
weight: 150
---

## Opis

**Sonus** to skalowalny, chmurowy system automatycznej transkrypcji i diarizacji zbudowany na Google Cloud Platform. Wykorzystuje WhisperX do precyzyjnej konwersji mowy na tekst oraz identyfikacji mówców. Architektura opiera się na Cloud Run Jobs i Pub/Sub do asynchronicznego przetwarzania zadań. System skanuje źródła, takie jak Google Drive, w poszukiwaniu nowych plików audio i wideo. Obsługuje formaty mp3, wav, m4a, flac, mp4, mov, avi oraz mkv. Infrastruktura jest zarządzana za pomocą Terraform lub OpenTofu. Projekt składa się z dwóch głównych komponentów: aktywatora i transkrybera. Kod źródłowy jest napisany w Pythonie i testowany przy użyciu pytest. Wymaga konta GCP, Dockera oraz Pythona 3.11+. Licencja CC0 1.0 Universal pozwala na swobodne wykorzystanie projektu.

## Linki

- [GitHub](https://github.com/hipotures/sonus)
