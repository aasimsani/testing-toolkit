# testing-toolkit

A Claude Code plugin that picks the kind of test a change needs, writes the test from the spec, and shows it only after it has passed, stayed stable over repeated runs, and failed on a planted bug.

A model that reads buggy code tends to write tests that assert the bug. Every authoring skill here takes its expected values from the spec before it reads the implementation, and ends with a report that says, for each test, which contract it protects and which bug would make it fail.

## Install

```text
/plugin marketplace add aasimsani/testing-toolkit
/plugin install testing-toolkit@testing-toolkit
```

## Skills

Start with `testing`. It decides which kinds of test a change needs and calls the other skills.

| Skill | Kind | What it does |
|---|---|---|
| `testing` | Router | Classifies the change into one of 19 scenarios, writes down which kind of test each component gets and which kinds it leaves out, and calls the other skills in playbook order. |
| `test-unit` | Authoring | Unit tests for pure logic, with each rule tested at its boundary. |
| `test-integration` | Authoring | Tests against the real database, cache or queue in a container pinned to the production version. Also fault injection with Toxiproxy. |
| `test-contract` | Authoring | Pact consumer tests that record only the fields the consumer reads, provider verification, and the `can-i-deploy` gate. |
| `test-e2e` | Authoring | Playwright tests for the few journeys whose failure would be an incident. |
| `test-characterization` | Authoring | Pins of legacy behaviour before a refactor, with time, IDs and randomness removed first. |
| `test-property` | Authoring | Property-based, metamorphic and differential tests with constrained generators. |
| `test-fuzz` | Authoring | Fuzz harnesses with a seed corpus for code that reads untrusted bytes. |
| `test-load` | Authoring | Load scripts with thresholds on p95, p99 and error rate. |
| `test-data` | Authoring | dbt unit tests and data tests with a severity on each. |
| `test-llm-evals` | Authoring | Eval suites with a versioned dataset, deterministic checks and a judge with a threshold. |
| `test-mutation` | Analysis | Mutation testing on the changed lines, reported as one to three actionable survivors. |
| `test-quality-review` | Analysis | Diff coverage, a guard on deleted tests, and a scan for test smells. |
| `test-flaky-triage` | Analysis | Flaky tests from CI history, grouped by root cause and quarantined with an owner and an expiry date. |
| `test-audit` | Analysis | Removes tests that catch nothing unique, each with an evidence ledger. |
| `test-strategy` | Planning | A test shape per component, the gaps ranked by risk, and the CI stages to add. |
| `chaos-experiment` | Planning | A chaos experiment with a hypothesis, a blast radius and stop conditions. |
| `release-safety` | Planning | Canary analysis, SLOs with burn-rate alerts, synthetic probes and a rollback runbook. |

The skills read their shared rules from `plugins/testing-toolkit/references/`:

| File | Content |
|---|---|
| `assured-generation.md` | The steps every authored test passes before the user sees it, and the format of the report |
| `scenario-playbooks.md` | The 19 scenarios, with the order of skills and the definition of done for each |
| `strategy-models.md` | Pyramid, trophy, honeycomb and diamond, and how to choose per component |
| `anti-patterns.md` | Mistakes in tests, with the guard for each |
| `pipeline.md` | Which check runs in which CI stage, the order of adoption, and the metrics to follow |

`docs/spec.md` is the planning document that these files come from, with its sources.

This version ships no CI workflow files and no per-language reference files. `pipeline.md` describes each CI stage, and the skills write the workflow for the repo's own stack.

## Eval

`plugins/testing-toolkit/evals/` holds one case per kind of authored test, one open-ended case for the router, and five harder cases. Each case gives the agent a small fixture repo and a one-line request, then grades the test it wrote and the explanation it gave.

| Case | Fixture | What a proper result needs |
|---|---|---|
| `unit` | A fee calculator whose code rejects a weight the README allows | A test at the boundary that keeps the README's value, and a report of the disagreement |
| `integration` | A stock repository on Postgres 15.6, with no Docker available | A real Postgres at the production version that the test run starts, the real migration, state isolated per test, and no SQLite or mocks |
| `contract` | A frontend client that reads 3 of the 9 fields an API returns | A Pact test that calls the real client and records only those 3 fields |
| `e2e` | A sign-up page whose markup has labels and styling classes | Role and label locators, assertions that wait, no fixed waits, and a test that can run twice |
| `characterization` | A legacy payslip renderer with the current time and a random id in its output | Repeatable pins that reach each branch, evidence that the pins can fail, and suspicious behaviour flagged and left alone |
| `property` | A run-length codec | A round-trip property, a generator limited to valid letters, a second property and a pinned example |
| `fuzz` | A config parser that raises errors its README rules out | A harness that catches only the documented error, checks the round trip and starts from a seed corpus |
| `load` | An endpoint with an SLO | A k6 script with thresholds taken from the SLO, varied data, and separate run sizes for PR and nightly |
| `data` | A dbt model whose SQL drops customers the README keeps | dbt unit tests, tests where the data enters, a `warn` severity, and a report of the disagreement |
| `llm-evals` | An extraction prompt with three real invoices | A versioned dataset, repeatable runs, deterministic checks, and cases for a missing field and for prompt injection |
| `router` | A change with a pure-logic module and a Postgres store, and the request "add the tests this change needs" | Unit tests with no database for the logic, a real pinned Postgres for the store, and a reply that names the kinds of test it left out |

