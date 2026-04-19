#!/usr/bin/env python3
"""
sudoku-test.py - Test puzzle uniqueness at scale.

Usage:
    python sudoku-test.py -c 100

Default test count is 100. Each test:
- runs sudoku-make.py with a random seed/difficulty
- pipes the result into sudoku-solve.py to count solutions
- prints: seed:<s> difficulty:<d> solution:<1|many>
"""

import argparse
import random
import subprocess
import sys

N = 9

def run_one(seed, difficulty, base_dir):
    """Generate a puzzle with given seed/difficulty and count solutions."""
    cmd_gen = [sys.executable, f"{base_dir}/utilities/sudoku-make.py",
               "-d", str(difficulty), "-s", str(seed)]
    cmd_solve = [sys.executable, f"{base_dir}/utilities/sudoku-solve.py"]

    try:
        gen = subprocess.run(cmd_gen, capture_output=True, text=True, check=False)
        if gen.returncode != 0:
            return None  # generation failed
        solve = subprocess.run(cmd_solve, input=gen.stdout, capture_output=True, text=True, check=False)
        if solve.returncode != 0:
            return None  # solve failed

        # Parse solution line from sudoku-solve.py output
        for line in solve.stdout.strip().splitlines():
            line = line.strip()
            if line.lower().startswith("solutions:"):
                sol = line.split(":", 1)[1].strip()
                return sol

        # fallback
        return "unknown"
    except Exception:
        return None

def main():
    parser = argparse.ArgumentParser(description="Test Sudoku puzzle uniqueness across many seeds.")
    parser.add_argument("-c", "--count", type=int, default=100,
                        help="Number of tests to run (default: 100)")
    args = parser.parse_args()

    if args.count <= 0:
        print("Error: count must be > 0", file=sys.stderr)
        sys.exit(1)

    base_dir = ".."
    rng = random.Random()
    ok = 0
    any_fail = False

    print(f"Running {args.count} tests...", file=sys.stderr)

    for _ in range(args.count):
        seed = rng.randrange(0, 2**32)
        difficulty = rng.randrange(1, 6)
        sol = run_one(seed, difficulty, base_dir)
        if sol is None:
            print(f"seed:{seed} difficulty:{difficulty} solution:error", file=sys.stderr)
            any_fail = True
        else:
            print(f"seed:{seed} difficulty:{difficulty} solution:{sol}")
            if sol == "1":
                ok += 1

    print(f"\nSummary: {ok}/{args.count} unique solutions found.", file=sys.stderr)
    if any_fail:
        print("Some tests failed; review stderr for details.", file=sys.stderr)

if __name__ == "__main__":
    main()