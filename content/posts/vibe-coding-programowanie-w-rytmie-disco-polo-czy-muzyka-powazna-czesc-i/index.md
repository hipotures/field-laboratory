---
title: "Vibe coding - programowanie w rytmie disco polo czy muzyka poważna? (część I)"
date: 2025-03-18
description: "Archiwalny tekst o vibe codingu, jego historii, narzędziach, zaletach, wadach i praktycznym znaczeniu dla programowania."
tags: ["vibe coding", "ai", "programowanie"]
categories: ["artykuly", "archiwum"]
authors: ["Andrzej Marszałek"]
---

## Wstęp

W świecie sztucznej inteligencji metody tworzenia oprogramowania przechodzą kolejną ewolucję. Jednym z najnowszych i najbardziej gorących trendów jest koncepcja Vibe Codingu (vibecoding) [0]. Termin ten, spopularyzowany przez Andreja Karpathy'ego, rewolucjonizuje tradycyjne podejście do programowania, oddając znaczną część procesu w ręce sztucznej inteligencji. Niniejszy artykuł ma na celu przybliżenie idei vibe codingu.

## Krótka historia czasu

Termin "vibe coding" po raz pierwszy pojawił się w lutym 2025 roku za sprawą Andreja Karpathy'ego [1]. Opisał on to podejście jako intuicyjny sposób kodowania, oparty na "wyczuciu" i wykorzystujący język naturalny do instruowania modeli AI w celu generowania kodu.

> There's a new kind of coding I call "vibe coding", where you fully give in to the vibes, embrace exponentials, and forget that the code even exists. It's possible because the LLMs (e.g. Cursor Composer w Sonnet) are getting too good. Also I just talk to Composer with SuperWhisper so I barely even touch the keyboard. I ask for the dumbest things like "decrease the padding on the sidebar by half" because I'm too lazy to find it. I "Accept All" always, I don't read the diffs anymore. When I get error messages I just copy paste them in with no comment, usually that fixes it. The code grows beyond my usual comprehension, I'd have to really read through it for a while. Sometimes the LLMs can't fix a bug so I just work around it or ask for random changes until it goes away. It's not too bad for throwaway weekend projects, but still quite amusing. I'm building a project or webapp, but it's not really coding - I just see stuff, say stuff, run stuff, and copy paste stuff, and it mostly works.

Jego słowa szybko zdobyły popularność. Już w kolejnym miesiącu termin ten trafił do słownika Merriam-Webster jako określenie slangowe [2].

Czym zatem jest vibe coding? W najprostszym ujęciu jest to praktyka programowania, w której osoba opisuje problem lub pożądaną funkcjonalność w kilku zdaniach, tworząc prompt dla dużego modelu językowego wyspecjalizowanego w generowaniu kodu. Zamiast ręcznie pisać każdą linię kodu i debugować go, programista "poddaje się wibracjom" i pozwala AI generować oraz modyfikować kod na podstawie instrukcji w języku naturalnym.

Proces ten często ma charakter iteracyjny i konwersacyjny. Użytkownik formułuje polecenia w prostym języku, a AI generuje kod, który następnie jest weryfikowany i udoskonalany poprzez kolejne prompty. Kluczowym aspektem vibe codingu jest fakt, że użytkownik może akceptować wygenerowany kod bez pełnego zrozumienia jego wewnętrznej implementacji. To odróżnia go od tradycyjnego programowania wspomaganego przez AI, gdzie programista zazwyczaj analizuje i rozumie wygenerowany kod.

## Od asemblera do tokenizera

Idea vibe codingu nie jest całkowicie nowa. Stanowi ona kolejny krok upraszczania programowania poprzez podnoszenie poziomu abstrakcji. Od kodu maszynowego, przez asembler, języki wysokiego poziomu, aż po frameworki - programiści od zawsze szukali bardziej intuicyjnych narzędzi.

Vibe coding idzie dalej w tych poszukiwaniach, próbując całkowicie oddać szczegóły implementacyjne w ręce AI, pozwalając człowiekowi skupić się na logice i koncepcji działania aplikacji. Można to postrzegać jako ewolucję idei pełnego "no-code", a pojawienie się zaawansowanych modeli AI generujących kod umożliwiło realizację tej wizji na szerszą skalę.

Pierwsze inteligentne asystenty programowania, oferujące zaawansowane podpowiedzi kodu i analizę statyczną, pojawiły się już w latach 2010 (IntelliJ IDEA). Przełom nastąpił w 2021 roku wraz z prezentacją modelu Codex przez OpenAI i wypuszczeniem GitHub Copilota. Te narzędzia, oparte na AI, zaczęły podpowiadać fragmenty kodu na podstawie kontekstu i komentarzy.

