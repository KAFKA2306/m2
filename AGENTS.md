# Repository Guidelines

## Project Structure
- `src/`: Python code for data retrieval, analysis, helpers, and indicator configuration.
- `tests/`: pytest tests.
- Root scripts: `refactored_update_data.py` and `visualize_data.py`.
- `data.yml`: saved data used by the visualizations.
- `.github/workflows/update.yml`: saved-data update.
- `.github/workflows/pages.yml`: tests, visualization build, and GitHub Pages publication.

## Commands
- Install dependencies: `python -m pip install -r requirements.txt`
- Run tests: `pytest -q`
- Update data: `python refactored_update_data.py`
- Rebuild historical data: `python refactored_update_data.py --backfill`
- Generate visualizations: `python visualize_data.py`

## Implementation
- Prefer the existing data retrieval and visualization modules over new wrappers.
- Keep indicator configuration in `src/config/indicators.yml`.
- Use standard Python naming and type hints where practical.
- Do not add overlapping formatters, linters, task runners, packaging manifests, or data-update entry points without a concrete need.

## Verification
- Keep tests under `tests/` with names matching `test_*.py`.
- Add focused tests when changing data retrieval, parsing, transforms, or fallback behavior.
- Do not weaken tests or CI to make a change pass.
- Do not present fixed correlations, interpretations, or data freshness as current facts without verifying the data and period.

## Security
- Do not commit secrets. Use environment variables when an external API requires credentials.
- When changing paths or entry points, update all corresponding GitHub Actions references.

## Data flow
Data retrieval → `data.yml` → `visualize_data.py` → GitHub Pages.

## Outcome-first task interpretation (Altitude / Depth / Range / Speed)

- **Altitude:** Interpret a task as a verifiable user outcome, not only the named intermediate step. Infer the smallest justified acceptance criteria from the request and current repository state; do not silently expand scope or override explicit instructions.
- **Depth:** Use primary/current evidence and real domain tools and methods. Verify the actual postcondition independently of agent self-report, preferably on the exact changed revision or target runtime.
- **Range:** Combine code, data, tests, runtime/UI, and domain expertise when that materially improves the outcome, while respecting canonical owners and avoiding duplicate systems.
- **Speed:** Complete authorized read-only and reversible work through implementation, focused checks, and read-back without unnecessary approval loops. Bound retries and stop at the proven outcome.
- These principles never bypass repository-specific security, privacy, permission, publication, spending, destructive-action, or release boundaries. State verified results and any remaining `UNVERIFIED` layers.
