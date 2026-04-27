---
title: mlarena
description: >-
  Workflow CLI do pracy nad konkursami Kaggle i eksperymentami ML.
full_description: >-
  ML Arena porządkuje pracę nad konkursami Kaggle: inicjalizację projektu, EDA, trening, wysyłanie submissionów i śledzenie wyników. Centralnym punktem jest CLI `mla.py`, które spina skrypty, konfiguracje YAML, profile uruchomień i metadane eksperymentów. Narzędzie zapisuje kontekst uruchomień, w tym hash gita, dzięki czemu łatwiej odtworzyć wynik. Obsługuje także pobieranie score'ów z Kaggle, zarządzanie miejscem na dysku i eksperymenty z Optuna. To infrastruktura robocza do szybkiej, powtarzalnej iteracji w projektach ML.
date: '2026-04-27'
repo: hipotures/mlarena
repo_url: https://github.com/hipotures/mlarena
homepage: ''
topics:
- kaggle
- machine-learning
- workflow
- cli
- python
- auto-gluon
- experiment-tracking
- data-science
project_type: tool
summary_en: >-
  ML Arena provides a standardized workflow for participating in Kaggle competitions. It centers on the `mla.py` CLI, streamlining the ML pipeline from initialization and EDA to model training, submission, and score tracking. The system emphasizes rapid iteration, reproducibility, and modularity. Key features include automated experiment tracking with git hashes, a YAML templating system, and automatic submission and score fetching. It supports execution profiles, disk space management, and Optuna-based hyperparameter tuning. The architecture consists of scripts, a core package, isolated project directories, and a tracking layer linking experiments to code versions.
generated: true
listed: true
draft: false
weight: 10
---

## Opis

ML Arena porządkuje pracę nad konkursami Kaggle: inicjalizację projektu, EDA, trening, wysyłanie submissionów i śledzenie wyników. Centralnym punktem jest CLI `mla.py`, które spina skrypty, konfiguracje YAML, profile uruchomień i metadane eksperymentów. Narzędzie zapisuje kontekst uruchomień, w tym hash gita, dzięki czemu łatwiej odtworzyć wynik. Obsługuje także pobieranie score'ów z Kaggle, zarządzanie miejscem na dysku i eksperymenty z Optuna. To infrastruktura robocza do szybkiej, powtarzalnej iteracji w projektach ML.

## Linki

- [GitHub](https://github.com/hipotures/mlarena)
