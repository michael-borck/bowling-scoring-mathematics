# The Mathematics of Ten-Pin Bowling: A Formal Analysis of the Traditional Scoring System

## Research Plan

**Target venues:** Mathematics Magazine, The College Mathematics Journal, or The American Mathematical Monthly

**Scope:** A self-contained mathematical treatment of the traditional ten-pin bowling scoring function. No simulation, no system comparison -- pure mathematics. This paper provides the rigorous foundation that Paper 1 (Skill, Sequence, and Scoring) builds on, but stands entirely on its own.

---

## Paper Outline

### 1. The Scoring Function as a Formal Object

Define the traditional scoring function precisely:

- **Domain:** The set of valid ball sequences. Each ball outcome is drawn from a finite alphabet {0, 1, ..., 10}, subject to frame constraints (two balls per frame must sum to at most 10, with exceptions in frame 10). A complete game is a sequence of 12 to 21 balls.
- **Range:** The integers 0 to 300.
- **Recursive structure:** The score after frame *k* depends on balls thrown in frames *k*, *k+1*, and possibly *k+2*. This is a sliding window with finite look-ahead (at most 2 balls beyond the current frame).
- **Connection to formal language theory:** The set of valid games forms a regular language over the alphabet {0, ..., 10}. The scoring function can be computed by a finite-state transducer. Characterise the minimal automaton that recognises valid game sequences.
- **Key question:** What class of functions does the traditional scoring function belong to? It is not a simple sum (unlike World Bowling). It is not a convolution. It is a particular kind of state-dependent accumulator with bounded look-ahead.

### 2. The State Space

Unify three existing computational approaches to the score distribution, showing they are different perspectives on the same underlying object:

- **Cooper & Kennedy (1990):** Generating function approach. The number of games achieving each score is encoded as coefficients of a polynomial. They compute this by multiplying frame-level generating functions, accounting for inter-frame dependencies.
- **Balmoral Software DP:** Dynamic programming over a state space that tracks pending bonuses. Iterates frame by frame.
- **Our exact enumeration (distributions.py):** Ball-by-ball DP with state (frame, ball, first_ball, pending_b1, pending_b2, score). Advances one ball at a time rather than one frame at a time.

All three compute the same object: the exact number of distinct games producing each score from 0 to 300.

**State representation analysis:**
- Minimal state: (frame, ball_within_frame, first_ball_pins, pending_bonus_1, pending_bonus_2, accumulated_score)
- Count the number of reachable states at each frame boundary
- Show that the state space is surprisingly small (~hundreds of thousands) despite the game space being ~5.7 quintillion
- Prove bounds on the state space size as a function of the number of frames

### 3. Symmetry and Asymmetry

The traditional scoring system has an elegant near-symmetry that is broken in exactly one place:

- **Frames 1-9:** Governed by identical rules. There is a translational symmetry -- the rules for frame *i* are the same as for frame *j* (for 1 <= i, j <= 9). The bonus structure creates dependencies *between* frames, but the *rules* are frame-independent.
- **Frame 10 breaks the symmetry:** Frame 10 follows different rules:
  - Extra balls are awarded (up to 3 total) but generate no new bonuses
  - It consumes pending bonuses from frame 9 but creates none
  - It is a "sink" in the bonus dependency graph
- **Characterise the break precisely:** What properties of frames 1-9 fail in frame 10? What is gained and lost?
- **Counterfactual: uniform rules.** What if frame 10 followed the same rules as frames 1-9 (with an 11th frame providing bonus balls for a frame-10 strike)? How does the score distribution change? What is the maximum possible score?
- **Generalisation to N frames:** Hohn (2009) considers games with N frames. For which N do the structural properties (multimodality, compounding, etc.) hold? The frame-10 anomaly becomes a "frame-N" anomaly for any finite game.

### 4. The Bonus Structure as a Dependency Graph

Model the bonus structure as a directed graph:

