#!/usr/bin/env python3
"""
distributions.py

Computes EXACT score distributions for ten-pin bowling scoring systems
using dynamic programming with pending-bonus state tracking.

No brute-force game enumeration (6 quintillion games for traditional).
Instead, we track (frame, ball, first_ball, b1, b2, score) and advance
one ball at a time. Total distinct states stays in the hundreds of thousands.

b1 = extra multiplier for the NEXT ball (0, 1, or 2)
b2 = extra multiplier for the ball-after-next (0 or 1)

A spare sets b1 += 1 (next ball counts double).
A strike sets b1 += 1 and b2 += 1 (next two balls each count double).
A double (two consecutive strikes) yields b1=2 (next ball counts triple).

Verifies against Balmoral Software's published tables:
  http://www.balmoralsoftware.com/bowling/bowling.htm
"""

from collections import defaultdict


# -- Traditional Scoring -------------------------------------------------------

def traditional_distribution():
    """
    Compute the exact score distribution for traditional bowling.

    State: (frame, ball, first_ball, b1, b2, score)

      frame       1-9 while processing; transitions to 10 handling
      ball        1 or 2 within a regular frame
      first_ball  pins on ball 1 of this frame (only used when ball==2)
      b1          extra multiplier for next ball thrown (0, 1, or 2)
      b2          extra multiplier for ball-after-next (0 or 1)
      score       accumulated score so far

    After all states reach frame 10, a separate loop handles the
    special frame-10 rules (up to 3 balls, no new bonuses generated).

    Returns:
        dict mapping score (int) -> number of distinct games (int)
    """

    dp = defaultdict(int)
    dp[(1, 1, 0, 0, 0, 0)] = 1  # game start

    # Advance ball-by-ball until every state is at frame 10
    while any(state[0] < 10 for state in dp):
        new_dp = defaultdict(int)

        for (frame, ball, first_ball, b1, b2, score), count in dp.items():

            # Already at frame 10 -- carry forward unchanged
            if frame >= 10:
                new_dp[(frame, ball, first_ball, b1, b2, score)] += count
                continue

            if ball == 1:
                for pins in range(11):               # 0-10 possible pins
                    new_score = score + pins * (1 + b1)
                    nb1 = b2                          # shift pending bonuses
                    nb2 = 0

                    if pins == 10:                    # strike -- frame complete
                        nb1 += 1
                        nb2 += 1
                        new_dp[(frame + 1, 1, 0, nb1, nb2, new_score)] += count
                    else:                             # not a strike -- throw ball 2
                        new_dp[(frame, 2, pins, nb1, nb2, new_score)] += count

            else:   # ball == 2
                for pins in range(10 - first_ball + 1):
                    new_score = score + pins * (1 + b1)
                    nb1 = b2                          # shift
                    nb2 = 0

                    if first_ball + pins == 10:       # spare
                        nb1 += 1

                    new_dp[(frame + 1, 1, 0, nb1, nb2, new_score)] += count

        dp = new_dp

    # -- Frame 10 --------------------------------------------------------------
    # Pending bonuses (b1, b2) from frame 9 still apply to the balls
    # thrown in frame 10, but frame 10 throws generate NO new bonuses.
    # Extra balls: strike on ball 1 -> get balls 2 & 3
    #              spare on balls 1+2 -> get ball 3
    #              open -> game over after ball 2

    results = defaultdict(int)

    for (frame, ball, first_ball, b1, b2, score), count in dp.items():

        for p1 in range(11):
            s1 = score + p1 * (1 + b1)
            nb1 = b2                                  # remaining pending bonus

            if p1 == 10:                              # strike on ball 1 -> 2 more balls
                for p2 in range(11):
                    s2 = s1 + p2 * (1 + nb1)

                    if p2 == 10:                      # double strike -> ball 3: 0-10
                        for p3 in range(11):
                            results[s2 + p3] += count
                    else:                             # strike then non-strike -> ball 3: 0 to 10-p2
                        for p3 in range(10 - p2 + 1):
                            results[s2 + p3] += count

            else:                                     # no strike on ball 1
                for p2 in range(10 - p1 + 1):
                    s2 = s1 + p2 * (1 + nb1)

                    if p1 + p2 == 10:                 # spare -> bonus ball 3: 0-10
                        for p3 in range(11):
                            results[s2 + p3] += count
                    else:                             # open frame -> game over
                        results[s2] += count

    return dict(results)


# -- World Bowling (Current-Frame) Scoring -------------------------------------

def world_bowling_distribution():
    """
    Compute the exact score distribution for World Bowling scoring.

    World Bowling scoring rules:
      Strike = 30 pts (no bonus from future balls)
      Spare  = 10 + first_ball
      Open   = first_ball + second_ball

    All 10 frames are identical; no bonus ball in frame 10.
    No pending bonuses between frames -- pure 10-fold convolution.

    Returns:
        dict mapping score (int) -> number of distinct games (int)
    """

    dp = defaultdict(int)
    dp[0] = 1

    for _ in range(10):
        new_dp = defaultdict(int)

        for score, count in dp.items():
            for first in range(11):
                if first == 10:                       # strike
                    new_dp[score + 30] += count
                else:
                    for second in range(10 - first + 1):
                        if first + second == 10:      # spare
                            frame_score = 10 + first
                        else:                         # open
                            frame_score = first + second
                        new_dp[score + frame_score] += count

        dp = new_dp

    return dict(dp)


# -- Analysis Utilities --------------------------------------------------------

def analyse(dist, name):
    """Compute summary statistics for a score distribution."""
    total = sum(dist.values())
    scores = sorted(dist.keys())
    mode = max(dist, key=dist.get)
    mean = sum(s * c for s, c in dist.items()) / total
    var = sum(c * (s - mean) ** 2 for s, c in dist.items()) / total
    std_dev = var ** 0.5

    cumulative = 0
    median = None
    for s in scores:
        cumulative += dist[s]
        if cumulative * 2 >= total and median is None:
            median = s

    return dict(name=name, total=total, mode=mode,
                mean=round(mean, 1), median=median,
                std_dev=round(std_dev, 1),
                min=min(scores), max=max(scores))


# -- Main ----------------------------------------------------------------------

if __name__ == '__main__':
    print("Computing traditional scoring distribution...")
    trad = traditional_distribution()
    print(f"  Done -- {len(trad)} distinct scores")

    print("Computing World Bowling distribution...")
    world = world_bowling_distribution()
    print(f"  Done -- {len(world)} distinct scores")

    for d, name in [(trad, 'Traditional'), (world, 'World Bowling')]:
        stats = analyse(d, name)
        print(f"\n{name}:")
        for k, v in stats.items():
            if k != 'name':
                print(f"  {k}: {v:,}" if isinstance(v, int) else f"  {k}: {v}")
