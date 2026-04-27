---
title: "Vibe coding - Vibe Operator AI (II)"
date: 2025-03-18
description: "Archiwalna druga część tekstu o vibe codingu: rola Vibe Operatora AI, kompetencje, proces pracy i przykład projektu Sonus."
tags: ["vibe coding", "ai", "programowanie"]
categories: ["artykuly", "archiwum"]
authors: ["Andrzej Marszałek"]
---

## Wstęp

W pierwszej części artykułu opisałem vibe coding, czyli praktykę programowania, w której "osoba" opisuje problem lub pożądaną funkcjonalność w kilku zdaniach, tworząc prompt dla dużego modelu językowego wyspecjalizowanego w generowaniu kodu. Modele językowe mogą generować nie tylko kod programu, ale także konfiguracje, dokumentację itp. Poniżej przedstawiam wizję vibe operatora, osoby, która jest w stanie wygenerować pełny produkt, posiadając odpowiednie przygotowanie oraz podam realny przykład działania vibe operatora.

## Vibe operator

Kilka tygodni temu, gdy pojęcie vibe codingu nie było jeszcze powszechne, tworząc kod od zera przy użyciu AI, nie widziałem, jak się nazywa to co robię, ale widziałem, że jest to niezła zabawa. Nazwałem swoją rolę Operatorem AI, aktualnie Vibe Operatorem AI, albo po prostu Vibe Operatorem. Vibe operator to specjalista, który wykorzystuje modele językowe oraz wyspecjalizowanych agentów (np. w zakresie kodowania, deep research itp.) do tworzenia kompletnych rozwiązań produktowych. Vibe Operator polega na AI w zakresie generowania kodu, konfiguracji, dokumentacji i testowania, niekoniecznie będąc ekspertem w każdej dziedzinie, w której tworzy produkt. Vibe Operator to specjalista, który wykorzystuje sztuczną inteligencję do tworzenia pełnych rozwiązań produktowych, np. takich jak kod w Pythonie, konfigurację infrastruktury w GCP pod produkt w Terraformie, dokumentację na dowolnym poziomie szczegółowości, testy jednostkowe i integracyjne, itp. Kluczową cechą tej roli jest zdolność do tworzenia rozwiązań w różnych dziedzinach bez konieczności posiadania dogłębnej, wcześniejszej wiedzy specjalistycznej. Vibe Operator wykorzystuje AI do analizowania tematów, przyswajania wiedzy i generowania niezbędnych komponentów.

Zakres obowiązków Vibe Operatora AI jest szeroki i obejmuje różne etapy cyklu życia oprogramowania:

- Generowanie kodu w różnych językach programowania
- Tworzenie konfiguracji infrastruktury (np. Terraform, Ansible, CloudFormation, dbt, Dataform, itp)
- Opracowywanie kompleksowej dokumentacji
- Generowanie testów jednostkowych, walidacyjnych i integracyjnych
- Dostarczanie szczegółowych opisów procesu tworzenia rozwiązania
- Analizowanie nowych tematów i szybkiego zdobywanie wiedzy przy użyciu AI
- Iteracyjne udoskonalanie wyników generowanych przez AI poprzez konwersacyjne prompty
- Potencjalne zarządzanie i integracja różnych agentów AI do obsługi konkretnych zadań

## Wymagane umiejętności i kompetencje

Aby efektywnie pełnić rolę Vibe Operatora, niezbędny jest konkretny zestaw umiejętności:

- Zaawansowane umiejętności prompt engineeringu: Zdolność do formułowania jasnych, konkretnych i efektywnych instrukcji dla modeli AI
- Podstawowa wiedza o programowaniu: Zrozumienie podstawowych koncepcji programistycznych, aby móc weryfikować i modyfikować kod generowany przez AI
- Umiejętność szybkiego uczenia się: Zdolność do szybkiego przyswajania wiedzy z różnych dziedzin przy pomocy AI
- Zdolność krytycznej oceny: Umiejętność oceny jakości, bezpieczeństwa i poprawności kodu generowanego przez AI
- Myślenie systemowe i produktowe: Zrozumienie, jak poszczególne komponenty łączą się w całość i jak tworzyć użyteczne produkty
- Podstawowa wiedza z zakresu bezpieczeństwa aplikacji: Świadomość potencjalnych zagrożeń bezpieczeństwa w kodzie
- Znajomość narzędzi AI: Biegłość w obsłudze różnych modeli językowych i asystentów kodowania
- Umiejętność Zarządzania Projektem: Planowanie, organizowanie i monitorowanie postępu prac

