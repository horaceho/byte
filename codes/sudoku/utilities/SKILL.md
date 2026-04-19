# Sudoku Utilities Skill

## Purpose
Reusable procedures for the Sudoku project utilities (`sudoku-make.py`, `sudoku-rate.py`, `sudoku-solve.py`, `sudoku-test.py`).

## Skill Conventions
- Use `sys.executable` when invoking sub-tools via subprocess to ensure the correct Python interpreter.
- Prefer explicit paths over relative paths when calling utilities from scripts.
- Capture `stderr` and `stdout` separately when chaining subprocesses to avoid stream stalls.
- Use `check=False` and inspect `returncode` rather than `check=True` for pipeline robustness.
- All utility output intended for human consumption should go to `stdout`; diagnostics/metadata go to `stderr`.
- The generator’s default (no `-v`) prints only the 9-row grid to `stdout`.
- The solver’s default prints only the grid and `Solutions:` line to `stdout`.
- The rate tool’s default prints only the grid and `Rating:` line to `stdout`.

## Key Workflows

### Generate → Rate → Solve → Test
1. Generate: `python utilities/sudoku-make.py [-d LEVEL] [-s SEED] [-v]`
2. Rate: `python utilities/sudoku-rate.py [-v]`
3. Solve: `python utilities/sudoku-solve.py [-v]`
4. Test at scale: `python utilities/sudoku-test.py -c [N]`

### Subprocess Safety (avoid stalls)
- When piping generator output directly to solver, use `stderr=subprocess.PIPE` and read `stdout` after completion:
  ```python
  gen = subprocess.run(cmd_gen, capture_output=True, text=True, check=False)
  solve = subprocess.run(cmd_solve, input=gen.stdout, capture_output=True, text=True, check=False)
  ```
- Never rely on interactive reads while the child writes to the same pipe; capture all output.

## Common Pitfalls & Fixes
- `Solution: error` in tests usually means subprocess path issues; always use `sys.executable` and explicit paths.
- Stream stalls occur when stdout/stderr are not fully consumed; use `capture_output=True` and read both streams.
- If verbose mode prints to stderr, ensure parsing logic does not expect those lines on stdout.

## Maintenance Notes
- Keep argument parsers consistent across utilities (shared flags: `-d`, `-s`, `-v`).
- When modifying output format, update all dependent parsers accordingly.
- Prefer compact 9-row default output for piping; reserve verbose details for stderr.