# Direction 9: Concentration Inequalities for Persistent Homology of Dependent Point Clouds, with Applications to Long-Memory Time Series

*Added: 2026-03-18. Synthesizes Direction 6 (concentration inequalities for random complexes) and Direction 8 (topological memory in financial markets).*

---

## Summary

Direction 6 asks: how tightly do persistent Betti numbers concentrate for **random complexes built from i.i.d. samples**? Direction 8 asks: can persistent homology of **delay-embedded financial time series** detect long-range memory (Hurst exponent)? Neither is complete alone. Direction 6 lacks application and stops at i.i.d. models. Direction 8 has no statistical foundation — the topological Hurst estimator it proposes is heuristic without concentration results.

This direction unifies them by extending the concentration machinery of Direction 6 from i.i.d. to **mixing, long-range dependent processes**, then deploying the result to give Direction 8 its theoretical backbone. The unifying object is fractional Brownian motion (fBm), whose Hurst exponent $H$ controls both the memory structure and — as we conjecture and aim to prove — the rate at which topological features concentrate.

---

## The Core Problem

Let $\{X_t\}_{t \geq 0}$ be a stationary stochastic process. Form the sliding window point cloud:

$$P_{d,\tau}^{(n)} = \left\{(X_t, X_{t+\tau}, \ldots, X_{t+(d-1)\tau})\right\}_{t=1}^{n} \subset \mathbb{R}^d$$

Let $\beta_k^{s,t}(P_{d,\tau}^{(n)})$ denote the persistent Betti numbers of $P_{d,\tau}^{(n)}$ under the Vietoris–Rips filtration. Define the **barcode count function**:

$$L_n^{(k)}(\epsilon) = \#\left\{\text{bars in } \text{Dgm}_k(P_{d,\tau}^{(n)}) \text{ with lifetime} > \epsilon\right\}$$

**Central question:** How does $L_n^{(k)}(\epsilon)$ concentrate around $\mathbb{E}[L_n^{(k)}(\epsilon)]$, and how does the concentration rate depend on the memory structure of $\{X_t\}$?

---

## The Gap: i.i.d. vs. Dependent

Direction 6 addresses the i.i.d. case via the Linial–Meshulam random complex model. The standard proof uses **Azuma–Hoeffding**:

$$P\!\left(|f(X_1, \ldots, X_n) - \mathbb{E}[f]| > t\right) \leq 2\exp\!\left(\frac{-2t^2}{\sum_i c_i^2}\right)$$

where $c_i$ are the bounded differences constants. This requires **independence**. For long-memory processes, the dependence structure destroys the martingale property needed.

**What fails:** If $\{X_t\}$ is fBm with $H > 0.5$, then $\text{Cov}(X_0, X_t) \sim t^{2H-2}$, which decays to zero but **not summably** — the process is not $L^1$-mixing. Standard concentration tools break down or give vacuous bounds.

**The gap:** No concentration results exist for persistent Betti numbers of point clouds from long-range dependent processes. The entire statistical foundation for topological analysis of correlated time series is missing.

---

## Mathematical Framework

### Step 1: Block Decomposition for Mixing Processes

Even though fBm with $H < 1$ is not strongly mixing in the traditional sense, its **increments** are strongly mixing with rate $\psi(k) \sim k^{2H-2}$ (Hurst, Rosenblatt). Partition the index set $\{1, \ldots, n\}$ into blocks of size $b_n$ (to be optimized):

$$\{1,\ldots,n\} = B_1 \cup B_2 \cup \ldots \cup B_{n/b_n}$$

Points in non-adjacent blocks are approximately independent (mixing decouples them). Apply Azuma–Hoeffding blockwise, collecting cross-block error terms controlled by the mixing rate.

### Step 2: The Concentration Bound

**Conjecture (main result to prove):**

For fBm $\{B^H_t\}$ with Hurst exponent $H \in (1/2, 1)$, the barcode count $L_n^{(1)}(\epsilon)$ satisfies:

$$P\!\left(\left|L_n^{(1)}(\epsilon) - \mathbb{E}[L_n^{(1)}(\epsilon)]\right| > t\right) \leq 2\exp\!\left(\frac{-t^2}{C(H) \cdot n^{2H}}\right)$$

where $C(H)$ is an explicit constant depending on $H$, $d$, $\tau$, and $\epsilon$.

**Key structural observation:** The variance factor $n^{2H}$ replaces $n$ from the i.i.d. case. This follows from the variance scaling of fBm: $\text{Var}(B^H_n) = n^{2H}$. As $H \to 1/2$, the bound recovers the i.i.d. rate $\exp(-t^2/Cn)$. As $H \to 1$, the bound loosens as $\exp(-t^2/Cn^2)$ — reflecting that maximum memory makes concentration hardest.

### Step 3: Scaling Law for the Expectation

Use the self-similarity of fBm — $\{B^H_{ct}\} \stackrel{d}{=} \{c^H B^H_t\}$ — to constrain the form of $\mathbb{E}[L_n^{(1)}(\epsilon)]$.

