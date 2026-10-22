# Research Writing Guide

This guide governs every prose artifact of a research topic: `research-plan.md`, `research-log.md`, gate reports and notebook markdown cells.

It implements sections 13.5 (narrative) and 13.6 (prose layout) of [`standard.md`](standard.md). The validator checks the mechanical parts; a reviewer checks the rest.

Contents:

1. [Language](#1-language)
2. [Layout](#2-layout)
3. [Notebook narrative](#3-notebook-narrative)
4. [Examples](#4-examples)

## 1. Language

### 1.1. Choosing the language

The topic language is chosen once, at initialization, with `--language en` or `--language vi`. It is stored as `language:` in section 1 of `research-plan.md`.

Every prose artifact of the topic uses that language. Do not mix languages between notebooks or log entries.

Identifiers stay in English in both languages: Problem Card keys, gate IDs, statuses, rule IDs, file names, column names and code.

### 1.2. Vietnamese topics

Write the sentence in Vietnamese and keep technical terms in English. Do not translate a term that the team reads in English in code, papers or dashboards.

Keep these in English: baseline, candidate, hypothesis, feature, label, target, threshold, split, train, validation, locked test, snapshot, manifest, pipeline, schema, entity, event time, leakage, metric, precision, recall, F1, guardrail, slice, support, confidence interval, bootstrap, seed, run, artifact, alert, episode, drift, rollback.

Do not add Vietnamese glosses in parentheses after an English term. If a term needs explaining, explain it in a separate sentence the first time it appears.

### 1.3. Numbers

Use `.` as the decimal separator in both languages, so prose matches the tables and code output it cites.

Do not use `.` or `,` as a thousands separator. Write `1381220` or `1 381 220`.

Always state the unit and the population of a number: "0.37 AUPRC on 28792 validation bins", not "0.37".

## 2. Layout

### 2.1. Headings

Each Markdown file has exactly one H1. Sections are numbered: `## 1.`, `### 1.1.`, `#### 1.1.1.`.

Notebooks keep the fixed section headings `## 1.` to `## 5.` from section 13.2 of the standard. Analysis blocks are `### 3.1.`, `### 3.2.` and so on, one per question.

### 2.2. Paragraphs

Never break a line in the middle of a sentence. One paragraph is one source line.

Keep one idea per paragraph, usually one to three sentences. Separate paragraphs with a blank line.

A blank line is also required between consecutive `**Label:** value` lines. Without it, Markdown and Jupyter render all labels as one clustered paragraph.

### 2.3. Bullets

One fact or decision per bullet, written as a full sentence.

Write relations in words. Do not chain symbols such as `→`, `·`, `⇔` or `vs` in place of a sentence. Arrows are allowed only for time ranges and data flow (`Bronze → Silver`).

When a bullet needs more than two sentences, it is a paragraph or a sub-section, not a bullet.

### 2.4. Tags and callouts

Mark the epistemic status of a statement with a leading tag when it is not obvious: `[FACT]`, `[HYPOTHESIS]`, `[DECISION]`, `[LIMITATION]`.

In `.md` files, use callouts (`> [!note]`, `> [!warning]`) for content the reader must not miss, such as an owner decision or an invalidated result. In notebooks, use a bold label instead, because Jupyter does not render callouts.

### 2.5. Tables

Use a table when the reader compares the same fields across rows. Every metric table follows section 13.4 of the standard: split, metric definition, threshold, support and uncertainty.

Introduce the table before it appears and explain it after. A table is never its own conclusion.

## 3. Notebook narrative

### 3.1. Who the reader is

Write for a teammate who knows the domain and the data but has never read the standard and never saw the conversation that produced the notebook.

That reader does not know what `S07`, `E12` or `G1` mean. Rule IDs, evidence IDs and gate codes go only in the **Trace:** line at the end of a block, never in a question, a **What to look for** or an **Answer**.

Reasoning stated in the conversation does not exist for this reader. If it matters, it goes into the notebook or the research log.

### 3.2. The notebook is a list of answered questions

Section 1 lists the questions the notebook answers, numbered `1.` to `n.`. Each question states in one sentence why it matters for the gate decision.

Section 3 has one block per question, `### 3.k.`, in the same order. Each block reads in three steps:

| Step | Label (en / vi) | Written | Contains |
|---|---|---|---|
| 1 | **What to look for:** / **Cần nhìn gì:** | before the code runs | which table or figure comes next, which column or region to look at, which result means "fine" and which means "problem" |
| 2 | code cell | | one function call for this question; at most one table or figure per cell |
| 3 | **Answer:** / **Trả lời:** | after the output | the direct answer in the first sentence, with numbers; whether the criterion from step 1 is met; the consequence for the next step |

Section 5 closes every question in a findings table with one row per question and one of the verdicts `Met` / `Not met` / `Partly met` / `Undetermined` (`vi`: `Đạt` / `Không đạt` / `Đạt một phần` / `Chưa xác định`). **Not proven**, **Limitations** and **Next decision** follow the table.

### 3.3. Rules that keep the thread intact

Every concern the prose raises is either a question with its own block or an item in **Not proven**. Do not name completeness, cadence or availability in an introduction and then never come back to them.

**What to look for** is a criterion, not a prediction to be forgotten. **Answer** always says whether the criterion was met, using the same words.

Never show a table or figure without saying first what it is for. A reader who meets an unexplained table has to reverse-engineer the decision behind it.

Describe the data and the result, not the history of the notebook. Reruns, replays and rewritten narrative belong in `research-log.md`.

Do not copy the same paragraph between notebooks. If two notebooks share a conclusion, state it in one and link to it from the other.

### 3.4. Order of work

Write the notebook in this order, so that criteria cannot be bent to fit results:

1. List the questions in section 1, each with why it matters for the gate decision.
2. Write every block's **What to look for** before any code runs.
3. Implement one module function per question, and write the code cells.
4. Execute the notebook from a clean kernel with placeholder answers.
5. Write each **Answer** and the findings table from the executed outputs.
6. Check every number in the answers against the output it cites, then run the validator.

Step 6 is not optional. A median of two values read as a range, or a minimum read as a maximum, produces a confident sentence that the table does not support.

Prefer numbers that appear in the displayed table. When an answer needs a number the table does not show, add it to the table or cite the artifact that contains it.

### 3.5. Rewriting a notebook that has already run

When a notebook is rewritten after its results are known, a criterion written now is not a prediction. Take every criterion from an approved source (the Evaluation Protocol, readiness thresholds or the Data Contract), not from the observed numbers.

Record in `research-log.md`, not in the notebook, that the criteria were written after the results were known. The notebook describes the data; the log describes how the notebook came to be.

Before replacing the old notebook, back it up and compare the new run's artifacts with the old run's. Only run metadata (IDs, environment, timing) may differ; any other difference is a change in results and must be explained in the log.

### 3.6. What the validator checks

The validator checks that every question has a block and a findings row, that each block has **What to look for** before its code and **Answer** after it with minimum word counts, that every table or figure sits inside a block with markdown after it, that verdicts use the allowed values, and that no audit codes appear in reader-facing prose.

It cannot check that an answer actually answers its question. That is the reviewer's job.

## 4. Examples

### 4.1. Clustered labels

Avoid this. It renders as one paragraph:

```markdown
**Câu hỏi:** Dữ liệu có đủ sạch để định nghĩa sự kiện không?
**Giả thuyết:** Số liệu §4 tái lập được.
**Dữ liệu/snapshot:** Bronze `ab805dc218c2`.
```

Prefer this:

```markdown
**Câu hỏi:** Dữ liệu có đủ sạch để định nghĩa sự kiện không?

**Giả thuyết:** Số liệu §4 của plan tái lập được.

**Dữ liệu/snapshot:** Bronze `ab805dc218c2`.
```

### 4.2. Dense bullets

Avoid this:

```markdown
- [FACT] RTT: p50 2,30 ms · p95 11,4 · p99 88,9 · max 2.145 ms → tail dài.
```

Prefer this:

```markdown
- [FACT] RTT has a long tail: p50 is 2.30 ms, p95 is 11.4 ms, p99 is 88.9 ms and the maximum is 2145 ms.
```

### 4.3. A question block

The question listed in section 1:

```markdown
2. RTT bị thiếu ở đâu và thiếu nghĩa là gì? RTT là một input chính của detector, nên cách xử lý giá trị thiếu ảnh hưởng trực tiếp tới score.
```

Its block in section 3:

```markdown
### 3.2. RTT bị thiếu ở đâu và thiếu nghĩa là gì?

**Cần nhìn gì:** Bảng dưới đếm probe thiếu RTT, tách theo camera reachable hay không. Thiếu khi unreachable là bình thường vì không có ping nào trả về. Thiếu khi camera vẫn reachable là dấu hiệu lỗi ở poller.
```

The code cell calls one function, `rtt_missing_breakdown(...)`, and displays one table. Then:

```markdown
**Trả lời:** RTT thiếu ở 949 trên 460723 probe. 520 trường hợp xảy ra khi camera unreachable, đúng như kỳ vọng.

429 trường hợp còn lại xảy ra khi camera vẫn reachable, ở 13 camera. Đây là lỗi poller chưa được giải thích, nên tiêu chí "chỉ thiếu khi unreachable" **không đạt**.

Hệ quả: giữ RTT là missing, không thay bằng 0, vì thay bằng 0 sẽ biến lỗi poller thành một phép đo tốt. Nguyên nhân của 429 probe được chuyển thành câu hỏi mở cho owner.

**Trace:** S07 completeness; threshold `rtt_missing_reachable` trong `g1-readiness-thresholds.json`.
```

Its row in the findings table:

```markdown
| # | Câu hỏi | Trả lời | Đánh giá | Hệ quả |
|---|---|---|---|---|
| 2 | RTT thiếu ở đâu? | 949 probe; 429 thiếu khi camera vẫn reachable | Đạt một phần | Giữ missing; hỏi owner nguyên nhân 429 probe |
```

### 4.4. Prose written for an auditor

Avoid this. It names rules instead of reasons, raises concerns it never answers, and narrates the notebook's own history:

```markdown
**Vì sao:** G1 cần kiểm tra nguồn, completeness, cadence và availability trước feature fitting theo S05–S08.

**Kết quả kỳ vọng:** Lần replay này dự kiến giữ 1381220 dòng. Kỳ vọng được viết trước lần replay này, không phải preregistration độc lập.
```

Prefer turning each concern into its own numbered question, as in 4.3.
