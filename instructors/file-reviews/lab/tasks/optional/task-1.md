# Review: `lab/tasks/optional/task-1.md`

**Date:** 2026-03-07

**Convention files used:**

- `contributing/conventions/writing/tasks.md` — Section 1 (task document template), Section 4 (task design principles), Section 5 (conceptual review dimensions D1–D12)
- `contributing/conventions/writing/common.md` — writing conventions (4.1–4.26)

---

## Conceptual findings

### D1. Learning objective clarity

1. **[Medium]** Line 9 — The Purpose reads "Set up `Grafana` as an alternative dashboard tool, connect it to `PostgreSQL`, and build visualizations using SQL queries." This describes *actions* the student will perform, not a *learning outcome*. A stronger Purpose would state what the student learns (e.g., "Learn how a dedicated dashboarding tool differs from a hand-built front-end dashboard by connecting `Grafana` to `PostgreSQL` and building visualizations.").

### D2. Step-by-step completeness

1. **[Low]** Line 42 — References `GF_SECURITY_ADMIN_USER` and `GF_SECURITY_ADMIN_PASSWORD` in `.env.docker.secret` without links. Students unfamiliar with the file may not know where to find it or what it contains. The file name should be linked per convention 4.22.

### D3. Student navigation

No issues found.

### D4. Checkpoints and feedback loops

1. **[Medium]** Lines 46–63 (Step 1.3) — After running `docker compose up`, there is no expected output or checkpoint showing the student that `Grafana` started successfully. A student whose container failed to start would proceed to the browser step and see nothing, with no guidance on what went wrong.
2. **[Medium]** Lines 44–63 (Step 1.3) — This step involves `Docker` infrastructure (starting containers, port binding) but has no collapsible troubleshooting block. Common failures include port 3000 already in use or containers exiting immediately.

### D5. Acceptance criteria alignment

1. **[Medium]** Line 147 — "The issue contains a reflection comment comparing the two dashboard approaches" is subjective. A reviewer (or autochecker) cannot objectively determine whether a comment adequately "compares" the approaches. Consider requiring specific structure (e.g., "The reflection comment addresses all three questions from step 1.6").

### D6. Difficulty and progression

No issues found.

### D7. Practical usability

1. **[Low]** Lines 59–62 — The login step says to use `admin`/`admin`, but step 1.2 (line 42) offers the option to change credentials. A student who changed the credentials in step 1.2 may be confused by step 1.3 telling them to use `admin`/`admin`. Add a note: "If you changed the credentials in step 1.2, use those instead."

### D8. LLM-independence

No issues found.

### D9. Git workflow coherence

1. **[Medium]** Lines 136–138 — Step 1.7 is titled "Finish the task" but contains only "Close the issue." Per convention, "Finish the task" is the heading for the PR + review ending. This task modifies `docker-compose.yml` (a code change) but does not follow the `Git workflow` (no branch, no PR). Either: (a) add a `Git workflow` step and change the ending to create a PR, or (b) rename the step to match the no-code ending pattern (e.g., close the issue with evidence).

### D10. Conceptual gaps and misconceptions

No issues found.

### D11. Controlled AI steps

Not applicable — no AI-assisted steps in this task.

### D12. Autochecker verifiability

1. **[High]** Line 146 — "The dashboard has at least 2 panels with data from `PostgreSQL`." It is unclear how the autochecker can verify `Grafana` dashboard content. `Grafana` dashboards live in its internal storage; verifying panel count and data source requires `Grafana` API access, which is not part of the standard autochecker channels (repository checks + VM `SSH`). Suggested fix: either provision the dashboard via a `JSON` file at a known path (checkable via `SSH`) or replace with a criterion the autochecker can verify (e.g., screenshot posted in the issue, or a `Grafana` API endpoint accessible on the VM).
2. **[High]** Line 147 — "The issue contains a reflection comment comparing the two dashboard approaches" is open-ended free text. The autochecker cannot verify whether the content of a comment adequately "compares" anything. Suggested fix: require a structured format (e.g., three separate answers to the three questions) or replace with a verifiable proxy (e.g., "The issue contains a comment with at least 3 lines").

---

## Convention findings

### Section 1. Task document template

1. **Line 15** — Missing `<h4>Diagram</h4>` section. The task involves actions across multiple environments (editor for `docker-compose.yml`, terminal for `Docker` commands, browser for `Grafana` UI, `Grafana` connecting to `PostgreSQL`). A Mermaid sequence diagram showing this flow should be added between Context and Table of contents, or an explicit decision to omit it should be justified (single-environment task).
2. **Lines 136–138** — Step 1.7 "Finish the task" uses the wrong ending pattern. "Finish the task" is reserved for the PR + review flow (create PR, get review). The current content ("Close the issue.") matches the no-code ending but uses the wrong heading name.

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

Not applicable.

### 4.7. Table of contents

No issues found.

### 4.8. Links and cross-references

No issues found.

### 4.9. Notes, tips, warnings

No issues found.

### 4.10. Images

Not applicable.

### 4.11. Collapsible hints and solutions

Not applicable.

### 4.12. Commit message format

Not applicable.

### 4.13. Diagrams

Not applicable (covered in Section 1 finding #1).

### 4.14. `<!-- TODO -->` comments

Not applicable.

### 4.15. `<!-- no toc -->` comments

Not applicable.

### 4.16. Code snippets in explanations

Not applicable.

### 4.17. Heading levels in section titles

Not applicable.

### 4.18. Inline formatting of technical terms

No issues found.

### 4.19. Steps with sub-steps

Not applicable.

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

Not applicable (placeholder used).

---

## TODOs

No TODOs found.

---

## Empty sections

No empty sections found.

---

## Summary

| Category | Count |
|---|---|
| Conceptual — High | 2 |
| Conceptual — Medium | 5 |
| Conceptual — Low | 2 |
| Convention violations | 2 |
| TODOs | 0 |
| Empty sections | 0 |
| **Total** | **11** |

**Overall assessment:** The task provides a clear, well-structured walkthrough for setting up `Grafana`, with good use of SQL examples and a useful reflection step. The most critical issues are (1) two acceptance criteria that the autochecker cannot verify (dashboard content and reflection quality), and (2) the "Finish the task" heading used with a close-issue ending instead of the PR+review flow. Remaining convention violations: the missing `<h4>Diagram</h4>` section (Section 1 #1) and the wrong ending pattern for step 1.7 (Section 1 #2/3).