## Narzędzia i Technologie Wykorzystywane przez Vibe Operatora

Vibe Operator korzysta z szerokiego wachlarza narzędzi i technologii:

- Duże modele językowe (LLM): GPT-4.5/GPT-4o/o3 (OpenAI), Claude 3.5/3.7 Sonnet (Anthropic), Gemini 2.0 Pro/Flash (Google), Code Llama 3 (Meta)
- Agenty i asystenci kodowania AI: Cursor, GitHub Copilot, Replit AI Agent/Ghostwriter, Amazon Q Developer/CodeWhisperer, Zencoder, Cline, Roo Code
- Platformy do budowania agentów AI: Vertex AI Agent Builder, Relevance AI, AutoGen, AgentGPT
- Narzędzia do Zarządzania Infrastrukturą jako Kod (IaC): Terraform, AWS CloudFormation, Azure Resource Manager, Dataform
- Systemy Kontroli Wersji: Git
- Narzędzia do Testowania: Pytest, JUnit, Selenium
- Narzędzia do Dokumentacji: Sphinx, Docusaurus
- Środowiska Programistyczne (IDE): VS Code, IntelliJ IDEA, PyCharm
- Platformy Chmurowe: Google Cloud Platform (GCP), Amazon Web Services (AWS), Microsoft Azure

## Proces pracy vibe operatora

Proces pracy vibe operatora zazwyczaj obejmuje następujące kroki:

- Analiza wymagań: Zrozumienie potrzeb klienta lub projektu
- Badanie tematu: Wykorzystanie AI do zdobycia wiedzy w danej dziedzinie
- Tworzenie promptów: Formułowanie precyzyjnych instrukcji dla AI
- Generowanie kodu i konfiguracji: Używanie AI do tworzenia niezbędnych komponentów
- Testowanie: Weryfikacja poprawności i jakości wygenerowanych rozwiązań
- Dokumentowanie: Tworzenie dokumentacji technicznej i użytkowej
- Wdrażanie: Konfigurowanie i uruchamianie rozwiązania
- Monitorowanie i Utrzymanie: Nadzorowanie działania systemu i wprowadzanie ewentualnych poprawek

Obecnie etapy 1–3 oraz 4–7 powinny zajmować mniej więcej po 50% czasu pracy. Jeśli etapy 1–3 nie zostaną odpowiednio przygotowane, wzrasta nakład pracy w etapach 4–7, co przekłada się na wyższe koszty (m.in. w zakresie promptów i refaktoryzacji kodu).

## Wyzwania i ograniczenia roli vibe operatora

Koncepcja vibe operatora wiąże się również z wyzwaniami i wadami:

- Zrozumienie produktu: Pełne udokumentowanie potrzeb klienta dotyczących produktu
- Wszystkie minusy vibe codingu: Opisane we wcześniejszym artykule
- Nadmierna zależność od AI: Ryzyko ograniczenia dalszego rozwoju operatora
- Utrzymanie kontroli nad AI: Zapewnienie, że vibe operator rozumie generowane rozwiązania w rozsądnym stopniu

## Jak zostać vibe operatorem?

Aby zostać vibe operatorem, warto skupić się na rozwoju następujących obszarów:

- Rozwijaj wyobraźnię :)
- Zdobądź podstawową wiedzę z zakresu programowania i IT
- Śledź aktualne newsy technologiczne (stwórz odpowiednich agentów)
- Buduj i aktualizuj bibliotekę narzędzi technologicznych IT (stwórz odpowiednich agentów)
- Naucz się efektywnie tworzyć prompty dla modeli językowych
- Rozwijaj umiejętności testowania i weryfikacji kodu (stwórz odpowiednich agentów)
- Buduj portfolio projektów, wykorzystując podejście vibe coding

## Przykład działania w trybie vibe operatora

### Potrzeba

Google nie udostępniało (styczeń/luty 2025) narzędzi do automatycznej transkrypcji spotkań Google Meet w języku polskim. Można było jedynie zapisać spotkanie jako plik audio/wideo (gdrive). Pojawiła się potrzeba transkrypcji tych plików z rozpoznawaniem osób i przypisaniem ich do konkretnych wypowiedzi oraz tworzenia podsumowania na podstawie tego pliku z opcją półautomatycznego wystawiania ticketów w Jira.

### Research i analiza tematu

Po przeprowadzeniu analizy (Deep Research) wybrałem narzędzie WhisperX [1]. Zapoznałem się z wiedzą dotyczącą transkrypcji i diaryzacji [2]. Wybrałem nazwę projektu: Sonus.

### Wybór technologii

