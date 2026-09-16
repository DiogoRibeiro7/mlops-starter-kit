"""Run the same quality checks locally as in CI, on any supported platform."""

from pathlib import Path
import subprocess
import sys


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    commands = [
        ["black", "--check", "src", "tests", "scripts"],
        ["flake8", "src", "tests", "scripts"],
        ["mypy"],
        ["pytest", "--cov", "--cov-report=term-missing"],
    ]
    for command in commands:
        subprocess.run([sys.executable, "-m", *command], cwd=root, check=True)


if __name__ == "__main__":
    main()
