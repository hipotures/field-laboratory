---
title: minotaur
description: Zaawansowany automatyczny system inżynierii cech używający Monte Carlo Tree Search (MCTS) z enterpriseowym zarządzaniem danymi do przewidywania nawozów rolniczych.
full_description: Minotaur to zaawansowany system automatycznego inżynierii cech oparty na algorytmie Monte Carlo Tree Search (MCTS). Głównym celem projektu jest optymalizacja prognozowania nawożenia w rolnictwie, szczególnie w kontekście konkursu Kaggle 'Predicting Optimal Fertilizers'. System wykorzystuje bazę danych DuckDB z wzorcem repozytorium i pulą połączeń dla wydajnego zarządzania danymi. Oferuje ponad 100 operacji inżynierii cech, w tym statystyczne, wielomianowe oraz domenowe (rolnicze i marynistyczne). Integracja z AutoGluon umożliwia szybkie ocenianie modeli ML z optymalizacją MAP@3. Architektura wspiera modułowe rozszerzanie operacji oraz wykrywanie sygnałów w cechach. System zapewnia zarządzanie sesjami, rejestrację zbiorów danych i śledzenie integralności. Kod jest napisany w Pythonie 3.12 z użyciem Pydantic dla bezpieczeństwa typów. Dokumentacja obejmuje szczegółowe przewodniki po MCTS, inżynierii cech i konfiguracji. Projekt zawiera również system migracji bazy danych i
  mechanizmy backupu.
date: '2026-04-27'
repo: hipotures/minotaur
repo_url: https://github.com/hipotures/minotaur
homepage: ''
topics:
- feature-engineering
- monte-carlo-tree-search
- duckdb
- auto-gluon
- agricultural-ai
- python
- data-science
project_type: tool
summary_en: Minotaur is an advanced automated feature engineering system driven by Monte Carlo Tree Search (MCTS). Its primary focus is optimizing fertilizer prediction for agriculture, specifically targeting the Kaggle 'Predicting Optimal Fertilizers' competition. The architecture utilizes DuckDB with a repository pattern and connection pooling for enterprise-grade data management. It includes over 100 feature engineering operations, covering statistical, polynomial, and domain-specific tasks for agriculture and maritime data. AutoGluon integration allows for rapid ML model evaluation optimized for MAP@3. The system features signal detection to filter low-signal features and supports modular custom operations. It provides robust session management, dataset registration, and integrity tracking via hash-based validation. Built with Python 3.12 and Pydantic, it ensures type safety and clean data access layers. Comprehensive documentation covers MCTS implementation, feature pipelines, and system
  configuration. The project also includes database migration tools and backup systems for reliability.
generated: true
listed: true
draft: false
weight: 200
---

## Opis

**Minotaur** to zaawansowany system automatycznego inżynierii cech oparty na algorytmie Monte Carlo Tree Search (MCTS). Głównym celem projektu jest optymalizacja prognozowania nawożenia w rolnictwie, szczególnie w kontekście konkursu Kaggle 'Predicting Optimal Fertilizers'. System wykorzystuje bazę danych DuckDB z wzorcem repozytorium i pulą połączeń dla wydajnego zarządzania danymi. Oferuje ponad 100 operacji inżynierii cech, w tym statystyczne, wielomianowe oraz domenowe (rolnicze i marynistyczne). Integracja z AutoGluon umożliwia szybkie ocenianie modeli ML z optymalizacją MAP@3. Architektura wspiera modułowe rozszerzanie operacji oraz wykrywanie sygnałów w cechach. System zapewnia zarządzanie sesjami, rejestrację zbiorów danych i śledzenie integralności. Kod jest napisany w Pythonie 3.12 z użyciem Pydantic dla bezpieczeństwa typów. Dokumentacja obejmuje szczegółowe przewodniki po MCTS, inżynierii cech i konfiguracji. Projekt zawiera również system migracji bazy danych i mechanizmy backupu.

## Linki

- [GitHub](https://github.com/hipotures/minotaur)