Kolejnym ważnym momentem była publiczna premiera ChatGPT 3.5 w 2022 roku. Zdolność do prowadzenia dialogu i generowania działającego kodu nawet dla złożonych zadań pokazała, że, cytując Andreja Karpathy'ego [3]:

> The hottest new programming language is English

Rok 2023 przyniósł gwałtowny wzrost popularności narzędzi AI do kodowania. W 2025 roku vibe coding stał się jednym z kluczowych trendów w branży IT, dyskutowanym jako potencjalna "nowa era programowania".

## Prompty i techniki stosowane w vibe codingu

Efektywne korzystanie z vibe codingu wymaga umiejętnego "rozmawiania" z AI poprzez tworzenie odpowiednich promptów. Kluczowe techniki to:

- **Opisy w języku naturalnym:** formułowanie wymagań w zwykłym języku zamiast pisania kodu.
- **AI jako partner:** traktowanie AI jako inteligentnego asystenta, który generuje kod na podstawie poleceń.
- **50/50:** poświęć 50% czasu na konsultację z AI i przygotowanie "scenariusza" kodowania. Pozostałe 50% czasu poświęć na pracę z generatorem kodu.
- **Podział programu na podprogramy:** oneshot coding ma się dobrze, ale jeszcze nie dzisiaj.
- **500:** to liczba śmierci w twoim kodzie. Optymalnie podzielić kod na pliki liczące nie więcej niż 400 linii. To może już być nieaktualne po pojawieniu się Text editor tool [4].
- **Iteracyjna pętla poprawek:** cykl prompt -> kod -> test -> feedback -> poprawiony kod.
- **Inżynieria promptów:** świadome konstruowanie zapytań, dodawanie wytycznych i narzucanie stylu.
- **Nadawanie roli AI:** ustawianie kontekstu lub roli, w jakiej ma wystąpić AI, np. "Jesteś ekspertem od UI/UX...".
- **Zaufanie vs weryfikacja:** balans między akceptowaniem sugestii AI bez sprawdzania a dokładną weryfikacją kodu. To sinusoida zachwytu i rozpaczy: im lepiej się przygotujesz, tym mniej będzie dramatów.

W sieci jest sporo materiałów na ten temat, ale prawdopodobnie, nim przeczytasz pięć z nich, pojawi się nowa, sprawniejsza technika. Zacznij np. od "Vibe Coding for Dummies" [5] lub "Vibe coding manual" [6].

## Przykłady użycia vibe codingu

- Klon Airbnb stworzony w kilkanaście minut [7].
- Brainy Docs - startup, który dzięki Vibe Codingowi błyskawicznie rozwija MVP konwertujące PDF-y na prezentacje wideo.
- Fly.pieter.com - gra przeglądarkowa MMO, stworzona przez indie developera Pietera Levelsa w zaledwie 30 minut przy użyciu AI, która szybko zaczęła przynosić ponad 50 tys. dolarów miesięcznie przychodu.
- Tłumacz menu w restauracji - aplikacja zbudowana w jedną noc przez blogera przy pomocy edytora Cursor.
- Robot rysujący - aplikacja webowa obsługująca DIY robota rysującego, zbudowana bez tradycyjnego kodowania, oparta wyłącznie na opisach funkcji dla AI.
- WebInsights - narzędzie SaaS do analizy stron internetowych, którego kod w 90% został wygenerowany przez ChatGPT [8].

Vibe coding znajduje zastosowanie w wielu różnych kontekstach. Kevin Roose, dziennikarz "New York Timesa" bez formalnego wykształcenia programistycznego, eksperymentował z vibe codingiem. Stworzył proste aplikacje na własne potrzeby, takie jak aplikacja analizująca zawartość jego lodówki i sugerująca składniki na lunch.

Startupy coraz częściej sięgają po tę metodę w celu przyspieszenia rozwoju produktów i tworzenia MVP. Y Combinator odnotował, że w ich zimowej edycji z 2025 roku aż 25% startupów miało bazy kodu wygenerowane w 95% przez AI.

Vibe coding jest również wykorzystywany do automatyzacji przepływów pracy w przedsiębiorstwach, eksperymentowania z projektowaniem gier, a nawet w edukacji, gdzie pomaga uczniom zrozumieć logikę programowania bez konieczności zagłębiania się w zawiłości składni. Non-developerzy mogą tworzyć proste aplikacje webowe, opisując pożądaną funkcjonalność w języku naturalnym. CEO Replit zauważył, że aż 75% ich klientów nigdy nie napisało ani jednej linii kodu, prawdopodobnie korzystając z funkcji AI.

