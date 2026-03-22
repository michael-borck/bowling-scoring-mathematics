# Cross-Disciplinary Mathematical Connections

Catalogue of connections between ten-pin bowling scoring and other mathematical fields.
Organised by tier (depth/novelty of connection) and inclusion status.

---

## Tier 1 — Deep Structural Connections (INCLUDE)

### 1. Statistical Mechanics / Partition Function
Cooper-Kennedy's transfer matrix IS a 1D lattice model partition function. Define
Z(β) = Σ exp(β·S(r)) over all games r. The substitution t = exp(β) converts the
generating function into a partition function. The 4 bonus states are "spin states"
with nearest-neighbour interactions spanning 2 sites.

**Yields:**
- Free energy F(β) = -β⁻¹ ln Z(β); derivatives give all cumulants
- Phase transition between "cold" (open frames dominate) and "hot" (consecutive strikes)
- Saddle-point method for asymptotic score distribution
- Connection to Ising model (1D, 4 states, range-2 interaction)
- Temperature parameter interpolates between uniform ensemble (β=0) and perfect game (β→∞)

### 2. Large Deviations (Gärtner-Ellis Theorem)
Frame scores form a 2-dependent stationary sequence. The cumulant generating function
Λ(β) = lim N⁻¹ ln E[exp(β·S_N)] exists (from largest eigenvalue of T(exp(β))).

**Yields:**
- Pr(S_N/N ≥ x) ≈ exp(-N·I(x)) where I(x) = sup_β [βx - Λ(β)]
- Exponentially precise tail bounds — far sharper than CLT
- Rate function I(30) gives exact exponential decay of perfect game probability
- Connects to the partition function via Legendre transform

### 3. Number Theory — Fibonacci Connection
The number of ways to place k non-adjacent strikes in 9 frames is C(10-k, k).
Sum over k: Σ C(10-k, k) = 89 = F₁₁ (11th Fibonacci number).

**Yields:**
- Clean theorem linking strike placement to Fibonacci numbers
- Follows from the standard identity: binary strings of length n with no adjacent 1s = F(n+2)
- Generalises: for N frames, non-adjacent strike placements sum to F(N+2)

---

## Tier 2 — Algebraically Clean (INCLUDE)

### 4. Transformation Monoid / Krohn-Rhodes Theory
The bonus state transitions generate a monoid M = ⟨τ_O, τ_P, τ_S⟩ acting on 4 states.
- τ_O: constant map to (0,0)
- τ_P: constant map to (1,0)
- τ_S: maps {(0,0),(1,0)} → (1,1) and {(1,1),(2,1)} → (2,1)
- τ_S² = constant map to (2,1)
- |M| = 5 elements

**Yields:**
- M is aperiodic (no non-trivial group component)
- Krohn-Rhodes complexity = 0
- Formal proof that the scoring system is purely irreversible/dissipative
- No computation in the bonus system is "undoable"

### 5. Dynamical Systems — Attractors and Relaxation
The bonus state system has two attractors:
- Cold attractor: (0,0) — stable under open frames
- Hot attractor: (2,1) — stable under consecutive strikes

**Yields:**
- Heating time (cold → hot) = 2 consecutive strikes
- Cooling time (hot → cold) = 2 non-strike frames
- Asymmetry: cooling loses the 3× multiplier on 10-pin balls, heating gains it
- This asymmetry is WHY the system rewards consistency
- Lyapunov exponent analysis of sensitivity to perturbation
- Connection to symbolic dynamics: topological entropy of bonus-state subshift

### 6. Tropical Geometry
Tropicalise the transfer matrix: replace (+, ×) with (max, +).

**Yields:**
- Tropical eigenvalue = 30 (maximum per-frame score)
- Tropical eigenvector identifies (2,1) as the dominant state
- Tropicalised scoring function computes max single-ball contribution
- Constraint surface tropicalises to a polyhedral complex

### 7. Coding Theory — Convolutional Codes
The 4-state bonus structure is a rate-R convolutional code.

**Yields:**
- The DP IS the Viterbi algorithm
- Trellis complexity ≈ 56 bits, consistent with compression from 62.31 to 5.8 bits
- Free distance relates to minimum pin changes between score levels
- Natural framework for the channel capacity analysis already in the paper

### 8. Ehrhart Theory
Open-frame score distribution = Ehrhart function of a hyperplane slice through
a product of N simplices in R^{2N}.

**Yields:**
- Volume of score level set is piecewise polynomial of degree 2N-1
- Ehrhart-Macdonald reciprocity gives duality in open-frame score distribution
- Connects to the theory of lattice point counting in polytopes

---

## Tier 3 — Elegant Observations (CATALOGUE ONLY — NOT INCLUDING YET)

### 9. Category Theory
Category Bowl with objects B(N,M,K) and score-preserving embeddings as morphisms.
- K defines a filtration: B(N,M,0) ↪ B(N,M,1) ↪ B(N,M,2)
- No non-trivial automorphisms for K ≥ 1 (bonuses break frame-permutation symmetry)
- Scoring function is a natural transformation

### 10. Morse Theory / Geometry of Game Space
Continuous relaxation of game space is product of N simplices.
- Scoring function is piecewise-linear on the stratified space
- Level sets change topology only at strata boundaries (marks)
- Open-frame preimage is a convex polytope

### 11. Boolean Algebra / Binary Decision Diagrams
- Scoring function representable as MTBDD (multi-terminal BDD)
- BDD width at each frame boundary = number of DP states
- BDD complexity is polynomial in N (despite exponential game space)

### 12. Multifractal Spectrum
Rényi dimensions of score distribution:
- D₀ = 1 (full support)
- D₁ = H₁/ln(301) ≈ 0.70 (information dimension)
- D∞ = H∞/ln(301) ≈ 0.61
- Gap D₀ - D∞ = 0.39 quantifies non-uniformity

### 13. Braid Theory (Thin Connection)
Bonus dependency strands cross when consecutive strikes occur.
- Commmutativity of addition trivialises the braid structure
- If bonus accumulation were non-commutative, braiding would matter
- Characterises WHY bowling scoring is simpler than it could be

---

## Physics / Astronomy Analogies (CATALOGUE ONLY)

### 14. Nuclear Chain Reaction Analogy
Strike = fission event releasing "bonus neutrons" (look-ahead).
If next frame is also a strike, neutrons trigger another reaction.
Critical mass = 2 consecutive strikes (the double).
Below threshold, chain dies (relaxation to (0,0)).

### 15. Gravitational Slingshot / Orbital Mechanics
Consecutive strikes are like chained gravitational assists.
Each boost sets up the next. 2-frame relaxation = sphere of influence.

### 16. CMB / Thermal Distribution
Score distribution's concentration around mode 77 with sparse tails
resembles a near-thermal distribution. The partition function temperature
parameter β makes this analogy precise (not just metaphorical).

---

## Recurrence / Difference Equations (INCLUDE — support existing Section 8)

### 17. Matrix Recurrence for Moment Generating Function
The MGF M_k(β) = E[exp(β·s_k)] satisfies:
  M_k(β) = T(exp(β)) · M_{k-1}(β)
Solution: M_k = T(exp(β))^k · M_0

**Yields:**
- Eigenvalues of T(exp(β)) control everything
- λ₁(β) = cumulant generating function per frame
- λ₂/λ₁ = convergence rate to asymptotic distribution
- Spectral gap = mixing rate of bonus-state chain
