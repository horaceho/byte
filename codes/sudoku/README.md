# Sudoku Project

## Overview
A collection of utilities for generating, solving, rating, and testing Sudoku puzzles.

## Project Structure
```
sudoku/
├── README.md              # This file
├── utilities/
│   ├── sudoku-make.py     # Puzzle generator
│   ├── sudoku-solve.py    # Puzzle solver
│   ├── sudoku-rate.py     # Difficulty rater
│   └── sudoku-test.py     # Batch tester
```

## Quick Start

Generate a puzzle:
```bash
python utilities/sudoku-make.py -d 3 -s 42
```

Rate a puzzle:
```bash
python utilities/sudoku-make.py -d 3 -s 42 | python utilities/sudoku-rate.py
```

Solve a puzzle:
```bash
python utilities/sudoku-make.py -d 3 -s 42 | python utilities/sudoku-solve.py
```

Batch test uniqueness (100 by default):
```bash
python utilities/sudoku-test.py -c 100
```

## Usage Details

### sudoku-make.py
- `-d LEVEL` — Difficulty 1 (easy) … 5 (hell)
- `-s SEED` — 0 … 2^32−1 for reproducibility
- `-v` — Print separators and metadata to stderr; default stdout is a clean 9-row grid (space-separated, no separators)

### sudoku-solve.py
- Reads puzzle from stdin or a filename
- Default stdout: 9 rows (space-separated) + `Solutions: 1` or `Solutions: Many`
- `-v` — Print grid and extra diagnostics to stderr

### sudoku-rate.py
- Reads puzzle from stdin or a filename
- Default stdout: 9 rows + `Rating: <1..5>`
- `-v` — Print grid and metadata to stderr

### sudoku-test.py
- `-c N` — Run N random tests (default 100)
- Prints per-test lines; summary on stderr
- Uses subprocesses with `sys.executable` for reliable invocation

## Notes
- Default output is designed for piping (no separators, space-separated digits).
- Use `-v` when you need human-readable grids or debugging details.
- All utilities validate input and report errors to stderr with non-zero exit codes.
- Prefer explicit paths and `sys.executable` when invoking utilities from subprocesses to avoid stalls and ensure correctness.