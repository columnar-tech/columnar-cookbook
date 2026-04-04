# Contributing

Thank you for your interest in contributing to Columnar Cookbook!

All contributors are expected to follow the [Code of Conduct](https://github.com/columnar-tech/columnar-cookbook?tab=coc-ov-file#readme).
Potential security vulnerabilities should be reported to security@columnar.tech.

## Development

### Prerequisites

- [Git](https://git-scm.com/) version control system
- [Pixi](https://pixi.prefix.dev/latest/) package manager

### Getting Started

1. Clone the repository:

    ```sh
    git clone https://github.com/columnar-tech/columnar-cookbook.git
    cd columnar-cookbook
    ```

2. Start a live-reloading development server on [localhost:8000](http://localhost:8000/):

    ```sh
    pixi run dev
    ```
    This will automatically build the website, watch for changes in the notebooks and templates, and refresh your browser as you work.

    **Alternatively**, to build and serve the website statically without watching for changes:

    ```sh
    pixi run build
    pixi run serve
    ```

## Adding a Recipe

### Create the Notebook

Place your notebook in the `notebooks/` directory with a descriptive kebab-case filename (e.g., `connect-to-mysql-with-adbc-in-python.ipynb`, `ingest-parquet-data-into-mariadb-with-adbc.ipynb`).
Start the notebook with an introductory Markdown cell that explains the topic, the tools used, and the requirements.
See the existing notebooks for reference.

### Register the Notebook

Add an entry to `registry.json` following the format of the existing entries.
Author IDs in your entry must match a key in `authors.json`.

### Add Yourself as an Author

If you are a first-time contributor, add an entry to `authors.json` following the format of the existing entries.

## Code Quality

This repository uses automated tools to maintain code quality:

- [Ruff](https://docs.astral.sh/ruff/): Python linting and formatting
- [ty](https://docs.astral.sh/ty/): Python type checking
- [nbformat](https://nbformat.readthedocs.io/): Jupyter notebook validation
- [nbconvert](https://nbconvert.readthedocs.io/): Jupyter notebook execution

### Before Committing

1. Run formatting, linting, type checking, and validation:

    ```sh
    pixi run format
    pixi run lint
    pixi run check-types
    pixi run validate
    ```

2. Test notebook execution (replace `<your-notebook>` with your notebook's filename):

    ```sh
    pixi run jupyter nbconvert \
    --to notebook \
    --execute notebooks/<your-notebook>.ipynb \
    --output test_output.ipynb
    ```

3. Clean up the test output (do not commit this file):

    ```sh
    rm notebooks/test_output.ipynb
    ```
