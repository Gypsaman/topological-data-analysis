# Persistent Homology

## Overview

**Persistent homology** is the central computational tool of TDA. It tracks how topological features — connected components, loops, voids — appear and disappear as we vary a scale parameter across a filtration. The key insight: features that persist across a wide range of scales are likely genuine structure; features that appear and disappear quickly are likely noise.

---

## 1. Motivation: The Scale Problem

Classical homology assigns a single topological summary to a space. But for point cloud data, the choice of scale matters enormously:
- At very small scales: many disconnected components (noisy)
- At very large scales: everything connects into one blob
- At intermediate scales: genuine topological structure emerges

Persistent homology resolves this by tracking topology **across all scales simultaneously**, encoding the result as a multi-scale summary (persistence diagram or barcode).

---

## 2. Filtrations and Persistent Homology Groups

Given a filtration $K_0 \subseteq K_1 \subseteq \cdots \subseteq K_m = K$, the inclusion maps $\iota_{i,j}: K_i \hookrightarrow K_j$ for $i \leq j$ induce homomorphisms on homology:

$$f_k^{i,j}: H_k(K_i) \to H_k(K_j)$$

**Definition:** The $(i,j)$-**persistent $k$-th homology group** is:

$$H_k^{i,j} = \text{im}(f_k^{i,j}) = Z_k(K_i) \big/ (B_k(K_j) \cap Z_k(K_i))$$

This captures the $k$-dimensional homology classes **born** at or before $K_i$ that still **survive** at $K_j$.

**Persistent Betti number:** $\beta_k^{i,j} = \text{rank}(H_k^{i,j})$ — the number of $k$-dimensional features born by step $i$ still alive at step $j$.

---

## 3. Birth and Death Pairs

Each homological feature can be associated with:
- **Birth time** $b$: the filtration index at which it first appears as a non-trivial homology class
- **Death time** $d$: the first index at which it merges with an older class or becomes a boundary (dies)

with $b < d$. Features with $d = +\infty$ are called **essential** (they persist forever).

**Persistence** of a feature: $\text{pers} = d - b$.

**Elder Rule:** When a new simplex merges two components (or kills a feature), the *younger* feature (born more recently) dies; the *older* one (born earlier) survives. This ensures a canonical pairing between birth and death events.

---

## 4. Persistence Diagrams and Barcodes

### 4.1 Persistence Diagram

The **$k$-dimensional persistence diagram** $\text{Dgm}_k(f)$ is the multiset of points $(b, d) \in \{(x,y) : x < y\} \cup \{+\infty\}$ corresponding to birth–death pairs of $k$-dimensional homology classes.

- Points far from the diagonal (large $d - b$) represent **significant topological features**
- Points near the diagonal (small $d - b$) represent **noise**
- The diagonal $\Delta = \{(x,x)\}$ is included with infinite multiplicity (for technical reasons involving distances)

### 4.2 Barcode

The **barcode** is the equivalent representation as a multiset of intervals $[b, d)$, one per persistence pair. Visualized as a collection of horizontal bars:

```
H0 (components): ─────────────────────────────────────────── (never dies)
                 ────────
                 ──────────────
H1 (loops):                    ──────────────────
                                      ────────
H2 (voids):                                      ──────
             0   ε₁   ε₂   ε₃   ε₄   ε₅   ε₆  ε₇
```

**Reading a barcode:**
- Each bar represents a topological feature
- Bar length = persistence (how long the feature exists)
- Long bars: genuine structure
- Short bars: topological noise

---

## 5. The Persistence Algorithm

### 5.1 Boundary Matrix

Order all $m$ simplices of the filtration as $\sigma_1, \sigma_2, \ldots, \sigma_m$ (consistent with filtration order: if $\sigma_i \subseteq \sigma_j$ then $i < j$). The **boundary matrix** $\partial$ is the $m \times m$ matrix over $\mathbb{F}$ where $\partial[i,j] = $ coefficient of $\sigma_i$ in $\partial(\sigma_j)$.

The matrix is strictly upper triangular and typically sparse.

### 5.2 Column Reduction Algorithm

**Goal:** Reduce $\partial$ to a matrix $R$ via left-to-right column operations (column additions) to extract persistence pairs.

**Pivot:** $\text{low}(j) = $ index of the lowest nonzero entry in column $j$.

**Algorithm:**
```
for j = 1 to m:
    while ∃ j' < j with low(j') = low(j):
        R[:, j] += R[:, j']   (over F)
    end while
end for
```

**Output:**
- If column $j$ reduces to nonzero with pivot $i = \text{low}(j)$: persistence pair $(\sigma_i, \sigma_j)$ — feature born at $\sigma_i$, died at $\sigma_j$
- If column $j$ reduces to zero AND $j$ is never a pivot: $\sigma_j$ = **essential feature** (infinite persistence)
- Complexity: $O(m^3)$ worst case; practically much faster due to sparsity

