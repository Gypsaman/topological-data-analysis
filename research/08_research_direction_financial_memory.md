# Direction 8: Topological Memory in Financial Markets

*Added: 2026-03-18. Inspired by Mandelbrot's "The Misbehavior of Markets" and existing TDA-in-finance literature.*

---

## Summary

Financial markets exhibit **long-range dependence** — correlations between price changes that decay as power laws, not exponentially. The classical tool for quantifying this is the **Hurst exponent** $H \in (0,1)$, with $H > 0.5$ indicating persistent trends (long memory) and $H < 0.5$ indicating mean-reversion (short memory). Mandelbrot's mature model, the **Multifractal Model of Asset Returns (MMAR)**, goes further: markets have a *spectrum* of Hurst exponents at different time scales, not a single one.

This direction proposes using **persistent homology of delay-embedded time series** as a richer topological invariant that captures the full multiscale memory structure of financial time series — replacing the scalar $H$ with a persistence diagram.

---

## Mandelbrot's Framework (Key Concepts)

From *The Misbehavior of Markets* (Mandelbrot & Hudson, 2004):

| Concept | Mathematical Content | Classical Tool |
|---------|---------------------|---------------|
| Long memory ("Joseph effect") | $\text{Cov}(X_0, X_t) \sim t^{2H-2}$, $H > 0.5$ | Hurst exponent, R/S analysis |
| Fat tails ("Noah effect") | $P(|X| > x) \sim x^{-\alpha}$, $\alpha < 2$ | Stable distributions, Hill estimator |
| Multifractality | Scaling exponent $h(q)$ varies with moment $q$ | Multifractal spectrum $f(\alpha)$ |
| Self-similarity | $\{X_{ct}\} \stackrel{d}{=} \{c^H X_t\}$ for fBm | Log-log regression |

The model of choice for long memory alone is **fractional Brownian motion (fBm)** $B^H_t$, the unique Gaussian process with stationary increments and self-similarity index $H$.

---

## The TDA Bridge: Delay Embeddings

Given a univariate time series $\{x_t\}_{t=1}^N$, the **sliding window embedding** (Takens-type) at dimension $d$ and lag $\tau$ produces the point cloud:

$$P_{d,\tau} = \left\{(x_t,\, x_{t+\tau},\, x_{t+2\tau},\, \ldots,\, x_{t+(d-1)\tau})\right\}_{t=1}^{N-(d-1)\tau} \subset \mathbb{R}^d$$

Compute the Vietoris–Rips persistent homology of $P_{d,\tau}$.

**Geometric intuition:**
- If $\{x_t\}$ has no memory ($H = 0.5$, random walk increments), $P_{d,\tau}$ is a diffuse i.i.d. cloud — no persistent loops.
- If $\{x_t\}$ has strong persistence ($H \gg 0.5$), correlations stretch the cloud into elongated structures — $H_1$ features (loops) persist longer.
- If $\{x_t\}$ is anti-persistent ($H < 0.5$), the cloud is compressed and oscillatory — features appear and die quickly.

This was used in Gidea & Katz (2018) for crash detection, but without the Hurst exponent connection and without theoretical justification.

---

## The Open Gap

**What exists:**
- Perea & Harer (2015): sliding window PH detects periodicity — $H_1$ features are persistent iff the signal is periodic.
- Gidea & Katz (2018): empirical evidence that TDA detects pre-crisis regimes in financial data.
- Thoppe & Yogeshwaran (2016), Kahle (2011): random topology for **i.i.d.** point processes.

**What is missing:**
- No theoretical result linking persistence diagram statistics to $H$ for **correlated** processes (fBm or long-memory processes).
- No "topological Hurst estimator" with provable consistency or rate of convergence.
- No topological analog of the multifractal spectrum.

---

## Proposed Contribution

### Core Conjecture

Let $\{B^H_t\}$ be fractional Brownian motion with Hurst exponent $H$. Let $\text{Dgm}_1(P_{d,\tau}^{(n)})$ be the degree-1 persistence diagram of the sliding window embedding of a length-$n$ discretization. Define:

$$L_n(\epsilon) = \#\{\text{bars in } \text{Dgm}_1 \text{ with lifetime} > \epsilon\}$$

**Conjecture:** $\mathbb{E}[L_n(\epsilon)] \sim n \cdot \epsilon^{-\alpha(H)}$ as $\epsilon \to 0$, where $\alpha(H)$ is a function of $H$ alone (for fixed $d, \tau$).