Under the rescaling $t \mapsto ct$, the point cloud $P_{d,\tau}$ transforms as $P_{d,\tau} \mapsto c^H P_{d,\tau}$, and the filtration parameter scales as $\epsilon \mapsto c^H \epsilon$. Therefore:

$$\mathbb{E}[L_n^{(1)}(\epsilon)] = \mathbb{E}[L_n^{(1)}(c^H \epsilon)] \cdot (\text{combinatorial factor})$$

This self-consistency equation constrains $\mathbb{E}[L_n^{(1)}(\epsilon)]$ to be a power law in $\epsilon$:

$$\mathbb{E}[L_n^{(1)}(\epsilon)] \sim n \cdot \epsilon^{-\alpha(H)}$$

**The scaling exponent $\alpha(H)$** encodes the Hurst exponent in the barcode count. If $\alpha(H)$ is strictly monotone in $H$ (which numerical experiments will check first), then $\epsilon \mapsto L_n^{(1)}(\epsilon)$ is a consistent estimator of $H$.

---

## The Topological Hurst Estimator

Given the scaling law, define the **topological Hurst estimator** $\hat{H}_{\text{top}}$:

1. Embed the time series: compute $P_{d,\tau}^{(n)}$.
2. Compute $\text{Dgm}_1(P_{d,\tau}^{(n)})$ via Ripser.
3. For a range of $\epsilon$ values, compute $L_n^{(1)}(\epsilon) = \#\{\text{bars with lifetime} > \epsilon\}$.
4. Fit $\log L_n^{(1)}(\epsilon) = -\hat{\alpha} \log \epsilon + \text{const}$ by OLS on the log-log plot.
5. Invert $\hat{\alpha} \mapsto \hat{H}$ using the calibrated function $\alpha(H)$.

**Theoretical properties to establish:**
- **Consistency:** $\hat{H}_{\text{top}} \to H$ in probability as $n \to \infty$. Follows from consistency of $\hat{L}_n$ and the concentration bound.
- **Rate of convergence:** From the concentration bound, $|\hat{H}_{\text{top}} - H| = O(n^{H-1/2} / \sqrt{n}) = O(n^{H-1})$. This matches the known minimax rate for Hurst estimation under long-range dependence (Istas & Lang 1997).
- **Robustness:** By the stability theorem for persistence diagrams ($d_B(\text{Dgm}(f), \text{Dgm}(g)) \leq \|f-g\|_\infty$), $\hat{H}_{\text{top}}$ is stable under monotone transforms of the time series — a property classical estimators (R/S, DFA, Whittle) do not share.

---

## Multifractal Extension (Direction 8 → Mandelbrot)

Mandelbrot's MMAR posits that real market returns are **multifractal**: different time scales exhibit different local Hurst exponents $h(t)$, with distribution described by the multifractal spectrum $f(\alpha)$.

The full persistence diagram $\text{Dgm}_1(P_{d,\tau}^{(n)})$ is multiscale by construction. Define the **scale-stratified barcode count**:

$$L_n^{(1)}(\epsilon_1, \epsilon_2) = \#\left\{\text{bars with birth in } [\epsilon_1, \epsilon_2] \text{ and lifetime} > \delta\right\}$$

This probes the topology at filtration scale $[\epsilon_1, \epsilon_2]$, corresponding to a specific time horizon. If the process is multifractal, the local scaling exponent $\alpha(\epsilon)$ computed at scale $\epsilon$ should recover $f^{-1}(\alpha(\epsilon))$ from the multifractal spectrum.

**Proposed result:** For a multifractal process with spectrum $f(\alpha)$, the scale-stratified barcode count satisfies:

$$\log L_n^{(1)}(\epsilon_1, \epsilon_2) \sim -f^{-1}(\alpha(\epsilon)) \cdot \log(\epsilon_2 - \epsilon_1)$$

This would make persistence diagrams a **topological multifractal analyzer** — reading the full Mandelbrot spectrum off the diagram geometry.

---

## Proposed Contributions (in order of difficulty)

| # | Contribution | Type | Difficulty |
|---|-------------|------|------------|
| 1 | Numerical calibration of $\alpha(H)$ for fBm delay embeddings | Computational | Low |
| 2 | Consistency of $\hat{H}_{\text{top}}$ assuming the scaling law | Statistical | Medium |
| 3 | Concentration inequality for mixing point clouds (block martingale) | Probabilistic | High |
| 4 | Proof of the scaling law via fBm self-similarity | Stochastic processes | High |
| 5 | Multifractal extension: topological recovery of $f(\alpha)$ | Multifractal analysis | Very high |

A paper with contributions 1–3 is already publishable. Contributions 4–5 would make it a strong journal paper.

---

## Why This Direction Is Strictly Better Than 6 or 8 Alone

**Direction 6 alone:** Abstract, no application. Proves concentration for an artificial model (Linial–Meshulam) that does not arise in practice. The paper answers a question that combinatorialists care about but no one else does.

**Direction 8 alone:** Interesting application, no theory. The topological Hurst estimator is a heuristic. Without concentration results, you cannot state consistency, give confidence intervals, or make claims about statistical power.

