# MLOps Starter Kit

A Python template for numeric classification projects, from validated job
configuration to versioned models and a prediction API. Start locally without
cloud credentials, then adapt the workflow to your data and deployment needs.

**Python 3.10-3.14 | Poetry 2.2.1 | MIT license | Pre-1.0**

## Start a Project

Follow the [quickstart](quickstart.md) to train a model on the included synthetic
dataset, evaluate it and write batch predictions. The
[prediction API guide](serving.md) covers local serving and Docker.

## Workflow Reference

| Task | Guide |
| --- | --- |
| Configure a job or validate a YAML/JSON file | [Configuration](configuration.md) |
| Train, tune, evaluate and explain a classifier | [Workflows](workflows.md#train-and-compare) |
| Promote a version or restore its predecessor | [Promotion and rollback](workflows.md#promote-and-roll-back) |
| Produce schema-checked predictions | [Batch inference](workflows.md#batch-inference) |
| Understand artifact integrity and module boundaries | [Architecture](architecture.md) |
| Plan a contribution or a release | [Roadmap](roadmap.md) and [releases](releases.md) |

## Scope and Trust

This is a local reference implementation, not a complete production platform.
Features must be finite numeric values; model artifacts use trusted pickle;
registry coordination is limited to a local filesystem. The service has no
built-in authentication or TLS. Read the [security policy](security.md) before
exposing it outside a trusted environment.

Synthetic example scores demonstrate workflow behavior, not real-world model
quality. Remote infrastructure, stronger evaluation gates and operational
integrations remain [planned work](roadmap.md#milestone-order).
