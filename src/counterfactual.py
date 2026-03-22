#!/usr/bin/env python3
"""
Counterfactual analysis: what if frame 10 followed the same rules as frames 1-9?

In this variant, a strike/spare in frame 10 generates look-ahead bonuses
into an 11th frame (which exists solely to provide bonus balls, like
frame 10 does in the real game for frame 9).

This lets us quantify exactly what the frame-10 asymmetry costs or buys.
"""

from collections import defaultdict
import sys
sys.path.insert(0, 'src')
from distributions import traditional_distribution, analyse


def uniform_rules_distribution():
    """
    Compute the score distribution under uniform rules:
    all 10 frames follow frames 1-9 rules, with an 11th frame
    providing bonus balls for frame 10 strikes/spares.

    Frame 11 follows the same terminal rules as frame 10 in
    the standard game (up to 3 balls, no new bonuses).
    """
    dp = defaultdict(int)
    dp[(1, 1, 0, 0, 0, 0)] = 1  # (frame, ball, first_ball, b1, b2, score)

    # Advance through frames 1-10 using IDENTICAL rules
    while any(state[0] < 11 for state in dp):
        new_dp = defaultdict(int)

        for (frame, ball, first_ball, b1, b2, score), count in dp.items():
            if frame >= 11:
                new_dp[(frame, ball, first_ball, b1, b2, score)] += count
                continue

            if ball == 1:
                for pins in range(11):
                    new_score = score + pins * (1 + b1)
                    nb1 = b2
                    nb2 = 0
                    if pins == 10:  # strike
                        nb1 += 1
                        nb2 += 1
                        new_dp[(frame + 1, 1, 0, nb1, nb2, new_score)] += count
                    else:
                        new_dp[(frame, 2, pins, nb1, nb2, new_score)] += count

            else:  # ball == 2
                for pins in range(10 - first_ball + 1):
                    new_score = score + pins * (1 + b1)
                    nb1 = b2
                    nb2 = 0
                    if first_ball + pins == 10:  # spare
                        nb1 += 1
                    new_dp[(frame + 1, 1, 0, nb1, nb2, new_score)] += count

        dp = new_dp

    # Frame 11: terminal frame (same rules as standard frame 10)
    # Consumes pending bonuses but creates none.
    results = defaultdict(int)

    for (frame, ball, first_ball, b1, b2, score), count in dp.items():
        for p1 in range(11):
            s1 = score + p1 * (1 + b1)
            nb1 = b2

            if p1 == 10:  # strike on ball 1
                for p2 in range(11):
                    s2 = s1 + p2 * (1 + nb1)
                    if p2 == 10:
                        for p3 in range(11):
                            results[s2 + p3] += count
                    else:
                        for p3 in range(10 - p2 + 1):
                            results[s2 + p3] += count
            else:
                for p2 in range(10 - p1 + 1):
                    s2 = s1 + p2 * (1 + nb1)
                    if p1 + p2 == 10:  # spare
                        for p3 in range(11):
                            results[s2 + p3] += count
                    else:
                        results[s2] += count

    return dict(results)


def main():
    print("Computing standard (traditional) distribution...")
    trad = traditional_distribution()
    trad_stats = analyse(trad, "Traditional (standard frame 10)")

    print("Computing uniform-rules distribution...")
    uniform = uniform_rules_distribution()
    uniform_stats = analyse(uniform, "Uniform rules (11 frames)")

    print("\n" + "=" * 65)
    print("Comparison: Standard vs Uniform Rules")
    print("=" * 65)

    for stats in [trad_stats, uniform_stats]:
        print(f"\n{stats['name']}:")
        for k, v in stats.items():
            if k != 'name':
                print(f"  {k}: {v:,}" if isinstance(v, int) else f"  {k}: {v}")

    # Key differences
    print("\n--- Key Differences ---")
    print(f"Max score (standard):  {trad_stats['max']}")
    print(f"Max score (uniform):   {uniform_stats['max']}")

    total_trad = sum(trad.values())
    total_uniform = sum(uniform.values())
    print(f"Total games (standard): {total_trad:,}")
    print(f"Total games (uniform):  {total_uniform:,}")
    print(f"  Ratio: {total_uniform / total_trad:.4f}")

    # How many distinct scores in each?
    print(f"Distinct scores (standard): {len(trad)}")
    print(f"Distinct scores (uniform):  {len(uniform)}")

    # Scores unique to one system
    only_uniform = set(uniform.keys()) - set(trad.keys())
    if only_uniform:
        print(f"Scores achievable only under uniform rules: {sorted(only_uniform)}")

    # Save comparison data
    with open('data/uniform_rules_distribution.csv', 'w') as f:
        f.write("score,count\n")
        for s in range(max(uniform.keys()) + 1):
            f.write(f"{s},{uniform.get(s, 0)}\n")

    print("\nSaved uniform rules distribution to data/uniform_rules_distribution.csv")


if __name__ == '__main__':
    main()
