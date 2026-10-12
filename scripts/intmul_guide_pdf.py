#!/usr/bin/env python3
"""Build a Polish PDF of the illustrated guide from the three series articles.

The Markdown articles in content/posts/mnozenie-liczb-calkowitych-*/ are the
single source of the translation. This script converts their translated
chapters to LaTeX (skipping web-only widgets, navigation and translator boxes),
adds a title page with attribution and compiles the result with Tectonic.

Figures must be the Polish vector PDFs produced by
    scripts/intmul_figures_pl.py --source ... --pdf-dir DIR

    python3 scripts/intmul_guide_pdf.py --figures DIR --tectonic /path/to/tectonic
"""
from __future__ import annotations

import argparse
import html
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PARTS = [
    "content/posts/mnozenie-liczb-calkowitych-1-problem-i-splot/index.md",
    "content/posts/mnozenie-liczb-calkowitych-2-rama-rzad-rekurencja/index.md",
    "content/posts/mnozenie-liczb-calkowitych-3-od-transformaty-do-wyniku/index.md",
]
OUTPUT = REPO / "content/posts/mnozenie-liczb-calkowitych-1-problem-i-splot/przewodnik-mnozenie-pl.pdf"
SKIP_SECTIONS = ("Od tłumacza: pół wieku", "Źródła")

PREAMBLE = r"""\documentclass[11pt]{article}
\usepackage{fontspec}
\usepackage[polish]{babel}
\usepackage{microtype}
\usepackage{amsmath,amssymb,mathtools,booktabs,array,longtable}
\usepackage[margin=1in]{geometry}
\usepackage{graphicx,xcolor,fancyhdr,needspace}
\usepackage[hyphens]{url}
\usepackage{hyperref}
\definecolor{readerblue}{HTML}{245CA6}
\definecolor{readerteal}{HTML}{147C80}
\hypersetup{colorlinks=true,linkcolor=readerblue,urlcolor=readerblue,
  pdftitle={Mnożenie liczb całkowitych poniżej n log n: ilustrowany przewodnik},
  pdfauthor={Rohan Arun; przekład: hipotures (z pomocą Claude)}}
\newcommand{\guidechapter}[2]{\par\bigskip\Needspace{8\baselineskip}\section*{#1}%
  \addcontentsline{toc}{section}{#1}\noindent{\small\color{readerteal}#2}\par\medskip}
\newcommand{\takeaway}[1]{\par\medskip\noindent\textcolor{readerteal}{\textbf{Co zabrać dalej.}} #1\par\medskip}
\newcommand{\explfigure}[2]{\begin{center}\begin{minipage}{\linewidth}\centering
  \includegraphics[width=\linewidth]{figures/#1.pdf}\par\smallskip
  \begin{minipage}{.96\linewidth}\small #2\end{minipage}\end{minipage}\end{center}}
\setlength{\emergencystretch}{3em}\tolerance=3000
\pagestyle{fancy}\fancyhf{}\fancyhead[L]{\small Mnożenie liczb całkowitych: ilustrowany przewodnik}\fancyfoot[C]{\thepage}
\setlength{\headheight}{14pt}
\title{Mnożenie liczb całkowitych poniżej \texorpdfstring{$n\log n$}{n log n}\\[8pt]\large Ilustrowany przewodnik}
\author{Rohan Arun\\[3pt]\small na podstawie pracy OpenAI \emph{Integer multiplication below $n\log n$} (23 września 2026)\\[8pt]
\small Przekład na język polski: hipotures, wygenerowany z pomocą Claude (Anthropic)}
\date{Polskie wydanie, 12 października 2026}
\begin{document}
\maketitle
\begin{abstract}
Przekład przewodnika \emph{Integer multiplication, illustrated} Rohana Aruna
(\url{https://github.com/rohanarun/integer-multiplication-illustrated}), objaśniającego
oryginalną argumentację z 24 rysunkami, przykładami obliczeniowymi i wyraźnym
rozróżnieniem między twierdzeniami źródła, rachunkami poglądowymi i warunkowymi
interfejsami dowodu. Według noty autora objaśnienia i rysunki przygotowano przy istotnej
pomocy OpenAI Codex. To nie jest nowy dowód ani oficjalna rewizja pracy źródłowej.
Wynik OpenAI nie przeszedł jeszcze niezależnej recenzji.

Licencja: Apache 2.0. Zmiany względem oryginału: przekład tekstu i etykiet rysunków;
dodany słowniczek polsko-angielski. Wersja internetowa z widżetami interaktywnymi:
\url{https://armum.eu/posts/mnozenie-liczb-calkowitych-1-problem-i-splot/}.
\end{abstract}
\tableofcontents\clearpage
"""

