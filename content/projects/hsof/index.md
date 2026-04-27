---
title: HSOF
description: >-
  Eksperymentalny system selekcji cech w Julii.
full_description: >-
  HSOF, czyli Hybrid Search for Optimal Features, to eksperymentalny system selekcji cech napisany w Julii. Pipeline składa się z trzech etapów: szybkiego filtrowania, wyboru podzbioru cech metodą Monte Carlo Tree Search oraz końcowej ewaluacji modelami XGBoost, RandomForest i LightGBM. Konfiguracja jest oparta na plikach YAML, a dane mogą być czytane z SQLite. Repozytorium zawiera przykład dla zbioru Titanic oraz testy jednostkowe dla głównych etapów przetwarzania.
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
summary_en: >-
  HSOF is a hybrid search-based feature selection system implemented in Julia. It executes a three-stage pipeline to reduce feature dimensionality. Stage 1 performs fast filtering using correlation, variance, and mutual information metrics. Stage 2 employs Monte Carlo Tree Search (MCTS) to select a subset of features. Stage 3 conducts final evaluation using XGBoost, RandomForest, and LightGBM models. The system is configured via YAML files and loads data from SQLite databases. It includes an example configuration for the Titanic dataset. The codebase is modular, with separate files for each pipeline stage. Unit tests are provided for each stage of the process.
generated: true
listed: true
draft: false
weight: 180
---

## Opis

**HSOF**, czyli Hybrid Search for Optimal Features, to eksperymentalny system selekcji cech napisany w Julii. Pipeline składa się z trzech etapów: szybkiego filtrowania, wyboru podzbioru cech metodą Monte Carlo Tree Search oraz końcowej ewaluacji modelami XGBoost, RandomForest i LightGBM. Konfiguracja jest oparta na plikach YAML, a dane mogą być czytane z SQLite. Repozytorium zawiera przykład dla zbioru Titanic oraz testy jednostkowe dla głównych etapów przetwarzania.

## Linki

- [GitHub](https://github.com/hipotures/HSOF)
