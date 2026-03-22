#!/usr/bin/env python3
"""
Information-theoretic analysis for Section 7:
- Shannon entropy of score distributions
- Preimage counting
- Comparison of traditional vs World Bowling information content
"""

import math
import sys
sys.path.insert(0, 'src')
from distributions import traditional_distribution, world_bowling_distribution


def entropy(dist):
    """Compute Shannon entropy H = -sum p(s) log2 p(s)."""
    total = sum(dist.values())
    h = 0.0
    for count in dist.values():
        if count > 0:
            p = count / total
            h -= p * math.log2(p)
    return h


def max_entropy(num_outcomes):
    """Maximum entropy for a uniform distribution over num_outcomes."""
    return math.log2(num_outcomes)


def game_entropy(total_games):
    """Entropy if every game were distinguishable (= log2 of game space)."""
    return math.log2(total_games)


def main():
    print("Computing distributions...")
    trad = traditional_distribution()
    world = world_bowling_distribution()

    trad_total = sum(trad.values())
    world_total = sum(world.values())

    print("\n" + "=" * 65)
    print("Information-Theoretic Analysis")
    print("=" * 65)

    # Shannon entropy
    h_trad = entropy(trad)
    h_world = entropy(world)
    h_max_301 = max_entropy(301)
    h_max_291 = max_entropy(len(world))
    h_game_trad = game_entropy(trad_total)
    h_game_world = game_entropy(world_total)

    print(f"\n--- Shannon Entropy of Score Distributions ---\n")
    print(f"Traditional scoring:")
    print(f"  H(S)           = {h_trad:.4f} bits")
    print(f"  Max possible   = log2(301) = {h_max_301:.4f} bits")
    print(f"  Efficiency     = {h_trad / h_max_301 * 100:.1f}%")
    print(f"  Game entropy   = log2(|G|) = {h_game_trad:.2f} bits")
    print(f"  Information    = {h_trad / h_game_trad * 100:.4f}% of game identity")

    print(f"\nWorld Bowling scoring:")
    print(f"  H(S)           = {h_world:.4f} bits")
    print(f"  Max possible   = log2({len(world)}) = {h_max_291:.4f} bits")
    print(f"  Efficiency     = {h_world / h_max_291 * 100:.1f}%")
    print(f"  Game entropy   = log2(|G|) = {h_game_world:.2f} bits")
    print(f"  Information    = {h_world / h_game_world * 100:.4f}% of game identity")

    print(f"\n--- Comparison ---")
    print(f"  H(traditional) - H(world) = {h_trad - h_world:.4f} bits")
    print(f"  Traditional is {2**(h_trad - h_world):.2f}x more informative")

    # Preimage analysis
    print(f"\n--- Preimage Size Distribution ---\n")

    # Categorise scores by preimage size
    unique_trad = [s for s, c in trad.items() if c == 1]
    unique_world = [s for s, c in world.items() if c == 1]

    print(f"Traditional: {len(unique_trad)} scores with unique preimage")
    print(f"  Scores: {sorted(unique_trad)}")
    print(f"World Bowling: {len(unique_world)} scores with unique preimage")
    print(f"  Scores: {sorted(unique_world)}")

    # Score ranges where preimage is very small
    print(f"\n--- Traditional: Smallest preimages ---")
    by_count = sorted(trad.items(), key=lambda x: x[1])
    for s, c in by_count[:15]:
        print(f"  Score {s:>3}: {c:>20,} games")

    print(f"\n--- World Bowling: Smallest preimages ---")
    by_count_w = sorted(world.items(), key=lambda x: x[1])
    for s, c in by_count_w[:15]:
        print(f"  Score {s:>3}: {c:>20,} games")

    # Surprise value of each score
    print(f"\n--- Surprise (self-information) of selected scores ---\n")
    print(f"{'Score':>5}  {'Trad Games':>20}  {'Trad Surprise':>15}  {'Meaning':>30}")
    print("-" * 75)
    for s in [0, 50, 77, 100, 150, 200, 250, 280, 290, 291, 300]:
        tc = trad.get(s, 0)
        if tc > 0:
            tp = tc / trad_total
            surprise = -math.log2(tp)
            if tc == 1:
                meaning = "unique game"
            elif s == 77:
                meaning = "maximum ambiguity (mode)"
            else:
                meaning = ""
            print(f"{s:>5}  {tc:>20,}  {surprise:>12.2f} bits  {meaning:>30}")

    # Save data
    with open('data/information_analysis.csv', 'w') as f:
        f.write("score,trad_count,world_count,trad_surprise,world_surprise\n")
        for s in range(301):
            tc = trad.get(s, 0)
            wc = world.get(s, 0)
            ts = -math.log2(tc / trad_total) if tc > 0 else float('inf')
            ws = -math.log2(wc / world_total) if wc > 0 else float('inf')
            f.write(f"{s},{tc},{wc},{ts:.6f},{ws if ws != float('inf') else 'inf'}\n")

    print("\nSaved to data/information_analysis.csv")


if __name__ == '__main__':
    main()
