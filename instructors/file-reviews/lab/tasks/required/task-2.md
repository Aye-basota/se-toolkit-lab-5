# Review: `lab/tasks/required/task-2.md`

/**Date:** 2026-03-07

**Convention files used:**

- `contributing/conventions/writing/tasks.md` — task structure, design principles, conceptual review dimensions (D1–D12)
- `contributing/conventions/writing/common.md` — writing conventions (4.1–4.26)

---

## Conceptual findings

### D1. Learning objective clarity

1. **[Low]** Line 9 (Purpose). Purpose contains two sentences: "Implement four analytics endpoints that perform `SQL` aggregation queries on the data populated by the ETL pipeline. Use pre-written tests to verify your implementation." The template specifies `<One sentence: what the student will learn.>`
   **Suggested fix:** Merge into one sentence, e.g., "Implement four analytics endpoints using `SQL` aggregation queries and verify them with pre-written tests."

### D2. Step-by-step completeness

1. **[Medium]** Lines 248–255 (Step 1.8.1). The step instructs students to run commands "on your VM" (including `cd se-toolkit-lab-5`, `git fetch`, `docker compose up`) but does not include SSH instructions or reference a prior step/wiki section for connecting to the VM. A student who doesn't remember the SSH procedure may be blocked.
   **Suggested fix:** Add a sub-step or link to the wiki for SSH connection before the VM commands, or reference the corresponding step in an earlier task (e.g., Task 1's deploy step).

2. **[Low]** Line 264 (Step 1.8.4). Compound instruction: "Try each analytics endpoint with `lab=lab-04` (or any lab that has data). Verify that each returns a `200` response with a `JSON` array." Two distinct actions in one step.
   **Suggested fix:** Split into two numbered steps: one for executing the endpoints, one for verifying the response.

### D3. Student navigation

1. **[Medium]** Line 13 (Context). "The ETL pipeline from Task 1" references Task 1 without a link. A student reading the Context section has no way to navigate to Task 1 for background.
   **Suggested fix:** Link to `./task-1.md`, e.g., "The ETL pipeline from [Task 1](./task-1.md) has populated..."

2. **[Medium]** Lines 92–109 (Step 1.5). The inline mini-ToC (lines 106–109) is not placed "right after the `###` heading" as required by convention 1.1 in tasks.md. Several paragraphs of introductory content (lines 94–103) and a TIP block (lines 96–101) appear between the heading and the mini-ToC.
   **Suggested fix:** Move the mini-ToC (with `<!-- no toc -->`) immediately after the `### 1.5.` heading. Place the introductory paragraphs and TIP block after the mini-ToC but before the first `####` sub-section.

### D4. Checkpoints and feedback loops

1. **[Medium]** Lines 248–258 (Step 1.8.1). The Docker deployment command (`docker compose ... up --build -d`) has no checkpoint. Students cannot verify whether the containers started correctly before proceeding to Swagger UI.
   **Suggested fix:** Add a checkpoint after the command, e.g., "You should see the containers starting. Run `docker compose ps` to verify all services are running."

2. **[Medium]** Lines 248–258 (Step 1.8.1). Infrastructure step (Docker, VM deployment) has no troubleshooting block. Convention 4.19 in tasks.md requires collapsible troubleshooting for environment-dependent steps.
   **Suggested fix:** Add a `<details><summary><b>Troubleshooting (click to open)</b></summary>` block covering common VM deployment failures (port conflicts, stale containers, missing `.env.docker.secret`).

### D5. Acceptance criteria alignment

No issues found.

### D6. Difficulty and progression

No issues found.

### D7. Practical usability

1. **[Medium]** Lines 248–258 (Step 1.8.1). The deploy step could silently fail with no checkpoint or troubleshooting guidance (see D4 findings 1–2). Students may proceed to Swagger UI and encounter confusing errors without understanding the root cause.
   **Suggested fix:** See D4 suggested fixes.

### D8. LLM-independence

No issues found. The task provides detailed query logic for manual implementation (steps 1.5.1–1.5.4) and TODO comments in the stubs. The AI tip is explicitly optional.

### D9. Git workflow coherence

No issues found.

### D10. Conceptual gaps and misconceptions

1. **[Low]** Line 131 (Step 1.5.1, query logic item 4). The `CASE WHEN` SQL syntax is referenced without explanation or link. Students unfamiliar with SQL case expressions may not know how to write them.
   **Suggested fix:** Add a brief NOTE or link to SQL `CASE WHEN` documentation.

### D11. Controlled AI steps

1. **[Low]** Lines 96–101 (TIP block). The AI tip provides an approximate prompt ("give it a prompt like:") rather than an exact or templated prompt. Convention 4.20 in tasks.md recommends exact prompts or templates with `<placeholders>` for reproducibility. Since AI use is optional, this is low severity.
   **Suggested fix:** Rephrase to "use this prompt:" and present the prompt in a fenced code block or `<placeholder>`-based template.

### D12. Autochecker verifiability

No issues found.

---

## Convention findings

### 4.1. Instructions wording

1. ~~**Line 264.** Compound instruction: "Try each analytics endpoint with `lab=lab-04` (or any lab that has data). Verify that each returns a `200` response with a `JSON` array." Convention: "Never write 'Do A and do B.' Instead, split into two numbered steps."~~

### 4.2. Terminal commands

No issues found.

### 4.3. Command Palette commands

Not applicable.

### 4.4. Options vs steps

No issues found.

### 4.5. Ordered lists

No issues found.

### 4.6. Mini-ToC

1. ~~**Lines 92–109.** The inline mini-ToC for step 1.5 is separated from its `###` heading by several paragraphs. Convention 1.1 in tasks.md: "Add an inline mini-ToC… right after the `###` heading." The `<!-- no toc -->` comment and bullet list should appear immediately after the heading line.~~

### 4.7. Table of contents

No issues found.

### 4.8. Links and cross-references

1. ~~**Line 13.** "The ETL pipeline from Task 1" — "Task 1" is not linked. Convention 4.8: "Provide a link to each file that exists in the repo." The file `lab/tasks/required/task-1.md` exists and should be linked.~~

### 4.9. Notes, tips, warnings

1. ~~**Lines 60–63.** Indented note inside a list item uses `> **Note:**` format. The correct fallback format for indented alerts is `> 🟦 **Note**` (with emoji, without colon) per convention 4.9.~~

### 4.10. Images

Not applicable.

### 4.11. Collapsible hints and solutions

No issues found.

### 4.12. Commit message format

No issues found.

### 4.13. Diagrams

Not applicable.

### 4.14. `<!-- TODO -->` comments

No issues found.

### 4.15. `<!-- no toc -->` comments

No issues found.

### 4.16. Code snippets in explanations

No issues found.

### 4.17. Heading levels in section titles

No issues found.

### 4.18. Inline formatting of technical terms

1. ~~**Line 99.** `SQLAlchemy/SQLModel` are not wrapped in backticks inside the TIP block. These are library/tool names and should be formatted as `` `SQLAlchemy` ``/`` `SQLModel` `` per convention 4.18.~~

### 4.19. Steps with sub-steps

No issues found.

### 4.20. Placeholders in docs

No issues found.

### 4.21. `docker compose up` commands

No issues found. Line 255 includes `--build`.

### 4.22. Environment variable references

No issues found.

### 4.23. Horizontal rules

No issues found.

### 4.24. Inline paths

No issues found.

### 4.25. Branch-on-remote references

Not applicable.

### 4.26. Example IP address

Not applicable (placeholder is used, not an example IP).

### Section 1. Task document template (tasks.md)

1. ~~**Lines 11–17.** Missing `<h4>Diagram</h4>` section. The task involves actions across multiple environments (local development, GitHub, VM deployment via Docker), so a Mermaid sequence diagram is required per convention 1.1: "Diagram is required whenever the task involves actions across multiple actors or environments."~~

2. ~~**Line 9.** Purpose contains two sentences. Template specifies `<One sentence: what the student will learn.>`~~

---

## TODOs

No TODOs found.

---

## Empty sections

1. **Line 36.** `## 1. Steps` — heading is immediately followed by `### 1.1.` with no content in between. (This is per template design — the section serves as a container for sub-sections.)

---

## Summary

| Category | Count |
|----------|-------|
| Conceptual — High | 0 |
| Conceptual — Medium | 5 |
| Conceptual — Low | 4 |
| Convention violations | 7 |
| TODOs | 0 |
| Empty sections | 1 (by design) |
| **Total** | **17** |

**Overall assessment:** The task is significantly improved from the prior review — all 18 previously flagged convention violations have been fixed, and the major structural issues (merged Git workflow/issue steps, missing wiki links, mis-numbered checkpoints) are resolved. The remaining issues are moderate: the deploy step (1.8) lacks a checkpoint and troubleshooting block for Docker on the VM, the `<h4>Diagram</h4>` section is missing despite multi-environment actions, the mini-ToC in step 1.5 is not placed immediately after the heading, and "Task 1" in the Context is not linked. The indented note fallback format needs the emoji prefix. These are all straightforward to fix.
