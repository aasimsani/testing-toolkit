# Testing Toolkit: Planning a Test-Building Skill Set

Nov 12, 2026 · @Aasim

## How to use this doc

Your instinct is right: testing techniques split by **what they leave behind**. That split decides how each one is packaged, as a skill that writes code, a skill that runs an analysis and reports, or a CI/ops template. This doc is the planning spec for a testing skill set in Claude Code. It sits beside the formal verification toolkit doc.

**The four kinds of artifact:**

| Kind | What it leaves behind | Examples | Packaged as |
| --- | --- | --- | --- |
| **Authored tests** | Test code committed to the repo and maintained like product code | Unit, integration, contract, E2E, snapshot/approval, data tests | Authoring skills (Claude writes the tests) |
| **Harness + campaign** | A small piece of code (harness, generator, script) plus a long or repeated run that produces findings | Property-based tests, fuzzing, load tests, chaos experiments, LLM eval suites | Authoring skill for the harness, plus a CI job for the campaign |
| **Analysis / gate** | No new test code; a report, score, or pass/fail gate over existing code and tests | Mutation testing, diff coverage, flaky detection, test-impact selection, SAST, dependency and secret scans, perf-regression comparison | Analysis skills (run, triage, explain) plus CI templates |
| **Runtime practice** | Config, runbooks, dashboards, and schedules that act on running systems | Canary analysis, SLO burn gates, synthetic monitoring, shadow traffic, DR drills, game days | Ops templates plus a planning skill; mostly not code in the app repo |