### 5.3 Twist Optimization

The **Twist/Clearing algorithm** (Chen & Kerber, 2011) exploits $\partial^2 = 0$: if column $j$ is already cleared (zeroed) in dimension $k$, the corresponding column in dimension $k-1$ need not be reduced. Processing from highest to lowest dimension and clearing known pairs dramatically accelerates computation — this is the basis of Ripser's efficiency.

---

## 6. Stability Theorems

Stability is what makes TDA scientifically rigorous: persistence diagrams change *continuously* with the input data.

### 6.1 Bottleneck Distance

Given two persistence diagrams $D_1$ and $D_2$, the **bottleneck distance** is:

$$d_B(D_1, D_2) = \inf_{\gamma} \sup_{x \in D_1} \|x - \gamma(x)\|_\infty$$

where the infimum is over all bijections $\gamma: D_1 \to D_2$ (matching points to points, or to their projection on the diagonal). Each unmatched point can be matched to its nearest point on the diagonal at cost equal to its persistence/2.

### 6.2 Wasserstein Distance

The **$p$-Wasserstein distance** ($p \geq 1$):

$$W_p(D_1, D_2) = \left[\inf_{\gamma} \sum_{x \in D_1} \|x - \gamma(x)\|_\infty^p\right]^{1/p}$$

As $p \to \infty$, $W_p \to d_B$. The $W_1$ and $W_2$ distances are commonly used in statistics and machine learning.

### 6.3 The Stability Theorem

**Theorem (Cohen-Steiner, Edelsbrunner, Harer, 2007):** Let $f, g: |K| \to \mathbb{R}$ be tame functions on a compact space. Then:

$$d_B(\text{Dgm}(f), \text{Dgm}(g)) \leq \|f - g\|_\infty$$

**Interpretation:** A perturbation of size $\varepsilon$ in the input (e.g., noise in data) can move points in the persistence diagram by at most $\varepsilon$ in the bottleneck distance. Short-lived features (near the diagonal) are noise-sensitive; long-lived features are robust.

This theorem validates using persistence diagrams as stable data descriptors.

---

## 7. The Structure Theorem

### 7.1 Persistence Modules

A **(pointwise finite-dimensional) persistence module** $\mathbb{V}$ over $\mathbb{R}$ is a collection of vector spaces $\{V_t\}_{t \in \mathbb{R}}$ and linear maps $v^{s,t}: V_s \to V_t$ for $s \leq t$, satisfying functoriality ($v^{t,t} = \text{id}$, $v^{s,t} = v^{r,t} \circ v^{s,r}$).

### 7.2 Interval Modules

For an interval $I \subseteq \mathbb{R}$, the **interval module** $\mathbb{k}^I$ is:
$$(\mathbb{k}^I)_t = \begin{cases} \mathbb{k} & t \in I \\ 0 & t \notin I \end{cases}, \quad \text{maps} = \begin{cases} \text{id} & s,t \in I \\ 0 & \text{otherwise} \end{cases}$$

### 7.3 Structure Theorem

**Theorem (Zomorodian–Carlsson 2005; Crawley-Boevey 2012):** Every pointwise finite-dimensional persistence module over a field $\mathbb{k}$ decomposes **uniquely** (up to isomorphism and reordering) as:

$$\mathbb{V} \cong \bigoplus_j \mathbb{k}^{I_j}$$

for a unique multiset of intervals $\{I_j\}$.

**Significance:** The persistence module arising from a filtration decomposes cleanly into interval modules — one per persistence pair. The multiset $\{I_j\}$ IS the barcode. This algebraic result justifies the entire computational pipeline.

**Why this breaks in 2+ parameters:** Multidimensional persistence modules (filtrations over $\mathbb{R}^n$, $n \geq 2$) do NOT admit such a clean decomposition — this is the central open problem in TDA theory.

---

## 8. Algebraic Stability and the Isometry Theorem

### 8.1 Interleaving Distance

Two persistence modules $\mathbb{V}$ and $\mathbb{W}$ are **$\varepsilon$-interleaved** if there exist natural transformations $\phi: \mathbb{V} \to \mathbb{W}[\varepsilon]$ and $\psi: \mathbb{W} \to \mathbb{V}[\varepsilon]$ (where $\mathbb{V}[\varepsilon]_t = V_{t+\varepsilon}$) such that appropriate diagrams commute.

$$d_I(\mathbb{V}, \mathbb{W}) = \inf\{\varepsilon : \mathbb{V}, \mathbb{W} \text{ are } \varepsilon\text{-interleaved}\}$$

### 8.2 Isometry Theorem

**Theorem (Chazal, de Silva, Glisse, Oudot — 2016):**

$$d_B(\text{Dgm}(\mathbb{V}), \text{Dgm}(\mathbb{W})) = d_I(\mathbb{V}, \mathbb{W})$$

The bottleneck distance between persistence diagrams equals the interleaving distance between persistence modules. This is the deepest stability result: it characterizes when two topological summaries are close in terms of an intrinsic algebraic distance.

