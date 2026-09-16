# Roadmap

Build a dependable, reusable MLOps template for tabular classification, with a
credential-free local workflow and optional production integrations.

The [delivery plan](docs/roadmap.md) is the source of truth for task status,
dependencies and acceptance criteria. Implemented code is still pre-1.0;
planned capabilities below are not available yet.

## Delivery Order

| Milestone | Outcome |
| --- | --- |
| [M1: Portable, reproducible artifacts](docs/roadmap.md#m1-portable-reproducible-artifacts) | Move and restore models with explicit compatibility checks |
| [M2: Defensible model evaluation](docs/roadmap.md#m2-defensible-model-evaluation) | Prevent leakage and tie promotion to independent evidence |
| [M3: Optional remote integrations](docs/roadmap.md#m3-optional-remote-integrations) | Add tested storage and tracking adapters without cloud requirements for local use |
| [M4: Operable serving](docs/roadmap.md#m4-operable-serving) | Deploy behind authentication, observe failures and rehearse rollback |
| [M5: Monitoring and retraining](docs/roadmap.md#m5-monitoring-and-retraining) | Detect data changes and evaluate candidates with human approval |
| [M6: Release and maintenance readiness](docs/roadmap.md#m6-release-and-maintenance-readiness) | Establish verified repository controls and a repeatable release process |

M1 and M2 are the next delivery priorities. M3 and M4 can then progress in
parallel; M5 follows evaluation and serving. M6 starts alongside M1 rather
than waiting until the end. Milestones are dependency-driven, not dated promises.

## Start Here

- [Next-work queue](docs/roadmap.md#next-work-queue): small, ordered deliverables.
- [Current baseline](docs/roadmap.md#current-baseline): implemented behavior and limits.
- [Release gates](docs/roadmap.md#release-gates): evidence required before release.
- [Tracking and review](docs/roadmap.md#tracking-and-review): ownership and completion rules.

Pick a task ID and follow [CONTRIBUTING.md](CONTRIBUTING.md#roadmap-work).
