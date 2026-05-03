# Group 7 — Final Presentation Script & Timeline

**Course:** CSE440 — Artificial Intelligence · **Section:** 01  
**Instructor:** Mohammad Shifat-E-Rabbi (MSRB)  
**Group:** 7  

**Members:**  

- Kazi Eraj Al Minahi Turjo — 1831906642  
- Md. Sabbir Hossain — 2212642042  
- Nashita Tasneem Noor — 2132126642  
- Talha Imtiaz — 2012211642  

**Project:** Development of a Poker Game Simulator with Expectiminimax AI (simplified Texas Hold’em).

---

## 1. Course manual — compliance checklist

Use this before **Class 23** (submission) and **Class 24** (Groups 6–10 present).

| Requirement | Notes for Group 7 |
|-------------|-------------------|
| **Slot** | **15 minutes**, sequential. Start **automatically** when your time begins—even if the previous group runs late. Unused time **is not** recovered. |
| **Attendance** | **Both** Class 23 and 24 (**everyone** must be present). |
| **Materials** | Present **only** what is already on **GitHub** before the deadline (PPTX, video, code). |
| **Laptops** | **Not allowed** — use classroom PC for GitHub and slides. |
| **Opening** | **Mandatory:** introduce **every** member with **full legal names**. |
| **Slides** | **Mandatory footer on every slide:** (1) group number (2) **all** member names. |
| **Slide style** | Short intro/significance/conclusion; **big picture** on PPT. Avoid walls of text and generic filler. |
| **Live run** | **Do not run** the app live. Use the **submitted one-minute screen-capture video** (user perspective). |
| **GitHub segment (~4 min)** | Cover: repo **home + README**, **commit history** scroll, **every part** of **code**, **every part** of **repo** (folders). |
| **`others/` contents** | Final PPTX, final report PDF, update PPTX, update report PDF, one-minute demo video — per manual. |
| **Marks** | Timeliness, report, presentation (**2.5%** among project components), code/GitHub (**2.5%**), teamwork visible in commits. |
| **Bonus** | Prepared **questions for other groups’** presentations. |

---

## 2. Master timeline (15:00 total)

Let **T = 0:00** when Group 7 **begins speaking** (start of your slot).

| Time from start | Length | Segment |
|-----------------|--------|---------|
| **0:00 – 1:00** | 1:00 | **A. Member introductions** (full names) |
| **1:00 – 9:30** | 8:30 | **B. Slide deck** |
| **9:30 – 10:30** | 1:00 | **C. One-minute demo video** (no live Streamlit run) |
| **10:30 – 14:30** | 4:00 | **D. GitHub walkthrough** |
| **14:30 – 15:00** | 0:30 | **E. Thank you + handoff** |

**Contingency:** If behind at **~8:00** into Part B, shorten **Experimental evaluation** and **Results** first; **protect** the video and **README + commits**.

---

## 3. Part A — Introductions (0:00 – 1:00)

**Kazi (0:00 – 0:15):**  
“Assalamu alaikum / good [morning/afternoon]. We are **Group 7**, CSE440 Section 01, **Strategic Poker Game Simulation with Expectiminimax**. I am **Kazi Eraj Al Minahi Turjo**.”

**Sabbir (0:15 – 0:30):**  
“I am **Md. Sabbir Hossain**.”

**Nashita (0:30 – 0:45):**  
“I am **Nashita Tasneem Noor**.”

**Talha (0:45 – 1:00):**  
“I am **Talha Imtiaz**. We will show our design, a one-minute user demo, then our repository on GitHub.”

---

## 4. Part B — Slide-by-slide script (1:00 – 9:30)

### B1 | 1:00 – 1:45 (45 s) — Title + project strip — **Kazi**

**Script:**  
“We built a **simplified Texas Hold’em** simulator. The AI core is **Expectiminimax with Monte Carlo** sampling. The interface is **Streamlit** with tabs. Our focus is **decision-making under uncertainty** — hidden opponent cards and random future community cards.”

---

### B2 | 1:45 – 3:05 (80 s) — Project at a Glance — **Kazi**