**The loop that ties them together:** analyses find gaps, and authoring skills close them. A surviving mutant, an uncovered changed line, a fuzz crash, or an incident becomes a new authored test. Meta's TestGen-LLM is the industrial proof that this loop works when every generated test must pass filters before a human sees it. It submits for review only tests it can guarantee improve the existing code base ([Meta, FSE '24](https://arxiv.org/pdf/2402.09171)). Every authoring skill in this doc should use the same filters.

**How to read the rest:** the taxonomy classifies every technique. Strategy models say how much of each to write. The architecture section says how the skills are packaged. The authoring, analysis, and scenario sections are the content of the skills. The CI section says where each runs.

## Taxonomy: every technique classified

About 40 techniques sort into the four kinds. Most code-producing techniques run on every PR. Most results-producing techniques run on a diff (PR) or a schedule (nightly). Runtime practices sit after deploy. **Kind** uses the four labels from above: A = authored tests, H = harness + campaign, G = analysis/gate, R = runtime practice.

### Correctness of code

| Technique | Kind | What gets committed | Runs at | Package as |
| --- | --- | --- | --- | --- |
| Unit tests | A | Test files | Pre-commit, PR | Authoring skill |
| Component / service tests (one service, real DB, faked neighbours) | A | Test files + container fixtures | PR | Authoring skill |
| Integration tests (real dependencies via Testcontainers) | A | Test files + fixtures | PR | Authoring skill |
| Characterization / approval / golden-master tests | A | Test files + approved snapshot files | PR | Authoring skill (legacy + refactor scenarios) |
| Snapshot tests (UI, API responses) | A | Test files + snapshots | PR | Authoring skill |
| Property-based tests | H | Properties + generators | PR (short), nightly (long) | Authoring skill + CI profile |
| Metamorphic tests | H | Relations + generators | PR | Authoring skill (often inside property-based) |
| Differential tests (old vs. new, ours vs. reference) | H | Harness + oracle | PR, nightly | Authoring skill |
| Fuzz testing | H | Fuzz harness + seed corpus | PR (\~10 min), nightly batch | Authoring skill (harness) + CI template (campaign) |
| Regression test for a bug | A | One focused test that failed before the fix | PR | Authoring skill (bug-fix scenario) |

### Correctness across boundaries

| Technique | Kind | What gets committed | Runs at | Package as |
| --- | --- | --- | --- | --- |
| Consumer-driven contract tests (Pact) | A + G | Consumer tests, provider verification; contracts live in a broker | PR + pre-deploy gate (`can-i-deploy`) | Authoring skill + CI template |
| Schema compatibility checks (OpenAPI, protobuf, Avro, DB migrations) | G | Config only | PR | CI template |
| API fuzzing from the schema (Schemathesis) | H | Config + auth hooks | PR, nightly | Authoring (light) + CI template |
| End-to-end tests (Playwright) | A | Specs, page objects, fixtures | PR (critical paths), main, pre-deploy | Authoring skill |
| Visual regression | A + G | Specs + baseline images | PR | Authoring + CI template |
| Accessibility checks | A + G | Assertions inside E2E or a scanner config | PR | Folded into E2E skill |
| Data quality tests (dbt tests, Great Expectations, Soda) | A | Test definitions (YAML/SQL) | Pipeline run, PR | Authoring skill |
| Data diffs (table before/after a change) | G | Nothing | PR on pipeline code | Analysis skill |

### Quality of the tests themselves

| Technique | Kind | What gets committed | Runs at | Package as |
| --- | --- | --- | --- | --- |
| Mutation testing | G | Config + ignore list | PR (diff only), nightly or weekly (full) | Analysis skill + CI template |
| Diff coverage | G | Threshold config | PR | CI template |
| Flaky-test detection + quarantine | G | Quarantine list / tags | Continuous over CI history | Analysis skill + CI template |
| Test-impact analysis / predictive selection | G | Config | PR | CI template |
| Test-smell review (tautological, over-mocked, no assertions) | G | Nothing | PR | Analysis skill |
| Test auditing / pruning (authoring gate, audit, campaign) | G | Deletions and consolidations, each backed by an evidence ledger | PR (gate on new tests), quarterly campaign | Analysis skill (test-audit) |

### Performance and resilience

| Technique | Kind | What gets committed | Runs at | Package as |
| --- | --- | --- | --- | --- |
| Micro-benchmarks + regression compare | H | Benchmark code + baseline | PR, main | Authoring + CI template |
| Load tests: smoke, average, stress, spike, soak (k6, Locust, Gatling) | H | Scripts + thresholds | Smoke on PR; others nightly or pre-release | Authoring skill + CI template |
| Fault injection in tests (Toxiproxy) | A | Tests with injected faults | PR, nightly | Authoring skill |
| Chaos experiments (Chaos Mesh, Litmus, AWS FIS) | H + R | Experiment definitions + hypothesis + abort criteria | Staging schedule, game days, production | Planning skill + ops template |
| Disaster-recovery drills | R | Runbooks + drill scripts | Quarterly | Planning skill + ops template |

### Release and production

| Technique | Kind | What gets committed | Runs at | Package as |
| --- | --- | --- | --- | --- |
| Canary analysis with auto-rollback | R | Rollout + analysis templates | Every deploy | Ops template |
| Feature-flag progressive rollout | R | Flag config | Every risky release | Ops template |
| Shadow / dark traffic | R | Mirroring + diff config | Major rewrites | Planning skill |
| Synthetic monitoring | R + A | Probe scripts (often reused E2E specs) | Every minute in production | Authoring (reuse E2E) + ops template |
| SLOs, error budgets, burn-rate alerts | R | SLO definitions | Continuous; used as a deploy gate | Planning skill + ops template |
| Production invariant monitors | R | Assertions on telemetry | Continuous | Links to formal-verification toolkit |

### Security and supply chain

| Technique | Kind | What gets committed | Runs at | Package as |
| --- | --- | --- | --- | --- |
| SAST with custom rules (Semgrep, CodeQL) | G | Rules | PR | CI template; skill only for writing custom rules |
| Dependency, licence, SBOM scanning | G | Config | PR, nightly | CI template |
| Secret scanning | G | Config | Pre-commit, PR | CI template |
| DAST (ZAP) | G | Config | Nightly on staging | CI template |
| IaC policy checks (Checkov, Conftest) | G | Policies | PR | CI template |

### AI features

| Technique | Kind | What gets committed | Runs at | Package as |
| --- | --- | --- | --- | --- |
| LLM eval suites (golden sets, rubric or LLM-as-judge scoring) | H | Datasets + scorers + thresholds | PR (small set), nightly (full) | Authoring skill + CI template |
| Red-team / prompt-injection sets | H | Attack datasets | Nightly, pre-release | Authoring skill |

## Test strategy models

No single shape fits every codebase. The skill should pick a shape **per component**, based on where that component's logic and bugs actually live. Each shape optimises for something different. The pyramid gives fast, isolated feedback on pure logic. The trophy gives integration-level confidence where the integration *is* the logic. The honeycomb targets microservices, where most bugs live at the seams ([howitworks.dev](https://howitworks-dev.pages.dev/testing-strategies/)).

| Model | Shape | Fits | Fails when | Source |
| --- | --- | --- | --- | --- |
| **Test pyramid** (Cohn, Fowler) | Many unit tests, fewer integration, very few E2E | Logic-heavy code: calculators, rules engines, parsers, domain models | Logic is mostly wiring; heavily mocked unit tests then catch nothing | [web.dev](https://web.dev/articles/ta-strategies) |
| **Testing trophy** (Kent C. Dodds) | Static checks at the base; integration tests are the widest band | Frontend and full-stack apps; "test what the user sees" | Logic is rich; reproducing every rule case through integration tests is slow and still misses edges | [howitworks.dev](https://howitworks-dev.pages.dev/testing-strategies/) |
| **Testing honeycomb** (Spotify) | Few implementation-detail tests, thick integrated-service middle, few integrated tests | Microservices; each service tested through its real API and real DB | A service holds complex internal logic; add a pyramid inside it | [web.dev](https://web.dev/ta-strategies) |
| **Testing diamond** | Thin unit layer, wide integration, thin E2E | Data-heavy systems and pipelines | Transformations have tricky logic; add property tests per transform | [qaskills](https://qaskills.sh/blog/test-pyramid-testing-strategy) |
| **Testing in production** | Canary, shadow traffic, synthetics, SLO gates | Distributed systems where staging can't reproduce production | No observability or rollback; then it is just shipping bugs | (see Runtime practice rows) |

**How the skill chooses, per component:**

1. Ask: *if this component breaks, where is the bug most likely?* In its own logic → pyramid. At the boundary with a DB, queue, or another service → honeycomb or trophy. In the user flow → trophy plus a few E2E tests.
2. Static analysis and types are the free bottom layer in every model. Turn them on before writing tests.
3. Write E2E tests only for the few journeys whose failure would be an incident (signup, checkout, core workflow). Push everything else down a layer.
4. Add a harness layer where the input space is large: property-based tests for logic, fuzzing for parsers, load tests for hot paths.
5. Add runtime practice once the service has real traffic. The test suite can't see production data shapes or load.

For microservices, the shift goes further. Instead of one big pyramid there are many small ones, which pushes emphasis onto contract testing and service-level integration tests ([testRigor](https://wptest4.testrigor.com/?p=1127727)).

## Skill architecture

Recommended shape: **one router skill, ten authoring skills, four analysis skills, three planning skills, and a folder of CI/ops templates that are not skills at all.** CI templates don't need judgement once installed, so they don't belong in a skill's context. Skills are for work where Claude must decide, write, or interpret.

### Folder layout

```
testing/                          # router: classify the change, pick a scenario playbook, call the right skills
  SKILL.md
  reference/
    scenario-playbooks.md         # the 14 scenarios in this doc
    strategy-models.md            # pyramid / trophy / honeycomb / diamond chooser
    assured-generation.md         # the shared filter protocol every authoring skill must pass (below)
    anti-patterns.md              # tautological tests, over-mocking, sleeps, etc.

# authoring skills: produce committed code
test-unit/            test-integration/     test-contract/        test-e2e/
test-characterization/test-property/        test-fuzz/            test-load/
test-data/            test-llm-evals/

# analysis skills: run tools, triage, explain, and hand gaps to authoring skills
test-mutation/        test-quality-review/  test-flaky-triage/  test-audit/

# planning skills: produce plans, configs, runbooks
test-strategy/        chaos-experiment/     release-safety/

ci-templates/                     # NOT a skill: copied into repos, referenced by skills
  pr-fast.yml  pr-extended.yml  main.yml  nightly.yml  pre-deploy.yml  rollout/
```

Each skill follows the same disclosure levels as the formal-verification skills. **L1** is the description. **L2** is SKILL.md: when to use, the workflow, 5 golden rules, and a one-line summary of top good/bad examples. **L3** is reference files per language or framework. **L4** is the examples: `good/`, `bad/`, each with source and lesson.

### The shared protocol: assured generation

LLM-written tests have one main failure. Asked to test buggy code, a model tends to write tests that assert the bug. One study measured this "misguidance effect": buggy code both increases tests that assert the wrong behaviour and suppresses tests that would find the bug ([Zhao et al., 2026](https://tldr.takara.ai/p/2607.22883)). Meta's answer was to accept a generated test only after it passes automated filters. In one evaluation, 75% of TestGen-LLM's tests built, 57% passed reliably, and 25% increased coverage. Overall it improved 11.5% of the classes it was applied to, and engineers accepted 73% of its recommendations ([Meta](https://arxiv.org/abs/2402.09171v1)).

Every authoring skill must run its output through this protocol before presenting it. Step 0 is the test-audit authoring gate (see Test auditing): if a test can't name its contract, the credible bug it would catch, and why no existing test already catches that bug, it isn't generated at all.

1. **Spec first, code second.** Derive expected behaviour from the ticket, docstring, API spec, or a human. Write that down before reading the implementation. In one experiment, 22 of 60 code-first suites passed on seeded bugs, versus 0 of 60 spec-first suites ([TestMu](https://www.testmuai.com/blog/ai-generated-tests-pass-broken-app/)).
2. **Builds and passes.** It compiles and passes on the current code, or for bug fixes it fails on the old code and passes on the fix.
3. **Not flaky.** Run it N times (e.g. 5) in random order; any non-determinism rejects it.
4. **Adds value.** It kills at least one mutant that the existing suite misses, or covers a changed line no other test covers. Otherwise discard it, however good it looks.
5. **Readable.** One behaviour per test, a descriptive name, and no assertions that restate the implementation.
6. **Human review.** Present only the survivors, each with a one-line note on what it guards and which mutant it kills.

## Authoring skills

Each authoring skill writes code that will be committed and maintained, so it carries the assured-generation protocol plus rules specific to its test type. The table is the content of each skill's SKILL.md. Tools are listed per language so the skill can detect the stack and load the matching L3 reference.

### Tools per language

| Skill | Python | TypeScript / JS | JVM | Go | Rust |
| --- | --- | --- | --- | --- | --- |
| test-unit | pytest | Vitest, Jest | JUnit 5 | `testing` + testify | `cargo test`, nextest |
| test-integration | pytest + testcontainers-python | Testcontainers Node | Testcontainers Java | testcontainers-go | testcontainers-rs |
| test-contract | pact-python | pact-js | pact-jvm | pact-go | pact-rust (via FFI) |
| test-e2e | Playwright Python | Playwright Test | Playwright Java | — | — |
| test-characterization | ApprovalTests.Python, syrupy | Jest/Vitest snapshots, ApprovalTests.NodeJS | ApprovalTests.Java | go-approval-tests, cupaloy | insta |
| test-property | Hypothesis | fast-check | jqwik | rapid, gopter | proptest |
| test-fuzz | Atheris | Jazzer.js | Jazzer | native `go test -fuzz` | cargo-fuzz |
| test-load | Locust | k6 (JS scripts) | Gatling | k6 | k6 / Goose |
| test-data | dbt tests + dbt unit tests, Great Expectations, Soda | — | — | — | — |
| test-llm-evals | promptfoo, DeepEval, Inspect | promptfoo | — | — | — |

### Rules per skill

| Skill | Use when | Golden rules | Reject the output if | Sources |
| --- | --- | --- | --- | --- |
| **test-unit** | Pure logic: calculations, parsing, rules, state machines | Assert behaviour from the spec, not from reading the code. One behaviour per test, named after it. Mock only true boundaries (clock, network, randomness). | It asserts that a mock was called with whatever the code passes; it re-states the implementation; no mutant dies | [tautological tests](https://getautonoma.com/blog/ai-generated-tests-pass-but-dont-assert) |
| **test-integration** | Code whose bugs live at the DB, cache, queue, or filesystem boundary | Use real dependencies in disposable containers, not mocks or in-memory substitutes. Fresh state per test. Pin image versions to production. | It uses H2/SQLite in place of Postgres; tests share state; order-dependent | [Docker](https://www.docker.com/blog/testcontainers-testing-with-real-dependencies/) |
| **test-contract** | Two services or a frontend and API that keep breaking each other | Consumer tests record only fields the consumer actually reads. Provider verifies against its real implementation. Publish to a broker and gate deploys with `can-i-deploy`. Record deployments. | The consumer asserts on fields it doesn't use (over-specified); no deployment records, so `can-i-deploy` can't reason about environments | [OneUptime](https://oneuptime.com/blog/post/2026-08-24-consumer-driven-contract-breaking-changes/view), [Tessl Pact skill](https://tessl.io/registry/testland/pact-contract-testing/1.1.10/files) |
| **test-e2e** | The few user journeys whose failure is an incident | Role- and label-based locators. Web-first assertions that auto-wait. A fresh browser context per test. Seed data through the API, not the UI. Fail CI on tests that only pass on retry. | Any `waitForTimeout`; CSS or XPath selectors tied to styling; `describe.serial` chains; tests depending on earlier tests | [Playwright checklist](https://testdino.com/blog/Playwright%20automation%20checklist), [TestMu](https://www.testmuai.com/blog/playwright-flaky-tests/) |
| **test-characterization** | Legacy code with no tests, before a refactor or migration | Record behaviour on untouched code. Neutralise time, IDs, and randomness first. Prove the pins can fail with mutation testing. Treat them as scaffolding: retire once real tests exist. | It pins non-deterministic output; snapshots too large to review; nobody can explain an update | [Feathers / Wikipedia](https://en.wikipedia.org/wiki/Characterization_test), [developertoolkit.ai](https://developertoolkit.ai/en/workflows/test/characterization-tests/), [HelpMeTest](https://helpmetest.com/blog/golden-master-testing/) |
| **test-property** | Large input spaces; invariants such as round-trip, idempotence, ordering, conservation | Use constrained strategies, not heavy `assume()`. Stateful tests for APIs with state. Pin found failures with explicit examples. Fixed seed in CI. | "Doesn't crash" as the only property; >50% of inputs filtered | Formal-verification doc, Hypothesis section |
| **test-fuzz** | Parsers, decoders, deserialisers, anything reading untrusted bytes | Small harness per entry point. A seed corpus of real inputs. Sanitizers on (ASan/UBSan where native). Each crash becomes a committed regression input. | The harness catches and swallows exceptions; no corpus; crashes not minimised | [ClusterFuzzLite](https://google.github.io/clusterfuzzlite/) |
| **test-load** | Hot paths, capacity planning, performance-sensitive changes | Scripts as code with thresholds (e.g. p95/p99 latency, error rate) so a failed threshold exits non-zero. Smoke-size run on PRs; load, stress, spike, and soak on a schedule. Realistic data variety to avoid cache-only results. | Soak tests in PR CI; averages instead of percentiles; one hot key hit forever | [Tessl k6](https://tessl.io/registry/testland/k6-load-testing), [Grafana docs](https://www.mintlify.com/grafana/k6-docs/testing-guides/automated-testing) |
| **test-data** | dbt models, ETL jobs, warehouse tables | dbt unit tests with static mock inputs for transformation logic. Schema and data tests (unique, not null, relationships, freshness) on real data. Set test severity so not every warning blocks. | Tests only on final marts; every check is blocking, so the pipeline alerts constantly | [Paradime](https://www.paradime.io/guides/dbt-unit-testing-guide), [Orchestra](https://getorchestra.io/guides/data-quality-with-dbt-great-expectations) |
| **test-llm-evals** | Prompts, RAG, agents, model upgrades | Versioned golden dataset (JSONL). Deterministic settings where possible. Hard deterministic checks plus a thresholded judge score. Separate capability evals (low pass rate, tracking progress) from regression evals (near 100%). | Only LLM-as-judge; dataset edits not versioned; a score improvement that coincides with a dataset change | [Tessl LLM regression](https://tessl.io/registry/testland/llm-regression-suite-author), [fast.io](https://fast.io/resources/ai-agent-prompt-regression-testing/), [Galtea](https://galtea.ai/blog/automated-llm-evaluation-building-a-ci-cd-quality-gate-that-actually-runs) |

**Snapshot tests deserve a special rule.** They are the easiest tests for an LLM to generate and the easiest for humans to rubber-stamp. A snapshot that gets regenerated blindly provides zero protection ([QASkills](https://qaskills.sh/blog/jest-snapshot-testing-guide-2026)). The skill should keep snapshots small, mask dynamic values, and require an explanation in the PR for every snapshot update.

## Analysis and gate skills

These write no product tests. They run a tool, separate signal from noise, explain findings in plain language, and hand real gaps to an authoring skill. Most of their value is triage: a CI step that floods reviewers with findings gets ignored.

### test-mutation

Mutation testing is the strongest check that tests catch real bugs, and the main defence against LLM tests that only restate the code. Industrial practice has settled on three rules, from Google's deployment across more than 24,000 developers and 1,000 projects ([Google, TSE 2021](https://deepai.org/publication/practical-mutation-testing-at-scale)):

1. **Mutate only changed lines**, during code review, never the whole codebase.
2. **Filter aggressively.** Skip "arid" lines such as logging and boilerplate, cap mutants per line and per review, and prefer operators with a history of producing useful findings.
3. **Surface few, actionable survivors** in the review UI, with a one-click "not useful" signal. Google found that non-actionable findings in review hurt both author and reviewer ([arXiv](https://arxiv.org/pdf/2102.11378)).

| Language | Tool | Diff-scoped mode |
| --- | --- | --- |
| Python | mutmut (cosmic-ray for larger codebases) | File-level only; filter results to diff lines yourself |
| JS / TS | StrykerJS | `--mutate "file:lines"`, incremental mode |
| JVM | PIT | Target classes from the diff |
| Rust | cargo-mutants | `--in-diff git.diff` |
| Go | gremlins, go-mutesting | Limited targeting |

**Skill workflow:** compute the diff → estimate the mutant count and ask before running anything over \~15 minutes → run → drop equivalent or arid survivors → report the score and the top 1–3 survivors, each with a suggested test → hand accepted survivors to `test-unit` to write the killing test.

**As a CI step:** PR job on the diff, advisory at first, blocking later on critical paths. A nightly or weekly full run on core modules builds a score trend.

### test-quality-review

This skill bundles three cheap checks:

- **Diff coverage gate.** Gate on coverage of the lines the PR changed, not a whole-repo percentage. A repo-wide number hides an untested change behind a large existing suite. Common thresholds are 70–80% of changed lines ([agentpatterns.ai](https://agentpatterns.ai/verification/diff-coverage-gate-agent-prs/)). Coverage only proves lines ran, not that they were checked ([QASkills](https://qaskills.sh/blog/code-coverage-diff-coverage-enforcement)), so pair it with mutation.
- **Test-deletion guard.** Block PRs that delete or skip tests unless they come with an explanation or a test-audit evidence ledger. Deleting tests is an easy path to a green build for an agent.
- **Test-smell scan.** Flag tests with no assertions, assertions only on mocks, `sleep` calls, catch-all exception handlers, snapshot files over \~50 lines, and tests that read the system clock or network.

### test-flaky-triage

Flakiness is a fleet problem, not a single-test one. Google has reported that about 1.5% of test executions were flaky but that, over time, about 16% of its tests showed some flakiness, and 84% of pass-to-fail transitions in CI were flakes rather than real bugs ([TestDino](https://testdino.com/blog/flaky-test-benchmark-report-2026)). Flaky tests also cluster: one 2025 study found 75% fail in correlated groups averaging 13.5 tests, so fixing one root cause clears many ([ThinkSys](https://thinksys.com/qa-testing/how-to-reduce-flaky-tests-automation-frameworks/)).

**Skill workflow:** mine CI history for tests with both outcomes on the same code → cluster by shared root cause (time, order, shared state, network, async waits) → quarantine automatically with an owner and an expiry date → propose the fix for the largest cluster. Quarantine without an expiry becomes a one-way door that silently drops coverage.

### Gates that are CI templates, not skills

| Gate | Tool examples | Notes |
| --- | --- | --- |
| Test-impact / predictive selection | Static dependency graphs (Bazel, Nx, pytest-testmon) or ML selection (Launchable) | Vendors report most of the value of a full run from a 10–20% subset ([Launchable](https://launchableinc.com/blog/the-right-tests-for-a-code-change-with-test-impact-analysis)); always keep a periodic full run |
| Performance regression | Benchmarks compared against a stored baseline; k6 thresholds | Fail on statistically meaningful slowdowns only |
| Contract gate | `can-i-deploy` | Runs before every deploy |
| Schema compatibility | `buf breaking`, OpenAPI diff, migration lint | PR |
| SAST / secrets / dependencies / IaC | Semgrep, CodeQL, gitleaks, OSV-Scanner, Checkov | A skill helps only to write custom Semgrep rules |

## Test auditing: the lean-suite skill

`test-audit` keeps the suite as small as possible while it still catches every credible regression. It is the counterweight to the authoring skills. Agents add tests easily; this skill makes them justify each one, and removes the ones that don't earn their place. The trigger was Peter Steinberger's report that OpenClaw deleted about 400k lines of its own tests without much change in coverage, because models write a test for every tiny change whether it is useful or not ([steipete on X](https://x.com/steipete/status/2103147927313199260)). His key prompt lesson: an agent told to "clean up" stops too early, so give it a numeric goal, such as removing 20% of the least useful tests while keeping coverage within 2% ([follow-up](https://x.com/steipete/status/2103148444701610233)).

**Value bar:** a test stays only if it catches a credible regression that no other test catches. Several published skills use this exact framing, e.g. "Tests earn their place by catching a credible regression that nothing else catches" ([mblode/test-audit](https://www.skills.sh/mblode/agent-skills/test-audit)).

### Three modes

| Mode | Trigger | Scope | Done when |
| --- | --- | --- | --- |
| **Gate** | Any authoring skill is about to add or change a test | The new or changed tests in the diff | Each test answers the four gate questions below, or is dropped |
| **Audit** | "Clean up these tests", a slow or noisy directory | Named files or one directory | A handful of high-confidence candidates, each with full evidence, deleted in one batch with validation green |
| **Campaign** | "Make the suite lean", a numeric target, or a quarterly schedule | A subsystem or the whole repo | Target met (or the ledger explains why not), coverage and mutation score within tolerance, preservation review passed |

The audit and campaign split follows the published test-audit skills from BuilderIO and mblode, which also both default to read-only discovery and evidence before edits ([BuilderIO](https://tessl.io/registry/skills/github/BuilderIO/agent-native/test-audit), [mblode](https://www.skills.sh/mblode/agent-skills/test-audit)).

### The authoring gate (runs inside assured generation)

Every new or changed test must answer four questions before it is kept. These are adapted from BuilderIO's gate:

1. **What contract does it protect?** A behaviour, invariant, API, or regression, named in one line.
2. **What credible bug would make it fail?** If you can't describe one, don't add it.
3. **Why doesn't an existing test already catch that?** Each contract has one owning test at the strongest boundary. If a near-duplicate exists, extend its table of cases instead of adding a new test.
4. **Does it need a test-only hook in production code** (an export, flag, or wrapper no real caller uses)? If yes, test at the real boundary instead.

A test that would break under a behaviour-preserving refactor is asserting implementation. Rewrite it at the owning boundary or drop it.

### What counts as bloat

| Category | Example | Default action |
| --- | --- | --- |
| Dead tests | Skipped, commented out, or testing a deleted source file | Delete |
| Assertion-free or rubber-stamp | Calls code, asserts nothing meaningful, or only "doesn't throw" | Delete; report the real gap rather than keep false coverage |
| Tautological / self-confirming | Expected value computed by the code under test; assertions satisfied by the test's own setup | Delete or rewrite from the spec |
| Mocked-everything | The module under test is itself mocked; the mock implements the behaviour being asserted | Delete or move to an integration test |
| Duplicate contract | Same path, same inputs, equivalent assertions, often from agents adding a new test per task instead of extending one ([audit-tests skill](https://skillsmp.com/creators/conn-castle/personal-context/agent-layer-skills-audit-tests)) | Keep the strongest owner; delete the rest |
| Near-duplicate examples | Ten tests differing only in input values | Fold into one table-driven or property test |
| Implementation-coupled | Pins private call shapes, call counts, or internal ordering already proven at the public boundary | Delete if the boundary test exists |
| Restated source | Greps for exact source strings, copied export lists, fixture inventories, restated config flags | Delete; keep only if it guards a user-facing contract |
| Test-only production seams | Exports, globals, or wrappers kept alive only by tests | Delete the test and the seam (net-negative production code) |
| Snapshot bloat | Large snapshots of plain data or whole pages | Replace with targeted assertions or delete |
| Fixture sprawl | The same setup copied across dozens of files | Consolidate into shared fixtures (no tests removed) |

**Never delete just because coverage doesn't change.** Retain tests that independently enforce a public API, protocol, config, migration, storage, security, access, platform-default, or release contract. Also retain guard tests that prove a check both passes and fails. A retained test that fails on baseline may be catching a product bug, so fix the code rather than the test. Being slow or static is not a reason to delete ([BuilderIO](https://tessl.io/registry/skills/github/BuilderIO/agent-native/test-audit)).

### Minimal-suite selection: fewest tests, same bug-finding power

Coverage alone is too weak a measure for pruning. Two tests can cover the same lines while only one checks the result. A test whose deletion changes neither coverage nor the set of killed mutants is a liability ([origo](https://origo.prose.sh/high-coverage-zero-signal)). So the campaign keeps the **mutant-kill set** constant, not just the coverage number:

1. **Build the evidence matrix.** For each test in scope, record the lines and branches it covers (per-test coverage contexts, e.g. `coverage.py --context=test`, Istanbul per-test, or llvm-cov per test binary) and the mutants it kills (mutation tools that report killing tests per mutant).
2. **Find zero-unique tests.** A test with no uniquely covered branch and no uniquely killed mutant is a candidate; everything it proves, something else proves too.
3. **Choose the keepers.** Pick a small set of tests that together still kill every mutant the full suite kills (greedy set cover over the kill matrix). Break ties toward tests at the owning public boundary, then deterministic, then fast.
4. **Consolidate before deleting.** Fold near-duplicate examples into table-driven or property-based tests. Merge copied setup into shared fixtures. OpenClaw's cleanup PRs did both, e.g. consolidating 41 copies of a directory setup ([PR #1397](https://github.com/openclaw/clawsweeper/pull/1397)) and replacing repeated cases with branch tables ([PR #184680](https://github.com/openclaw/openclaw/pull/184680)).
5. **Apply the retention bar** to every candidate before it goes in the ledger.

### Evidence ledger (one row per candidate)

Each candidate gets a row before anything is edited, per BuilderIO's evidence rules:

- Name and location
- What failure it can detect
- Non-test callers of anything it keeps alive
- **The stronger test that still proves the same contract** (named explicitly)
- Unique coverage and unique mutant kills (should be zero)
- Risk
- Validation command

OpenClaw's commit messages model the "retained coverage" field: each deletion names the file that still covers the removed behaviour ([PR #182725](https://github.com/openclaw/openclaw/pull/182725)).

### Campaign workflow

1. **Set a numeric target up front.** If the user gave none, propose one. Default: remove the least useful 20% of test declarations in scope, keep line and branch coverage within 2 points of baseline, keep the mutation score on core modules at or above baseline, and keep every retained test green. (The first three limits follow [mblode](https://www.skills.sh/mblode/agent-skills/test-audit); the mutation limit is this toolkit's addition.)
2. **Baseline.** Record test count, test LOC, suite runtime, line and branch coverage, and the mutation score on core modules.
3. **Discover read-only.** Build the evidence matrix and the ledger.
4. **Edit in batches**, one coherent owner boundary per batch and one PR per batch. Each commit message lists what was removed and what retained test covers it.
5. **Re-measure after each batch.** Revert a batch that breaks a tolerance.
6. **Preservation review.** A fresh-context reviewer, human or a separate agent, checks that every security, contract, and migration test survived.
7. **Report.** Tests and LOC removed (test and production separately), runtime saved, coverage delta, mutation delta, retained false positives with reasons, and follow-ups.
8. **Prevent regrowth.** Propose additions to the repo's AGENTS.md or CLAUDE.md based on the patterns this audit found, so agents stop writing them ([mblode](https://llmbase.ai/skills/mblode/test-audit/)).

### How it plugs into the rest of the toolkit

- **Assured generation gains a step 0:** the four gate questions run before a generated test is even executed.
- **test-quality-review's deletion guard** blocks unexplained test deletions, but accepts deletions that come with a test-audit ledger. That separates disciplined pruning from an agent deleting tests to get a green build.
- **CI:** the gate runs on PRs that add tests as an advisory review comment. Campaigns run quarterly, or when suite runtime or test LOC grows faster than production LOC.
- **Metric:** track tests (and suite runtime) per killed mutant on core modules; a lean suite keeps this flat or falling as the codebase grows.

## Planning skills

These produce plans, configs, and runbooks rather than test code. Their job is to force the discipline that makes risky techniques safe.

| Skill | Produces | Refuses to finish without | Sources |
| --- | --- | --- | --- |
| **test-strategy** | Per-component shape (pyramid, trophy, honeycomb, diamond), which skills apply, CI stages to install, a gap list ranked by risk | A named risk for each component ("where would the bug be?") | Strategy models section |
| **chaos-experiment** | Experiment definition (Chaos Mesh, Litmus, AWS FIS, or Toxiproxy for local), hypothesis, run log template, learning question | A steady-state metric tied to a real user journey; a falsifiable hypothesis with a threshold and time window; blast-radius limits; stop conditions set before running (e.g. on error-budget burn); a rollback plan | [Principles summary](https://educative.io/blog/chaos-engineering-process-principles), [System Design Space](https://system-design.space/en/chapter/chaos-engineering-tooling) |
| **release-safety** | Rollout config (canary steps, analysis templates with success/failure conditions), SLO definitions and burn-rate alerts, synthetic probe list, rollback runbook | Metrics that compare canary to stable, not to a fixed number; at least one business KPI alongside error rate and latency | [Argo Rollouts](https://argoproj.github.io/rollouts), [OneUptime](https://oneuptime.com/blog/post/2026-02-26-argocd-canary-analysis-prometheus/markdown) |

Chaos adoption should be staged: start with game days in staging, then move to scheduled automated experiments as confidence grows ([ResumeLens](https://www.resumelens.org/blog/devops/chaos-engineering-litmus-gremlin-chaos-mesh)). The skill should only suggest production experiments once SLOs, alerting, and rollback exist.

## Scenario playbooks

The router skill's first job is to recognise which scenario it is in. The scenario decides the order of skills and the definition of done. These 19 playbooks go into `reference/scenario-playbooks.md`. **Signal** is what the router looks for in the request or diff.

### Changing code

| Scenario | Signal | Playbook (skills in order) | Done when |
| --- | --- | --- | --- |
| **Bug fix** | Issue link, "fix", a stack trace | 1. `test-unit` / `test-integration`: write a test that reproduces the bug and **fails on current code**. 2. Fix. 3. Test passes. 4. `test-mutation` on the diff. | The test failed before the fix and passes after; no surviving mutants on changed lines |
| **New feature in existing code** | New endpoint, function, or component | 1. `test-strategy`: pick the shape for this component. 2. Spec-first authoring at the right layer. 3. `test-quality-review` (diff coverage). 4. `test-mutation` advisory. | Diff coverage ≥ threshold; every acceptance criterion has a test |
| **Refactor (no behaviour change)** | "refactor", "clean up", moved code | 1. Check the current tests kill mutants in the area. If not, `test-characterization` first. 2. Refactor. 3. All pins still pass. 4. Optional `test-property` with old vs. new as oracle. | Same observable behaviour proved by pins or a differential test |
| **Legacy code with no tests** | Low coverage, no tests in the module | 1. Find seams. 2. `test-characterization` on untouched code. 3. Prove the pins can fail (`test-mutation`). 4. Change code. 5. Replace pins with real tests over time. | Pins in place and proven to fail on mutants before any edit |
| **Performance-sensitive change** | Hot path, query change, caching | 1. Benchmark baseline. 2. Change. 3. `test-load` smoke with thresholds. 4. Scheduled stress/soak if risky. | No meaningful regression in p95/p99 or throughput |
| **Dependency or framework upgrade** | Lockfile or major version bump | 1. Full suite + `test-contract` verification. 2. Differential test of key outputs old vs. new. 3. Canary on deploy. | Contracts green; no diffs on golden outputs |
| **Security fix** | CVE, auth, injection, input handling | 1. Regression test that exploits the bug. 2. Fix. 3. `test-fuzz` on the affected parser or handler. 4. Custom Semgrep rule to prevent recurrence. | Exploit test fails before and passes after; rule in CI |

### Building new things

| Scenario | Signal | Playbook | Done when |
| --- | --- | --- | --- |
| **Greenfield service** | New repo or service skeleton | 1. `test-strategy` (honeycomb for services, pyramid for libraries). 2. Install `ci-templates`. 3. `test-integration` with containers from day one. 4. `test-contract` for every consumer. 5. Smoke `test-load`. 6. `release-safety` (canary, SLOs). | Every layer has at least one test and CI runs all stages |
| **New API endpoint** | Route or OpenAPI change | 1. Update the OpenAPI spec. 2. Schemathesis run. 3. `test-integration` for business rules. 4. `test-contract` if consumers exist. 5. Schema-compatibility gate. | Spec-driven fuzzing clean; contracts verified |
| **Service-to-service integration** | New client of another service | 1. `test-contract` (consumer side). 2. Provider verification. 3. Fault tests with Toxiproxy (timeouts, 5xx, slow responses). 4. `can-i-deploy` gate. | Pact verified; failure modes tested |
| **Frontend feature** | Component or page change | 1. Component tests (trophy shape). 2. One `test-e2e` journey if critical. 3. Visual regression + accessibility. | Behaviour assertions, not snapshots, on logic |
| **Data pipeline / dbt model** | SQL, ETL, schema change | 1. `test-data`: dbt unit tests on transformation logic. 2. Schema and data tests. 3. Data diff vs. production. 4. Freshness and volume monitors. | Unit tests green; data diff explained |
| **LLM feature / prompt change** | Prompt, model, or retrieval change | 1. `test-llm-evals`: golden set + deterministic checks + judge. 2. Red-team set for user-facing input. 3. Shadow or canary with eval sampling. | Regression pass rate ≥ baseline; no new red-team failures |
| **Database schema migration** | Migration file | 1. Migration test on a production-sized snapshot (time + locks). 2. Old code vs. new schema and new code vs. old schema. 3. Backfill test. 4. Rollback test. | Both version pairs pass; migration time measured |

### Operating systems

| Scenario | Signal | Playbook | Done when |
| --- | --- | --- | --- |
| **Infrastructure / config change** | Terraform, Helm, k8s manifests | 1. IaC policy gate. 2. Plan review. 3. Canary or staged apply. 4. `chaos-experiment` if it changes failure domains. | Policies pass; staged rollout healthy |
| **Incident follow-up** | Postmortem action item | 1. Regression test reproducing the trigger (unit, integration, or fault-injection level). 2. `chaos-experiment` that recreates the failure. 3. SLO alert review. | The failure is reproducible in CI or staging and now handled |
| **Flaky-suite crisis** | Retry rates climbing, "just re-run it" culture | 1. `test-flaky-triage`. 2. Quarantine with expiry. 3. Fix the largest clusters first. | Flake rate below the target agreed with the team |
| **Bootstrapping testing on a repo** | "Add tests to this repo" | 1. `test-strategy` audit of current state. 2. CI templates. 3. Characterization on the riskiest modules. 4. Diff-coverage gate for new code only. 5. Mutation nightly. | New code is gated; legacy debt is visible but not blocking |
| **Test-suite bloat (lean-suite campaign)** | Slow suite; test LOC growing faster than production LOC; many agent-added tests | 1. test-audit campaign with a numeric target (default: remove 20% of tests, coverage within 2 points, mutation score not lower). 2. Consolidate into table-driven or property tests. 3. Batch PRs, each with an evidence ledger. 4. Add the patterns found to AGENTS.md. | Target met; coverage and mutation score within tolerance; preservation review passed |

## CI/CD pipeline: what runs where

Each stage has a time budget, and a check moves later in the pipeline once it costs more than its stage allows. Results-type steps (mutation, fuzz, load) run on the **diff** early and in **full** on a schedule. Code-type steps (unit, integration, E2E) run on every change, with impact analysis trimming them when suites get large.

| Stage | Budget | Runs | Blocks merge or deploy? |
| --- | --- | --- | --- |
| **Pre-commit** (local hook) | < 30 s | Formatters, linters, type checks, secret scan, unit tests for touched files | Locally only |
| **PR — fast** | < 10 min | Unit + integration (impact-selected if large), diff coverage, schema-compat checks, SAST, dependency scan, contract consumer tests, Schemathesis on changed endpoints, LLM evals (small golden set) on prompt changes | Yes |
| **PR — extended** (parallel, may finish after review starts) | < 30 min | Diff-scoped mutation testing, fuzzing of changed targets (ClusterFuzzLite defaults to 10 minutes per run and stops at the first crash, [docs](https://docsearch.algolia.com/mcp/docs/repo/google/clusterfuzzlite)), critical-path E2E, k6 smoke, visual regression | Advisory first; blocking on critical paths once trusted |
| **Main / merge** | < 30 min | Full unit + integration, full E2E set, provider contract verification, benchmark compare vs. baseline | Blocks the deploy pipeline |
| **Nightly** | Hours | Full mutation on core modules, batch fuzzing (builds corpus), load/stress/spike, flaky-test detection over history, full LLM eval set + red-team, DAST on staging, full dependency audit | Opens issues; doesn't block merges |
| **Weekly / scheduled** | Hours | Soak tests, chaos experiments in staging, DR restore drill (monthly or quarterly), mutation score trend report, test-audit campaign (quarterly, or when test LOC grows faster than production LOC) | Opens issues |
| **Pre-deploy** | < 5 min | `can-i-deploy` contract gate, migration dry-run, SLO error-budget check (enough budget left to ship?) | Yes |
| **Deploy / canary** | 10–60 min | Progressive traffic with automated analysis; e.g. Argo Rollouts queries metrics and drives automatic promotion or rollback ([Argo](https://argoproj.github.io/rollouts)). Synthetic probes against the canary. | Auto-rollback |
| **Production (continuous)** | Always on | Synthetic monitoring, SLO burn-rate alerts, invariant monitors, sampled LLM eval on live traffic | Pages a human |

**Template files:** `ci-templates/` ships one workflow per stage (`pr-fast.yml`, `pr-extended.yml`, `main.yml`, `nightly.yml`, `pre-deploy.yml`) plus `rollout/` for Argo Rollouts analysis templates. The router skill installs the ones a repo is missing, rather than regenerating them each time.

**Rollout order for a team adopting this:**

1. PR-fast + diff coverage.
2. Characterization on risky modules.
3. Nightly mutation (advisory).
4. Contract gate.
5. Canary analysis.
6. PR mutation as a blocking check on critical paths.
7. Chaos and DR drills.

## Anti-patterns and guards

Every anti-pattern below becomes an `examples/bad/` entry in the relevant skill: the broken test, the symptom, the guard that catches it, and the fix. The LLM-specific ones come first, because an agent writing tests will hit them more often than a human.

### LLM-written tests

| Anti-pattern | Symptom | Guard | Source |
| --- | --- | --- | --- |
| Oracle copied from the code under test | Tests pass on buggy code; they assert what the code does, not what it should do | Spec-first prompting; mutation check | [Misguidance effect](https://tldr.takara.ai/p/2607.22883), [TestMu](https://www.testmuai.com/blog/ai-generated-tests-pass-broken-app/) |
| Same model writes the code and the tests | Both share the same mistaken assumptions; coverage looks high while most mutants survive | Separate spec step; different-context review; mutation | [Tian Pan](https://tianpan.co/blog/2026-05-04-ai-generated-tests-coverage-illusion) |
| Tautological / mock-only assertions | "verify mock called with X" where X is whatever the code passes | test-quality-review smell scan | [Autonoma](https://getautonoma.com/blog/ai-generated-tests-pass-but-dont-assert) |
| Exact-value examples instead of invariants | Green suite misses input permutations | Push to property-based tests where an invariant exists | [DEV case study](https://dev.to/sofiabennett84/when-ai-generated-tests-pass-but-dont-protect-a-case-study-in-false-assurance-2gj8) |
| Deleting or skipping failing tests | Green build, fewer tests | Test-deletion guard blocks the PR | [agentpatterns.ai](https://agentpatterns.ai/verification/diff-coverage-gate-agent-prs/) |
| "Fixing" a failing test by changing its expectation | The bug is now enshrined | Rule: never edit an assertion to match new output without a spec reason in the PR | — |
| Generated tests never checked for flakiness | Intermittent failures weeks later | Assured-generation step 3: run N times in random order | [Meta TestGen-LLM](https://arxiv.org/pdf/2402.09171) |

### Authored tests in general

| Anti-pattern | Symptom | Guard | Source |
| --- | --- | --- | --- |
| Mocks or in-memory fakes for the DB | Passes in CI, fails on real SQL, constraints, or transactions | test-integration rules: real containers | [Docker](https://www.docker.com/blog/testcontainers-testing-with-real-dependencies/) |
| Fixed sleeps in UI tests | Slow and flaky | Web-first assertions; lint for `waitForTimeout` | [Better Stack](https://betterstack.com/community/guides/testing/avoid-flaky-playwright-tests/) |
| Retries hide flakes | Green on retry; the flake never gets fixed | Fail CI on tests that only pass on retry | [TestMu](https://www.testmuai.com/blog/playwright-flaky-tests/) |
| Giant snapshots, updated blindly | Bugs approved into the baseline | Size limit; PR explanation required | [Pinpoint](https://testwithpinpoint.com/blog/snapshot-testing-guide) |
| Golden masters kept forever | Nobody reviews them; updates become automatic | Retire once real tests cover the behaviour | [HelpMeTest](https://helpmetest.com/blog/golden-master-testing/) |
| E2E for everything | Slow, flaky suite; teams stop trusting it | Strategy skill limits E2E to critical journeys | [web.dev](https://web.dev/ta-strategies?authuser=1004904077) |
| Repo-wide coverage target | Teams game it with low-value tests; untested diffs hide | Diff coverage + mutation instead | [QASkills](https://qaskills.sh/blog/code-coverage-diff-coverage-enforcement) |

### Results-type steps

| Anti-pattern | Symptom | Guard | Source |
| --- | --- | --- | --- |
| Full-codebase mutation on every PR | Hours of CI; results ignored | Diff-scoped mutation; full run nightly | [Google](https://research.google/pubs/pub50658/) |
| Dumping every surviving mutant on reviewers | Alert fatigue | Cap at 1–3 actionable survivors per PR | [Google](https://arxiv.org/pdf/2102.11378) |
| Quarantine with no expiry or owner | Coverage silently shrinks | Owner + expiry; weekly review | [ThinkSys](https://thinksys.com/qa-testing/how-to-reduce-flaky-tests-automation-frameworks/) |
| Soak or stress tests in PR CI | Multi-hour PRs; the team disables the job | Smoke on PR, heavier runs scheduled | [Tessl k6](https://tessl.io/registry/testland/k6-load-testing) |
| Average latency thresholds | Tail regressions ship | p95/p99 thresholds | [QASkills](https://qaskills.sh/blog/k6-load-testing-p95-p99-guide) |
| Chaos without a hypothesis or abort criteria | The experiment becomes an incident | chaos-experiment skill refuses to run without steady state, blast radius, and abort conditions | [Chaos skill](https://skillselion.com/skills/alirezarezvani/claude-skills/chaos-engineering), [System Design Space](https://system-design.space/en/chapter/chaos-engineering-tooling) |
| Eval dataset edited alongside the prompt | Score "improves" because the test got easier | Version the dataset; record its version in every run | [Galtea](https://galtea.ai/blog/automated-llm-evaluation-building-a-ci-cd-quality-gate-that-actually-runs) |
| Regression evals stuck at 100% for weeks | They no longer catch anything | Promote harder capability cases into the regression set | [fast.io](https://www.fast.io/resources/ai-agent-prompt-regression-testing.md) |

## Metrics that tell you the test system works

Track a small set, and trend them rather than gating on absolutes. Start with the first five; add the rest once the basics are stable.

| Metric | Measures | How | Healthy direction |
| --- | --- | --- | --- |
| Mutation score on changed code | Whether tests catch real behaviour changes | Diff-scoped mutation per PR, aggregated weekly | Up; surviving mutants per PR near zero on critical paths |
| Diff coverage | Whether new code carries its own tests | diff-cover or similar on every PR | Stable at or above the team threshold |
| Flake rate | Trust in the suite | Share of tests with both outcomes on unchanged code over a window | Down; agree a target with the team |
| PR feedback time (p50 / p90) | Developer experience | Time from push to PR-fast result | Under the stage budget |
| Escaped defects | What tests missed | Bugs found in production, tagged by the layer that should have caught them | Down; each one drives a new test and a playbook review |
| Quarantine size and age | Hidden coverage loss | Count and oldest entry | Small, nothing past its expiry |
| Test-to-fix lead time on incidents | Learning loop | Postmortem date → regression test merged | Short |
| Change failure rate (DORA) | Release safety | Deploys causing rollback or incident | Down |
| Canary rollback rate | Whether pre-production testing catches issues | Auto-rollbacks / deploys | Low but non-zero; zero may mean the canary analysis is too lax |
| Eval regression pass rate | LLM feature stability | Per-PR eval run vs. baseline | At or above baseline |
| Tests per killed mutant | Suite leanness | Test count (and suite runtime) divided by mutants killed on core modules | Flat or down as the codebase grows |

The escaped-defects metric is the one to review regularly. Each escaped bug is tagged with the layer and playbook that should have caught it, so the playbooks, not just the tests, get better over time.

## How this connects to the formal verification toolkit

The two skill sets cover different questions about the same system. They should share a router so the user never has to choose between them. Formal methods ask "can the design ever do the wrong thing?" This toolkit asks "does the code we shipped do the right thing on the inputs and conditions we can exercise?"

| Handoff | From → to | What moves |
| --- | --- | --- |
| Model counterexample → regression test | Formal (TLA+/Alloy) → `test-integration` / `test-unit` | A deterministic test that forces the same interleaving or state |
| Model-based test traces | Formal → `test-property` (stateful) | Traces replayed against the implementation |
| Property library | Shared | Conservation, idempotence, order independence, and oracle equivalence are used by both Hypothesis tests and formal specs |
| Mutation as sanity check | `test-mutation` → both | The same idea checks that specs aren't vacuous and that tests aren't tautological |
| Fault models | Shared | The fault switches in the formal doc (crash, duplicate, reorder, partition, skew) map to Toxiproxy tests and chaos experiments here |
| Runtime invariant monitors | Formal (trace validation) ↔ release-safety | Spec-derived monitors run beside SLO alerts in production |
| Incident follow-up | Release-safety → both | Every incident gets a regression test; protocol-level incidents also get a model update |

**Combined router logic:** classify the change with this doc's scenario playbooks first. Escalate to the formal toolkit when the scenario involves concurrency, distributed state, retries, permissions, or rule tables, using the escalation ladder in that doc. Property-based tests live in both; the testing toolkit owns their authoring, and the formal toolkit owns the property library.

## Sources

Research and industry practice

- [Practical Mutation Testing at Scale: A View from Google](https://research.google/pubs/pub50658/) (TSE 2021); [arXiv version](https://arxiv.org/pdf/2102.11378)
- [Automated Unit Test Improvement using LLMs at Meta (TestGen-LLM)](https://arxiv.org/abs/2402.09171v1)
- [Evaluating the misguidance effect of buggy code in LLM-generated tests](https://tldr.takara.ai/p/2607.22883)
- [Design choices made by LLM-based test generators prevent them from finding bugs](https://arxiv.org/html/2412.14137v1)
- [Why AI-generated tests pass when your app is broken (spec-first vs. code-first experiment)](https://www.testmuai.com/blog/ai-generated-tests-pass-broken-app/)
- [Flaky test benchmark report 2026](https://testdino.com/blog/flaky-test-benchmark-report-2026); [flaky clusters and quarantine](https://thinksys.com/qa-testing/how-to-reduce-flaky-tests-automation-frameworks/)
- [Characterization test (Feathers)](https://en.wikipedia.org/wiki/Characterization_test)

Strategy

- [Pyramid or Crab? (web.dev)](https://web.dev/articles/ta-strategies)
- [Testing strategies: pyramids, trophies, and honeycombs](https://howitworks-dev.pages.dev/testing-strategies/)

Tools and practices

- [Testcontainers: testing with real dependencies](https://www.docker.com/blog/testcontainers-testing-with-real-dependencies/)
- [Consumer-driven contracts and can-i-deploy](https://oneuptime.com/blog/post/2026-08-24-consumer-driven-contract-breaking-changes/view)
- [Playwright anti-flake checklist](https://testdino.com/blog/Playwright%20automation%20checklist)
- [ClusterFuzzLite](https://google.github.io/clusterfuzzlite/)
- [k6 automated performance testing](https://www.mintlify.com/grafana/k6-docs/testing-guides/automated-testing)
- [cargo-mutants incremental PR testing](https://mutants.rs/pr-diff.html)
- [Diff-coverage gating for agent PRs](https://agentpatterns.ai/verification/diff-coverage-gate-agent-prs/)
- [Predictive test selection (Launchable)](https://launchableinc.com/blog/the-right-tests-for-a-code-change-with-test-impact-analysis)
- [dbt unit testing](https://www.paradime.io/guides/dbt-unit-testing-guide)
- [LLM regression suites](https://tessl.io/registry/testland/llm-regression-suite-author); [evals in CI](https://galtea.ai/blog/automated-llm-evaluation-building-a-ci-cd-quality-gate-that-actually-runs)
- [Chaos engineering principles](https://educative.io/blog/chaos-engineering-process-principles); [experiment guardrails](https://system-design.space/en/chapter/chaos-engineering-tooling)
- [Argo Rollouts](https://argoproj.github.io/rollouts)

Prior-art skills to mine (don't copy wholesale)

- [Diff-scoped mutation testing skill](https://www.claudepluginhub.com/skills/pvillega-ct-plugins-ct/mutation-testing)
- [Pact contract testing skill](https://tessl.io/registry/testland/pact-contract-testing)
- [Playwright automation skill](https://skillselion.com/skills/petrkindlmann/qa-skills/playwright-automation)
- [Chaos engineering skill](https://skillselion.com/skills/alirezarezvani/claude-skills/chaos-engineering)
- [Data quality frameworks skill](https://www.skills.sh/wshobson/agents/data-quality-frameworks)

Test auditing

- [Peter Steinberger: OpenClaw removed \~400k test LOC](https://x.com/steipete/status/2103147927313199260); [numeric-target prompt](https://x.com/steipete/status/2103148444701610233)
- [OpenClaw cleanup PR examples](https://github.com/openclaw/openclaw/pull/182725), [#184680](https://github.com/openclaw/openclaw/pull/184680), [clawsweeper #1397](https://github.com/openclaw/clawsweeper/pull/1397)
- [BuilderIO test-audit skill](https://tessl.io/registry/skills/github/BuilderIO/agent-native/test-audit); [mblode test-audit skill](https://www.skills.sh/mblode/agent-skills/test-audit); [audit-tests skill](https://skillsmp.com/creators/conn-castle/personal-context/agent-layer-skills-audit-tests)
- [High coverage, zero signal](https://origo.prose.sh/high-coverage-zero-signal)
