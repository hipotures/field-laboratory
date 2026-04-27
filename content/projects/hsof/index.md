---
title: HSOF
description: HSOF - Hybrid Search for Optimal Features, uproszczony 3-etapowy system selekcji cech zaimplementowany w Julia.
full_description: HSOF to system doboru cech oparte na hybrydowym wyszukiwaniu, zaimplementowane w języku Julia. Narzędzie realizuje trójstopniowy proces redukcji wymiarowości danych. Pierwszy etap to szybkie filtrowanie cech na podstawie korelacji, wariancji i informacji wzajemnej. Drugi etap wykorzystuje algorytm Monte Carlo Tree Search (MCTS) do selekcji podzbioru cech. Trzeci etap przeprowadza ostateczną ewaluację przy użyciu modeli XGBoost, RandomForest i LightGBM. System konfiguruje się za pomocą plików YAML i obsługuje dane z baz SQLite. Projekt zawiera przykładową konfigurację dla zbioru danych Titanic. Kod jest podzielony na moduły odpowiadające poszczególnym etapom pipeline'u. Dostępne są testy jednostkowe dla każdego etapu procesu.
date: '2026-04-27'
repo: hipotures/HSOF
repo_url: https://github.com/hipotures/HSOF
homepage: ''
topics:
- feature-selection
- julia
- machine-learning
- mcts
- dimensionality-reduction
- data-science
project_type: tool
summary_en: HSOF is a hybrid search-based feature selection system implemented in Julia. It executes a three-stage pipeline to reduce feature dimensionality. Stage 1 performs fast filtering using correlation, variance, and mutual information metrics. Stage 2 employs Monte Carlo Tree Search (MCTS) to select a subset of features. Stage 3 conducts final evaluation using XGBoost, RandomForest, and LightGBM models. The system is configured via YAML files and loads data from SQLite databases. It includes an example configuration for the Titanic dataset. The codebase is modular, with separate files for each pipeline stage. Unit tests are provided for each stage of the process.
generated: true
listed: true
draft: false
weight: 180
---

## Opis

**HSOF** to system doboru cech oparte na hybrydowym wyszukiwaniu, zaimplementowane w języku Julia. Narzędzie realizuje trójstopniowy proces redukcji wymiarowości danych. Pierwszy etap to szybkie filtrowanie cech na podstawie korelacji, wariancji i informacji wzajemnej. Drugi etap wykorzystuje algorytm Monte Carlo Tree Search (MCTS) do selekcji podzbioru cech. Trzeci etap przeprowadza ostateczną ewaluację przy użyciu modeli XGBoost, RandomForest i LightGBM. System konfiguruje się za pomocą plików YAML i obsługuje dane z baz SQLite. Projekt zawiera przykładową konfigurację dla zbioru danych Titanic. Kod jest podzielony na moduły odpowiadające poszczególnym etapom pipeline'u. Dostępne są testy jednostkowe dla każdego etapu procesu.

## Linki

- [GitHub](https://github.com/hipotures/HSOF)
