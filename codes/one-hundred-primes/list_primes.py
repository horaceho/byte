#!/usr/bin/env python3
"""List the first 100 prime numbers."""

def first_n_primes(n: int):
    primes = []
    candidate = 2
    while len(primes) < n:
        is_prime = all(candidate % p != 0 for p in primes)
        if is_prime:
            primes.append(candidate)
        candidate += 1
    return primes

if __name__ == "__main__":
    for i, p in enumerate(first_n_primes(100), start=1):
        print(f"{i:3d}. {p}")
