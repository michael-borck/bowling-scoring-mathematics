#!/usr/bin/env python3
"""
Generalised bowling scoring: B(N, M, K)

N = number of frames
M = number of pins
K = bonus depth (0, 1, or 2)

Computes exact score distributions, state space sizes, and
summary statistics for the parametric family.
"""

import math
from collections import defaultdict


def omega(M):
    """Number of outcomes per standard frame with M pins."""
    return (M + 1) * (M + 2) // 2


def omega_terminal(M):
    """Number of outcomes for the terminal frame with M pins."""
    # Open: sum_{a=0}^{M-1} (M-a) = M(M+1)/2 ... wait
    # Open: first ball a in 0..M-1, second ball b in 0..M-a,
    #        with a+b < M. So b in 0..M-a-1: that's (M-a) choices.
    #        Total open = sum_{a=0}^{M-1} (M-a) = M(M+1)/2
    # Actually: open means a+b < M, so b in {0,...,M-a-1}, giving M-a choices.
    # sum_{a=0}^{M-1} (M - a) = sum_{j=1}^{M} j = M(M+1)/2
    n_open = M * (M + 1) // 2

    # Spare: a in 0..M-1, b = M-a (1 choice), third ball c in 0..M: M+1 choices
    # Total spare = M * 1 * (M+1) = M(M+1)
    n_spare = M * (M + 1)

    # Strike: first ball = M.
    # Second ball B in 0..M.
    # If B = M (another strike): third ball C in 0..M: M+1 choices
    # If B < M: third ball C in 0..M-B: M-B+1 choices
    # Total = (M+1) + sum_{B=0}^{M-1}(M-B+1) = (M+1) + sum_{j=2}^{M+1} j
    #       = (M+1) + ((M+1)(M+2)/2 - 1) = (M+1) + (M+1)(M+2)/2 - 1
    n_strike = (M + 1)  # B=M case
    for B in range(M):
        n_strike += (M - B + 1)

    return n_open + n_spare + n_strike


def generalised_distribution(N, M, K):
    """
    Compute the exact score distribution for B(N, M, K).

    Returns dict mapping score -> count.
    """
    if K not in (0, 1, 2):
        raise ValueError("K must be 0, 1, or 2")

    if K == 0:
        return _distribution_k0(N, M)
    elif K == 1:
        return _distribution_k1(N, M)
    else:
        return _distribution_k2(N, M)


def _distribution_k0(N, M):
    """No bonuses: score = pinfall. Simple convolution."""
    dp = defaultdict(int)
    dp[0] = 1

    for frame_num in range(1, N + 1):
        new_dp = defaultdict(int)
        for score, count in dp.items():
            if frame_num < N:
                # Standard frame: strike (M) or two balls summing to <= M
                new_dp[score + M] += count  # strike
                for a in range(M):
                    for b in range(M - a + 1):
                        new_dp[score + a + b] += count
            else:
                # Terminal frame: same scoring, open/spare/strike
                # Open
                for a in range(M):
                    for b in range(M - a):
                        new_dp[score + a + b] += count
                # Spare: a + b = M, bonus ball c
                for a in range(M):
                    b = M - a
                    for c in range(M + 1):
                        new_dp[score + a + b + c] += count
                # Strike
                for b2 in range(M + 1):
                    if b2 == M:
                        for b3 in range(M + 1):
                            new_dp[score + M + b2 + b3] += count
                    else:
                        for b3 in range(M - b2 + 1):
                            new_dp[score + M + b2 + b3] += count
        dp = new_dp

    return dict(dp)


