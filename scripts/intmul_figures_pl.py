#!/usr/bin/env python3
"""Render Polish versions of the 24 figures from "Integer multiplication, illustrated".

The figure generators are the work of Rohan Arun
(https://github.com/rohanarun/integer-multiplication-illustrated, Apache-2.0).
This script does not vendor them: it copies them from a local checkout into a
temporary directory, replaces the visible English labels with Polish ones,
switches numbers to a decimal comma, runs the generators and converts the
results to WebP for the three article bundles. Mathematical content is unchanged.

Requires Python with NumPy, Matplotlib and Pillow, plus the pl_PL.UTF-8 locale.

    python3 scripts/intmul_figures_pl.py --source /path/to/integer-multiplication-illustrated
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SERIES = "content/posts/mnozenie-liczb-calkowitych-{}"
PARTS = {
    "1-problem-i-splot": ["11-proof-roadmap", "12-growth-rates", "13-convolution-groups",
                          "14-evaluate-recover", "01-convolution", "16-tape-order", "02-role-volume"],
    "2-rama-rzad-rekurencja": ["17-rank-directions", "18-frame-example", "03-restoration",
                               "04-common-frame", "21-intersection-cancellation", "19-recursion-ledger",
                               "05-recursion", "15-frequency-patterns", "24-complex-turns", "06-butterfly"],
    "3-od-transformaty-do-wyniku": ["07-signed-shift", "08-permutations", "20-error-budget",
                                    "22-bottleneck", "09-rounding", "10-margins", "23-proof-obligations"],
}

# Injected after the imports of generate_figures.py: Polish decimal comma on axes.
LOCALE_PATCH = """
import locale
locale.setlocale(locale.LC_NUMERIC, 'pl_PL.UTF-8')
plt.rcParams['axes.formatter.use_locale'] = True
"""

REPLACEMENTS: dict[str, list[tuple[str, str]]] = {
    "generate_figures.py": [
        ("import numpy as np\n", "import numpy as np\n" + LOCALE_PATCH),
        ("dpi=160", "dpi=200"),
        ("'Example approximation: 12.27'", "'Przykładowe przybliżenie: 12,27'"),
        ("'Correct integer: 12'", "'Poprawna liczba całkowita: 12'"),
        ("ax.set_xticks([11,11.5,12,12.5,13])", "ax.set_xticks([11,11.5,12,12.5,13],['11','11,5','12','12,5','13'])"),
        ("'After every scale is undone: absolute error must be strictly below 1/2'",
         "'Po cofnięciu wszystkich skal błąd bezwzględny musi być ostro mniejszy niż 1/2'"),
        ("['Prefix moves','Chunk exchanges','Butterfly rounds','CRT / axis layouts','Gaussian maps','Chirps / products','Packed products']",
         "['Przesunięcia prefiksów','Wymiany porcji','Rundy motylków','CRT / układy osi','Odwzorowania gaussowskie','Chirpy / iloczyny','Iloczyny upakowane']"),
        ("r'Target $\\kappa=2^{-182}$'", "r'Cel: $\\kappa=2^{-182}$'"),
        ("r'$-\\log_2(g_i)$: farther right means a smaller margin (worse)'",
         "r'$-\\log_2(g_i)$: im dalej w prawo, tym mniejszy margines (gorzej)'"),
        ("f'{max(0,v):.2f}'", "f'{max(0,v):.2f}'.replace('.',',')"),
    ],
    "generate_foundations.py": [
        # Fig. 24: move the labels off the axes so the lines do not cut through "i" and "−i".
        ("ax.text(1.16*x,1.16*y,label,ha='center',va='center',fontsize=14)",
         "ax.text(*{'1':(1.08,.13),'i':(.1,1.13),'−1':(-1.08,.13),'−i':(.1,-1.15)}[label],label,"
         "ha='right' if label=='−1' else 'left',va='center',fontsize=14)"),
        ("r'Input-length scale $b=\\log_2n$'", "r'Skala długości wejścia $b=\\log_2n$'"),
        ("r'$\\log_2$ of the formula value'", "r'$\\log_2$ wartości wzoru'"),
        ("'Compare shapes, not measured seconds'", "'Porównuj kształty, a nie zmierzone sekundy'"),
        ("r'Ratio to $n\\log_2n$'", "r'Stosunek do $n\\log_2n$'"),
        ("r'Toy saving $\\kappa=1/4$: ratio $b^{-1/4}$'", "r'Poglądowa oszczędność $\\kappa=1/4$: stosunek $b^{-1/4}$'"),
        ("['Average','Cosine pattern','Sine pattern','Alternating','Their sum']",
         "['Średnia','Wzorzec cosinusowy','Wzorzec sinusowy','Wzorzec naprzemienny','Suma']"),
        ("ax.set_xlabel('Position',fontsize=9)", "ax.set_xlabel('Pozycja',fontsize=9)"),
        ("axes[0].set_ylabel('Value')", "axes[0].set_ylabel('Wartość')"),
        ("'Rank 1: two arrows, one independent direction'", "'Rząd 1: dwie strzałki, jeden niezależny kierunek'"),
        ("'Rank 2: two independent directions'", "'Rząd 2: dwa niezależne kierunki'"),
        ("['Initial bound','Add local error 0.02','Then rescale by 8','Alternative: rescale by 32']",
         "['Ograniczenie początkowe','Dodaj błąd lokalny 0,02','Potem przeskaluj ×8','Alternatywa: przeskaluj ×32']"),
        ("'Strict rounding threshold: 1/2'", "'Ostry próg zaokrąglenia: 1/2'"),
        ("ax.text(v+.018,j,f'{v:.2f}'", "ax.text(v+.018,j,f'{v:.2f}'.replace('.',',')"),
        ("'Certified upper bound on absolute error (toy example)'",
         "'Gwarantowane górne ograniczenie błędu bezwzględnego (przykład poglądowy)'"),
        ("'Central contribution'", "'Wkład centralny'"),
        ("'Side correction'", "'Korekta boczna'"),
        ("'Net coefficient'", "'Współczynnik netto'"),
        ("'3 (self)'", "'3 (ten sam)'"),
        ("'Intersection size of two triples'", "'Rozmiar przecięcia dwóch trójek'"),
        ("ylabel='Coefficient'", "ylabel='Współczynnik'"),
        ("'Complex construction: cancel unwanted terms'", "'Wersja zespolona: znoszenie niechcianych wyrazów'"),
        ("['Overlap','Central','Side XOR','Net']", "['Przecięcie','Centralny','Boczny XOR','Netto']"),
        ("'Bit construction: arithmetic modulo two'", "'Wersja bitowa: arytmetyka modulo 2'"),
        ("['Starting toy profile','Improve an easy term','Improve the limiting term']",
         "['Profil wyjściowy','Poprawa łatwego składnika','Poprawa składnika ograniczającego']"),
        ("['Margin A','Margin B','Margin C']", "['Margines A','Margines B','Margines C']"),
        ("f'min = {min(profile):.2f}'", "f'min = {min(profile):.2f}'.replace('.',',')"),
        ("'Toy margins: larger is better'", "'Marginesy poglądowe: większy znaczy lepszy'"),
        ("'Multiply by i:\\nturn a quarter-circle\\ncounterclockwise'",
         "'Mnożenie przez i:\\nobrót o ćwierć okręgu\\nprzeciwnie do ruchu\\nwskazówek zegara'"),
    ],
    "generate_concrete.py": [
        ("'The familiar long multiplication'", "'Znane mnożenie pisemne'"),
        ("'Convolution coefficient'", "'Współczynnik splotu'"),
        ("'Incoming carry'", "'Przeniesienie z niższej pozycji'"),
        ("f'{v} + {c} → digit {d}'", "f'{v} + {c} → cyfra {d}'"),
        ("['Ones','Tens','Hundreds']", "['Jedności','Dziesiątki','Setki']"),
        ("ax.set_ylabel('Before carrying')", "ax.set_ylabel('Przed przeniesieniem')"),
        ("'Convolution + one carry pass'", "'Splot + jedno przejście przeniesień'"),
        ("f'Role {k}: 4B = V/3'", "f'Rola {k}: 4B = V/3'"),
        ("'Whole rows are dealt cyclically; each row keeps its entire suffix'",
         "'Całe wiersze są rozdawane cyklicznie; każdy zachowuje cały sufiks adresu'"),
        ("'12 rows × B bits = V bits total. All three role streams have matching local shapes.'",
         "'12 wierszy × B bitów = łącznie V bitów. Wszystkie trzy strumienie ról mają zgodny kształt lokalny.'"),
        ("'Source x'", "'Źródło x'"),
        ("'Target y'", "'Cel y'"),
        ("'Scratch a'", "'Pomocniczy a'"),
        ("'Scratch returns to 7'", "'Rejestr pomocniczy wraca do 7'"),
        ("'Actual register value'", "'Rzeczywista wartość rejestru'"),
        ("'Borrow a register containing 7: add x = 3 to y = 5, then return the 7'",
         "'Pożycz rejestr z wartością 7: dodaj x = 3 do y = 5, a potem oddaj 7'"),
        ("'Array A'", "'Tablica A'"),
        ("'Array B'", "'Tablica B'"),
        ("'A common frame can be a quarter-turn of the address grid'",
         "'Wspólną ramą może być obrót siatki adresów o ćwierć obrotu'"),
        ("label='Linear width cost'", "label='Koszt liniowy względem szerokości'"),
        ("r'Toy cost: $f^{\\log_2(3/2)}$'", "r'Koszt poglądowy: $f^{\\log_2(3/2)}$'"),
        ("xlabel='Width f'", "xlabel='Szerokość f'"),
        ("ylabel='Cost per unit volume'", "ylabel='Koszt na jednostkę objętości'"),
        ("'Doubling width multiplies cost by 1.5'", "'Podwojenie szerokości mnoży koszt przez 1,5'"),
        ("xlabel='Number of doublings'", "xlabel='Liczba podwojeń'"),
        ("ylabel='Toy cost / linear cost'", "ylabel='Koszt poglądowy / koszt liniowy'"),
        ("'The gap compounds at every scale'", "'Przewaga narasta na każdej skali'"),
        ("'divide by 2'", "'podziel przez 2'"),
        ("'Upper branch: (6 + 2)/2\\nLower branch: (6 − 2)/2'", "'Gałąź górna: (6 + 2)/2\\nGałąź dolna: (6 − 2)/2'"),
        ("f'slot {j}\\na{j}'", "f'pole {j}\\na{j}'"),
        ("'wrap: negate a₃'", "'zawinięcie: zmiana znaku a₃'"),
        ("'Multiply by y modulo y⁴ + 1'", "'Mnożenie przez y modulo y⁴ + 1'"),
        ("f'freq {k}'", "f'częst. {k}'"),
        ("'A × B entry by entry'", "'A × B element po elemencie'"),
        ("title+' in order P'", "title+' w porządku P'"),
        ("'Reorder both inputs the same way: each frequency still meets its partner'",
         "'Przestaw oba wejścia tak samo, a każda częstotliwość nadal spotka swoją parę'"),
        ("['Stored order','Required order']", "['Porządek zapisany','Porządek wymagany']"),
        ("'Move records to their partners'", "'Przenieś rekordy do partnerów'"),
        ("['Input','Bit 0','Bit 1','Bit 2']", "['Wejście','Bit 0','Bit 1','Bit 2']"),
        ("'Mix matching values through butterfly layers'", "'Łącz pasujące wartości w warstwach motylków'"),
        ("f'{a} × {bv} = {a*bv}\\nposition {i+j}'", "f'{a} × {bv} = {a*bv}\\npozycja {i+j}'"),
        ("['4 ones','1 ten']", "['4 jedności','1 dziesiątka']"),
        ("['3 ones','2 tens']", "['3 jedności','2 dziesiątki']"),
        ("'Same color = same output position'", "'Ten sam kolor = ta sama pozycja wyniku'"),
        ("ax.set_ylabel('Coefficient before carrying')", "ax.set_ylabel('Współczynnik przed przeniesieniem')"),
        ("'Add along each colored diagonal'", "'Dodaj wzdłuż każdej kolorowej przekątnej'"),
        ("xlabel='Sample point x'", "xlabel='Punkt próbkowania x'"),
        ("ylabel='Value'", "ylabel='Wartość'"),
        ("'Evaluate each input at the same points'", "'Oblicz oba wejścia w tych samych punktach'"),
        ("ylabel='Product A(x)B(x)'", "ylabel='Iloczyn A(x)B(x)'"),
        ("'Three products determine this quadratic'", "'Trzy iloczyny wyznaczają ten trójmian kwadratowy'"),
        ("'A 3 × 3 array'", "'Tablica 3 × 3'"),
        ("'Read rows: 0 1 2 | 3 4 5 | 6 7 8'", "'Odczyt wierszami: 0 1 2 | 3 4 5 | 6 7 8'"),
        ("'Read columns: 0 3 6 | 1 4 7 | 2 5 8'", "'Odczyt kolumnami: 0 3 6 | 1 4 7 | 2 5 8'"),
        ("'One tape head scans positions'", "'Jedna głowica przechodzi kolejne pozycje taśmy'"),
        ("['Add x and y','Rotate both, then add','Rotate only x: wrong sum']",
         "['Dodaj x i y','Obróć oba, potem dodaj','Obróć tylko x: zła suma']"),
        ("f'{3**d} calls\\nV/{2**d} each'", "['1 wywołanie','3 wywołania','9 wywołań'][d]+f'\\npo V/{2**d}'"),
        ("'Circle area = volume of one call'", "'Pole koła = objętość jednego wywołania'"),
        ("'Naive doubling: 2ʲ'", "'Naiwne podwajanie: 2ʲ'"),
        ("'Total visited: (3/2)ʲ'", "'Łącznie odwiedzone: (3/2)ʲ'"),
        ("xlabel='Depth j'", "xlabel='Głębokość j'"),
        ("ylabel='Volume visited / V'", "ylabel='Odwiedzona objętość / V'"),
        ("'More calls, but each call is smaller'", "'Więcej wywołań, ale każde mniejsze'"),
        ("['Algebra example','Concrete tape program','All-size proof']",
         "['Przykład algebraiczny','Konkretny program taśmowy','Dowód dla każdego rozmiaru']"),
        ("'Outputs match, and scratch\\nreturns to its starting value'",
         "'Wyniki się zgadzają, a rejestr\\npomocniczy wraca do startu'"),
        ("'Head movement, copies, routing,\\nand cleanup are charged'",
         "'Ruch głowic, kopie, trasowanie\\ni sprzątanie są wliczone w koszt'"),
        ("'Every input size satisfies\\nthe cost and error bounds'",
         "'Każdy rozmiar wejścia spełnia\\nograniczenia kosztu i błędu'"),
        ("'Finite replay checks\\na concrete instance'", "'Skończony test sprawdza\\nkonkretny przypadek'"),
        ("'A scalar identity alone\\ndoes not price movement'", "'Sama tożsamość skalarna\\nnie wycenia przemieszczeń'"),
        ("'A finite run alone\\ndoes not prove every size'", "'Skończony przebieg nie\\nobejmuje wszystkich n'"),
        ("'Three different claims require three different kinds of evidence'",
         "'Trzy różne twierdzenia wymagają trzech różnych rodzajów uzasadnienia'"),
    ],
}


def translate(source: Path, work: Path) -> None:
    for name, pairs in REPLACEMENTS.items():
        text = (source / name).read_text(encoding="utf-8")
        for old, new in pairs:
            if old not in text:
                sys.exit(f"{name}: label not found, generator changed? {old!r}")
            text = text.replace(old, new)
        (work / name).write_text(text, encoding="utf-8")


def to_webp(png: Path, target: Path) -> None:
    from PIL import Image

    with Image.open(png) as image:
        image.convert("RGB").save(target, "WEBP", quality=90, method=6)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--source", type=Path, required=True,
                        help="checkout of rohanarun/integer-multiplication-illustrated")
    parser.add_argument("--pdf-dir", type=Path,
                        help="also copy Polish vector PDFs here (for the LaTeX guide)")
    args = parser.parse_args()

    with tempfile.TemporaryDirectory(prefix="intmul-pl-") as tmp:
        work = Path(tmp)
        (work / "figures").mkdir()
        translate(args.source.resolve(), work)
        subprocess.run([sys.executable, "generate_concrete.py"], cwd=work, check=True)

        for part, names in PARTS.items():
            images = REPO / SERIES.format(part) / "images"
            images.mkdir(parents=True, exist_ok=True)
            for name in names:
                to_webp(work / "figures" / f"{name}.png", images / f"{name}.webp")
        if args.pdf_dir:
            args.pdf_dir.mkdir(parents=True, exist_ok=True)
            for pdf in sorted((work / "figures").glob("*.pdf")):
                shutil.copy2(pdf, args.pdf_dir / pdf.name)
    print(f"Rendered {sum(map(len, PARTS.values()))} Polish figures.")


if __name__ == "__main__":
    main()