If $\alpha(H)$ is monotone in $H$, then the empirical version $\hat{L}_n(\epsilon)$ is a **topological Hurst estimator** — reading the Hurst exponent off the log-log slope of the barcode length distribution.

### Specific Results to Prove

1. **Scaling law for fBm:** Prove or establish strong numerical evidence that $\alpha(H)$ exists and is monotone. Use the self-similarity of fBm: under the scaling $B^H_{ct} \stackrel{d}{=} c^H B^H_t$, the point cloud $P_{d,\tau}$ rescales predictably, constraining the form of $\alpha(H)$.

2. **Consistency of the estimator:** Show that the log-log slope estimator $\hat{\alpha}_n \to \alpha(H)$ as $n \to \infty$ (law of large numbers for persistent Betti numbers of dependent point clouds).

3. **Multiscale extension:** For a multifractal process (MMAR), the diagram $\text{Dgm}_1(P_{d,\tau})$ at different filtration scales $\epsilon$ reveals different local Hurst exponents — providing a **topological proxy for the multifractal spectrum** $f(\alpha)$.

4. **Short vs. long memory discrimination:** Define:
   - *Topological short memory index*: total persistence of $H_0$ features (connected components) at small filtration values.
   - *Topological long memory index*: total persistence of $H_1$ features (loops) across all scales.

   Prove that these separate $H < 0.5$ from $H > 0.5$ with statistical consistency.

---

## Why This Is Better Than Classical Methods

| Method | What it captures | Limitations |
|--------|-----------------|------------|
| R/S analysis (Hurst 1951) | Single $H$ | Biased for short series; assumes stationarity |
| DFA (Peng et al. 1994) | Single $H$ per scale | Requires long series; no geometric insight |
| Wavelet estimator | $H$ at each scale | No topological structure; sensitive to wavelet choice |
| **Topological estimator (proposed)** | Full multiscale structure via $\text{Dgm}_1$ | Richer invariant; robust to monotone transforms; handles non-stationarity via windowing |

The topological estimator is **equivariant under monotone transforms** of the time series (by the stability theorem), which classical estimators are not.

---

## Empirical Validation Plan

1. **Synthetic:** Generate fBm with $H \in \{0.3, 0.4, 0.5, 0.6, 0.7, 0.8\}$ using the Davies-Harte or Cholesky method. Compute $\text{Dgm}_1(P_{d,\tau})$ for each. Estimate $\alpha(H)$ from log-log plots.

2. **Real data:** Apply to daily log-returns of equity indices (S&P 500, available freely via Yahoo Finance / FRED). Compare topological Hurst estimates to classical R/S and DFA estimates.

3. **Crisis detection:** Replicate and extend Gidea & Katz (2018) — show that the topological long memory index spikes before known crises (2008, COVID crash 2020).

---

## Why It Fits Our Constraints

- **Compute:** fBm simulation is $O(n^2)$ (Cholesky) or $O(n \log n)$ (Davies-Harte). For $n = 10{,}000$, trivial on a laptop. Ripser handles the point clouds in seconds.
- **Math intensity:** Very high. Requires stochastic processes (fBm, self-similarity), concentration inequalities for dependent processes, and persistent homology theory.
- **Data:** Synthetic (fully controlled) + freely available financial data.
- **Novelty path:** A scaling law $\alpha(H)$ for delay-embedded fBm would be the first rigorous connection between Hurst exponent and persistence diagram statistics. Natural venues: *Foundations of Computational Mathematics*, *Journal of Applied and Computational Topology*, *Quantitative Finance*, or *Stochastic Processes and their Applications*.

---

## Key References

- Mandelbrot, Hudson, *The Misbehavior of Markets*, Basic Books, 2004
- Mandelbrot, "A Multifractal Model of Asset Returns," Cowles Foundation Discussion Paper, 1997
- Perea, Harer, "Sliding Windows and Persistence: An Application of Topological Methods to Signal Analysis," FoCM 2015
- Gidea, Katz, "Topological Data Analysis of Financial Time Series: Landscapes of Crashes," Physica A, 2018
- Taqqu, "Fractional Brownian Motion and Long-Range Dependence," in *Theory and Applications of Long-Range Dependence*, Birkhäuser, 2003
- Thoppe, Yogeshwaran, "On the Rate of Convergence for Central Limit Theorems of Sojourn Times of Gaussian Processes," 2016
- Kahle, "Topology of Random Clique Complexes," DCG 2009
- Davies, Harte, "Tests for Hurst Effect," Biometrika 1987

---

*Document created: 2026-03-18.*