def _distribution_k1(N, M):
    """K=1: spare-depth bonuses only. State: (b1, score) where b1 in {0,1}."""
    dp = defaultdict(int)
    dp[(0, 0)] = 1  # (b1, score)

    for frame_num in range(1, N + 1):
        new_dp = defaultdict(int)
        for (b1, score), count in dp.items():
            if frame_num < N:
                # Strike: M pins, contributes M*(1+b1), sets new b1=1
                new_score = score + M * (1 + b1)
                new_dp[(1, new_score)] += count
                # Non-strike: two balls
                for a in range(M):
                    s1 = score + a * (1 + b1)
                    nb1 = 0  # shift: no b2 in K=1
                    for b in range(M - a + 1):
                        s2 = s1 + b * (1 + nb1)
                        if a + b == M:  # spare
                            new_dp[(1, s2)] += count
                        else:
                            new_dp[(0, s2)] += count
            else:
                # Terminal frame: consumes b1, no new bonuses
                # We need to handle all terminal frame cases
                # Strike on ball 1
                s1 = score + M * (1 + b1)
                for p2 in range(M + 1):
                    s2 = s1 + p2  # no bonus on ball 2 in terminal
                    if p2 == M:
                        for p3 in range(M + 1):
                            new_dp[(0, s2 + p3)] += count
                    else:
                        for p3 in range(M - p2 + 1):
                            new_dp[(0, s2 + p3)] += count
                # Non-strike on ball 1
                for a in range(M):
                    s1 = score + a * (1 + b1)
                    for b in range(M - a + 1):
                        s2 = s1 + b
                        if a + b == M:  # spare
                            for p3 in range(M + 1):
                                new_dp[(0, s2 + p3)] += count
                        else:
                            new_dp[(0, s2)] += count
        dp = new_dp

    return {score: count for (_, score), count in dp.items() if count > 0}


def _distribution_k2(N, M):
    """K=2: standard bonus depth. State: (frame, ball, first_ball, b1, b2, score)."""
    dp = defaultdict(int)
    dp[(1, 1, 0, 0, 0, 0)] = 1

    # Process frames 1 to N-1
    while any(state[0] < N for state in dp):
        new_dp = defaultdict(int)
        for (frame, ball, first_ball, b1, b2, score), count in dp.items():
            if frame >= N:
                new_dp[(frame, ball, first_ball, b1, b2, score)] += count
                continue
            if ball == 1:
                for pins in range(M + 1):
                    new_score = score + pins * (1 + b1)
                    nb1 = b2
                    nb2 = 0
                    if pins == M:  # strike
                        nb1 += 1
                        nb2 += 1
                        new_dp[(frame + 1, 1, 0, nb1, nb2, new_score)] += count
                    else:
                        new_dp[(frame, 2, pins, nb1, nb2, new_score)] += count
            else:
                for pins in range(M - first_ball + 1):
                    new_score = score + pins * (1 + b1)
                    nb1 = b2
                    nb2 = 0
                    if first_ball + pins == M:  # spare
                        nb1 += 1
                    new_dp[(frame + 1, 1, 0, nb1, nb2, new_score)] += count
        dp = new_dp

    # Terminal frame N
    results = defaultdict(int)
    for (frame, ball, first_ball, b1, b2, score), count in dp.items():
        for p1 in range(M + 1):
            s1 = score + p1 * (1 + b1)
            nb1 = b2
            if p1 == M:  # strike
                for p2 in range(M + 1):
                    s2 = s1 + p2 * (1 + nb1)
                    if p2 == M:
                        for p3 in range(M + 1):
                            results[s2 + p3] += count
                    else:
                        for p3 in range(M - p2 + 1):
                            results[s2 + p3] += count
            else:
                for p2 in range(M - p1 + 1):
                    s2 = s1 + p2 * (1 + nb1)
                    if p1 + p2 == M:  # spare
                        for p3 in range(M + 1):
                            results[s2 + p3] += count
                    else:
                        results[s2] += count

    return dict(results)


def analyse(dist, label=""):
    """Summary statistics."""
    total = sum(dist.values())
    scores = sorted(dist.keys())
    mode = max(dist, key=dist.get)
    mean = sum(s * c for s, c in dist.items()) / total
    var = sum(c * (s - mean) ** 2 for s, c in dist.items()) / total
    std = var ** 0.5
    entropy = -sum((c / total) * math.log2(c / total)
                    for c in dist.values() if c > 0)
    min_ent = -math.log2(max(c / total for c in dist.values()))

    return {
        'label': label,
        'total_games': total,
        'num_scores': len(dist),
        'min': min(scores),
        'max': max(scores),
        'mode': mode,
        'mean': round(mean, 2),
        'std': round(std, 2),
        'H1': round(entropy, 3),
        'H_inf': round(min_ent, 3),
    }