**Script:**  
“**Problem:** Poker is imperfect information — we never see the opponent’s hole cards, and **chance** matters on every street.  
**Goal:** A **playable** simulator where the agent chooses actions using **Expectiminimax**, so we can **see search under randomness**.  
**Output:** A **Streamlit** app — **play one hand**, a **Kid Play** tab for beginners, and **Simulation & Evaluation** to run **many hands** and compare modes.”

---

### B3 | 3:05 – 3:40 (35 s) — Key idea — **Sabbir**

**Script:**  
“Our pipeline combines **game engine**, **hand evaluation**, **Expectiminimax search**, and **Monte Carlo sampling**. At each decision, the AI considers **legal actions**, estimates **expected value**, and chooses the action with the **highest EV**.”

---

### B4 | 3:40 – 4:50 (70 s) — System Architecture — **Kazi**

**Script:**  
“Architecture is layered. **Top:** Streamlit — play, kid mode, simulation. **Middle:** game logic — **deck, players, rules, game engine**, and metric collection. **Bottom:** **Expectiminimax** — it reads a **compact search state** and returns an **action**. Data flows **state → AI → action → engine updates pot and rounds**.”

---

### B5 | 4:50 – 6:05 (75 s) — Game Flow and Core Modules — **Nashita**

**Script:**  
“One hand runs **preflop → flop → turn → river → showdown**. Each player has **two private** cards; the board adds **three**, then **fourth**, **fifth**; **best five from seven** wins.  

Brief file map: **`deck.py`** — cards and shuffle; **`player.py`** — stacks, bets, fold state; **`poker_rules.py`** — seven-card hand ranking; **`game_engine.py`** — street transitions and showdown; **`expectiminimax.py`** — search and EV; **`evaluation.py`** — automated batches; **`main.py`** — Streamlit entry.”

---

### B6 | 6:05 – 7:30 (85 s) — Expectiminimax in Our Simulator — **Sabbir**

**Script:**  
“**MAX nodes:** the AI chooses among **fold**, **call or check**, and **discrete raise sizes** to control branching.  
**MIN nodes:** the opponent is not a full equilibrium solver — we approximate response with a **simple policy**.  
**CHANCE nodes:** unknown cards — we **sample** from the remainder of the deck.  
**Leaf evaluation:** **Monte Carlo rollouts** estimate **relative hand strength** and **payoff-style utility**.  
**Final choice:** at the root we compare actions and pick the **highest estimated expected value**. We also store values for **root decision analysis** in the UI.”

---

### B7 | 7:30 – 8:40 (70 s) — Implementation / User Features — **Nashita**

**Script:**  
“**Play Game** runs AI versus opponent: **chips, pot, stage, board, winner**, and **AI root-action EV** display when enabled.  

**Kid Play** uses **simpler language** — useful for demos and teaching.  

**Simulation & Evaluation** runs **automated hands** — **rates, chip trends, decision time**, comparing **Expectiminimax** to a **simpler baseline**.”

---

### B8 | 8:40 – 9:05 (25 s) — Experimental Evaluation — **Talha**

**Script:**  
“In one **representative automated run**: **two hundred** hands, Expectiminimax versus baseline. Expectiminimax **win rate fifty-five percent** in that run — **higher** than baseline here. **Average decision time** about **fifty milliseconds** — **more compute** than a trivial policy.”

**Note:** If slide numbers disagree with the **final report**, say explicitly: “This slide is **run configuration A**; the report cites **depth X / samples Y**” — avoid contradicting yourselves silently.

---

### B9 | 9:05 – 9:20 (15 s) — What the Results Tell Us — **Talha**

**Script:**  
“Interpretation: **search** improved strategic quality versus our **simple baseline** in this experiment, but **latency** rises from lookahead and sampling. **Increasing depth or sample count** can improve estimates but **slows** the interactive app.”

---

### B10 | 9:20 – 9:30 (10 s) — Limitations — **Sabbir** + bridge — **Kazi**

**Sabbir (~5–10 s max):**  
“Limitations: **heads-up simplified** setting, **basic opponent model**, **capped depth and samples** for responsiveness, **representative not tournament-scale** evaluation.”  

**Kazi (~5 s):**  
“Next — our **submitted one-minute demo**, then **GitHub**.”

**Optional rehearsal variant:** If you consistently finish Part B early, expand **Limitations + Future work** to **35–40 s** (move video start — only after timed practice).

---