- **Vertices:** The individual balls thrown in a game (12 to 21 balls).
- **Edges:** A strike in frame *i* creates directed edges from ball 1 of frame *i* to the next two balls (wherever they fall). A spare creates an edge to the next one ball.
- **Properties of this graph:**
  - Maximum out-degree: 2 (from a strike)
  - Maximum in-degree: 2 (a ball can be a bonus ball for at most two preceding frames -- when preceded by a double)
  - Path lengths: The longest directed path has length 3 (a double followed by any ball)
  - Connected components: In a game of all open frames, the graph has no edges. A perfect game has maximum connectivity.
- **Maximum bonus chain:** Prove that the maximum "chain" of bonus dependencies has length 3 (the triple: three consecutive strikes, where the first strike's bonus depends on the next two balls, the second strike's bonus depends on two balls, etc.)
- **Connection to combinatorics on words:** The bonus pattern of a game (sequence of S=strike, P=spare, O=open for each frame) is a word over {S, P, O}. The dependency graph is determined by this word. Classify the possible dependency graphs by the frame-outcome word.
- **The "price of scattering":** A ball that is a bonus ball for a preceding strike or spare has higher marginal value than an isolated ball. Quantify this multiplier effect.

### 5. Extremal Problems

Several natural optimisation questions arise:

- **Strike placement:** Given exactly *k* strikes in 10 frames (and the rest open with fixed pin counts), what orderings of the strikes maximise or minimise the total score?
  - **Conjecture (to prove analytically):** Consecutive strikes maximise the score. Prove this by showing that swapping a strike into adjacency with another strike never decreases the score (a local exchange argument).
  - Minimum: strikes as spread out as possible (frames 1, 3, 5, 7, 9 for k=5).
  - Quantify the gap between max and min for each k.

- **Fixed pin count, variable score:** Given that a bowler knocks down exactly *P* total pins across all balls, what is the range of possible scores?
  - Every pin knocked down in a bonus position is worth 2x or 3x. So the score can exceed the pin count substantially.
  - Maximum score for a given pin count (concentrate pins into strikes).
  - Minimum score for a given pin count (spread pins into open frames with no bonuses).

- **The "price of scattering":** Define this as max_score(k strikes) - min_score(k strikes) for fixed k and fixed open-frame outcomes. This measures how much score is lost by distributing strikes rather than concentrating them. Derive a closed-form expression.

- **Impossibility results:** Which scores are achievable by exactly one game? (We know 0 and 300 are unique. What about 291? Others?) Characterise the scores with unique preimages.

### 6. The Score Distribution

The score distribution over all possible games (assuming each valid ball outcome is equally likely) has remarkable structure:

- **Multimodality:** The distribution has multiple peaks. Why?
  - The peaks occur at intervals related to the bonus structure. Each additional strike shifts probability mass by approximately 20-30 points (the bonus increment).
  - Prove (or give a rigorous heuristic for) the location of the peaks in terms of the expected bonus from 0, 1, 2, ... strikes.
  - Connection to VanDerwerken & Kenter (2018), who discuss the multimodal structure.

- **Generating function approach (Cooper & Kennedy 1990):**
  - The distribution is encoded as the coefficient sequence of a product of frame-level generating functions.
  - For frames 1-9 (with dependencies), the generating function is not a simple product -- it must account for the carry-forward bonuses.
  - Characterise the generating function's algebraic structure.

- **Exact enumeration approach (our DP):**
  - Ball-by-ball state tracking produces the exact distribution.
  - Verify against Cooper & Kennedy and Balmoral.
  - Advantages: can easily modify rules and recompute.

- **Asymptotic behaviour:**
  - Tail behaviour near 0 and 300.
  - The distribution near 300 is sparse (few games score above 280).
  - The distribution near 0 is also sparse but less so.
  - Central limit theorem considerations: the score is a sum of dependent random variables. Under what conditions does a CLT apply?

### 7. Information Content and Preimage Counting

The scoring function is many-to-one. Investigate the structure of the preimages:

- **Preimage size:** For each score *s* in {0, ..., 300}, define f(s) = number of distinct games producing score s. This is exactly the score distribution computed in Section 6.
  - f(0) = 1, f(300) = 1 (unique games).
  - f(77) = 172,542,309,343,731,946 (the mode -- most common score).
  - How does f(s) vary? Plot and characterise.

