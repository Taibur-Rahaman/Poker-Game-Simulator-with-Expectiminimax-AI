# Final Report Review & Correction Checklist — Group 7

**Course:** CSE440, Section 01  
**Project:** Strategic Poker Game Simulation Using Expectiminimax Under Uncertain Card Events  

**Authors:**  

- Kazi Eraj Al Minahi Turjo — 1831906642  
- Md. Sabbir Hossain — 2212642042 *(verify against RDS)*  
- Nashita Tasneem Noor — 2132126642  
- Talha Imtiaz — 2012211642  

Use this list before exporting the **8-page IEEE-style final report PDF** for GitHub (`others/`) and the printed **both-sided** copy.

---

## 1. Must fix (submission / clarity)

### 1.1 Title page and abstract layout

- **Problem:** Talha’s affiliation/contact block appeared misplaced relative to Abstract; stray fragments (e.g. “chance outcomes. This makes poker a practical example of the …”) leaked into wrong positions after PDF/copy-paste.
- **Fix:** Restore a clean **IEEE-style first page**: course header → title → **all four authors and affiliations in one coherent block** → **Abstract** (one continuous paragraph) → **Index Terms** → body sections.

### 1.2 Equation (2) — value function \(V(s)\)

- **Problem:** The piecewise definition was **scrambled or incomplete** in the draft (fragments, missing MAX case, broken `cases` / display math).
- **Fix:** Show **three** coherent cases explicitly, for example:
  - **AI (MAX):** \(\max_{a \in A(s)} V(T(s,a))\)
  - **Opponent (MIN / policy layer):** \(\min_{a \in A(s)} V(T(s,a))\) *or* the expected value under your stated opponent policy — **be consistent** with what you implemented.
  - **Chance:** \(\sum_{o \in O(s)} P(o\mid s)\, V(T(s,o))\) (or integral / expectation notation as appropriate), with sampling noted in prose.

### 1.3 Tables mixed with prose

- **Problem:** Table 3 (metrics) was interleaved with paragraphs from Sections 7.3 / 7.4 (“largest raise…”, interpretation text).
- **Fix:** Separate **tabular content** from **running text**. Each table: caption + rows only; subsection text continues **below** or **above**, not mid-table.

### 1.4 Table formatting (especially Table 4)

- **Problem:** Line breaks split cells awkwardly (e.g. “Verified” / “card draw”).
- **Fix:** Proofread **every table** in the **compiled PDF** (not only the editor).

### 1.5 Package name consistency

- **Problem:** “poker ai” (space) vs actual package name.
- **Fix:** Use **`poker_ai`** everywhere in the report.

### 1.6 Section numbering and headings

- **Problem:** Bullet-style headings (“• Introduction”) are nonstandard for article-style double-column reports.
- **Fix:** Use **numbered sections** (e.g. **1** Introduction, **2** …) and consistent heading levels per your IEEE template.

### 1.7 Student IDs

- **Fix:** Confirm **every** ID matches **RDS** exactly. Any mismatch is a serious submission error.

---

## 2. Strongly recommended (accuracy & fairness)

### 2.1 Decision time wording

- **Issue:** “0.152 seconds **per hand**” may be ambiguous (per hand vs per AI decision).
- **Fix:** Define precisely: e.g. wall-clock for **all Seat 0 decisions in one hand**, or **mean per decision**, and keep **Abstract** and **Section 7.2** aligned with the code.

### 2.2 Positive-hand rate vs “win rate”

- **Issue:** Loose use of “win rate” conflicts with your careful definition of **positive-hand rate**.
- **Fix:** Use **one term** in abstract/slides/report or add a sentence linking them.

### 2.3 Baseline vs Expectiminimax (variance)

- **Issue:** Baseline led in cumulative chips in one run while Expectiminimax led on positive-hand frequency — readers may miss that this is variance.
- **Fix:** Keep **one explicit paragraph** stating that **frequency** and **chip magnitude** disagree in short runs; avoid over-claiming.

### 2.4 Figure numbering and order

- **Issue:** References to Figures 1–8 should match **final PDF order** (no figure number appearing before its anchor in the narrative).
- **Fix:** Compile once; skim figure list vs first mention order.

---

## 3. References and acknowledgments

### 3.1 IEEE-style references

- **Problem:** Bullet list of references instead of **[1]**, **[2]** with matching in-text cites.
- **Fix:** Switch to **numbered** reference list aligned with cites like **[1], [4], [6]** in prior work.

### 3.2 AI-assisted disclosure

- **Status:** Acknowledgment of AI-assisted drafting is appropriate; ensure it matches institutional/course norms and lists tools used (**ChatGPT** etc.) as already drafted.

---

## 4. Optional polish

| Item | Suggestion |
|------|-------------|
| Index Terms | Check capitalization / punctuation vs IEEE conventions. |
| Member contributions | Optionally add **one tangible artifact per person** (module, demo, figures). |

---

## 5. Bottom line for the group

Scientific narrative and humility about limitations are appropriate for course level. The **main grade risk** is **layout and LaTeX damage**: **authors/Abstract**, **Equation (2)**, and **Table 3 merged with §7 prose**. Correct those first, then **IDs**, **terminology**, and **reference formatting**.

---

*Checklist derived from an internal review of the Group 7 final report draft. Update this file if the PDF content changes.*