SOURCES = r"""
\section*{Źródła}
\addcontentsline{toc}{section}{Źródła}
\begin{enumerate}
\item Rohan Arun, \emph{Integer multiplication, illustrated},
  \url{https://github.com/rohanarun/integer-multiplication-illustrated}, Apache 2.0.
\item OpenAI, \emph{Integer multiplication below $n\log n$}, 23 września 2026, commit
  \texttt{adc7f1241b42e322a6451854ab7e4b4c146bf78a},
  \url{https://github.com/openai/math/tree/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Integer-multiplication-below-n-log-n-September-23-2026}.
\item CrocSwap/integer-mult-bounds, \url{https://github.com/CrocSwap/integer-mult-bounds};
  lista współtwórców: \url{https://github.com/CrocSwap/integer-mult-bounds/blob/main/CONTRIBUTORS.md}.
\item D. Harvey, J. van der Hoeven, \emph{Integer multiplication in time $O(n\log n)$},
  Annals of Mathematics 193 (2021).
\end{enumerate}
\end{document}
"""

MATH = re.compile(r"(\\\(.*?\\\))")


def escape_text(text: str) -> str:
    text = text.replace("\\", "\x00")
    for char in "&%#_{}":
        text = text.replace(char, "\\" + char)
    return text.replace("\x00", "\\").replace("~", r"\textasciitilde{}")


def inline(text: str) -> str:
    """Convert inline Markdown or HTML to LaTeX, leaving \\( ... \\) math untouched."""
    text = html.unescape(re.sub(r"<br\s*/?>", r" \\\\ ", text))
    text = re.sub(r"<a [^>]*href=\"([^\"]+)\"[^>]*>(.*?)</a>", r"[\2](\1)", text)
    text = re.sub(r"<code>(.*?)</code>", r"`\1`", text)
    text = re.sub(r"<sup>(.*?)</sup>", "\x04\\1\x05", text)
    text = re.sub(r"<(strong|b)>(.*?)</\1>", r"**\2**", text)
    text = re.sub(r"<(em|i)>(.*?)</\1>", r"*\2*", text)
    text = re.sub(r"<[^>]+>", "", text)
    maths: list[str] = []

    def keep_math(m: re.Match) -> str:
        maths.append(m.group(1))
        return f"\x03{len(maths) - 1}\x03"

    text = MATH.sub(keep_math, text)
    links: list[str] = []

    def keep_link(m: re.Match) -> str:
        url = m.group(2).replace("#", r"\#").replace("%", r"\%")
        links.append(rf"\href{{{url}}}{{{convert_marks(m.group(1))}}}")
        return f"\x01{len(links) - 1}\x01"

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", keep_link, text)
    text = convert_marks(text)
    text = re.sub(r"\x01(\d+)\x01", lambda m: links[int(m.group(1))], text)
    text = re.sub("\x04(.*?)\x05", r"\\textsuperscript{\1}", text)
    return re.sub(r"\x03(\d+)\x03", lambda m: maths[int(m.group(1))], text)


