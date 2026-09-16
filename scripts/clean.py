"""Remove generated reports and build outputs, preserving model artifacts."""

from pathlib import Path
import shutil


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    for name in (".pytest_cache", ".mypy_cache", "htmlcov", "dist", "build"):
        target = root / name
        if target.is_symlink() or not target.resolve().is_relative_to(root):
            raise ValueError(
                f"refusing to clean outside the checkout: {target}"
            )
        if target.is_dir():
            shutil.rmtree(target)


if __name__ == "__main__":
    main()
