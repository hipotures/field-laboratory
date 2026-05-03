---
title: "Stała Millsa: liczba, która koduje liczby pierwsze"
date: 2026-05-04
description: "Krótka notka o stałej Millsa: jak jedna liczba rzeczywista może wyznaczać nieskończony ciąg liczb pierwszych i dlaczego nie jest to praktyczny generator."
tags: ["matematyka", "liczby pierwsze", "stała Millsa", "teoria liczb"]
categories: ["artykuly"]
authors: ["Andrzej Marszałek"]
resources:
  - src: "images/*"
    params:
      gallery: false
      kind: image
---

Stała Millsa jest jednym z tych wyników teorii liczb, które brzmią prawie jak sztuczka: istnieje taka liczba rzeczywista A, że kolejne wartości

<div class="math-block">⌊A<sup>3ⁿ</sup>⌋</div>

są liczbami pierwszymi. Nie chodzi jednak o praktyczny algorytm produkowania pierwszych, tylko o eleganckie twierdzenie egzystencjalne: jedna liczba rzeczywista może zakodować nieskończony ciąg liczb pierwszych.

<figure class="infographic-figure">
  <a class="infographic-figure-link" href="images/A.png" target="_blank" rel="noopener">
    <img src="images/A.png" width="1156" height="1831" alt="Plansza wyjaśniająca konstrukcję stałej Millsa i kolejne liczby pierwsze Millsa.">
  </a>
  <figcaption>Stała Millsa wybiera liczby pierwsze przez potęgowanie jednej liczby rzeczywistej i branie części całkowitej.</figcaption>
</figure>

Najczęściej cytowana wartość tej stałej to:

<div class="math-block">A ≈ 1.3063778838630806904686144926…</div>

Dla niej początek ciągu wygląda tak:

<div class="math-block">⌊A³⌋ = 2</div>
<div class="math-block">⌊A⁹⌋ = 11</div>
<div class="math-block">⌊A²⁷⌋ = 1361</div>
<div class="math-block">⌊A⁸¹⌋ = 2521008887</div>

Te liczby nazywa się czasem liczbami pierwszymi Millsa.

## Skąd bierze się konstrukcja?

Jeżeli chcemy mieć:

<div class="math-block">pₙ = ⌊A<sup>3ⁿ</sup>⌋</div>

to musi zachodzić:

<div class="math-block">pₙ ≤ A<sup>3ⁿ</sup> &lt; pₙ + 1</div>

Po wzięciu pierwiastka dostajemy przedział, w którym musi leżeć A:

<div class="math-block">pₙ<sup>1/3ⁿ</sup> ≤ A &lt; (pₙ + 1)<sup>1/3ⁿ</sup></div>

Każda kolejna liczba pierwsza zawęża więc możliwe położenie stałej. Konstrukcja działa tak, aby te przedziały były ze sobą zgodne.

Załóżmy, że mamy już liczbę pierwszą pₙ. Ponieważ:

<div class="math-block">A<sup>3ⁿ⁺¹</sup> = (A<sup>3ⁿ</sup>)³</div>

następna liczba pierwsza powinna leżeć między kolejnymi sześcianami:

<div class="math-block">pₙ³ &lt; pₙ₊₁ &lt; (pₙ + 1)³</div>

Na przykład dla p₁ = 2 szukamy liczby pierwszej między 8 i 27. Najmniejsza taka liczba to 11. Potem między 11³ = 1331 i 12³ = 1728 pojawia się 1361. Dalej z 1361³ wychodzi kolejny ogromny przedział, w którym można wybrać następną liczbę pierwszą.

## Dlaczego sześciany?

Kluczowy fakt jest taki, że między kolejnymi sześcianami odstęp jest duży:

<div class="math-block">(x + 1)³ - x³ = 3x² + 3x + 1</div>

Dla dużego x to bardzo szeroki przedział. Mills użył znanych wyników o przerwach między liczbami pierwszymi, aby zagwarantować, że w takim przedziale znajdzie się liczba pierwsza.

Gdyby zamiast wykładników 3ⁿ użyć 2ⁿ, trzeba byłoby gwarantować liczby pierwsze między kolejnymi kwadratami:

<div class="math-block">x² i (x + 1)²</div>

To jest znacznie trudniejsze i prowadzi do hipotezy Legendre’a, która pozostaje nierozwiązana. Sześciany dają więcej miejsca, dlatego konstrukcja Millsa jest osiągalna znanymi metodami.

## Dlaczego to nie jest generator?

Formalnie wzór:

<div class="math-block">⌊A<sup>3ⁿ</sup>⌋</div>

daje liczby pierwsze. Praktycznie nie jest to jednak użyteczny generator. Żeby policzyć duże n, trzeba znać A z ogromną precyzją. A te kolejne cyfry stałej są wyznaczane przez kolejne liczby pierwsze z konstrukcji.

Innymi słowy: stała Millsa nie daje taniej drogi do nowych liczb pierwszych. Ona raczej pokazuje, że można ukryć nieskończony ciąg liczb pierwszych w jednej liczbie rzeczywistej.

Najkrócej: sedno stałej Millsa polega na kodowaniu, nie na obliczeniowej praktyczności.
