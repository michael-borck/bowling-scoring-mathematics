#!/usr/bin/env python3
"""
Analyse the state space of the traditional bowling scoring DP.

Counts reachable states at each frame boundary to demonstrate
how the state space remains tractable despite the enormous game space.
"""

from collections import defaultdict


def count_states_by_frame():
    """
    Run the ball-by-ball DP, recording the number of distinct states
    at each frame boundary.

    Returns a list of (frame, num_states, num_games) tuples.
    """
    dp = defaultdict(int)
    dp[(1, 1, 0, 0, 0, 0)] = 1

    results = []
    results.append((1, len(dp), sum(dp.values())))

    # Advance through frames 1-9
    while any(state[0] < 10 for state in dp):
        new_dp = defaultdict(int)

        for (frame, ball, first_ball, b1, b2, score), count in dp.items():
            if frame >= 10:
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
            else:
                for pins in range(10 - first_ball + 1):
                    new_score = score + pins * (1 + b1)
                    nb1 = b2
                    nb2 = 0
                    if first_ball + pins == 10:  # spare
                        nb1 += 1
                    new_dp[(frame + 1, 1, 0, nb1, nb2, new_score)] += count

        dp = new_dp

        # Count states at each frame boundary
        max_frame = max(state[0] for state in dp)
        frame_states = {s for s in dp if s[0] == max_frame}
        total_paths = sum(dp[s] for s in frame_states)
        results.append((max_frame, len(frame_states), total_paths))

    # Count frame-10 entry states
    f10_states = {s for s in dp}
    results.append(("10 (entry)", len(f10_states), sum(dp.values())))

    return results


def analyse_bonus_state_distribution():
    """
    At the frame-10 boundary, analyse the distribution of
    (b1, b2) pending bonus states.
    """
    dp = defaultdict(int)
    dp[(1, 1, 0, 0, 0, 0)] = 1

    while any(state[0] < 10 for state in dp):
        new_dp = defaultdict(int)
        for (frame, ball, first_ball, b1, b2, score), count in dp.items():
            if frame >= 10:
                new_dp[(frame, ball, first_ball, b1, b2, score)] += count
                continue
            if ball == 1:
                for pins in range(11):
                    new_score = score + pins * (1 + b1)
                    nb1 = b2
                    nb2 = 0
                    if pins == 10:
                        nb1 += 1
                        nb2 += 1
                        new_dp[(frame + 1, 1, 0, nb1, nb2, new_score)] += count
                    else:
                        new_dp[(frame, 2, pins, nb1, nb2, new_score)] += count
            else:
                for pins in range(10 - first_ball + 1):
                    new_score = score + pins * (1 + b1)
                    nb1 = b2
                    nb2 = 0
                    if first_ball + pins == 10:
                        nb1 += 1
                    new_dp[(frame + 1, 1, 0, nb1, nb2, new_score)] += count
        dp = new_dp

    # Analyse bonus states at frame 10
    bonus_counts = defaultdict(lambda: {'states': 0, 'games': 0})
    score_range = defaultdict(lambda: [301, -1])

    for (frame, ball, first_ball, b1, b2, score), count in dp.items():
        key = (b1, b2)
        bonus_counts[key]['states'] += 1
        bonus_counts[key]['games'] += count
        score_range[key][0] = min(score_range[key][0], score)
        score_range[key][1] = max(score_range[key][1], score)

    return bonus_counts, score_range


def main():
    print("=" * 65)
    print("State Space Analysis: Traditional Bowling Scoring DP")
    print("=" * 65)

    print("\n--- Reachable states at each frame boundary ---\n")
    results = count_states_by_frame()

    print(f"{'Frame':<15} {'Distinct States':>20} {'Game Paths':>25}")
    print("-" * 62)
    for frame, states, paths in results:
        print(f"{str(frame):<15} {states:>20,} {paths:>25,}")

    print("\n--- Pending bonus states at frame 10 entry ---\n")
    bonus_counts, score_range = analyse_bonus_state_distribution()

    print(f"{'(b1, b2)':<12} {'States':>12} {'Games':>25} {'Score Range':>15}")
    print("-" * 66)
    total_states = 0
    total_games = 0
    for key in sorted(bonus_counts.keys()):
        s = bonus_counts[key]['states']
        g = bonus_counts[key]['games']
        lo, hi = score_range[key]
        total_states += s
        total_games += g
        print(f"{str(key):<12} {s:>12,} {g:>25,} {lo:>6}-{hi:<6}")

    print("-" * 66)
    print(f"{'Total':<12} {total_states:>12,} {total_games:>25,}")

    # Compression ratio
    print(f"\n--- Compression ---")
    print(f"Game space:  {total_games:,} distinct games")
    print(f"State space: {total_states:,} reachable DP states")
    print(f"Compression: {total_games / total_states:,.0f}:1")


if __name__ == '__main__':
    main()
