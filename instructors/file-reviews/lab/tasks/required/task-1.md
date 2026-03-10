# Review: `lab/tasks/required/task-1.md`

- **Date:** 2026-03-07
- **Convention files used:**
  - `contributing/conventions/writing/tasks.md` — task structure, design principles, conceptual review dimensions (D1–D12)
  - `contributing/conventions/writing/common.md` — writing conventions (4.1–4.26)

---

## Conceptual findings

### D1. Learning objective clarity

No issues found.

### D2. Step-by-step completeness

1. **[Medium]** Line 206 — "Start the `Qwen code` coding agent in the terminal inside the project directory." No instructions on how to start the agent, no link to a wiki page or setup guide. A student unfamiliar with Qwen code would not know what command to run or how to install/configure it.

   **Suggested fix:** Add a link to a wiki page explaining how to start Qwen code (e.g., `[Start the `Qwen code` coding agent](../../../wiki/qwen-code.md#start-the-agent)`), or inline the startup command.

### D3. Student navigation

No issues found.

### D4. Checkpoints and feedback loops

No issues found.

### D5. Acceptance criteria alignment

No issues found.

### D6. Difficulty and progression

No issues found.

### D7. Practical usability

1. **[Medium]** Line 206 — "Start the `Qwen code` coding agent" assumes the student has the agent installed and knows how to start it. No installation prerequisites, no link to documentation. A student on a fresh setup would be blocked at this step.

   **Suggested fix:** Either link to a wiki page with setup instructions or add a prerequisite note referencing where Qwen code is installed/configured (e.g., in `setup.md`).

### D8. LLM-independence

1. **[High]** Lines 206–211 — Step 1.4.2 requires using the `Qwen code` AI agent to implement the pipeline but does not provide a non-AI alternative path. Convention 4.16 (LLM-independence) requires tasks to be completable without LLMs unless the task explicitly states that students must use an AI. The step is not labeled as AI-required, and no fallback path exists for students who don't use the agent.

   **Suggested fix:** Either (a) provide an explicit non-AI path (e.g., "Implement the five functions by following the TODO comments in `etl.py` — use the existing models in `backend/app/models/` as reference"), or (b) clearly label the step as AI-required per convention 4.16 ("When a task explicitly requires AI use, mark it as a separate, clearly labeled part").

### D9. Git workflow coherence

No issues found.

### D10. Conceptual gaps and misconceptions

1. **[Low]** Line 74 — "The API has HTTP Basic Auth" is stated without explanation or a link to learn more. Students unfamiliar with HTTP Basic Auth may not understand what this means or how the `-u` flag in `curl` relates to it.

   **Suggested fix:** Add a brief inline explanation or a `> [!NOTE]` block explaining that HTTP Basic Auth sends credentials as `username:password` and that `curl -u` provides these credentials.

### D11. Controlled AI steps

1. **[Medium]** Lines 206–221 — The AI prompt is provided (line 209) and there is a review checklist (lines 215–221), but the task does not require AI curation annotations (`KEPT`/`FIXED`/`DISCARDED`) per convention 4.24. Students are asked to "review" the generated code but have no structured way to demonstrate critical evaluation of the AI output.

   **Suggested fix:** If AI-generated code curation is a learning objective, add the three annotation labels requirement and require at least one `DISCARDED` item. If not, consider adding a concrete checkpoint for the review step (e.g., "Confirm the code matches all six checklist items before proceeding").

2. **[Low]** Lines 206–221 — The step lacks a concrete verification checkpoint after the AI generates code. The review checklist (lines 215–221) tells students what to look for but does not provide a pass/fail check to confirm the implementation is correct before proceeding to run it.

   **Suggested fix:** Add a checkpoint such as: "After reviewing, confirm the code passes a quick syntax check or imports without errors."

### D12. Autochecker verifiability

No issues found.

---

## Convention findings

### Section 1. Task document template

1. **Lines 42–63:** Step 1.2 combines issue creation (lines 44–48) and branch creation (lines 50–58) with an explanatory note (lines 60–63). The task template shows step 1.2 as only issue creation (`Title: [Task] <Task title>`). Branch creation is part of the Git workflow referenced in step 1.1.

### 4.1. Instructions wording

No issues found.

### 4.2. Terminal commands

No issues found.

### 4.3. Command Palette commands

Not applicable.

### 4.4. Options vs steps

Not applicable.

### 4.5. Ordered lists

No issues found.

### 4.6. Mini-ToC

No issues found.

### 4.7. Table of contents

No issues found.

### 4.8. Links and cross-references

No issues found.

### 4.9. Notes, tips, warnings

No issues found.

### 4.10. Images

Not applicable.

### 4.11. Collapsible hints and solutions

No issues found.

### 4.12. Commit message format

No issues found.

### 4.13. Diagrams

No issues found.

### 4.14. `<!-- TODO -->` comments

Not applicable.

### 4.15. `<!-- no toc -->` comments

No issues found.

### 4.16. Code snippets in explanations

Not applicable.

### 4.17. Heading levels in section titles

Not applicable.

### 4.18. Inline formatting of technical terms

No issues found.

### 4.19. Steps with sub-steps

No issues found.

### 4.20. Placeholders in docs

No issues found.

### 4.21. `docker compose up` commands

No issues found.

### 4.22. Environment variable references

No issues found.

### 4.23. Horizontal rules

No issues found.

### 4.24. Inline paths

No issues found.

### 4.25. Branch-on-remote references

Not applicable.

### 4.26. Example IP address

Not applicable.

---

## TODOs

No `<!-- TODO ... -->` comments found.

---

## Empty sections

No empty sections found.

---

## Summary

| Category                | Count |
| ----------------------- | ----- |
| Conceptual — High       | 1     |
| Conceptual — Medium     | 3     |
| Conceptual — Low        | 2     |
| Convention violations   | 1     |
| TODOs                   | 0     |
| Empty sections          | 0     |
| **Total**               | **7** |

**Overall assessment:** The task is well-structured with clear steps, good checkpoints, proper troubleshooting blocks, and well-aligned acceptance criteria. The remaining high-severity issue is the LLM-independence violation (step 1.4.2 requires an AI agent without providing a non-AI alternative or labeling the step as AI-required). Medium issues: missing Qwen code startup instructions (D2, D7) and missing AI curation annotations (D11). Low issues: unexplained HTTP Basic Auth (D10) and missing post-generation verification checkpoint (D11). Convention violation: the combined issue+branch step (Section 1 #1).
