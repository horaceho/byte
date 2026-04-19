#!/usr/bin/env python3
"""
sudoku-rate.py - Rate the difficulty of a Sudoku puzzle.

Input:
    - Via pipe: cat puzzle.txt | python sudoku-rate.py
    - Via file: python sudoku-rate.py puzzle.txt [-v]

Output:
    Default: 9-line puzzle (space-separated digits) followed by:
        Rating: <1..5>
    With -v/--verbose: separators and extra details printed to stderr.
"""

import argparse
import copy
import re
import sys

N = 9
BOX = 3

# ── Difficulty profile ──
DIFFICULTY_PROFILE = {
    1: 30,
    2: 35,
    3: 40,
    4: 48,
    5: 54,
}

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
        if '+' in line or '-------' in line:
            if verbose:
                sys.stderr.write(line + '\n')
            continue
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
    """Return canonical 9-row puzzle (space-separated digits, no separators)."""
    lines = []
    for r in range(N):
        lines.append(" ".join(str(x) for x in board[r]))
    return "\n".join(lines)

def format_board_verbose(board):
    """Return puzzle with separators (for verbose stderr output)."""
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

def generate_full_grid():
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
    cells = [(r, c) for r in range(N) for c in range(N)]
    random.shuffle(cells)
    removed = 0
    for (r, c) in cells:
        if removed >= n_removals:
            break
        backup = board[r][c]
        board[r][c] = 0
        import copy
        test = copy.deepcopy(board)
        if count_solutions(test, limit=2) == 1:
            removed += 1
        else:
            board[r][c] = backup
    return board

def naked_single_steps(board):
    b = copy.deepcopy(board)
    steps = 0
    changed = True
    while changed:
        changed = False
        for r in range(N):
            for c in range(N):
                if b[r][c] == 0:
                    cands = [v for v in range(1, N + 1) if valid(b, r, c, v)]
                    if len(cands) == 1:
                        b[r][c] = cands[0]
                        steps += 1
                        changed = True
    return steps

def backtracks_without_ordering(board):
    b = copy.deepcopy(board)
    bt = [0]

    def _solve_no_order():
        for r in range(N):
            for c in range(N):
                if b[r][c] == 0:
                    for num in range(1, N + 1):
                        if valid(b, r, c, num):
                            b[r][c] = num
                            if _solve_no_order():
                                bt[0] += 1
                                return True
                            b[r][c] = 0
                    return False
        return True

    _solve_no_order()
    return bt[0]

def backtracks_with_ordering(board):
    b = copy.deepcopy(board)
    bt = [0]

    def _solve_ordered():
        rbest, cbest, candsbest, best = -1, -1, [], None
        for rr in range(N):
            for cc in range(N):
                if b[rr][cc] == 0:
                    cur = [v for v in range(1, N + 1) if valid(b, rr, cc, v)]
                    if best is None or len(cur) < len(best[2]):
                        rbest, cbest, candsbest, best = rr, cc, cur, (rr, cc, cur)
        if best is None:
            return True
        rr, cc, cands = best
        for num in cands:
            b[rr][cc] = num
            if _solve_ordered():
                return True
            b[rr][cc] = 0
            bt[0] += 1
        return False

    _solve_ordered()
    return bt[0]

def _possibles_for_cell(board, r, c):
    if board[r][c] != 0:
        return set()
    used = set()
    for i in range(N):
        used.add(board[r][i])
        used.add(board[i][c])
    br0, bc0 = (r // BOX) * BOX, (c // BOX) * BOX
    for i in range(br0, br0 + BOX):
        for j in range(bc0, bc0 + BOX):
            used.add(board[i][j])
    return {v for v in range(1, N + 1) if v not in used}

def _constrained_neighbors_score(board, r, c, num):
    score = 0
    for i in range(N):
        if board[r][i] == 0 and num in _possibles_for_cell(board, r, i):
            score += 1
        if board[i][c] == 0 and num in _possibles_for_cell(board, i, c):
            score += 1
    br0, bc0 = (r // BOX) * BOX, (c // BOX) * BOX
    for i in range(br0, br0 + BOX):
        for j in range(bc0, bc0 + BOX):
            if board[i][j] == 0 and num in _possibles_for_cell(board, i, j):
                score += 1
    return score

def rate_difficulty(board):
    empty = sum(1 for r in range(N) for c in range(N) if board[r][c] == 0)
    if empty >= 60:
        return 5, "Very few givens (>=60), requires advanced techniques."
    if empty >= 52:
        return 4, "Many empty cells (52-59); hard for beginners."
    if empty >= 46:
        return 3, "Moderate empty cells (46-51); intermediate level."
    if empty >= 40:
        return 2, "Fairly few blanks (40-45); relatively easy."
    return 1, "Many givens (<=39); straightforward to solve."

def main():
    parser = argparse.ArgumentParser(description="Rate Sudoku puzzle difficulty.")
    parser.add_argument("filename", nargs="?", type=argparse.FileType("r"), default=None,
                        help="File containing the puzzle (9 rows of 9 chars each).")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Print separators and additional details (to stderr).")
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
        print(format_board_verbose(board), file=sys.stderr)
    else:
        print(format_board(board))

    rating, reason = rate_difficulty(board)
    if args.verbose:
        empty = sum(1 for r in range(N) for c in range(N) if board[r][c] == 0)
        ns = naked_single_steps(board)
        bt_no = backtracks_without_ordering(board)
        bt_yes = backtracks_with_ordering(board)
        print(f"Empty cells: {empty}", file=sys.stderr)
        print(f"Naked-single placements: {ns}", file=sys.stderr)
        print(f"Backtracks (no ordering): {bt_no}", file=sys.stderr)
        print(f"Backtracks (with ordering): {bt_yes}", file=sys.stderr)
        print(f"Reason: {reason}", file=sys.stderr)

    print(f"Rating: {rating}")

if __name__ == "__main__":
    main()