def convert_marks(text: str) -> str:
    codes: list[str] = []

    def keep_code(m: re.Match) -> str:
        raw = m.group(1)
        # Long hashes and file names may break anywhere; split before escaping.
        code = r"\allowbreak{}".join(escape_text(raw[k:k + 8]) for k in range(0, len(raw), 8))
        codes.append(r"\texttt{" + code + "}")
        return f"\x02{len(codes) - 1}\x02"

    text = re.sub(r"`([^`]+)`", keep_code, text)
    text = escape_text(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", text, flags=re.S)
    text = re.sub(r"\*(.+?)\*", r"\\emph{\1}", text, flags=re.S)
    return re.sub(r"\x02(\d+)\x02", lambda m: codes[int(m.group(1))], text)


def table(rows: list[str]) -> str:
    cells = [[c.strip() for c in row.strip().strip("|").split("|")] for row in rows]
    head, body = cells[0], cells[2:]
    # The glossary has a short status column; give the terms more room.
    widths = [0.33, 0.30, 0.29] if head[-1] == "Status" else [0.9 / len(head)] * len(head)
    spec = "".join(rf">{{\raggedright\arraybackslash}}p{{{width:.2f}\linewidth}}" for width in widths)
    lines = [rf"\begin{{longtable}}{{@{{}}{spec}@{{}}}}", r"\toprule",
             " & ".join(rf"\textbf{{{inline(c)}}}" for c in head) + r" \\", r"\midrule\endhead"]
    lines += [" & ".join(inline(c) for c in row) + r" \\" for row in body]
    lines += [r"\bottomrule", r"\end{longtable}"]
    return "\n".join(lines)


def convert(markdown: str) -> str:
    body = markdown.split("\n---\n", 1)[1]  # drop front matter
    blocks = re.split(r"\n\s*\n", body)
    out: list[str] = []
    skipping = False
    pending_heading: str | None = None
    i = 0
    while i < len(blocks):
        block = blocks[i].strip()
        i += 1
        if not block:
            continue
        if block.startswith("## "):
            title = block[3:].strip()
            skipping = title.startswith(SKIP_SECTIONS)
            pending_heading = None if skipping else title
            if pending_heading and title.startswith("Od tłumacza"):
                out.append(rf"\guidechapter{{{inline(title)}}}{{\textbf{{Dodatek tłumacza}}}}")
                pending_heading = None
            continue
        if skipping:
            continue
        if block.startswith('<p class="chapter-kicker">'):
            tag = re.search(r'chapter-tag">([^<]+)<', block).group(1)
            text = re.sub(r"^.*?</span>\s*", "", block[len('<p class="chapter-kicker">'):]).removesuffix("</p>")
            out.append(rf"\guidechapter{{{inline(pending_heading or '')}}}{{\textbf{{{tag}}}\quad {inline(text)}}}")
            pending_heading = None
            continue
        if pending_heading:
            out.append(rf"\guidechapter{{{inline(pending_heading)}}}{{}}")
            pending_heading = None
        if re.fullmatch(r'<div class="[\w-]*table">|</div>', block):
            continue  # styling wrapper around a Markdown table: keep the table
        if block.startswith("<div"):
            while "</div>" not in block and i < len(blocks):  # boxes may span paragraphs
                block += "\n\n" + blocks[i]
                i += 1
            if 'class="table-notes"' in block:
                notes = re.findall(r"<p>(.*?)</p>", block, re.S)
                out.append(r"{\small\noindent " + r"\\".join(inline(n) for n in notes) + r"\par}\medskip")
                continue
            if "Co zabrać dalej" in block:
                text = re.sub(r"^.*?</span>\s*", "", block, flags=re.S)
                out.append(r"\takeaway{" + inline(text.replace("</div>", "").strip()) + "}")
            continue  # credit, series, translator, status boxes and widgets are web-only
        if block.startswith("<figure"):
            name = re.search(r'images/([\w-]+)\.webp', block).group(1)
            caption = re.search(r"<figcaption>(.*?)</figcaption>", block, re.S).group(1)
            out.append(rf"\explfigure{{{name}}}{{{inline(caption)}}}")
            continue
        if block.startswith('<p class="source-anchor">'):
            out.append(r"{\footnotesize\raggedright\textit{" + inline(block) + r"}\par}")
            continue
        if block.startswith(("**Dalej", "**Wstecz")) or block == "---":
            continue
        if block.startswith(r"\["):
            out.append(block)
            continue
        if block.startswith("|"):
            out.append(table(block.splitlines()))
            continue
        if block.startswith("- "):
            items = re.split(r"\n(?=- )", block)
            out.append("\\begin{itemize}\n" + "\n".join(
                r"\item " + inline(item[2:]) for item in items) + "\n\\end{itemize}")
            continue
        if re.match(r"\d+\. ", block):
            items = re.split(r"\n(?=\d+\. )", block)
            out.append("\\begin{enumerate}\n" + "\n".join(
                r"\item " + inline(re.sub(r"^\d+\.\s*", "", item)) for item in items) + "\n\\end{enumerate}")
            continue
        out.append(inline(block))
    return "\n\n".join(out)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--figures", type=Path, required=True, help="directory with Polish figure PDFs")
    parser.add_argument("--tectonic", default="tectonic", help="Tectonic executable")
    parser.add_argument("--keep-tex", type=Path, help="also save the generated .tex here")
    args = parser.parse_args()

    tex = PREAMBLE + "\n\n".join(convert((REPO / part).read_text(encoding="utf-8")) for part in PARTS) + SOURCES
    with tempfile.TemporaryDirectory(prefix="intmul-pdf-") as tmp:
        work = Path(tmp)
        shutil.copytree(args.figures, work / "figures")
        (work / "przewodnik.tex").write_text(tex, encoding="utf-8")
        if args.keep_tex:
            shutil.copy2(work / "przewodnik.tex", args.keep_tex)
        result = subprocess.run([args.tectonic, "--keep-logs", "przewodnik.tex"], cwd=work,
                                capture_output=True, text=True)
        if result.returncode != 0:
            sys.stderr.write(result.stdout[-4000:] + result.stderr[-4000:])
            sys.exit("Tectonic failed")
        shutil.copy2(work / "przewodnik.pdf", OUTPUT)
    print(f"Wrote {OUTPUT.relative_to(REPO)}")


if __name__ == "__main__":
    main()
