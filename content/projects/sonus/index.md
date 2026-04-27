---
title: sonus
description: >-
  System transkrypcji i diarizacji oparty na WhisperX oraz usługach GCP.
full_description: >-
  Sonus automatyzuje transkrypcję i diarizację plików audio oraz wideo. Przetwarzanie opiera się na WhisperX, a zadania są uruchamiane w Google Cloud Platform przez Cloud Run Jobs i Pub/Sub. Komponent aktywatora wyszukuje nowe pliki, a transkryber wykonuje właściwe przetwarzanie. Infrastruktura jest opisana w Terraform/OpenTofu, a kod aplikacyjny jest napisany w Pythonie.
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
summary_en: >-
  Sonus is a scalable, cloud-native automated transcription and diarization system built on Google Cloud Platform. It leverages WhisperX for high-accuracy speech-to-text conversion and speaker identification. The architecture uses Cloud Run Jobs and Pub/Sub for asynchronous task processing. An activator component scans sources like Google Drive for new audio and video files. Supported formats include mp3, wav, m4a, flac, mp4, mov, avi, and mkv. Infrastructure is managed as code using Terraform or OpenTofu. The system consists of an activator service and a transcriber worker. The codebase is written in Python and tested with pytest. Prerequisites include a GCP account, Docker, and Python 3.11+. The project is released under the CC0 1.0 Universal license.
generated: true
listed: true
draft: false
weight: 150
---

## Opis

**Sonus** automatyzuje transkrypcję i diarizację plików audio oraz wideo. Przetwarzanie opiera się na WhisperX, a zadania są uruchamiane w Google Cloud Platform przez Cloud Run Jobs i Pub/Sub. Komponent aktywatora wyszukuje nowe pliki, a transkryber wykonuje właściwe przetwarzanie. Infrastruktura jest opisana w Terraform/OpenTofu, a kod aplikacyjny jest napisany w Pythonie.

## Linki

- [GitHub](https://github.com/hipotures/sonus)
