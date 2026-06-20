# AGENTS.md

## Cursor Cloud specific instructions

This is a Python 3.12 FastAPI + FastAPI-MCP service (a parking-lot lookup example).
It is managed with the [`uv`](https://docs.astral.sh/uv/) package manager. Standard
commands live in the `Makefile` and `README.md`; prefer those.

### Service overview
- Single service: `main.py` starts a Uvicorn server on `0.0.0.0:5000`.
  - REST docs (Swagger UI): `http://localhost:5000/docs`
  - MCP endpoint (SSE): `http://localhost:5000/mcp`
  - Endpoints: `POST /parking/nearby` and `POST /parking/info` (mock data, no external services or secrets needed).

### Run / lint / test
- Run dev server: `make dev` (equivalently `uv run python main.py`). It is NOT a hot-reload server; restart the process after code changes.
- Lint: `uv run ruff check .` and `uv run ruff format --check .` (the `make check` target also runs `uv lock --locked` and full `pre-commit`, which needs network to install hook envs).
- Tests: `make test` / `uv run python -m pytest`. There is currently no `tests/` directory, so pytest exits with code 5 ("no tests collected") — this is expected, not a failure.

### Non-obvious gotchas
- `pyproject.toml` declares a heavy, unused dependency `ttt-video` (git) that transitively pulls `torch`, `torchvision`, `xformers`, `triton`, `transformers`, etc. `uv sync` installs all of it (multi-GB), even though `main.py` never imports it. Do not be surprised by the large `.venv`.
- The app code uses Traditional Chinese strings; ensure UTF-8 output when inspecting responses.
