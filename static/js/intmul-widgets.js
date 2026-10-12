// Interactive widgets for the Polish series on integer multiplication.
// Each element <div class="intmul" data-intmul="NAME"> is replaced by a widget.
(() => {
  "use strict";

  const PALETTE = ["blue", "teal", "gold", "plum", "green", "rust"];
  const SUP = "⁰¹²³⁴⁵⁶⁷⁸⁹";
  const sup = (n) => String(n).replace(/\d/g, (d) => SUP[d]);
  const place = (digit, pos) => (pos === 0 ? String(digit) : `${digit}·10${sup(pos)}`);
  const fmt = (x, digits = 4) =>
    Number(x).toLocaleString("pl-PL", { maximumFractionDigits: digits });

  function el(tag, attrs = {}, ...children) {
    const node = document.createElement(tag);
    for (const [key, value] of Object.entries(attrs)) {
      if (key === "class") node.className = value;
      else if (key === "text") node.textContent = value;
      else if (key.startsWith("on")) node.addEventListener(key.slice(2), value);
      else node.setAttribute(key, value);
    }
    for (const child of children.flat()) {
      if (child != null) node.append(child);
    }
    return node;
  }

  function numberInput(label, value, attrs = {}) {
    const input = el("input", { type: "number", value: String(value), ...attrs });
    return { input, field: el("label", { class: "intmul-field" }, el("span", { text: label }), input) };
  }

  function rangeInput(label, value, min, max, step = 1) {
    const input = el("input", { type: "range", min, max, step, value: String(value) });
    const out = el("output", { text: String(value) });
    input.addEventListener("input", () => { out.textContent = input.value; });
    return {
      input,
      field: el("label", { class: "intmul-field intmul-range" }, el("span", { text: label }), input, out),
    };
  }

  function header(root, title, note) {
    root.append(el("p", { class: "intmul-title", text: title }));
    if (note) root.append(el("p", { class: "intmul-note", text: note }));
  }

  // 1. Long multiplication as convolution, with carries.
  function convolution(root) {
    header(root, "Kalkulator splotu",
      "Wpisz dwie liczby. Iloczyny cyfr o tej samej sumie pozycji i + j mają ten sam kolor i trafiają do tego samego współczynnika.");
    const a = numberInput("Pierwsza liczba", root.dataset.a || 23, { min: 0, max: 99999999 });
    const b = numberInput("Druga liczba", root.dataset.b || 14, { min: 0, max: 99999999 });
    const controls = el("div", { class: "intmul-controls" }, a.field, b.field);
    const grid = el("div", { class: "intmul-scroll" });
    const coeffs = el("div", { class: "intmul-coeffs" });
    const carries = el("div", { class: "intmul-scroll" });
    const result = el("p", { class: "intmul-result", "aria-live": "polite" });
    root.append(controls, grid, el("p", { class: "intmul-label", text: "Współczynniki splotu (przed przeniesieniem)" }),
      coeffs, el("p", { class: "intmul-label", text: "Jedno przejście przeniesień, od najniższej pozycji" }), carries, result);

    const digitsOf = (text) => {
      const clean = String(text).replace(/\D/g, "").replace(/^0+(?=\d)/, "").slice(0, 8) || "0";
      return [...clean].reverse().map(Number);
    };
    const highlight = (k) => {
      root.querySelectorAll("[data-pos]").forEach((cell) => {
        cell.classList.toggle("is-dim", k !== null && cell.dataset.pos !== String(k));
      });
    };

    function render() {
      const da = digitsOf(a.input.value);
      const db = digitsOf(b.input.value);
      const c = Array(da.length + db.length - 1).fill(0);
      da.forEach((x, i) => db.forEach((y, j) => { c[i + j] += x * y; }));

      const table = el("table", { class: "intmul-grid" });
      const head = el("tr", {}, el("th", { text: "×" }));
      for (let j = db.length - 1; j >= 0; j--) head.append(el("th", { text: place(db[j], j) }));
      table.append(head);
      for (let i = da.length - 1; i >= 0; i--) {
        const row = el("tr", {}, el("th", { text: place(da[i], i) }));
        for (let j = db.length - 1; j >= 0; j--) {
          const k = i + j;
          row.append(el("td", {
            class: `intmul-c-${PALETTE[k % PALETTE.length]}`, "data-pos": k,
            title: `pozycja ${k}`, onmouseenter: () => highlight(k), onmouseleave: () => highlight(null),
          }, el("strong", { text: String(da[i] * db[j]) }), el("small", { text: `poz. ${k}` })));
        }
        table.append(row);
      }
      grid.replaceChildren(table);

      coeffs.replaceChildren(...c.map((value, k) => el("span", {
        class: `intmul-chip intmul-c-${PALETTE[k % PALETTE.length]}`, "data-pos": k,
        onmouseenter: () => highlight(k), onmouseleave: () => highlight(null), tabindex: 0,
        onfocus: () => highlight(k), onblur: () => highlight(null),
      }, el("small", { text: `c${k}` }), el("strong", { text: String(value) }))));

      const steps = el("table", { class: "intmul-table" });
      steps.append(el("tr", {}, ...["pozycja", "współczynnik", "+ przeniesienie", "= suma", "cyfra", "dalej"].map((t) => el("th", { text: t }))));
      let carry = 0;
      const digits = [];
      c.forEach((value, k) => {
        const total = value + carry;
        const digit = total % 10;
        const next = Math.floor(total / 10);
        digits.push(digit);
        steps.append(el("tr", { "data-pos": k }, ...[k, value, carry, total, digit, next].map((t) => el("td", { text: String(t) }))));
        carry = next;
      });
      while (carry > 0) {
        steps.append(el("tr", {}, ...[digits.length, 0, carry, carry, carry % 10, Math.floor(carry / 10)].map((t) => el("td", { text: String(t) }))));
        digits.push(carry % 10);
        carry = Math.floor(carry / 10);
      }
      carries.replaceChildren(steps);

      const product = digits.reverse().join("").replace(/^0+(?=\d)/, "");
      const check = (BigInt(da.slice().reverse().join("")) * BigInt(db.slice().reverse().join(""))).toString();
      result.textContent = `Wynik: ${product}` + (product === check ? " — zgadza się ze zwykłym mnożeniem." : ` (błąd: oczekiwano ${check})`);
    }
    a.input.addEventListener("input", render);
    b.input.addEventListener("input", render);
    render();
  }

  // 2. How large n must be before (log n)^-kappa gives a visible saving.
  function scale(root) {
    header(root, "Jak duże musi być n?",
      "Pomijając stałe, nowa granica dzieli się przez n·log n jak (log₂ n)^(−κ). Wybierz κ i oszczędność, którą chcesz zobaczyć.");
    const presets = [
      { label: "poglądowe κ = 1/4", exp: 2 },
      { label: "społeczność: κ ≈ 0,00152", exp: -Math.log2(0.001517760977820331) },
      { label: "OpenAI: κ = 2⁻¹⁸²", exp: 182 },
    ];
    const kappa = rangeInput("−log₂ κ", 2, 0.5, 200, 0.01);
    const saving = el("select", {},
      ...[["1", "1%"], ["10", "10%"], ["50", "50% (dwa razy mniej)"]].map(([v, t]) => el("option", { value: v, text: t })));
    saving.value = "50";
    const buttons = el("div", { class: "intmul-buttons" }, ...presets.map((p) => el("button", {
      type: "button", text: p.label,
      onclick: () => { kappa.input.value = String(p.exp); kappa.input.dispatchEvent(new Event("input")); },
    })));
    const out = el("div", { class: "intmul-output", "aria-live": "polite" });
    root.append(buttons, el("div", { class: "intmul-controls" }, kappa.field,
      el("label", { class: "intmul-field" }, el("span", { text: "Oszczędność względem n·log n" }), saving)), out);

    // Numbers of the form 2^x, shown via powers of ten when x is large.
    const pow2 = (x) => {
      if (x < 40) return fmt(2 ** x, 0);
      const exp10 = x * Math.LOG10E * Math.LN2;
      if (exp10 < 1e6) return `≈ 10^${fmt(Math.floor(exp10), 0)}`;
      return `2^(${sci(x)})`;
    };
    const sci = (x) => {
      if (x < 1e6) return fmt(x, 2);
      const e = Math.floor(Math.log10(x));
      return `${fmt(x / 10 ** e, 2)}·10^${e}`;
    };

    function render() {
      const minusLog2Kappa = Number(kappa.input.value);
      kappa.field.querySelector("output").textContent = fmt(minusLog2Kappa, 2);
      const k = 2 ** -minusLog2Kappa;
      const s = Number(saving.value) / 100;
      // (log2 n)^(-k) = 1 - s  =>  log2 n = 2^E,  E = log2(1/(1-s)) / k
      const E = Math.log2(1 / (1 - s)) / k;
      const log2n = E < 1024 ? 2 ** E : Infinity;
      const rows = [
        ["κ", k > 1e-4 ? fmt(k, 6) : `2^(−${fmt(minusLog2Kappa, 2)})`],
        ["potrzebne log₂ n", pow2(E)],
        ["długość wejścia n (w bitach)", log2n <= 50 ? `2${sup(Math.round(log2n))} ≈ ${fmt(2 ** log2n, 0)}`
          : E < 40 ? `2^(${fmt(log2n, 0)})` : `2^(2^(${sci(E)}))`],
      ];
      let verdict;
      if (log2n <= 50) verdict = "To mieści się w pamięci dużego komputera (2⁵⁰ bitów to ok. 128 TiB).";
      else if (log2n <= 266) verdict = "Taka liczba bitów nie zmieści się w żadnym komputerze: 2²⁶⁶ to mniej więcej liczba atomów w obserwowalnym Wszechświecie.";
      else verdict = "Wejście miałoby więcej bitów, niż jest atomów w obserwowalnym Wszechświecie (ok. 2²⁶⁶). Zysk jest czysto asymptotyczny.";
      out.replaceChildren(
        el("dl", { class: "intmul-dl" }, ...rows.flatMap(([t, d]) => [el("dt", { text: t }), el("dd", { text: d })])),
        el("p", { text: verdict }),
        el("p", { class: "intmul-note", text: "To tylko arytmetyka idealizowanego stosunku. Nieznane stałe i próg działania algorytmu przesuwają tę granicę jeszcze dalej." }));
    }
    kappa.input.addEventListener("input", render);
    saving.addEventListener("change", render);
    render();
  }

  // 3. Normalized two-point butterflies applied on each address bit.
  function butterfly(root) {
    header(root, "Motylki krok po kroku",
      "H₀(u, v) = ((u + v)/2, (u − v)/2). Każda warstwa łączy rekordy, których adresy różnią się jednym bitem.");
    const input = el("input", { type: "text", value: root.dataset.values || "8, 4, 2, 2", "aria-label": "Wartości wejściowe" });
    const size = el("select", {}, el("option", { value: "4", text: "4 rekordy (2 bity)" }), el("option", { value: "8", text: "8 rekordów (3 bity)" }));
    const svgBox = el("div", { class: "intmul-scroll" });
    const out = el("div", { class: "intmul-output", "aria-live": "polite" });
    root.append(el("div", { class: "intmul-controls" },
      el("label", { class: "intmul-field intmul-wide" }, el("span", { text: "Wartości (przecinki lub spacje; ułamki z kropką)" }), input),
      el("label", { class: "intmul-field" }, el("span", { text: "Rozmiar" }), size)), svgBox, out);

    size.addEventListener("change", () => {
      input.value = size.value === "8" ? "8, 4, 2, 2, 6, 0, 1, 3" : "8, 4, 2, 2";
      render();
    });

    function render() {
      const n = Number(size.value);
      const bits = Math.log2(n);
      const parsed = input.value.split(/[\s,;]+/).filter(Boolean).map(Number).filter((x) => Number.isFinite(x));
      const values = Array.from({ length: n }, (_, i) => parsed[i] ?? 0);
      const layers = [values];
      for (let bit = 0; bit < bits; bit++) {
        const prev = layers[layers.length - 1];
        const next = prev.slice();
        const mask = 1 << bit; // the first layer pairs adjacent records
        for (let i = 0; i < n; i++) {
          if (i & mask) continue;
          const u = prev[i], v = prev[i | mask];
          next[i] = (u + v) / 2;
          next[i | mask] = (u - v) / 2;
        }
        layers.push(next);
      }

      const colW = 150, rowH = 44, padX = 60, padY = 30;
      const width = padX * 2 + colW * bits, height = padY * 2 + rowH * (n - 1) + 20;
      const ns = "http://www.w3.org/2000/svg";
      const svg = document.createElementNS(ns, "svg");
      svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
      svg.setAttribute("class", "intmul-svg");
      svg.setAttribute("role", "img");
      svg.setAttribute("aria-label", "Sieć motylków z wartościami w każdej warstwie");
      const add = (tag, attrs, text) => {
        const node = document.createElementNS(ns, tag);
        for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, v);
        if (text != null) node.textContent = text;
        svg.append(node);
        return node;
      };
      const x = (layer) => padX + layer * colW;
      const y = (i) => padY + i * rowH;
      for (let bit = 0; bit < bits; bit++) {
        const mask = 1 << bit;
        for (let i = 0; i < n; i++) {
          const partner = i ^ mask;
          add("line", { x1: x(bit), y1: y(i), x2: x(bit + 1), y2: y(i), class: "intmul-wire" });
          add("line", { x1: x(bit), y1: y(i), x2: x(bit + 1), y2: y(partner), class: (i & mask) ? "intmul-wire is-minus" : "intmul-wire is-plus" });
        }
        add("text", { x: (x(bit) + x(bit + 1)) / 2, y: height - 4, class: "intmul-svg-caption" }, `warstwa ${bit + 1}`);
      }
      layers.forEach((vals, layer) => vals.forEach((v, i) => {
        add("rect", { x: x(layer) - 34, y: y(i) - 14, width: 68, height: 28, rx: 6, class: layer === bits ? "intmul-node is-out" : "intmul-node" });
        add("text", { x: x(layer), y: y(i) + 5, class: "intmul-svg-value" }, fmt(v));
      }));
      for (let i = 0; i < n; i++) add("text", { x: 8, y: y(i) + 5, class: "intmul-svg-addr" }, i.toString(2).padStart(bits, "0"));
      svgBox.replaceChildren(svg);

      const maxIn = Math.max(...values.map(Math.abs));
      const maxOut = Math.max(...layers[bits].map(Math.abs));
      out.replaceChildren(
        el("p", { text: `Wynik: [${layers[bits].map((v) => fmt(v)).join("; ")}]` }),
        el("p", { text: `Największy moduł: wejście ${fmt(maxIn)}, wyjście ${fmt(maxOut)}. Normalizowana warstwa nigdy nie zwiększa maksimum.` }),
        el("p", { class: "intmul-note", text: "Krawędzie ciągłe niosą sumę (u + v)/2, przerywane różnicę (u − v)/2. Odwrotność: u = a + d, v = a − d." }));
    }
    input.addEventListener("input", render);
    render();
  }

  // 4. Borrowing a scratch register and returning it.
  function registers(root) {
    header(root, "Pożyczony rejestr",
      "Wpisz dowolne x, y i dowolną zawartość rejestru pomocniczego a. Cztery aktualizacje dodają x do y i oddają a bez zmian.");
    const x = numberInput("x (źródło)", 3);
    const y = numberInput("y (cel)", 5);
    const a = numberInput("a (pomocniczy)", 7);
    const ops = [
      ["y ← y − a", (s) => ({ ...s, y: s.y - s.a }), "y"],
      ["a ← a + x", (s) => ({ ...s, a: s.a + s.x }), "a"],
      ["y ← y + a", (s) => ({ ...s, y: s.y + s.a }), "y"],
      ["a ← a − x", (s) => ({ ...s, a: s.a - s.x }), "a"],
    ];
    let step = 0;
    const table = el("div", { class: "intmul-scroll" });
    const out = el("p", { class: "intmul-result", "aria-live": "polite" });
    const nextBtn = el("button", { type: "button", text: "Następny krok", onclick: () => { step = Math.min(step + 1, 4); render(); } });
    const allBtn = el("button", { type: "button", text: "Pokaż wszystko", onclick: () => { step = 4; render(); } });
    const resetBtn = el("button", { type: "button", text: "Od początku", onclick: () => { step = 0; render(); } });
    const randBtn = el("button", {
      type: "button", text: "Losowe a",
      onclick: () => { a.input.value = String(Math.floor(Math.random() * 199) - 99); step = 4; render(); },
    });
    root.append(el("div", { class: "intmul-controls" }, x.field, y.field, a.field),
      el("div", { class: "intmul-buttons" }, nextBtn, allBtn, resetBtn, randBtn), table, out);

    function render() {
      const start = { x: Number(x.input.value) || 0, y: Number(y.input.value) || 0, a: Number(a.input.value) || 0 };
      const states = [start];
      ops.forEach(([, f]) => states.push(f(states[states.length - 1])));
      const t = el("table", { class: "intmul-table" });
      t.append(el("tr", {}, ...["krok", "operacja", "x", "y", "a"].map((h) => el("th", { text: h }))));
      states.forEach((s, i) => {
        const changed = i > 0 ? ops[i - 1][2] : null;
        const row = el("tr", { class: i > step ? "is-hidden" : i === step ? "is-current" : "" },
          el("td", { text: String(i) }), el("td", { text: i === 0 ? "start" : ops[i - 1][0] }),
          ...["x", "y", "a"].map((key) => el("td", { class: key === changed ? "is-changed" : "", text: i > step ? "?" : String(s[key]) })));
        t.append(row);
      });
      table.replaceChildren(t);
      nextBtn.disabled = step >= 4;
      const end = states[4];
      out.textContent = step < 4
        ? `Krok ${step} z 4.`
        : `Koniec: y = ${start.y} + ${start.x} = ${end.y}, x = ${end.x} bez zmian, a wróciło do ${end.a}.` +
          (end.a === start.a && end.y === start.y + start.x ? " Tożsamość działa dla każdej wartości a." : "");
    }
    [x, y, a].forEach((f) => f.input.addEventListener("input", render));
    render();
  }

  // 5. Recursive accounting: s calls on volume V/W per width factor m.
  function recursion(root) {
    header(root, "Ile kosztuje rekurencja?",
      "Rodzic o szerokości m·f wywołuje s dzieci, każde na objętości V/W. Opłaca się, gdy s/W < m.");
    const m = rangeInput("m (mnożnik szerokości)", 2, 2, 8);
    const W = rangeInput("W (liczba ról)", 2, 1, 8);
    const s = rangeInput("s (liczba wywołań)", 3, 1, 64);
    const chart = el("div", { class: "intmul-scroll" });
    const out = el("div", { class: "intmul-output", "aria-live": "polite" });
    root.append(el("div", { class: "intmul-controls" }, m.field, W.field, s.field), chart, out);

    function render() {
      const mv = Number(m.input.value), Wv = Number(W.input.value), sv = Number(s.input.value);
      const ratio = sv / Wv;
      const q = Math.log(ratio) / Math.log(mv);
      const depths = [0, 1, 2, 3, 4, 5, 6];
      const total = depths.map((j) => ratio ** j);
      const naive = depths.map((j) => mv ** j);
      const maxV = Math.max(...total, ...naive);

      const ns = "http://www.w3.org/2000/svg";
      const width = 640, height = 220, padL = 46, padB = 34, barW = 28;
      const svg = document.createElementNS(ns, "svg");
      svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
      svg.setAttribute("class", "intmul-svg");
      svg.setAttribute("role", "img");
      svg.setAttribute("aria-label", "Porównanie łącznej odwiedzonej objętości z naiwnym kosztem na kolejnych głębokościach");
      const add = (tag, attrs, text) => {
        const node = document.createElementNS(ns, tag);
        for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, v);
        if (text != null) node.textContent = text;
        svg.append(node);
      };
      const scaleY = (v) => (Math.log(v) / Math.log(maxV || 2)) * (height - padB - 16);
      add("line", { x1: padL, y1: height - padB, x2: width - 10, y2: height - padB, class: "intmul-axis" });
      depths.forEach((j) => {
        const cx = padL + 20 + j * ((width - padL - 40) / depths.length);
        const hN = maxV > 1 ? scaleY(naive[j]) : 0;
        const hT = maxV > 1 ? Math.max(scaleY(Math.max(total[j], 1)), 0) : 0;
        add("rect", { x: cx, y: height - padB - hN, width: barW, height: hN, class: "intmul-bar is-naive" });
        add("rect", { x: cx + barW + 4, y: height - padB - hT, width: barW, height: hT, class: "intmul-bar" });
        add("text", { x: cx + barW, y: height - padB + 18, class: "intmul-svg-caption" }, `j = ${j}`);
      });
      add("text", { x: padL, y: 14, class: "intmul-svg-legend" }, "szare: naiwne mʲ · kolorowe: (s/W)ʲ · skala logarytmiczna");
      chart.replaceChildren(svg);

      let verdict;
      if (ratio < 1) verdict = "s/W < 1: koszt maleje z głębokością. W prawdziwej konstrukcji tak dobre parametry się nie zdarzają.";
      else if (ratio < mv) verdict = `Oszczędność: wykładnik q = log_${mv}(${fmt(ratio, 3)}) ≈ ${fmt(q, 3)} < 1. Koszt rośnie wolniej niż szerokość.`;
      else if (ratio === mv) verdict = "s/W = m: brak ostrej oszczędności, rekurencja kosztuje tyle co naiwne podwajanie.";
      else verdict = `s/W > m: rekurencja jest droższa niż metoda naiwna (q ≈ ${fmt(q, 3)} > 1).`;
      const eta = (Wv * mv - sv) / (Wv * mv);
      out.replaceChildren(
        el("dl", { class: "intmul-dl" },
          el("dt", { text: "s/W" }), el("dd", { text: fmt(ratio, 4) }),
          el("dt", { text: "deficyt η = (Wm − s)/(Wm)" }), el("dd", { text: fmt(eta, 4) }),
          el("dt", { text: "objętość po 6 poziomach" }), el("dd", { text: `${fmt(total[6], 2)}·V zamiast ${fmt(naive[6], 0)}·V` })),
        el("p", { text: verdict }),
        el("p", { class: "intmul-note", text: "W pracy deficyt jest rzędu 2⁻⁵⁰, więc wykładnik spada tylko minimalnie poniżej 1." }));
    }
    [m, W, s].forEach((f) => f.input.addEventListener("input", render));
    render();
  }

  const widgets = { convolution, scale, butterfly, registers, recursion };
  function init() {
    document.querySelectorAll(".intmul[data-intmul]").forEach((root) => {
      const build = widgets[root.dataset.intmul];
      if (!build || root.dataset.ready) return;
      root.dataset.ready = "1";
      root.replaceChildren();
      build(root);
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