Vibe coding sprawdza się również w szybkim tworzeniu prototypów, testowaniu pomysłów, naprawianiu błędów, usprawnianiu rutynowych zadań, a nawet generowaniu złożonych algorytmów.

## Narzędzia do vibe codingu

Do wspierania vibe codingu powstał już bogaty ekosystem narzędzi. Wśród popularnych platform i asystentów AI dla programistów warto wymienić Cursor, edytor kodu oparty na VS Code, który integruje asystenta kodowania bezpośrednio w IDE, umożliwiając pisanie i edytowanie kodu w języku naturalnym oraz przewidywanie kolejnych edycji. Cursor oferuje wsparcie dla różnych dużych modeli językowych.

Kolejnym popularnym narzędziem jest GitHub Copilot, asystent kodowania AI zintegrowany z VS Code i innymi edytorami, który sugeruje kod w trakcie pisania i może generować całe funkcje lub moduły na podstawie komentarzy. Posiada również tryb czatu do bardziej zaawansowanych instrukcji i debugowania.

Replit, internetowe IDE, oferuje funkcje Ghostwriter i Replit AI Agent, które potrafią generować kod front-endowy i back-endowy oraz konfigurować bazy danych. Uniwersalnym asystentem jest ChatGPT od OpenAI, który może generować fragmenty kodu, rozwiązywać problemy programistyczne i pomagać w debugowaniu poprzez konwersację. Nowsze wersje ChatGPT potrafią również uruchamiać kod i obsługiwać pliki.

Warto wspomnieć o topowym modelu do kodowania, jakim jest Claude od Anthropic, który charakteryzuje się dużym oknem kontekstowym. Na rynku pojawiają się również nowe platformy dedykowane vibe codingowi, takie jak Pythagora, Bolt, Lovable i Cline, z których niektóre oferują interfejsy no-code lub działają bezpośrednio w przeglądarce.

Różnorodność i rosnąca liczba narzędzi wspierających vibe coding świadczą o znaczącym zainteresowaniu i inwestycjach w to podejście.

## Zalety

Vibe coding niesie ze sobą szereg znaczących korzyści. Przede wszystkim obniża próg wejścia do świata programowania, czyniąc tworzenie oprogramowania dostępnym dla szerszego grona odbiorców, w tym dla osób bez rozległej wiedzy na temat języków programowania i składni. Umożliwia to nawet osobom bez doświadczenia w kodowaniu tworzenie prostych, działających aplikacji w bardzo krótkim czasie.

Kolejną kluczową zaletą jest znaczne przyspieszenie procesu tworzenia oprogramowania. AI potrafi generować kod w tempie nieosiągalnym dla człowieka, co pozwala na szybsze tworzenie prototypów i wdrażanie produktów. Zadania, które tradycyjnie zajmowały tygodnie, dzięki vibe codingowi można zrealizować w ciągu kilku dni. Badania pokazują, że programiści korzystający z narzędzi AI odnotowują znacząco krótszy czas realizacji zadań.

Odciążając programistów od żmudnych zadań związanych ze składnią i powtarzalnym kodem, vibe coding pozwala im skupić się na wyższym poziomie projektowania i rozwiązywania problemów, co sprzyja kreatywności. Umożliwia to również osobom z ograniczoną wiedzą programistyczną aktywne uczestnictwo w procesie tworzenia oprogramowania. Dzięki szybkiemu prototypowaniu deweloperzy mogą w krótkim czasie tworzyć funkcjonalne wersje demonstracyjne bez konieczności martwienia się o szczegóły implementacji niskiego poziomu.

Asystenci AI automatyzują powtarzalne zadania, zwiększając produktywność programistów. AI potrafi generować kod szkieletowy, refaktoryzować istniejący kod, a nawet sugerować optymalizacje. Ponadto narzędzia AI wspomagają szybsze debugowanie, analizując błędy i sugerując rozwiązania w czasie rzeczywistym. Kod generowany przez AI często charakteryzuje się spójnością i zgodnością ze standardowymi wzorcami i najlepszymi praktykami.

## Wady

Pomimo wielu zalet vibe coding nie jest wolny od wad i ograniczeń. Kod generowany przez AI nie zawsze jest zoptymalizowany pod kątem wydajności i może nie przestrzegać najlepszych praktyk programistycznych, co potencjalnie prowadzi do powstawania nieefektywnego lub zawierającego błędy oprogramowania. Sam Karpathy przyznał, że narzędzia AI nie zawsze potrafią naprawić błędy.

