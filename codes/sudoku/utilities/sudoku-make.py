#!/usr/bin/env python3
"""
sudoku-make.py - Generate Sudoku puzzles with configurable difficulty and seed.

Usage:
    python sudoku-make.py [-d LEVEL] [-s INTEGER] [-v]

Arguments:
    -d LEVEL      Difficulty level from 1 (easy) to 5 (hell difficult)
    -s INTEGER    Random seed (0 to 2^32-1) for reproducible puzzles
    -v            Print separators and metadata (to stderr)

Output:
    Default: 9-row grid without separators, suitable for piping.
    Verbose: separators and a comment line with seed/difficulty are printed.
"""

import argparse
import random
import sys

# ── Grid size ────────────────────────────
N = 9
BOX = 3

# ── Difficulty profile ────────────────────────────
DIFFICULTY_PROFILE = {
    1: 30,
    2: 35,
    3: 40,
    4: 48,
    5: 54,
}

def valid(board, row, col, num):
    """Return True if placing `num` at (row, col) is valid."""
    if num in board[row]:
        return False
    if num in (board[r][col] for r in range(N)):
        return False
    br, bc = (row // BOX) * BOX, (col // BOX) * BOX
    for r in range(br, br + BOX):
        for c in range(bc, bc + BOX):
            if board[r][c] == num:
                return False
    return True

def solve(board):
    """Backtracking solver. Returns True if a solution exists."""
    for r in range(N):
        for c in range(N):
            if board[r][c] == 0:
                for num in range(1, N + 1):
                    if valid(board, r, c, num):
                        board[r][c] = num
                        if solve(board):
                            return True
                        board[r][c] = 0
                return False
    return True

def count_solutions(board, limit=2):
    """Count solutions up to `limit`. Stops early if limit exceeded."""
    cnt = [0]

    def _backtrack():
        for r in range(N):
            for c in range(N):
                if board[r][c] == 0:
                    for num in range(1, N + 1):
                        if valid(board, r, c, num):
                            board[r][c] = num
                            _backtrack()
                            board[r][c] = 0
                            if cnt[0] >= limit:
                                return
                    return
        cnt[0] += 1

    _backtrack()
    return cnt[0]

def generate_full_grid():
    """Generate a complete, valid Sudoku grid."""
    board = [[0] * N for _ in range(N)]
    nums = list(range(1, N + 1))
    for box in range(BOX):
        start = box * BOX
        random.shuffle(nums)
        for i in range(BOX):
            for j in range(BOX):
                board[start + i][start + j] = nums[i * BOX + j]
    solve(board)
    return board

def remove_cells(board, n_removals):
    """Remove n_removals cells from a full grid, ensuring a unique solution."""
    cells = [(r, c) for r in range(N) for c in range(N)]
    random.shuffle(cells)

    removed = 0
    for (r, c) in cells:
        if removed >= n_removals:
            break
        backup = board[r][c]
        board[r][c] = 0

        import copy
        test_board = copy.deepcopy(board)
        if count_solutions(test_board, limit=2) == 1:
            removed += 1
        else:
            board[r][c] = backup

    return board

def format_board_with_separators(board):
    """Convert a 9x9 board into a human-readable string with separators."""
    lines = []
    line_sep = "+-------+-------+-------+"
    for r in range(N):
        if r % BOX == 0:
            lines.append(line_sep)
        row_str = ""
        for c in range(N):
            if c % BOX == 0:
                row_str += "| "
            val = board[r][c]
            row_str += (". " if val == 0 else f"{val} ")
        row_str += "|"
        lines.append(row_str)
    lines.append(line_sep)
    return "\n".join(lines)

def format_board_no_separators(board):
    """Convert a 9x9 board into a plain 9-line string (no separators)."""
    lines = []
    for r in range(N):
        row_str = ""
        for c in range(N):
            val = board[r][c]
            row_str += (". " if val == 0 else f"{val} ")
        lines.append(row_str.strip())
    return "\n".join(lines)

def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate a Sudoku puzzle in text format.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Difficulty 1=easy \u2026 5=hell; Seed must be a 32-bit unsigned integer."
    )
    parser.add_argument("-d", "--difficulty", type=int, default=3,
                        help="Difficulty level 1\u20135 (default: 3)")
    parser.add_argument("-s", "--seed", type=int, default=None,
                        help="Random seed (0 to 2^32-1) for reproducibility")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Print separators and metadata (to stderr)")

    return parser.parse_args()

def main():
    args = parse_args()

    if not (1 <= args.difficulty <= 5):
        print("Error: --difficulty must be between 1 and 5.", file=sys.stderr)
        sys.exit(1)

    seed = args.seed
    if seed is not None:
        if not (0 <= seed <= 0xFFFFFFFF):
            print("Error: --seed must be a 32-bit unsigned integer (0..4294967295).", file=sys.stderr)
            sys.exit(1)
    else:
        seed = random.randrange(0, 0xFFFFFFFF + 1)

    random.seed(seed)

    profile = DIFFICULTY_PROFILE[args.difficulty]
    full = generate_full_grid()
    puzzle = remove_cells(full, profile)

    if args.verbose:
        print(f"# Seed: {seed}  Difficulty: {args.difficulty}", file=sys.stderr)
        print(format_board_with_separators(puzzle), file=sys.stderr)
    else:
        # Plain 9-row output with spaces between numbers
        for row in puzzle:
            print(" ".join(str(x) for x in row))

if __name__ == "__main__":
    main()