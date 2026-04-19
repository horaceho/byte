# Byte — AI Agent Project Home

This directory holds agent-specific artifacts (memory, skills, logs). Do not store task progress or temporary state here; use `~/AI/Byte/codes/sudoku/` for reproducible project artifacts.

## Sudoku utilities (sudoku/)
- Location: `~/AI/Byte/codes/sudoku/`
- Quick pipeline:
  - Generate: `python utilities/sudoku-make.py -d 3 -s 42`
  - Rate: `python utilities/sudoku-make.py -d 3 -s 42 | python utilities/sudoku-rate.py`
  - Solve: `python utilities/sudoku-make.py -d 3 -s 42 | python utilities/sudoku-solve.py`
  - Batch test: `python utilities/sudoku-test.py -c 100`
- Details and options are in `~/AI/Byte/codes/sudoku/README.md`.
- Notes:
  - Default outputs are pipe-friendly (no separators, space-separated digits).
  - Use `-v` to emit human-readable grids and diagnostics to stderr.
  - Prefer `sys.executable` and explicit paths when invoking utilities from subprocesses for reliability.

## Project notes
- Agent memory/skills live in this repo root (`memory/`, `skills/`, `SOUL.md`).
- Task-specific code and data (e.g., Sudoku) live under `codes/` to keep the workspace organized.