Szybkie generowanie kodu bez odpowiedniego projektu i architektury może skutkować narastaniem długu technicznego, utrudniając przyszłe utrzymanie i modyfikacje. Dokładność i niezawodność vibe codingu są silnie uzależnione od możliwości silnika AI. Debugowanie kodu wygenerowanego przez AI może być trudne, zwłaszcza jeśli "programiści" nie w pełni go rozumieją.

Niektórzy eksperci wyrażają frustrację z powodu braku kontroli i precyzji podczas korzystania z narzędzi do generowania kodu AI. Kod generowany przez AI może wprowadzać luki bezpieczeństwa, a źle wytrenowane modele AI albo źle napisane prompty mogą generować kod z wadami bezpieczeństwa.

Bazy kodu silnie oparte na vibe codingu mogą stać się trudniejsze w nawigacji i utrzymaniu ze względu na niespójności w strukturze i logice. Programiści mogą zbytnio polegać na AI, co potencjalnie ograniczy ich zdolność do samodzielnego pisania kodu i doprowadzi do pogorszenia fundamentalnych umiejętności programistycznych. Istnieją również obawy etyczne związane z potencjalnymi uprzedzeniami w danych treningowych, które mogą prowadzić do generowania niesprawiedliwych lub dyskryminujących rozwiązań.

Vibe coding nie jest jeszcze zalecany do tworzenia krytycznej infrastruktury ani większych projektów.

## Podsumowanie (od AI)

Podsumowując pierwszą część, vibe coding reprezentuje znaczącą zmianę podejścia w tworzeniu oprogramowania, czyniąc je bardziej dostępnym i wydajnym. Ma potencjał zrewolucjonizowania branży poprzez zwiększenie intuicyjności i dostępności procesu programowania. Niemniej jednak należy uważnie rozważyć wyzwania związane z jakością kodu, debugowaniem, długiem technicznym, bezpieczeństwem oraz koniecznością nadzoru ze strony człowieka.

Przyszłość vibe codingu prawdopodobnie będzie opierać się na zrównoważonym podejściu, w którym AI zwiększa produktywność, a programiści pozostają głęboko zaangażowani w bazę kodu, zapewniając jej jakość i utrzymanie. Kluczowe dla pomyślnego wdrożenia vibe codingu będzie opracowanie standardowych technik inżynierii promptów, wdrożenie solidnych procesów testowania i przeglądu kodu oraz eksploracja narzędzi AI wspomagających debugowanie.

Przyszłość tworzenia oprogramowania prawdopodobnie będzie modelem hybrydowym, w którym AI i ludzcy programiści współpracują, wykorzystując mocne strony AI przy jednoczesnym łagodzeniu jego słabości poprzez staranne praktyki i nadzór.

## Podsumowanie (non AI)

To, co dzisiaj nazywamy vibe codingiem, w przyszłości stanie się podstawową metodą wytwarzania oprogramowania. Jeszcze rok temu zastanawiałem się, czy współczesne języki programowania są optymalne dla AI, czy nie powinien powstać język stworzony przez AI dla AI, gdzie człowiek jest zbędnym pośrednikiem. Dla nas najważniejszy jest efekt końcowy, produkt. W jakim języku powstanie, jakich zasobów użyje, jest bez znaczenia.

Powstaje nowy zawód, do którego wykonywania predyspozycje programisty mogą okazać się niewystarczające. A jeśli nie programista, to kto? O tym w drugiej części artykułu.

## Źródła

- [0] [Vibe coding - Wikipedia](https://en.wikipedia.org/wiki/Vibe_coding)
- [1] [@karpathy, Feb 3, 2025](https://x.com/karpathy/status/1886192184808149383)
- [2] [Merriam-Webster: vibe-coding](https://www.merriam-webster.com/slang/vibe-coding)
- [3] [@karpathy, Jan 24, 2023](https://x.com/karpathy/status/1617979122625712128)
- [4] [Anthropic: Text editor tool](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/text-editor-tool)
- [5] [Vibe Coding for Dummies](https://x.com/IndieHackers/status/1899851967767449645)
- [6] [Vibe coding manual](https://www.reddit.com/r/ChatGPTCoding/comments/1j5l4xw/vibe_coding_manual/)
- [7] [Klon Airbnb](https://x.com/SullyOmarr/status/1893757471799308321)
- [8] [WebInsights](https://dev.to/vorniches/vibe-coding-yeah-ive-been-doing-it-for-two-years-ea2)
