#!/usr/bin/env python3
"""
scoring.py

Core scoring functions for traditional and World Bowling ten-pin bowling.

These functions take a sequence of ball outcomes (pin counts) and return
the total game score. They implement the complete rules including the
special frame-10 handling.
"""


def score_traditional(balls):
    """
    Score a complete game under traditional rules.

    Args:
        balls: list of pin counts for each ball thrown in sequence.

    Returns:
        Integer score, or None if the sequence is invalid.
    """
    score = 0
    i = 0
    for frame in range(10):
        if i >= len(balls):
            return None
        if frame < 9:
            if balls[i] == 10:          # strike
                if i + 2 >= len(balls):
                    return None
                score += 10 + balls[i+1] + balls[i+2]
                i += 1
            else:
                if i + 1 >= len(balls):
                    return None
                if balls[i] + balls[i+1] > 10:
                    return None         # invalid
                score += balls[i] + balls[i+1]
                if balls[i] + balls[i+1] == 10:     # spare
                    if i + 2 >= len(balls):
                        return None
                    score += balls[i+2]
                i += 2
        else:   # frame 10
            if balls[i] == 10:          # strike
                if i + 2 >= len(balls):
                    return None
                b2 = balls[i+1]
                b3 = balls[i+2]
                if b2 == 10:
                    score += 10 + b2 + b3
                elif b2 + b3 > 10:
                    return None
                else:
                    score += 10 + b2 + b3
            else:
                if i + 1 >= len(balls):
                    return None
                if balls[i] + balls[i+1] > 10:
                    return None
                if balls[i] + balls[i+1] == 10:     # spare
                    if i + 2 >= len(balls):
                        return None
                    score += 10 + balls[i+2]
                else:
                    score += balls[i] + balls[i+1]
    return score


def score_world(balls):
    """
    Score a complete game under World Bowling (current-frame) rules.

    World Bowling rules:
      Strike = 30 pts (no bonus from future balls)
      Spare  = 10 + first_ball of that frame
      Open   = first_ball + second_ball

    All 10 frames follow identical rules. No bonus balls in frame 10.

    Args:
        balls: list of pin counts for each ball thrown.

    Returns:
        Integer score, or None if invalid.
    """
    score = 0
    i = 0
    for frame in range(10):
        if i >= len(balls):
            return None
        if balls[i] == 10:              # strike
            score += 30
            i += 1
        else:
            if i + 1 >= len(balls):
                return None
            if balls[i] + balls[i+1] > 10:
                return None
            if balls[i] + balls[i+1] == 10:
                score += 10 + balls[i]  # spare
            else:
                score += balls[i] + balls[i+1]
            i += 2
    return score
