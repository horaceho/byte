#!/usr/bin/env python3
"""
sudoku-solve.py - Solve Sudoku puzzles and check solution uniqueness.

Input:
    - Via pipe: cat puzzle.txt | python sudoku-solve.py
    - Via file: python sudoku-solve.py puzzle.txt [-v]

Output:
    The puzzle printed in canonical text form followed by:
        Solutions: 1
    or:
        Solutions: Many

    With -v/--verbose: separators and extra details are printed.
"""

import argparse
import copy
import re
import sys

N = 9
BOX = 3

def parse_board(lines, verbose):
    """Parse 9 data lines into a 9x9 int matrix.
       Accepts digits 1-9 and '.' or '0' for empty cells.
       Skips separator lines and removes all whitespace.
    """
    board = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Skip separator lines
        if '+' in line or '-------' in line:
            if verbose:
                sys.stderr.write(line + '\n')
            continue
        # Remove all whitespace/pipes, keep only digits/dots
        cleaned = re.sub(r'[|\s]', '', line)
        cleaned = re.sub(r'[^0-9.]', '', cleaned)
        row = [int(ch) if ch in "123456789" else 0 for ch in cleaned]
        if len(row) != N:
            raise ValueError(f"Expected {N} columns, got {len(row)}.")
        board.append(row)
        if len(board) == N:
            break
    if len(board) != N:
        raise ValueError(f"Expected {N} rows, got {len(board)}.")
    return board

def format_board(board):
    """Return canonical text representation (with separators)."""
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

def valid(board, row, col, num):
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

def main():
    parser = argparse.ArgumentParser(description="Solve Sudoku puzzles.")
    parser.add_argument("filename", nargs="?", type=argparse.FileType("r"), default=None,
                        help="File containing the puzzle (9 rows of 9 chars each).")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Print separators and extra details.")
    args = parser.parse_args()

    if args.filename is not None:
        lines = args.filename.readlines()
    else:
        data = sys.stdin.read().strip().splitlines()
        lines = [ln for ln in data if ln.strip()]

    try:
        board = parse_board(lines, args.verbose)
    except ValueError as e:
        print(f"Error parsing puzzle: {e}", file=sys.stderr)
        sys.exit(1)

    if args.verbose:
        print(format_board(board), file=sys.stderr)
    else:
        # Compact format: plain 9 rows, space-separated
        for row in board:
            print(" ".join(str(x) for x in row))

    if not has_unique_solution(board):
        print("Warning: Puzzle may not have a unique solution.", file=sys.stderr)

    cnt = [0]
    b = copy.deepcopy(board)

    def _solve():
        for r in range(N):
            for c in range(N):
                if b[r][c] == 0:
                    for num in range(1, N + 1):
                        if valid(b, r, c, num):
                            b[r][c] = num
                            if _solve():
                                cnt[0] += 1
                                if cnt[0] >= 2:
                                    return True
                            b[r][c] = 0
                    return False
        return True

    _solve()

    if args.verbose:
        if cnt[0] == 1:
            print("Solutions: 1", file=sys.stderr)
        else:
            print("Solutions: Many", file=sys.stderr)
    else:
        if cnt[0] == 1:
            print("Solutions: 1")
        else:
            print("Solutions: Many")

def has_unique_solution(board):
    cnt = [0]
    b = copy.deepcopy(board)

    def _solve():
        for r in range(N):
            for c in range(N):
                if b[r][c] == 0:
                    for num in range(1, N + 1):
                        if valid(b, r, c, num):
                            b[r][c] = num
                            _solve()
                            b[r][c] = 0
                            if cnt[0] >= 2:
                                return True
                    return False
        cnt[0] += 1
        return True

    _solve()
    return cnt[0] == 1

if __name__ == "__main__":
    main()