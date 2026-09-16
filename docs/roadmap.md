# Roadmap

## Direction

Deliver a reusable template for tabular classification that a team can adopt,
test, release and operate with explicit data, model and deployment contracts.
Keep the default workflow local and credential-free. Add infrastructure only
when a concrete deployment needs it, through independently tested integrations.

This is the maintained delivery plan, not a list of supported features. The
baseline below was reviewed against `main` at `73c6ac6` on 2026-09-16. The
package declares version `0.1.0` and is pre-1.0; that is not evidence of a
published release. No milestone below is complete or assigned yet, and there
are no delivery-date commitments. Owners and estimates are agreed when work
is taken up, not inferred from this document.

## Current Baseline

| Area | Implemented | Boundary or remaining gap |
| --- | --- | --- |
| Workflows | Typed YAML/JSON configuration; training, tuning, evaluation, explanations and batch prediction | Finite numeric features; no integrated categorical preprocessing or time/group-aware validation workflow |
| Evaluation | Seeded holdout, training-only cross-validation, accuracy/precision/recall/F1 | Promotion uses stored accuracy; no required independent evaluation report or incumbent comparison |
| Persistence | Immutable snapshots, checksums, local writer locking, atomic JSON metadata, promotion and rollback history | Absolute artifact paths; trusted pickle; no versioned migration contract or distributed coordination |
| Reproducibility | Resolved configurations, seeds, dataset fingerprints and local run records | No per-artifact code/runtime compatibility manifest |
| Serving | FastAPI prediction, schema validation, liveness and readiness | One model loaded at startup; no built-in authentication, telemetry or deployment runbook |
| Delivery | Linux/Windows tests, 85% branch-aware coverage gate, wheel checks and train/serve container smoke tests | No automated Python package publication; repository settings and operational guarantees need separate verification |

The small [synthetic dataset](../data/README.md) exercises the workflow. Its
scores, including evaluation on the full example table, are not evidence of
generalization. See [architecture](architecture.md), [workflows](workflows.md)
and [security](../SECURITY.md) for current contracts and limitations.

## Milestone Order

Priority indicates delivery order, not a security severity. P0 establishes
correctness and release discipline; P1 enables team deployment; P2 extends
operations after those foundations have evidence.

| ID | Milestone | Priority | State | Prerequisites |
| --- | --- | --- | --- | --- |
| M1 | Portable, reproducible artifacts | P0 | Planned | Current baseline |
| M2 | Defensible model evaluation | P0 | Planned | M1-01 manifest contract; evaluation design can start now |
| M3 | Optional remote integrations | P1 | Planned | M1; M2-03 for remote promotion parity |
| M4 | Operable serving | P1 | Planned | M1 and M2; M3 only for a remote-backed deployment |
| M5 | Monitoring and retraining | P2 | Planned | M2 and M4; M3 only for remote storage/tracking |
| M6 | Release and maintenance readiness | P0 | Planned | Start repository controls now; complete release gates after M1, M2 and M4 |

M3 and M4 can run in parallel using the local backend for serving. M6 is a
cross-cutting track, not a final cleanup phase. Remote infrastructure and
automated monitoring are not prerequisites for a local-core 1.0 release.

## Next-Work Queue

These are the first issue-sized tasks, not an assertion that work has started.
Use the stable IDs below in issues and PRs; create an issue and agree its scope
before implementation. Every item is currently unassigned.

| Order | Task | First deliverable | Ready when |
| --- | --- | --- | --- |
| 1 | M1-01 | Artifact/registry manifest proposal, legacy fixtures and compatibility policy | Ready for design |
| 2 | M1-02 | Relocation test, portable reference format and migration command design | M1-01 format agreed |
| 3 | M2-01 | Leakage-focused fixtures and split/preprocessing configuration proposal | Ready for design; persistence follows M1-01 |
| 4 | M2-02 | Independent evaluation report schema and example data partitions | Split contract in M2-01 agreed |
| 5 | M6-01 | Required-check inventory and repository-settings verification record | Ready; can run alongside items 1-4 |

Finish a small, tested deliverable before expanding an integration. Broader
tasks below can be split into child issues without changing their roadmap ID.

## M1: Portable, Reproducible Artifacts

**Outcome:** a trusted model can be moved, restored and resolved without editing
registry JSON, with an explicit compatibility decision before deserialization.

- [ ] **M1-01: Version the persistence contract.** Define artifact and registry
  schema versions. Record package/Python/library versions, source revision when
  available, dirty/unknown source state, configuration and data fingerprints,
  feature schema and seed. Keep a readable manifest outside the pickle payload.
  Specify supported load combinations and explicit rejection of unknown formats.
- [ ] **M1-02: Make references portable.** Resolve local snapshot references
  relative to the registry root. Provide a backed-up, repeatable migration from
  existing absolute paths, reject path traversal and document external-file
  imports. Preserve model IDs, checksums, aliases and rollback history.
