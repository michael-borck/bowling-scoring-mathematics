#!/usr/bin/env python3
"""
Extremal analysis for Section 5:
- Score range for k strikes (consecutive vs scattered)
- Price of scattering
- Fixed pin count, variable score
- Unique preimage scores
"""

import sys
sys.path.insert(0, 'src')
from scoring import score_traditional


def max_score_k_strikes_consecutive(k, open_pins=0):
    """
    Maximum score with exactly k strikes in frames 1-9,
    placed consecutively starting from frame 1.
    Remaining frames are open with (open_pins, 0).
    Frame 10 is open with (open_pins, 0).

    For the cleanest analysis, use open_pins=0.
    """
    # Build game with k consecutive strikes starting at frame 1
    balls = []
    for frame in range(1, 10):
        if frame <= k:
            balls.append(10)  # strike
        else:
            balls.append(open_pins)
            balls.append(0)

    # Frame 10: open with (open_pins, 0)
    balls.append(open_pins)
    balls.append(0)

    return score_traditional(balls), balls


def min_score_k_strikes_scattered(k, open_pins=0):
    """
    Minimum score with exactly k strikes in frames 1-9,
    placed as far apart as possible.
    Remaining frames are open with (open_pins, 0).
    Frame 10 is open with (open_pins, 0).
    """
    # Spread strikes as evenly as possible across 9 frames
    # For k strikes, place in frames that maximise gaps
    strike_frames = set()
    if k > 0:
        # Distribute k strikes across 9 frames, maximally spread
        # Use every ceil(9/k)-th frame
        for i in range(k):
            frame = 1 + round(i * 9 / k)
            if frame > 9:
                frame = 9
            # Avoid collisions
            while frame in strike_frames and frame <= 9:
                frame += 1
            if frame <= 9:
                strike_frames.add(frame)

    # If we couldn't place all k, try again with simple spacing
    if len(strike_frames) < k:
        strike_frames = set()
        # Place in odd frames first, then even
        candidates = list(range(1, 10, 2)) + list(range(2, 10, 2))
        for i in range(min(k, 9)):
            strike_frames.add(candidates[i])

    balls = []
    for frame in range(1, 10):
        if frame in strike_frames:
            balls.append(10)
        else:
            balls.append(open_pins)
            balls.append(0)

    balls.append(open_pins)
    balls.append(0)

    return score_traditional(balls), balls, sorted(strike_frames)


def analyse_k_strikes_exhaustive(k, open_first=0, open_second=0):
    """
    For k strikes in frames 1-9, exhaustively find max and min scores
    over all possible placements. Non-strike frames are (open_first, open_second).
    Frame 10 is always (open_first, open_second).
    """
    from itertools import combinations

    if k > 9:
        return None

    best_score = -1
    best_frames = None
    worst_score = 999
    worst_frames = None

    for strike_frames in combinations(range(1, 10), k):
        balls = []
        for frame in range(1, 10):
            if frame in strike_frames:
                balls.append(10)
            else:
                balls.append(open_first)
                balls.append(open_second)

        balls.append(open_first)
        balls.append(open_second)

        s = score_traditional(balls)
        if s is not None:
            if s > best_score:
                best_score = s
                best_frames = strike_frames
            if s < worst_score:
                worst_score = s
                worst_frames = strike_frames

    return best_score, best_frames, worst_score, worst_frames


def unique_preimage_scores():
    """
    Find all scores with exactly 1 game producing them.
    Uses the full distribution.
    """
    from distributions import traditional_distribution
    dist = traditional_distribution()
    unique = sorted(s for s, count in dist.items() if count == 1)
    return unique, dist


def main():
    print("=" * 65)
    print("Extremal Analysis")
    print("=" * 65)

    # --- Strike placement analysis (open frames = gutter balls) ---
    print("\n--- Strike Placement: k strikes, open frames = (0,0) ---\n")
    print(f"{'k':>3}  {'Max Score':>10} {'Max Frames':<25} {'Min Score':>10} {'Min Frames':<25} {'Gap':>5}")
    print("-" * 85)

    for k in range(0, 10):
        result = analyse_k_strikes_exhaustive(k, 0, 0)
        if result:
            best_s, best_f, worst_s, worst_f = result
            gap = best_s - worst_s
            print(f"{k:>3}  {best_s:>10}  {str(best_f):<25} {worst_s:>10}  {str(worst_f):<25} {gap:>5}")

    # --- With non-zero open frames ---
    print("\n--- Strike Placement: k strikes, open frames = (4,3) ---\n")
    print(f"{'k':>3}  {'Max Score':>10} {'Max Frames':<25} {'Min Score':>10} {'Min Frames':<25} {'Gap':>5}")
    print("-" * 85)

    for k in range(0, 10):
        result = analyse_k_strikes_exhaustive(k, 4, 3)
        if result:
            best_s, best_f, worst_s, worst_f = result
            gap = best_s - worst_s
            print(f"{k:>3}  {best_s:>10}  {str(best_f):<25} {worst_s:>10}  {str(worst_f):<25} {gap:>5}")

    # --- Unique preimage scores ---
    print("\n--- Scores with unique preimages (exactly 1 game) ---\n")
    unique, dist = unique_preimage_scores()
    print(f"Scores with exactly 1 game: {unique}")
    print(f"Count: {len(unique)}")

    # Also show scores with very few preimages
    print("\n--- Scores with fewest preimages (top 20) ---\n")
    by_count = sorted(dist.items(), key=lambda x: x[1])
    for score, count in by_count[:20]:
        print(f"  Score {score:>3}: {count:>20,} games")

    # --- Scores with most preimages (top 10) ---
    print("\n--- Scores with most preimages (top 10) ---\n")
    by_count_desc = sorted(dist.items(), key=lambda x: x[1], reverse=True)
    for score, count in by_count_desc[:10]:
        print(f"  Score {score:>3}: {count:>25,} games")


if __name__ == '__main__':
    main()
