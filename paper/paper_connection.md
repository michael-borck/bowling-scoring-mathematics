# Bowling Scoring Paper Series: Connection Map

## Overview

Three papers form a coordinated study of ten-pin bowling scoring from different angles, for different audiences.

---

## The Three Papers

### Paper 1: Skill, Sequence, and Scoring
- **Full title:** Skill, Sequence, and Scoring: A Mathematical Argument for Traditional Ten-Pin Bowling Scoring
- **Project:** `/Users/michael/Projects/skill-sequence-scoring/`
- **Venue:** Journal of Quantitative Analysis in Sports (JQAS)
- **Status:** In progress

### Paper 2: Win Probability Analysis
- **Full title:** Win Probability in Ten-Pin Bowling (working title)
- **Project:** `/Users/michael/Projects/bowling-wpa-analysis/`
- **Venue:** Journal of Quantitative Analysis in Sports (JQAS)
- **Status:** In progress

### Paper 3: The Mathematics of Bowling Scoring
- **Full title:** The Mathematics of Ten-Pin Bowling: A Formal Analysis of the Traditional Scoring System
- **Project:** `/Users/michael/Projects/bowling-scoring-mathematics/`
- **Venue:** Mathematics Magazine / College Mathematics Journal / American Mathematical Monthly
- **Status:** Planning

---

## Comparison Table

| Dimension | Paper 1 (Skill & Sequence) | Paper 2 (Win Probability) | Paper 3 (Mathematics) |
|---|---|---|---|
| **Central question** | Does traditional scoring reward skill better than World Bowling? | What is the probability of winning at any point in a match? | What are the formal mathematical properties of the scoring function? |
| **Methods** | Exact enumeration, simulation, information theory | Markov chains, dynamic programming, empirical validation | Formal analysis, generating functions, combinatorics, graph theory |
| **Key results** | Traditional scoring is more sequence-sensitive, skill-discriminating, and information-rich | In-game win probability model for strategic decision-making | Characterisation of the scoring function's structure, extremal results, distribution analysis |
| **Audience** | Sports analytics researchers, bowling governance | Sports analytics researchers, bowling coaches/players | Mathematicians, recreational mathematics enthusiasts |
| **Venue** | JQAS | JQAS | Mathematics Magazine / CMJ / AMM |
| **Tone** | Applied — argues for a position using mathematical evidence | Applied — builds a practical tool grounded in probability | Pure — explores the mathematics for its own sake |
| **Needs the others?** | Builds on Paper 3's foundations, independent of Paper 2 | Independent of Papers 1 and 3 | Fully self-contained |
| **Shared code** | `bowling_distributions.py`, `bowling_analysis.py` | Own codebase | `distributions.py`, `scoring.py` (derived from Paper 1's code) |

---

## Dependency Structure

```
Paper 3 (Mathematics)          Paper 2 (Win Probability)
   Pure foundations                Independent stream
        |
        v
Paper 1 (Skill & Sequence)
   Applied comparison
```

- **Paper 3 -> Paper 1:** Paper 1 cites Paper 3 for the formal proofs of sequence sensitivity, the bonus dependency structure, and the score distribution properties. Paper 1 can state these as facts with a citation rather than re-proving them.
- **Paper 2** is independent. It shares the bowling domain but addresses a completely different question (in-game win probability vs scoring system properties).
- **Paper 3** is self-contained. A Mathematics Magazine reader needs no knowledge of the JQAS papers or the traditional-vs-World-Bowling debate.

---

## Shared Themes

Despite different audiences and questions, all three papers touch on:

1. **The bonus/look-ahead structure** of traditional scoring (the defining feature that makes it mathematically interesting)
2. **The state space** of bowling games (all three need to enumerate or model the space of possible games)
3. **Frame 10 as a special case** (all three must handle the asymmetry)

---

## Timeline Considerations

- Paper 3 should ideally be submitted first (or simultaneously with Paper 1) so that Paper 1 can cite it.
- Paper 2 can be submitted independently at any time.
- If Paper 3 is not yet published when Paper 1 is submitted, Paper 1 can include the key proofs in an appendix and note that a full treatment is forthcoming.