- [ ] **M1-03: Prove recovery and replay.** Add backup/restore guidance and
  process-level interruption/concurrent-writer tests. Record enough provenance
  to reproduce predictions and metrics in the same locked environment; document
  tolerances and do not promise byte-identical pickle files across runtimes.

**Exit evidence:** Linux and Windows tests train two versions, promote both,
copy the registry to a different root, remove the original, predict and roll
back successfully. Legacy migration is repeatable; unsupported versions and
corrupt artifacts fail with actionable errors before loading. Interrupted writes
leave either a valid state or a documented, tested recovery path. Pickle still
requires a trusted publisher; a checksum is not authentication.

## M2: Defensible Model Evaluation

**Outcome:** model selection and promotion use traceable evidence without data
leakage, including cases where accuracy alone is misleading.

- [ ] **M2-01: Integrate preprocessing and split strategies.** Persist a
  scikit-learn pipeline for numeric/categorical features and explicit missing
  value policies. Fit transformations inside training folds only. Add configured
  stratified, chronological and group-aware splits with recorded assignments;
  reject impossible splits instead of silently changing the requested strategy.
- [ ] **M2-02: Produce independent evaluation reports.** Separate train,
  validation and final evaluation examples. Record model/data/split identifiers,
  sample counts, class distribution, confusion matrix and per-class metrics.
  Define positive-label and averaging behavior for binary/multiclass metrics.
  Flag reused or overlapping evaluation data where detectable and document the
  limits of detecting overlap without stable sample identifiers.
- [ ] **M2-03: Gate promotion on evidence.** Select named metrics and thresholds,
  compare a candidate with the incumbent on the same evaluation dataset, and
  record the report, decision and reason. Reject missing/non-finite metrics,
  mismatched model or dataset identities and failed gates without changing the
  alias. Keep manual approval distinct from an automated metric pass.

**Exit evidence:** regression tests catch fold leakage, group overlap and future
rows entering temporal training. Imbalanced and multiclass fixtures exercise
metric semantics. An end-to-end test trains two candidates, evaluates them on
an untouched partition, rejects a failing candidate, promotes an approved one
and rolls back with the evidence retained. Existing numeric workflows retain
coverage or have explicit migration notes.

## M3: Optional Remote Integrations

**Outcome:** a team can use shared infrastructure without changing job logic
or requiring cloud credentials to run the local quickstart.

- [ ] **M3-01: Define backend contracts.** Separate artifact storage, run tracking
  and registry responsibilities at the existing `io` boundary. Document identity,
  error, retry, idempotency and promotion-concurrency semantics. Run a common
  contract suite against the local backend before adding remote implementations.
- [ ] **M3-02: Add one object-storage adapter.** Select a provider in an issue
  based on a real deployment requirement. Support portable references, verified
  downloads and interrupted-upload handling. Define retention with dry-run and
  protection for active and rollback-referenced versions; never delete by default.
- [ ] **M3-03: Add one tracking/registry integration.** Select a backend with a
  documented decision, preserve run and evaluation lineage, and test promotion
  conflicts. Ship dependencies as extras, use external secret configuration and
  redact credentials from logs and stored configuration.

**Exit evidence:** contract tests cover authentication failure, timeout, retry,
missing/corrupt objects and concurrent promotion. A service-backed integration
job verifies behavior beyond mocks, with protected credentials where required.
The core test suite and quickstart still work without a network service or
optional dependencies. Document supported backend versions and failure modes.

## M4: Operable Serving

**Outcome:** deploy and roll back a pinned model with documented security
boundaries, observable behavior and measured capacity.

- [ ] **M4-01: Deliver a secured deployment example.** Choose one deployment
  target and provide authentication/TLS at the ingress, external secret handling,
  request-size/time limits and least-privilege artifact access. Keep non-root
  containers and read-only model mounts. Do not expose an unauthenticated API
  as the production example.
- [ ] **M4-02: Add service telemetry.** Emit structured request/error logs,
  correlation IDs, model-version identity and request count/latency/error metrics.
  Keep labels bounded and omit raw feature values and credentials by default.
  Protect diagnostic endpoints and document liveness versus readiness behavior.
- [ ] **M4-03: Rehearse deployment and rollback.** Pin a model version per
  deployment, drain in-flight requests on shutdown and document restart-based
  updates. Define latency/error/capacity targets for a stated model, payload,
  hardware and concurrency before measuring them. Add an incident runbook.

**Exit evidence:** deployment tests reject unauthenticated traffic, exercise
request limits and readiness failures, and verify telemetry without sensitive
payloads. A reproducible load report meets the declared targets. A recorded
rollout/rollback drill restores the previous model and includes recovery time.
Container smoke tests alone are not an operational readiness claim.

## M5: Monitoring and Retraining

**Outcome:** detect meaningful data changes and evaluate replacement models
without treating drift as permission to replace a deployed model.

- [ ] **M5-01: Establish monitoring inputs.** Version reference datasets and
  feature summaries; define collection windows, sample-size requirements, data
  retention and optional delayed-label joins. Keep request-payload collection
  disabled unless the adopting team explicitly configures it.
