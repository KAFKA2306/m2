# Repository Guidelines

## Project Structure & Module Organization
- `src/`: Python package code
  - `data/` (fetchers), `analysis/`, `visualization/`, `utils/`, `config/indicators.yml` (indicator definitions)
- `tests/`: Pytest suite (e.g., `test_data_fetcher.py`)
- Root scripts: `update_data.py`, `refactored_update_data.py`, `visualize_data.py`, `economic_ultrathink_dashboard.py`, `generate_dashboard_site.py`
- Artifacts: generated `.png` charts and `data.yml` (public cache)
- `dashboard/`: static site output for Pages

## Build, Test, and Development Commands
- Install (dev): `python -m pip install -e .[dev]`
- Run update: `python refactored_update_data.py` (add `--backfill` for 5y rebuild)
- Generate visuals: `python visualize_data.py` and `python economic_ultrathink_dashboard.py`
- Build site: `python generate_dashboard_site.py` (outputs to `dashboard/`)
- Tests: `pytest -q` (optionally `pytest --cov=src` if `pytest-cov` installed)

## Coding Style & Naming Conventions
- Python 3.8+; 4‑space indentation; UTF‑8
- Use type hints for public functions; docstrings with triple quotes
- Names: `snake_case` for modules/functions, `PascalCase` for classes, `UPPER_CASE` for constants
- Formatting: `black` (default line length 88)
- Linting: `flake8` before PR; static checks with `mypy` where practical

## Testing Guidelines
- Framework: `pytest`
- Location: `tests/` with files named `test_*.py`; mirror package structure when feasible
- Write focused unit tests for data fetching, parsing, and transforms; include edge cases and fallbacks
- Aim for coverage on touched code; prefer `pytest -q` locally before pushing

## Commit & Pull Request Guidelines
- Style: Conventional Commits (e.g., `feat:`, `fix:`, `docs:`, `ci:`, `chore:`); imperative mood, concise subject
- Link issues (`Fixes #123`) and describe changes, assumptions, and validation
- Include screenshots of updated charts/dashboards when visuals change
- PR checklist: tests pass; `black .` and `flake8` clean; no unrelated file churn; generated assets only where expected

## Security & Configuration Tips
- Indicators live in `src/config/indicators.yml`; keep categories and `display_scale` consistent
- Do not commit secrets; current FRED/Yahoo paths require none. If adding APIs, use environment variables
- Changing file paths may require updating GitHub Actions in `.github/workflows/`

## Architecture Overview
Data pipeline: fetch (FRED/Yahoo) → analyze (`src/analysis`) → visualize (`src/visualization`) → static site (`dashboard/`) deployed via GitHub Pages.