- **Preimage structure:** For a given score *s*, what do the games in the preimage have in common? Can we characterise the "level sets" of the scoring function?

- **Shannon entropy:** Compute the entropy H = -sum p(s) log p(s) where p(s) = f(s) / total_games. This measures how much information a score reveals about the game.
  - Compare with the entropy of World Bowling scoring. (Traditional has higher entropy -- it is more informative.)
  - What is the theoretical maximum entropy for a function from the game space to {0, ..., 300}?

- **What does a score tell you?** Given only a player's score, what can you infer about the game?
  - A score of 300 tells you everything (perfect game).
  - A score of 77 tells you almost nothing (maximum ambiguity).
  - A score of 291 tells you everything (unique game).
  - Formalise this as a channel capacity or mutual information problem.

### 8. Generalisation: N Frames, M Pins, K Bonus Balls

Embed the traditional scoring system in a parametric family:

- **Parameters:**
  - N = number of frames (standard: 10)
  - M = number of pins (standard: 10)
  - K = bonus balls for a strike (standard: 2), for a spare (standard: 1)
  - Frame-10 rule: special (standard) or uniform (hypothetical)

- **Which properties depend on N=10, M=10?**
  - Multimodality of the distribution: structural (holds for general N, M) or accidental?
  - The compounding bonus structure: depends on K, not on N or M.
  - The state space size: how does it scale with N and M?
  - Maximum score: N * M * (1 + K/M * M) -- derive the general formula.

- **Connection to Hohn (2009):** Hohn's thesis generalises the bowling scoring problem to N frames. Relate our results to his, identify what is new.

- **Degenerate cases:**
  - K=0: no bonuses, score = total pins (trivial).
  - K=N: every frame's bonus extends to the end of the game (maximally coupled).
  - M=1: binary bowling (knock down the pin or don't). Simplest non-trivial case.

---

## Key References

1. **Cooper, C. N. & Kennedy, R. E. (1990).** "A Generating Function for the Distribution of the Scores of all Possible Bowling Games." *Mathematics Magazine*, 63(4), 239-243. -- Generating function approach via a 4-state transition matrix (OPEN, SPARE, STRIKE, DOUBLE). The foundational paper.

2. **Hohn, J. L. (2009).** "Generalized Probabilistic Bowling Distributions." Masters Thesis, Western Kentucky University. -- Generalisation to N frames, arithmetic mean derivation, the "Hohn Distribution" for probabilistic frame scoring.

3. **Balmoral Software.** "All About Bowling Scores." http://www.balmoralsoftware.com/bowling/bowling.htm -- Independent verification of exact score distributions via DP.

4. **VanDerwerken, D. N. & Kenter, F. H. J. (2018).** "A Generative Markov Model for Bowling Scores." *Journal of Quantitative Analysis in Sports*, 14(4), 213-226. -- 4th-order Markov model with Bayesian shrinkage for empirical score distributions; documents multimodality in PBA data.

---

## Connection to the Other Papers

- **Paper 1 (Skill, Sequence, and Scoring)** uses the mathematical properties developed here -- particularly the bonus dependency structure, sequence sensitivity, and score distribution -- as the foundation for comparing traditional and World Bowling scoring. This paper (Paper 3) provides the rigorous proofs; Paper 1 applies them.
- **Paper 3 is self-contained.** It does not require the simulation results or the scoring system comparison from Paper 1. A reader of Mathematics Magazine needs no context about the World Bowling debate.
- The shared computational code (distributions.py, scoring.py) ensures consistency between the papers.

---

## Work Plan

1. **Formalise definitions** (Sections 1-2): Write precise definitions, enumerate the state space, verify against existing literature.
2. **Prove structural results** (Sections 3-5): Symmetry analysis, dependency graph properties, extremal theorems.
3. **Compute and analyse** (Sections 6-7): Score distribution, preimage counting, entropy calculations.
4. **Generalise** (Section 8): Parametric family, identify which results are structural vs accidental.
5. **Write and polish** for Mathematics Magazine style (accessible to a broad mathematical audience, emphasis on elegance over technicality).