**Direction 9 (combined):**
- The concentration result (Direction 6 machinery) is no longer abstract — it is the *proof of consistency* for a concrete new estimator.
- The financial application (Direction 8) is no longer heuristic — it has a complete statistical theory behind it.
- The paper speaks to three communities simultaneously: **stochastic topology** (concentration for dependent processes), **statistical TDA** (new estimator with rates), and **mathematical finance** (topological approach to Mandelbrot's memory).
- The key formula $\text{Var} \sim n^{2H}$ cleanly unifies both directions: $H = 1/2$ recovers Direction 6 exactly.

---

## Empirical Validation

### Synthetic experiments

| Experiment | Parameters | Goal |
|-----------|-----------|------|
| fBm simulation | $H \in \{0.3, 0.5, 0.6, 0.7, 0.9\}$, $n = 5000$, $d = 3$, $\tau = 1$ | Calibrate $\alpha(H)$ |
| Concentration check | 500 realizations per $H$, compare empirical vs. theoretical bound | Validate the bound |
| Estimator comparison | $\hat{H}_{\text{top}}$ vs. R/S, DFA, Whittle on fBm | Benchmark accuracy |
| Monotone robustness | Apply $x \mapsto x^3$ before embedding; recheck $\hat{H}_{\text{top}}$ | Test stability advantage |

### Real data experiments

| Dataset | Source | Goal |
|---------|--------|------|
| S&P 500 daily log-returns (1950–2024) | Yahoo Finance / FRED | Estimate $H$ per decade; compare to crisis periods |
| VIX index | CBOE | Test topological long memory during stress regimes |
| FX rates (EUR/USD, JPY/USD) | Federal Reserve H.10 | Check multifractal extension |

All datasets are freely available. Processing $n = 10{,}000$ points in $\mathbb{R}^3$ takes under 10 seconds in Ripser.

---

## Why It Fits Our Constraints

- **Compute:** fBm simulation via Davies-Harte ($O(n \log n)$), Ripser for PH. Entire empirical section runs in under 2 hours on a laptop.
- **Math intensity:** Very high. Requires probability theory (mixing, martingales, concentration), stochastic processes (fBm, self-similarity, multifractals), and persistent homology (stability, structure theorem, random topology).
- **Data:** Synthetic (controlled) + freely available financial data (no proprietary sources).
- **Novelty:** The concentration bound for dependent complexes is the first of its kind. The topological Hurst estimator is the first TDA-based estimator with provable statistical guarantees.

---

## Target Venues

| Venue | Fit |
|-------|-----|
| *Foundations of Computational Mathematics* | Theory-heavy, TDA-friendly |
| *Stochastic Processes and their Applications* | Probability + processes angle |
| *Journal of Applied and Computational Topology* | Core TDA venue |
| *Quantitative Finance* | If empirical results are strong |
| *Bernoulli* | Statistical theory angle |

---

## Key References

**Concentration and random topology:**
- Kahle, "Topology of Random Clique Complexes," DCG 2009
- Kahle, "Sharp Vanishing Thresholds for Cohomology of Random Flag Complexes," Annals of Math 2014
- Boucheron, Lugosi, Massart, *Concentration Inequalities*, Oxford 2013
- Linial, Meshulam, "Homological Connectivity of Random 2-Complexes," Combinatorica 2006

**Fractional Brownian motion and long memory:**
- Taqqu, "Fractional Brownian Motion and Long-Range Dependence," in *Theory and Applications of Long-Range Dependence*, Birkhäuser 2003
- Istas, Lang, "Quadratic Variations and Estimation of the Local Hölder Index of a Gaussian Process," Annales de l'IHP 1997
- Davies, Harte, "Tests for Hurst Effect," Biometrika 1987

**TDA for time series:**
- Perea, Harer, "Sliding Windows and Persistence," FoCM 2015
- Gidea, Katz, "Topological Data Analysis of Financial Time Series," Physica A 2018

**Mandelbrot and multifractals:**
- Mandelbrot, Hudson, *The Misbehavior of Markets*, Basic Books 2004
- Mandelbrot, "A Multifractal Model of Asset Returns," Cowles Foundation 1997

**Persistence theory:**
- Cohen-Steiner, Edelsbrunner, Harer, "Stability of Persistence Diagrams," DCG 2007
- Chazal et al., *The Structure and Stability of Persistence Modules*, Springer 2016

---

## Relationship to Other Directions

- **Builds on Direction 6:** Uses its concentration framework as a starting point; extends from i.i.d. to mixing processes.
- **Gives Direction 8 its foundation:** The concentration bound is exactly the missing statistical theory for the topological Hurst estimator.
- **Connects to Direction 2:** Fréchet means of persistence diagrams from fBm realizations inherit the non-uniqueness problem — the concentration bound here would also clarify when Fréchet means are well-behaved.
- **Connects to Direction 4:** The mixing-block technique generalizes to graphs with correlated edge weights, potentially giving stability bounds under dependent coarsening.

---

*Document created: 2026-03-18. Synthesizes Directions 6 and 8.*
