"""Training entrypoint."""

from mlops_starter_kit.jobs.training import TrainingJob


def main(config_path: str = "confs/training.yaml") -> None:
    """Entry point for model training."""
    with TrainingJob.from_file(config_path) as job:
        job.run()


if __name__ == "__main__":
    main()