W GCP istnieje kilka opcji, ze względu na prognozowaną używalność (niska, 5-10 transkrypcji dziennie) wybrałem najtańszą opcję: CloudRun. Do tego PubSub, secrets, gcs oraz CI/CD: cloud-source, cloud-build, artifact-registry.

### Wybór architektury rozwiązania

Rozwiązanie podzieliłem na dwie niezależne części:

- activator - kod służący do poszukiwania źródeł z plikami multimedialnymi na udostępnionych zasobach (gdrive, gcs, ftp), tworzący jsona zawierającego informacje o pliku do przetwarzania. Każdy plik tworzył osobnego jsona, który lądował w kolejce PubSub. Aktywator uruchamiał się cyklicznie
- transcriber - kod pobierający jsona z PubSub i plik z danego udostępnionego miejsca, na którym wykonywała się transkrypcja i diaryzacja. Wyniki były zapisywane w lokalizacji pliku źródłowego. Transkryber uruchamiał się cyklicznie, ograniczyłem maksymalną liczba równoległych instancji

### Praca z AI

Używając modelu o3-mini-high stworzyłem plik StepByStep.md zawierający wszystkie kroki budowy architektury. Stworzyłem także README.md, zawierający ogólny opis projektu. Po zakończeniu budowy wygenerowałem także kod budujący 10 arkuszy prezentacji Google Slides z przedstawieniem Projektu Sonus.

Przykładowy prompt do budowy i aktualizacji pliku README.md
Przykładowy prompt do budowy i aktualizacji pliku StepByStep.md

Po stworzeniu i dopracowaniu pliku StepByStep (który i tak był aktualizowany wielokrotnie w czasie budowy) przystąpiłem do kodowania. Użyłem VS Code z pluginami Cline [3] oraz RooCode [4].

Krok po kroku zbudowałem kod, infrastrukturę, dokumentację oraz katalog z przykładami plików multimedialnych (m.in. do testów). Ze względu na to, że był to mój pierwszy tak duży projekt, przeprowadzałem kilka refaktoryzacji kodu. Przetestowałem kilka modeli LLM, także opensource (posiadam lokalny serwer 2x4090+192GB RAM). TOP1 został Claude 3.5 Sonnet [5], pomimo prób przestawienia się na tańsze modele, zawsze wracałem do C3.5S. Działałem półautomatycznie, pozwalałem na automatyczną modyfikację, ale przed zapisem przeglądałem zmiany (ze względu na wcześniejsze problemy z urywaniem plików). Każda zmiana przed wypchnięciem do Cloud Source była odnotowywana w CHANGELOG.md

### Przykład

Wystartowałem w piątek po południu, zakończyłem budowę w poniedziałek, całość zajęła mi około 40 godzin. Koszt tokenów ~5 tysięcy złotych. Praca w vibe codingu przypomina sinusoidę – czasami model idealnie łapie intencje, a innym razem niszczy połowę kodu, co zmusza do cofania zmian i rozpoczynania pracy od nowa. Częściowo problemy wynikały z niezachowania limitu 500 linii w plikach. W przypadku narzędzia Cline, gdy występowały problemy z metodą 'diff', system przełączał się na pełną aktualizację, co często prowadziło do urywania kodu. Dodatkowo w Vertexie AI, w czasie budowy tego projektu nie było dostępnej opcji prompt cache, która pojawiła kilka dni późnej. Prawdopodobnie pozwoliłoby to zredukować koszty 4x.

### Wyprodukowany tekst

- kody python: ~5000 linii
- kod terraform: ~1500 linii
- plik StepByStep: ~2500 linii
- inne pliki tekstowe .md: -2500 linii
- pozostałe pliki (yaml, Dockerfile, itp): ~1000 linii

## Podsumowanie

Specjalizacja w IT powoli dobiega końca. Oczywiście nie jest tak, że wypromptujesz konfigurację wszystkiego, przynajmniej jeszcze nie dzisiaj a przynajmniej dzisiaj jeszcze nie mamy wystarczającego zaufania do AI. Z biegiem czasu to się zmieni. Niedługo pojawią się prawdziwe jednoosobowe firmy zarządzane przez sterowane lub samodzielne AI. Ciekawe, kiedy pojawi się pierwsza jednoosobowa firma zarządzana przez AI, która osiągnie kapitalizację miliarda dolarów. Czy można będzie mówić, że to firma jednoosobowa czy może multiagentowa?

Z drugiej strony, przy tak szybkim rozwoju AI, zawód vibe operatora może błysnąć tylko na chwilę, po czym pozostanie jedynie żartobliwy skrót