def count_dp_states(N, M):
    """Count reachable DP states at terminal frame boundary for K=2."""
    dp = defaultdict(int)
    dp[(1, 1, 0, 0, 0, 0)] = 1

    while any(state[0] < N for state in dp):
        new_dp = defaultdict(int)
        for (frame, ball, first_ball, b1, b2, score), count in dp.items():
            if frame >= N:
                new_dp[(frame, ball, first_ball, b1, b2, score)] += count
                continue
            if ball == 1:
                for pins in range(M + 1):
                    new_score = score + pins * (1 + b1)
                    nb1 = b2
                    nb2 = 0
                    if pins == M:
                        nb1 += 1
                        nb2 += 1
                        new_dp[(frame + 1, 1, 0, nb1, nb2, new_score)] += count
                    else:
                        new_dp[(frame, 2, pins, nb1, nb2, new_score)] += count
            else:
                for pins in range(M - first_ball + 1):
                    new_score = score + pins * (1 + b1)
                    nb1 = b2
                    nb2 = 0
                    if first_ball + pins == M:
                        nb1 += 1
                    new_dp[(frame + 1, 1, 0, nb1, nb2, new_score)] += count
        dp = new_dp

    return len(dp)


def main():
    print("=" * 75)
    print("Generalised Bowling: B(N, M, K) Parameter Study")
    print("=" * 75)

    # Vary N with M=10, K=2
    print("\n--- Varying N (M=10, K=2) ---\n")
    print(f"{'N':>3} {'|G|':>20} {'Scores':>8} {'Max':>5} {'Mode':>5} "
          f"{'Mean':>7} {'Std':>6} {'H1':>7} {'States':>8}")
    print("-" * 75)

    for N in range(1, 11):
        dist = generalised_distribution(N, 10, 2)
        stats = analyse(dist)
        states = count_dp_states(N, 10)
        print(f"{N:>3} {stats['total_games']:>20,} {stats['num_scores']:>8} "
              f"{stats['max']:>5} {stats['mode']:>5} {stats['mean']:>7} "
              f"{stats['std']:>6} {stats['H1']:>7} {states:>8,}")

    # Vary M with N=10, K=2
    print("\n--- Varying M (N=10, K=2) ---\n")
    print(f"{'M':>3} {'omega(M)':>10} {'|G|':>25} {'Max':>5} {'Mode':>5} "
          f"{'Mean':>7} {'H1':>7}")
    print("-" * 70)

    for M in [1, 2, 3, 4, 5]:
        dist = generalised_distribution(10, M, 2)
        stats = analyse(dist)
        print(f"{M:>3} {omega(M):>10} {stats['total_games']:>25,} "
              f"{stats['max']:>5} {stats['mode']:>5} {stats['mean']:>7} "
              f"{stats['H1']:>7}")

    # Vary K with N=10, M=10
    print("\n--- Varying K (N=10, M=10) ---\n")
    print(f"{'K':>3} {'Max':>5} {'Mode':>5} {'Mean':>7} {'Std':>6} {'H1':>7}")
    print("-" * 40)

    for K in [0, 1, 2]:
        dist = generalised_distribution(10, 10, K)
        stats = analyse(dist)
        print(f"{K:>3} {stats['max']:>5} {stats['mode']:>5} "
              f"{stats['mean']:>7} {stats['std']:>6} {stats['H1']:>7}")

    # State space growth: N vs states for M=10, K=2
    print("\n--- State Space Growth (M=10, K=2) ---\n")
    print(f"{'N':>3} {'States':>10} {'|G|':>20} {'Compression':>15}")
    print("-" * 50)

    for N in range(1, 11):
        states = count_dp_states(N, 10)
        dist = generalised_distribution(N, 10, 2)
        total = sum(dist.values())
        # States here count pre-terminal states
        ratio = total / states if states > 0 else 0
        print(f"{N:>3} {states:>10,} {total:>20,} {ratio:>15,.0f}")


if __name__ == '__main__':
    main()
