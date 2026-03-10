# Review: `lab/tasks/required/task-3.md`

- **Date:** 2026-03-07
- **Convention files used:**
  - `contributing/conventions/writing/tasks.md` — task structure, design principles, conceptual review dimensions (D1–D12)
  - `contributing/conventions/writing/common.md` — writing conventions (4.1–4.26)

---

## Conceptual findings

### D1. Learning objective clarity

1. **[Low]** Line 9 (Purpose): The Purpose contains two objectives joined with "and": "Add charts to the front-end to visualize the analytics data from Task 2, **and** learn to integrate a chart library into a React application." A single, concrete learning outcome is preferred.
   - **Suggested fix:** Pick one outcome, e.g., "Learn to integrate a chart library into a React application to visualize analytics data."

### D2. Step-by-step completeness

1. **[Medium]** Lines 114–122 (step 1.5): The step says "Update `frontend/src/App.tsx` to include navigation" but provides only vague bullet-point suggestions, not concrete step-by-step instructions. A beginner may not know how to implement this without AI assistance.
   - **Suggested fix:** Provide a concrete code snippet or placeholder template showing the state variable, navigation buttons, and conditional rendering. Alternatively, give an exact AI prompt as done in step 1.4.

### D3. Student navigation

No issues found.

### D4. Checkpoints and feedback loops

1. **[Medium]** Step 1.3 (lines 44–68): No checkpoint after installing the chart library. Students have no way to verify the install succeeded.
   - **Suggested fix:** Add expected output after `npm install` (e.g., "You should see output similar to: `added N packages`") or a verification command like `npm ls chart.js`.

2. **[Medium]** Step 1.5 (lines 114–122): No checkpoint after adding navigation. Students don't verify that navigation works until step 1.7, two steps later. A silent mistake here propagates.
   - **Suggested fix:** Add a brief checkpoint such as "You will verify navigation works in step 1.7" or provide an intermediate checkpoint.

3. **[Low]** Step 1.6 (lines 137–143): No expected output shown for a successful `npm run typecheck`. Students unfamiliar with `TypeScript` may not know what "passing" looks like.
   - **Suggested fix:** After step 2, add: "If there are no type errors, the command produces no output and exits silently."

4. **[Medium]** Step 1.9, line 248 (item 6): "Verify the Dashboard page shows charts" is a checkpoint worded as a numbered step. Per convention 4.18, checkpoints should be indented under the action step they verify, not numbered as separate steps.
   - **Suggested fix:** Replace step 6 with a navigation action ("Navigate to the Dashboard page") and indent the verification text beneath it — matching the pattern used in step 1.7 (lines 189–191).

### D5. Acceptance criteria alignment

No issues found.

### D6. Difficulty and progression

No issues found.

### D7. Practical usability

1. **[Medium]** Lines 118–122 (step 1.5): The manual approach provides only vague bullet points ("Add a state variable", "Add buttons or links", "Render the Items table or the Dashboard component"). A beginner without AI assistance would struggle to implement this.
   - **Suggested fix:** Provide a concrete code snippet or placeholder template for `App.tsx` with the navigation logic, similar to the TIP in step 1.4.

### D8. LLM-independence

1. **[Medium]** Step 1.4 (lines 70–112): The step's numbered instructions (1–3) are structured entirely around AI agent use ("Open the coding agent", "Give it a prompt", "Review the generated code"). The manual fallback (TIP at lines 102–112) provides only a minimal `Chart.js` registration snippet — it does not cover fetching data from the API, building the `chartData` object, or handling loading/error states, all of which are required by the acceptance criteria. A student who does not use an AI has no complete path to finish the component.
   - **Suggested fix:** Either explicitly label step 1.4 as AI-required (per convention 4.16: "When a task explicitly requires AI use, mark it as a separate, clearly labeled part") or expand the TIP into a complete non-AI implementation path, or restructure the step to use Method 1 / Method 2 format.

### D9. Git workflow coherence

No issues found.

### D10. Conceptual gaps and misconceptions

No issues found.

### D11. Controlled AI steps

1. **[Low]** Line 82 (step 1.4, item 2): The prompt is introduced with "Give it a prompt **like**:", making it a suggestion rather than an exact prompt. Per convention 4.20 (Controlled task environment), the prompt should be exact or templated with `<placeholders>` so the AI interaction is reproducible.
   - **Suggested fix:** Change "Give it a prompt like:" to "Give it this prompt:" or "Use this prompt:".

2. **[Low]** Line 85: The AI prompt uses the `<lab-id>` placeholder, but it is not linked to a wiki section or defined inline per convention 4.20. Line 92 provides informal guidance ("Use a default such as `lab-04`…") but does not formally explain where students find valid lab IDs.
   - **Suggested fix:** Link `<lab-id>` to a wiki section that explains how to find valid lab IDs, or define it inline with the `(without < and >)` clarification.

### D12. Autochecker verifiability

No issues found.

---

## Convention findings

### Task document template (tasks.md Section 1)

No issues found.

### 4.1. Instructions wording

No issues found.

### 4.2. Terminal commands

No issues found.

### 4.3. Command Palette commands

Not applicable.

### 4.4. Options vs steps

No issues found.

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

No issues found.

### 4.12. Commit message format

No issues found.

### 4.13. Diagrams

Not applicable.

### 4.14. `<!-- TODO -->` comments

Not applicable.

### 4.15. `<!-- no toc -->` comments

Not applicable.

### 4.16. Code snippets in explanations

No issues found.

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

Not applicable (uses `<your-vm-ip-address>` placeholder, not a hardcoded example).

---

## TODOs

No TODOs found.

---

## Empty sections

No empty sections found.

---

## Summary

| Category                      | Count |
|-------------------------------|-------|
| Conceptual — High             | 0     |
| Conceptual — Medium           | 6     |
| Conceptual — Low              | 4     |
| Convention violations         | 0     |
| TODOs                         | 0     |
| Empty sections                | 0     |
| **Total**                     | **10**|

**Overall assessment:** The task follows the template structure correctly and covers a coherent learning objective. All convention violations have been addressed. Remaining issues are conceptual: missing checkpoints for steps 1.3, 1.5, and 1.6, a checkpoint disguised as a numbered step in step 1.9, step 1.5 (Add navigation) is underspecified for students who don't use AI, and the manual fallback in step 1.4's TIP is too minimal to satisfy LLM-independence. No TODOs or empty sections were found.