---

## 9. Vectorizations of Persistence Diagrams

Persistence diagrams live in a non-Euclidean space, making them incompatible with standard ML pipelines. Several vectorizations have been developed:

### 9.1 Persistence Landscapes

Introduced by Peter Bubenik (2015). The **persistence landscape** $\lambda: \mathbb{N} \times \mathbb{R} \to \mathbb{R}$ is defined by "tent functions" over persistence pairs, stacked by height:

$$\lambda(k, t) = k\text{-th largest value of } \min(t - b_i, d_i - t) \text{ over all pairs } (b_i, d_i)$$

**Properties:**
- Lives in a Banach space (enables means, standard deviations, statistical tests)
- 1-Lipschitz with respect to the 1-Wasserstein distance
- Stable under perturbations

### 9.2 Persistence Images

Introduced by Adams et al. (2017, JMLR). Map persistence diagrams to 2D images by:
1. Weight each point $(b, d)$ by a persistence-weighted function
2. Place Gaussian kernels at each point in the birth-persistence plane
3. Discretize into a finite-dimensional vector

**Properties:**
- Finite-dimensional (easy for ML)
- Stable under Wasserstein distance
- Computationally efficient

### 9.3 Other Vectorizations

| Method | Space | Stability | Reference |
|--------|-------|-----------|-----------|
| Persistence landscapes | Banach | Wasserstein | Bubenik, 2015 |
| Persistence images | $\mathbb{R}^{m \times m}$ | Wasserstein | Adams et al., 2017 |
| Sliced Wasserstein kernel | RKHS | Stable | Carrière et al., 2017 |
| Persistence Fisher kernel | RKHS | Stable | Le & Yamada, 2018 |
| PersLay | Learnable | Varies | Carrière et al., 2020 |
| Betti curves | $L^2$ functions | Stable | — |
| Euler characteristic curve | $L^2$ functions | Stable | — |

---

## 10. Zigzag Persistence

**Standard persistence** uses monotone filtrations: $K_0 \hookrightarrow K_1 \hookrightarrow \cdots \hookrightarrow K_n$ (only additions). **Zigzag persistence** (Carlsson & de Silva, 2010) allows:

$$K_0 \leftrightarrow K_1 \leftrightarrow K_2 \leftrightarrow \cdots$$

where each arrow can be either an inclusion or a restriction (deletion). The resulting zigzag diagrams of homology groups still decompose into interval modules by Gabriel's theorem, giving a valid barcode.

**Applications:**
- Tracking topology of evolving/moving point clouds
- Level-set persistence
- Bootstrap sampling for statistical TDA tests
- Mapper analysis with overlapping bins

---

## 11. Extended Persistence

Introduced by Cohen-Steiner, Edelsbrunner, and Harer (2009). Extends the filtration "beyond" the complex using Poincaré/Lefschetz duality to capture topology at the "superlevel set" side. This pairs essential features that standard persistence leaves unpaired.

Extended persistence enables a full pairing of all homology classes (including relative homology classes) into finite intervals.

---

## Summary: The TDA Pipeline

```
Raw Data (point cloud, image, network, time series)
        ↓
Construct Filtration
(Vietoris-Rips, Alpha, Sublevel-set, Cubical...)
        ↓
Compute Persistent Homology
(Column reduction / cohomology algorithm)
        ↓
Persistence Diagrams / Barcodes
        ↓
Vectorize or Compare
(Landscapes, Images, Wasserstein distance...)
        ↓
Downstream Analysis
(Machine learning, hypothesis testing, visualization)
```

---

## Key References

| Paper | Authors | Year | Contribution |
|-------|---------|------|-------------|
| *Topological persistence and simplification* | Edelsbrunner, Letscher, Zomorodian | 2002 | Introduced persistence algorithm |
| *Computing persistent homology* | Zomorodian, Carlsson | 2005 | Algebraic formulation, Structure Theorem |
| *Stability of persistence diagrams* | Cohen-Steiner, Edelsbrunner, Harer | 2007 | Stability theorem |
| *Proximity of persistence modules* | Chazal, Cohen-Steiner, Glisse, Guibas, Oudot | 2009 | Algebraic stability |
| *Decomposition of persistence modules* | Crawley-Boevey | 2015 | Structure theorem for $\mathbb{R}$-indexed modules |
| *The Structure and Stability of Persistence Modules* | Chazal, de Silva, Glisse, Oudot | 2016 | Isometry theorem |
| *Zigzag Persistence* | Carlsson, de Silva | 2010 | Zigzag theory |
| *Persistence landscapes* | Bubenik | 2015 | Statistical topology |
| *Persistence images* | Adams et al. | 2017 | ML-compatible vectorization |

---

*Previous: [01_foundations.md](01_foundations.md) | Next: [03_algorithms_and_software.md](03_algorithms_and_software.md)*
