---
name: testing
description: "Decides which kinds of test a change needs, and gets them written. Classifies the change (bug fix, new feature, refactor, legacy code, new endpoint, migration, prompt change, incident follow-up and more), picks a test shape per component, then calls the authoring, analysis and planning skills of this plugin in playbook order. Use when asked to add tests, add the tests a change needs, test a change, improve a test suite, set up testing or CI stages on a repo, or when the kind of test is not decided yet. Not for running an existing suite once or for debugging one failing test."
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

### 2. Name the phase

A test written while the code is being built and a test written to check finished code have different aims, so they are different kinds of test. Name the phase before you choose a kind, and tell the user which one you picked.

| Phase | Signal | Aim of each test | Kinds of test |
|---|---|---|---|
| **Building, test-first** | "TDD", "write the test first", "the next failing test", a function that does not exist yet | State the next behaviour before the code exists. The test fails first because the code is missing, and it decides the interface of that code | One example-based test per behaviour: `test-unit`, or `test-integration` when the behaviour is at a database or a queue. At most one acceptance test at the outer boundary of the feature |
| **Testing code that exists** | "Add tests for", "is this covered", a finished diff, a release, an audit | Find the bugs that the author did not think of | Every kind in the table at the top: the boundary of each rule, rules in combination, properties, fuzzing, real dependencies, contracts, journeys, load, and mutation of the diff |

In the building phase, write one failing test, run it, show that it fails for the reason you expect, and hand back for the code. Never write a suite ahead of the code. Leave mutation runs, property campaigns, fuzzing, load tests and broad E2E for the testing phase, because they slow the red, green, refactor cycle and they check code that is still changing. The failing run counts as the evidence for step 4 of assured generation, in place of a planted bug.

The tests that the building phase leaves behind cover the cases the author had in mind, so they do not replace the testing phase. When the feature is green, run the playbook of step 1 on it as code that exists.

When the request does not show the phase, treat code that exists as the testing phase, and code that is missing as the building phase.

### 3. Choose the kinds of test

For each component the change touches, ask where the bug is most likely if the component breaks, and choose the kind of test from the answer. When the request covers more than one function or file, read `${CLAUDE_PLUGIN_ROOT}/references/strategy-models.md` first. Turn on static analysis and types before you write a test.

Write the choice down before you write a test, and keep it in the final report:

| Component | Where the bug would be | Kind of test | Skill |
|---|---|---|---|
| `tax/rates.py` | Its own logic: the boundary of each rate band | Unit | `test-unit` |
| `ledger/repo.py` | The database: constraints, conflicts and transactions | Integration | `test-integration` |

Then name the kinds of test you considered and left out, with one reason each, such as "no E2E test, because this change adds no user journey". Write no test of a kind that has no credible bug behind it.

For a single function with an obvious kind, one line replaces the table.

### 4. Run the playbook

Call the skills in the order the playbook gives. Every authoring skill follows `${CLAUDE_PLUGIN_ROOT}/references/assured-generation.md`, so read that file before the first test.

### 5. Close the loop

Hand each gap that an analysis finds to the authoring skill for its layer. Stop when the playbook's "Done when" column holds, and say which parts of it you could not check.

### 6. Report

Give the report that `${CLAUDE_PLUGIN_ROOT}/references/assured-generation.md` describes: one row per test with the contract it protects, the bug that would make it fail, and the evidence. Put the scenario, the phase, the table of choices from step 3 and the kinds of test you left out above it. Add the playbook steps you ran, and the steps you skipped with the reason.

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
| `${CLAUDE_PLUGIN_ROOT}/references/strategy-models.md` | Step 3 |
| `${CLAUDE_PLUGIN_ROOT}/references/assured-generation.md` | Before any test is written |
| `${CLAUDE_PLUGIN_ROOT}/references/anti-patterns.md` | Before you show tests, and when you review tests |
| `${CLAUDE_PLUGIN_ROOT}/references/pipeline.md` | The user asks where a check runs, or the repo needs CI stages |
