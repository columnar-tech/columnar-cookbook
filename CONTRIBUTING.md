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

2. Build the website:

    ```sh
    pixi run build
    ```

3. Serve the website to [localhost:8000](http://localhost:8000/):

    ```sh
    pixi run serve
    ```

## Code Quality

This repository uses automated tools to maintain code quality:

- [Ruff](https://docs.astral.sh/ruff/): Python linting and formatting
- [ty](https://docs.astral.sh/ty/): Python type checking
- [nbformat](https://nbformat.readthedocs.io/): Jupyter notebook validation
- [nbconvert](https://nbconvert.readthedocs.io/): Jupyter notebook execution

### Before Commiting

1. Run formatting, linting, type checking, and validation:

    ```sh
    pixi run format
    pixi run lint
    pixi run check-types
    pixi run validate
    ```

2. Test notebook execution:

    ```sh
    pixi run jupyter nbconvert \
    --to notebook \
    --execute notebooks/duckdb.ipynb \
    --output test_output.ipynb
    ```