- [ ] **M5-02: Report data and model changes.** Add schema, missingness and
  distribution checks with configured thresholds and tested alert routing.
  Measure model quality only when labels exist; label-free drift reports must
  not claim an observed accuracy drop.
- [ ] **M5-03: Build an approval-gated retraining example.** Create traceable
  candidate runs from a schedule or alert, prevent duplicate/concurrent triggers
  and cap retries/resource use. Apply M2 evaluation gates and require explicit
  approval before promotion, retaining the incumbent for rollback.

**Exit evidence:** stationary, shifted, undersized and unlabeled fixtures produce
the expected reports without spurious quality claims. An integration scenario
triggers retraining once, rejects a degraded candidate, leaves the live model
unchanged without approval and verifies rollback after an approved replacement.

## M6: Release and Maintenance Readiness

**Outcome:** maintainers can verify repository controls and publish, validate
and recover a release using a documented process.

- [ ] **M6-01: Verify repository controls.** Inventory required checks, configure
  the applicable branch rules/review policy, and verify vulnerability reporting
  and dependency-update handling. Record actual settings and plan limitations;
  repository files do not prove that GitHub controls are enabled.
- [ ] **M6-02: Automate trusted distribution.** Agree the publication destination
  and configure protected release approval and short-lived/trusted publishing
  credentials where supported. Validate tag/version agreement, build once,
  promote the tested artifacts and attach checksums, provenance and an SBOM.
  Rehearse package installation and container startup from published artifacts.
- [ ] **M6-03: Establish the maintenance contract.** Document supported Python,
  dependency and artifact versions, deprecation/migration rules, security triage
  ownership and release/rollback responsibilities. Exercise a release candidate
  from a clean clone and record upgrade, restore and failed-release procedures.

**Exit evidence:** maintainer verification records link to the configured
controls; a release rehearsal supplies workflow and artifact evidence plus a
fresh-environment install test. Secrets are absent from logs/artifacts, required
approvals cannot be bypassed by the normal publishing path, and the release
checklist has named maintainers. No production-readiness claim is made solely
because tests or a tag build passed.

## Release Gates

Milestones organize work, not version numbers. Assign a version and scope only
when maintainers select a release; use the [release process](releases.md).

- Every release requires green required CI checks, reviewed migration notes,
  an updated changelog and successful installed-package/container validation.
- A local-core **1.0 candidate** additionally requires M1, M2, M4 and M6 exit
  evidence, a documented public CLI/config/API/artifact compatibility policy,
  and no unresolved release-blocking correctness or security issues. Record
  the release-blocker triage decision rather than relying on an empty issue list.
- M3 and M5 are optional tracks for that candidate. Ship an adapter or monitoring
  integration as supported only after its own exit evidence is complete; label
  incomplete experiments explicitly and keep them outside default dependencies.

## Tracking and Review

Use `Planned`, `In progress`, `Blocked`, `Done` or `Deferred` consistently.
Planned means scoped but uncommitted; In progress requires an assigned issue;
Blocked requires a linked dependency and next action; Deferred records why and
when to reconsider. Check a task only when its definition of done is satisfied.
Mark a milestone Done only when all tasks and its exit evidence are complete.

For each task, the tracking issue must contain its roadmap ID, one accountable
owner, scope/non-goals, dependencies, acceptance tests and links to implementing
PRs. The owner updates status and evidence in the same PR that changes progress.
Split work into child issues when needed; an open PR is not completed work.
At initial publication, tasks have no assigned owners or linked delivery issues.

Definition of done:

1. Code changes are merged and applicable acceptance tests pass in CI;
   non-code changes have the verification evidence described below.
2. Relevant failure paths and integration contracts have regression coverage;
   the existing 85% branch-aware coverage floor is preserved.
3. User docs, examples, security implications and migration/changelog entries
   match the delivered behavior.
4. The issue links verifiable evidence for non-code work such as GitHub settings,
   deployment drills or publication rehearsals; no credentials are included.
5. A maintainer accepts the evidence and updates this roadmap's status.

Maintainers review the next-work queue at each release-planning checkpoint and
when a dependency or security finding changes priorities. Review monthly while
delivery is active; record the review date and decisions in the roadmap PR.
Keep incomplete items visible instead of resetting them to a new wishlist.

## Scope and Risks

- Artifact portability and schema changes require migration tests and backups;
  do not silently invalidate existing registries.
- Preprocessing and validation can change reported scores. Leakage tests and
  independent evaluation take priority over adding more algorithms.
- Remote services add cost, credentials and failure modes. Select one concrete
  backend per need and keep contract tests and a usable local path.
- Authentication/TLS, secrets, retention and operational targets depend on the
  adopting organization. Examples must make those responsibilities explicit.
- Deep-learning workflows, LLM serving, a feature store, a web dashboard,
  multi-cloud parity, an orchestration platform and autonomous production
  promotion are outside this plan. The optional PyTorch dependency does not
  imply a supported deep-learning workflow.
