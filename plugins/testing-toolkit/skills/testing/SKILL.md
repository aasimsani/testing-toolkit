---
name: testing
description: "Routes any testing request to the right kind of test and the right order of work. Classifies the change (bug fix, new feature, refactor, legacy code, new endpoint, migration, prompt change, incident follow-up and more), picks a test shape per component, then calls the authoring, analysis and planning skills of this plugin in playbook order. Use when asked to add tests, test a change, improve a test suite, set up testing or CI stages on a repo, or when the kind of test is not decided yet. Not for running an existing suite once or for debugging one failing test."
---

# Testing

Testing techniques differ in what they leave in the repo, and that decides which skill does the work.

| Kind | What it leaves | Skills |
|---|---|---|
| **Authored tests** | Test code that is committed and maintained like product code | `test-unit`, `test-integration`, `test-contract`, `test-e2e`, `test-characterization`, `test-data` |
| **Harness plus campaign** | A small harness, generator or script, plus a long or repeated run that produces findings | `test-property`, `test-fuzz`, `test-load`, `test-llm-evals` |
| **Analysis or gate** | A report, a score or a pass/fail gate over existing code and tests | `test-mutation`, `test-quality-review`, `test-flaky-triage`, `test-audit` |
| **Runtime practice** | Config, runbooks and schedules that act on running systems | `test-strategy`, `chaos-experiment`, `release-safety` |

The kinds form a loop. An analysis finds a gap, and an authoring skill closes it. A surviving mutant, an uncovered changed line, a fuzz crash or an incident each becomes one new authored test.

## Workflow

### 1. Classify the scenario

Read `${CLAUDE_PLUGIN_ROOT}/references/scenario-playbooks.md` and find the row whose signal matches the request or the diff. Tell the user which scenario you picked in one sentence. When two rows fit, run the stricter one.

### 2. Pick the shape for each component

When the request covers more than one function or file, read `${CLAUDE_PLUGIN_ROOT}/references/strategy-models.md`. For each component, ask where the bug is most likely if the component breaks, and choose the layer from the answer. Turn on static analysis and types before you write a test.

Skip this step for a single function with an obvious layer.

### 3. Run the playbook

Call the skills in the order the playbook gives. Every authoring skill follows `${CLAUDE_PLUGIN_ROOT}/references/assured-generation.md`, so read that file before the first test.

### 4. Close the loop

Hand each gap that an analysis finds to the authoring skill for its layer. Stop when the playbook's "Done when" column holds, and say which parts of it you could not check.

### 5. Report

Give the report that `${CLAUDE_PLUGIN_ROOT}/references/assured-generation.md` describes: one row per test with the contract it protects, the bug that would make it fail, and the evidence. Add the scenario, the playbook steps you ran, and the steps you skipped with the reason.

## Rules

- Never delete or skip a failing test to make the build pass.
- Never change an expected value to match the code's output without a reason from the spec.
- Never report a step that did not run as a pass.
- Write E2E tests only for journeys whose failure would be an incident. Move every other check down a layer.
- Prefer one more row in an existing table of cases over a new test.

## When to use the formal-verification toolkit

Tests check the inputs and conditions that you can exercise. A model checks every case in a stated scope. Suggest the `formal-verification` skill of the fv-toolkit plugin when the scenario involves concurrency, distributed state, retries, permissions or rule tables. A counterexample from a model comes back here as a deterministic regression test in `test-unit` or `test-integration`.

## Reference files

| File | Read when |
|---|---|
| `${CLAUDE_PLUGIN_ROOT}/references/scenario-playbooks.md` | Step 1, always |
| `${CLAUDE_PLUGIN_ROOT}/references/strategy-models.md` | Step 2 |
| `${CLAUDE_PLUGIN_ROOT}/references/assured-generation.md` | Before any test is written |
| `${CLAUDE_PLUGIN_ROOT}/references/anti-patterns.md` | Before you show tests, and when you review tests |
| `${CLAUDE_PLUGIN_ROOT}/references/pipeline.md` | The user asks where a check runs, or the repo needs CI stages |
