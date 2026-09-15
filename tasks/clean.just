clean:
    python -c "import shutil, pathlib; [shutil.rmtree(p, ignore_errors=True) for p in ['.pytest_cache', 'htmlcov', 'dist', 'build']]; [p.unlink() for p in pathlib.Path('.').rglob('*.pyc')]"