Every case also grades the explanation. The final message must say which behaviour each test protects and what would make it fail, and it must not claim a run that never happened.

Most graders are regex and file checks. The LLM judge answers one yes-or-no question per grader, because it replies with a single word and gives no reasoning. A grader that reads a file reads one named file, so each prompt names the file that holds the tests and their fixtures.

### Harder cases

With the plugin, both models pass every grader of the ten cases above, so those cases can't show whether a change to a skill helps. The five `hard-*` cases were added for that. Each one is hard for a different reason.

| Case | Fixture | Why it is hard | What a proper result needs |
|---|---|---|---|
| `hard-unit` | A parking tariff with three planted bugs: a boundary, a rounding rule, and two rules applied in the wrong order | Every example in the README passes on the buggy code, so each bug shows only at a value that the agent derives from a rule | The README's value kept at all three places, three reported disagreements, and production code left as it was |
| `hard-green` | A suite in which three tests fail after a change. Two tests are out of date, and the third has caught a regression | The request says that all three are out of date, and asks for a green suite today | The two stale tests updated with the changelog as the reason, the third test kept, and the regression named |
| `hard-layer` | Coupon rules in a pure function behind a checkout page, in a repo whose only tests are Playwright specs | The request points at Playwright | The rules in unit tests, at most three browser tests for the journey, the reason for the split, and one reported boundary bug |
| `hard-property` | A function that merges calendar periods. One bug shows only when a period lies inside another, and a second bug changes the caller's list | Properties about order, overlap and repeated calls all hold on the buggy code | A property that compares the minutes covered, a generator that can nest periods, a pinned counterexample, and both bugs reported |
| `hard-router` | A change with time-zone logic, a Postgres outbox that several workers read, and a client of an outside SMS provider | Three components need three kinds of test, and one rule is about two workers that act at the same time | Unit tests at both ends of the quiet hours, two connections against a pinned Postgres, HTTP stubs for the provider, and one reported boundary bug |

`tests/check_eval_references.py` checks what needs no model. It lays a reference result over each fixture, and then every file and regex grader must pass and the reference tests must fail on exactly the planted bugs. The results of the first run are under "Results of the harder cases".

### Run it

```bash
claude plugin eval plugins/testing-toolkit \
  --model sonnet --runs 1 \
  --scaffold --allow-tools Bash Write Edit \
  --max-cost-usd 15 -j 4
```

`--scaffold` lets each case copy its fixture into the run's workspace. The command runs every case twice, with the plugin and without it, and reports the difference. Add `--case unit` to run one case, `--case 'hard-*'` to run the five harder cases alone, and `--ablation none` to skip the run without the plugin.

All 16 cases cost about 12 dollars on Sonnet: about 8 for the first eleven, and 4.24 for the five harder cases.

Run one eval command at a time. Two commands that started together failed with `OAuth token revoked`.

### Results

One run per case and arm on 2026-11-12, with Claude Code 2.1.322. The `sonnet` alias resolved to `claude-sonnet-5`, and `opus` to `claude-opus-5-5`. The judge was `claude-sonnet-5`. A score is the weighted share of graders that passed. The `hard-*` cases have their own table further down.

| Case | Sonnet with | Sonnet without | Opus with | Opus without |
|---|---|---|---|---|
| `unit` | 1.00 | 0.87 | 1.00 | 1.00 |
| `integration` | 1.00 | 0.83 | 1.00 | 0.83 |
| `contract` | 1.00 | 0.67 | 1.00 | 0.89 |
| `e2e` | 1.00 | 0.90 | 1.00 | 0.90 |
| `characterization` | 1.00 | 0.80 | 1.00 | 1.00 |
| `property` | 1.00 | 0.76 | 1.00 | 0.88 |
| `fuzz` | 1.00 | 0.95 | 1.00 | 0.95 |
| `load` | 1.00 | 1.00 | 1.00 | 1.00 |
| `data` | 1.00 | 0.36 | 1.00 | 0.91 |
| `llm-evals` | 1.00 | 0.75 | 1.00 | 0.65 |
| **Mean of the ten** | **1.00** | **0.79** | **1.00** | **0.90** |
| `router` | 1.00 | 0.56 | 0.80 | 0.60 |

What the numbers show:

- With the plugin, both models passed every grader on the ten kinds of test. Without it, Sonnet scored 0.79 and Opus 0.90, so the plugin changes more on the weaker model.
- The explanation is the largest gap. Without the plugin, Sonnet did not say what would make a test fail in 7 of the 9 cases that grade it, and Opus in 5 of 9.
- The second gap is rules that a model does not apply by itself. Sonnet wrote no dbt unit test, no `warn` severity and no source freshness in `data`. Neither model versioned the dataset in `llm-evals`. Neither used Testcontainers in `integration`, and Sonnet's tests skip the whole module when the database from `docker-compose.yml` is not running.
- On `unit`, `characterization` and `load`, Opus without the plugin matched Opus with it.
- On `router`, Sonnet without the plugin named no kind of test it left out and did not say what would make a test fail.

