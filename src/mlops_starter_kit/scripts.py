"""CLI with validation, machine-readable output and actionable errors."""

import argparse
import json
import logging
from pathlib import Path
import sys
from typing import Any, Sequence

from mlops_starter_kit.version import __version__
from mlops_starter_kit.io.artifacts import json_default
from mlops_starter_kit.io.configs import load_config_file
from mlops_starter_kit.jobs import (
    EvaluationsJob,
    ExplanationsJob,
    InferenceJob,
    Job,
    PromotionJob,
    RollbackJob,
    TrainingJob,
    TuningJob,
)

JOB_TYPES: dict[str, type[Job[Any]]] = {
    "training": TrainingJob,
    "tuning": TuningJob,
    "inference": InferenceJob,
    "evaluations": EvaluationsJob,
    "explanations": ExplanationsJob,
    "promotion": PromotionJob,
    "rollback": RollbackJob,
}


def schema() -> dict[str, Any]:
    return {
        "usage": "mlops-starter-kit CONFIG",
        "job_kinds": sorted(JOB_TYPES),
        "schemas": {
            kind: job.config_type.model_json_schema()
            for kind, job in JOB_TYPES.items()
        },
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a reproducible MLOps job"
    )
    parser.add_argument("config", nargs="?", default="confs/training.yaml")
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument(
        "--schema", action="store_true", help="Print job JSON schemas"
    )
    parser.add_argument(
        "--validate", action="store_true", help="Validate without running"
    )
    parser.add_argument(
        "--debug", action="store_true", help="Show tracebacks on failure"
    )
    return parser


def job_from_config(path: str | Path) -> Job[Any]:
    config = load_config_file(path)
    job_spec = config.get("job", {})
    if not isinstance(job_spec, dict):
        raise ValueError("job must be a mapping with a kind field")
    kind = job_spec.get("kind", Path(path).stem)
    if not isinstance(kind, str) or kind not in JOB_TYPES:
        raise ValueError(f"unsupported job kind: {kind}")
    return JOB_TYPES[kind](config)


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
    try:
        if args.schema:
            result = schema()
        else:
            job = job_from_config(args.config)
            if args.validate:
                result = job.config.model_dump(mode="json")
            else:
                with job:
                    result = job.run()
        print(
            json.dumps(result, indent=2, allow_nan=False, default=json_default)
        )
        return 0
    except (OSError, ValueError, TypeError) as exc:
        if args.debug:
            raise
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
