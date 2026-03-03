from pathlib import Path

import nbformat

ROOT = Path(__file__).parent.parent
NOTEBOOKS_DIR = ROOT / "notebooks"


def validate_notebooks() -> int:
    notebooks = sorted(NOTEBOOKS_DIR.glob("*.ipynb"))
    errors: list[tuple[Path, Exception]] = []

    print(f"Validating {len(notebooks)} notebooks")

    for path in notebooks:
        try:
            notebook = nbformat.read(path, as_version=4)
            nbformat.validate(notebook)
            print(f"OK: {path.relative_to(ROOT)}")
        except Exception as e:
            errors.append((path, e))
            print(f"FAIL: {path.relative_to(ROOT)}")

    if errors:
        print(f"Found {len(errors)} invalid notebook(s):")
        for path, error in errors:
            print(f"  {path.relative_to(ROOT)}: {error}")
        return 1

    print(f"All {len(notebooks)} notebooks valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(validate_notebooks())
