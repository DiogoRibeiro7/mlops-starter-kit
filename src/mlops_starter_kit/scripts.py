"""Command line entrypoint for starter jobs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from mlops_starter_kit.io.configs import load_config_file
from mlops_starter_kit.jobs import (
    EvaluationsJob,
    ExplanationsJob,
    InferenceJob,
    PromotionJob,
    RollbackJob,
    TrainingJob,
    TuningJob,
)

JOB_TYPES = {
    "training": TrainingJob,
    "tuning": TuningJob,
    "inference": InferenceJob,
    "evaluations": EvaluationsJob,
    "explanations": ExplanationsJob,
    "promotion": PromotionJob,
    "rollback": RollbackJob,
}


def schema() -> dict[str, object]:
    """Return a compact CLI schema."""
    return {
        "usage": "mlops-starter-kit CONFIG",
        "job_kinds": sorted(JOB_TYPES),
        "config": {"job": {"kind": "training"}},
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run an MLOps starter-kit job"
    )
    parser.add_argument(
        "config",
        nargs="?",
        default="confs/training.yaml",
        help="Path to a job config",
    )
    parser.add_argument(
        "--schema",
        action="store_true",
        help="Print the starter job schema and exit",
    )
    return parser


def job_from_config(path: str | Path):
    """Create a job instance from a config file."""
    config = load_config_file(path)
    kind = config.get("job", {}).get("kind", Path(path).stem)
    try:
        job_type = JOB_TYPES[str(kind)]
    except KeyError as exc:
        raise ValueError(f"unsupported job kind: {kind}") from exc
    return job_type(config)


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entrypoint."""
    args = build_parser().parse_args(argv)
    if args.schema:
        print(json.dumps(schema(), indent=2))
        return 0
    job = job_from_config(args.config)
    with job:
        result = job.run()
    print(
        json.dumps(
            {key: str(value) for key, value in result.items()}, indent=2
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