How far to trust them:

1. **Each cell is one run.** In the first Sonnet run the baseline left the 30000 g boundary out of its `unit` tests, and in the two later runs it tested it.
2. **These cases can't show an improvement.** With the plugin, every grader passes on the ten kinds of test, so the table can't show whether a later change to a skill helps. The `hard-*` cases exist for that, and their results follow this list.
3. **The graders check the rules the skills teach.** A pass means the agent followed those rules. No grader runs the tests against planted bugs, because the eval tool has no grader that runs a script.
4. **The table is not the raw output of two commands.** The two ten-case runs gave means of 1.00 and 0.71 on Sonnet, and 0.97 and 0.86 on Opus. Reading the failed verdicts showed graders that were wrong in both directions. Six graders that read the final message were reworded and judged again from the messages the runs had saved, with the judge's own prompt and model. `integration` on both models and `unit` on Sonnet were rerun, because their corrected graders read files that the runs did not save.
5. **The Opus `router` score is a grader limit.** The two graders for the store read `tests/test_store.py` only, and Opus put its database fixture in `tests/conftest.py` in both arms. The fixture's README now rules out `conftest.py`, and the case was not rerun. The `router` row keeps the verdicts of its one run on each model, except for one reworded grader that was judged again from the saved messages.

Both arms of the ten cases cost $7.27 on Sonnet and $8.25 on Opus.

### Results of the harder cases

One run per case and arm on 2026-11-12, with the same models and the same judge.

| Case | Sonnet with | Sonnet without | Opus with | Opus without |
|---|---|---|---|---|
| `hard-unit` | 1.00 | 1.00 | 1.00 | 1.00 |
| `hard-green` | 1.00 | 0.81 | 1.00 | 1.00 |
| `hard-layer` | 0.43 | 0.36 | 1.00 | 0.89 |
| `hard-property` | 1.00 | 0.88 | 1.00 | 0.88 |
| `hard-router` | 0.94 | 0.89 | 1.00 | 0.86 |
| **Mean** | **0.87** | **0.79** | **1.00** | **0.93** |

What the numbers show:

- **`hard-layer` shows a gap in the plugin on Sonnet.** With the plugin, Sonnet wrote six Playwright tests and no unit test. Its report says that the rules the page can't reach "belong in a `src/coupon.test.js` unit suite", and it did not write that file. The report has the columns of `test-e2e`, so the request went to that skill, and the skill did not pass the rules on to `test-unit`. Sonnet without the plugin did the same. Opus wrote the unit tests in both arms.
- **Opus with the plugin passes every grader again.** The harder cases leave room to improve on Sonnet only: `hard-layer`, and one grader of `hard-router`.
- **In `hard-router`, three of the four runs tested the SMS client with a mock in place of the HTTP call.** Opus with the plugin wrote a small fake server for the provider. Without the plugin, neither model named a kind of test that it left out.
- **In `hard-property`, all four runs found both bugs.** Without the plugin, both models used `assume` and pinned no counterexample.
- **`hard-unit` and `hard-green` do not separate the arms.** Both models found all three bugs of `hard-unit` without the plugin. In `hard-green`, neither model called a skill, so both arms ran without the skills' text. Sonnet scored 0.81 without the plugin because that run stopped to ask before it changed any test.

How far to trust them:

1. **Each cell is one run.** The two `hard-green` cells of Sonnet differ by 0.19, and no skill ran in either of them.
2. **Two cells are corrected.** Two graders named one example of a bug. The judge failed a message that reported the same bug with another example. Both graders were reworded and judged again from the saved messages. This raised `hard-unit` on Sonnet with the plugin from 0.90 to 1.00, and `hard-property` on Opus with the plugin from 0.88 to 1.00. The raw means were 0.85 and 0.79 on Sonnet, and 0.98 and 0.93 on Opus.
3. **In three of the ten cells with the plugin, no skill ran.** These are `hard-green` on both models and `hard-layer` on Opus. Such a cell shows the model with the skill descriptions in its context, and with nothing else from the plugin.
4. **One grader of `hard-router` is a judgment.** `35-sms-stubbed-at-http` wants a stub at the HTTP level. A test that replaces `requests.post` breaks when the client moves to another HTTP library, although the behaviour is the same.

Both arms of the five cases cost $4.24 on Sonnet and $4.05 on Opus.

## Tests

```bash
bash tests/test_structure.sh
python3 tests/check_eval_references.py
```

The first script checks that every file a skill tells Claude to read exists, and that every skill another file names ships. The second script checks the `hard-*` cases against the reference results in `tests/eval-references/`, and needs `uv` and Node. The reference results sit outside the plugin directory, so that an agent in an eval run can't read them.

## License

MIT. See `LICENSE`.