## 5. Part C — One-minute demo video (9:30 – 10:30)

**Intro (whoever owns the demo file, ~5 s):**  
“This is our **submitted one-minute demo** — **screen capture**, **user perspective**. We do **not** run Streamlit live, per course rules.”

**Play video (60 s).**

---

## 6. Part D — GitHub walkthrough (10:30 – 14:30)

**Style:** Classroom browser → **public repo** already submitted. Zoom **~110%**. **Scroll** quickly; **do not** execute code.

| Time | Speaker | Script / actions |
|------|---------|-------------------|
| **10:30 – 11:05** | **Kazi** | Repo **home**. **README** — name, setup, run command (`requirements.txt`, `main.py`). Open **`main.py`** — tabs / entry (**~10–15 s**). |
| **11:05 – 11:35** | **Talha** | **Commits** history — scroll to show activity **over time**, **multiple authors** if applicable. One line: “continuous teamwork.” |
| **11:35 – 12:25** | **Kazi** | **`poker_ai/game_engine.py`** (adjust path if different) — top / middle / bottom scroll: betting loop, streets, showdown. |
| **12:25 – 13:05** | **Sabbir** | **`expectiminimax.py`** — MAX/MIN/chance structure, recursion depth, sampling. |
| **13:05 – 13:35** | **Talha** | **`evaluation.py`**; peek **`visualization.py`** if used; **`poker_rules.py`** or **`deck.py`** — brief. |
| **13:35 – 14:10** | **Nashita** | **`kid_ui.py`**, **`player.py`**; folders **`data/`**, **`support/`**, **`others/`** (PPTX, PDF, video). **`requirements.txt`**. |
| **14:10 – 14:30** | **Kazi** | Any **remaining** files/folders; “That completes the repository walkthrough.” |

---

## 7. Part E — Closing (14:30 – 15:00)

**Kazi (~20–25 s):**  
“We built a **modular** simplified Hold’em simulator with **Expectiminimax under uncertainty** — chance nodes and Monte Carlo estimation. Deliverables match the submitted **GitHub** package. Thank you.”

**All:** Acknowledge instructor; yield room for **Questions** until hard **15:00** end — next group protocol per manual.

---

## 8. Speaker responsibility summary

| Member | Sections |
|--------|----------|
| **Kazi** | Intro orchestration; title, glance, architecture; repo README / `main` / engine / close; timers recommended |
| **Sabbir** | Key idea; Expectiminimax; short limitations; live `expectiminimax.py` |
| **Nashita** | Game flow + modules; UI features; `kid_ui` / `player` / `others` folders |
| **Talha** | Evaluation + results slides; commits; `evaluation.py` (+ related files) |

---

## 9. Slide content map (for deck alignment)

1. Title / course / group / names & IDs + “game type / AI / interface / focus”  
2. Project at a Glance — problem, goal, output  
3. Key idea — engine + eval + search + EV  
4. System Architecture — layers + data flow  
5. Game Flow and Core Modules — streets + file list  
6. Expectiminimax — MAX / MIN / CHANCE / MC / root choice  
7. Implementation — Play Game, Kid Play, Simulation  
8. Experimental Evaluation — N hands, win rate, decision time  
9. What the Results Tell Us — quality vs cost  
10. (Optional) GitHub tree — or rely on live walk only  
11. Limitations & Future Work — if not fully spoken in Part B bridge  
12. Conclusion — three bullets → thank you  

---

## 10. Pre-presentation rehearsal checklist

- [ ] **Footer** on every slide: **Group 7** + all names  
- [ ] Dry run with **timer** — hit **9:30 ±15 s** before video  
- [ ] Classroom PC: GitHub loads; **logged in** only if needed; **video** plays from **`others/`** or embedded slide  
- [ ] Narration **under** noisy room — subtitles on video optional  
- [ ] Align **evaluation numbers** between **PPT** and **report** or annotate “representative run”  
- [ ] Prepare **one question** each for bonus (other groups)  
- [ ] **Printed report** handed in Class 23 start (course rule for all groups)  
- [ ] Confirm **`others/`** on GitHub has all five artifacts before deadline  

---

*Prepared for Group 7 final presentation script practice. Adjust file paths (`poker_ai/...`) to match the repository layout if names differ.*
