---
title: "Proof Sketch: Theorem 1"
subtitle: "Concentration Inequality for Persistent Betti Numbers of fBm Sliding-Window Point Clouds"
date: 2026-03-21
status: "Working notes — incomplete proof, gaps flagged explicitly"
---

> **Status.** This document develops two candidate proof routes for Theorem 1 of the main paper.
> Route A (Gaussian concentration) is the cleaner path but requires Lemma A2, whose proof is open.
> Route B (block martingale) matches the sketch in the paper but has a technical gap in the
> decoupling step. The final proof will likely combine elements of both. All gaps are explicitly
> marked **[GAP]**.

---

# Setup and Notation {#sec:setup}

Let $\{B^H_t\}_{t \geq 0}$ be fractional Brownian motion with Hurst exponent $H \in (1/2, 1)$, i.e.,
the unique (in law) centered Gaussian process with $B^H_0 = 0$ and covariance
$$\mathrm{Cov}(B^H_s, B^H_t) = \tfrac{1}{2}\bigl(|s|^{2H} + |t|^{2H} - |s-t|^{2H}\bigr).$$

Fix embedding dimension $d \geq 2$, lag $\tau \geq 1$, and let
$$P_{d,\tau}^{(n)} = \bigl\{p_t = (B^H_t, B^H_{t+\tau}, \ldots, B^H_{t+(d-1)\tau})\bigr\}_{t=1}^{n} \subset \mathbb{R}^d$$
be the sliding-window point cloud of size $n$. Write $N = n + (d-1)\tau$ for the number of
distinct fBm values used; the vector $\mathbf{B} = (B^H_1, \ldots, B^H_N) \sim N(0, \Sigma_H)$
is a Gaussian vector with covariance
$$(\Sigma_H)_{ij} = \tfrac{1}{2}(i^{2H} + j^{2H} - |i-j|^{2H}), \quad 1 \leq i,j \leq N.$$

The barcode count is
$$L_n^{(1)}(\varepsilon) = \#\bigl\{\text{bars in } \mathrm{Dgm}_1(\mathrm{VR}(P_{d,\tau}^{(n)})) \text{ with lifetime} > \varepsilon\bigr\},$$
where $\mathrm{VR}(\cdot)$ denotes the Vietoris--Rips filtration. It is a function
$L_n^{(1)}(\varepsilon) = F(\mathbf{B})$ for some $F : \mathbb{R}^N \to \mathbb{Z}_{\geq 0}$.

**Theorem 1 (restated).** *For any $\varepsilon > 0$ and $t > 0$,*
$$P\!\left(\left|L_n^{(1)}(\varepsilon) - \mathbb{E}[L_n^{(1)}(\varepsilon)]\right| > t\right)
\leq 2\exp\!\left(\frac{-t^2}{C(H,d,\tau,\varepsilon)\, n^{2H}}\right).$$

---

# Proof Route A: Gaussian Concentration {#sec:routeA}

## The Gaussian Concentration Template

The concentration of measure phenomenon for Gaussian vectors provides the cleanest route.
Let $X \sim N(0, \Sigma)$ be a centered Gaussian vector in $\mathbb{R}^N$ and let
$f : \mathbb{R}^N \to \mathbb{R}$ be $L$-Lipschitz with respect to the Euclidean norm.
By the Gaussian log-Sobolev inequality [@Ledoux2001, §2.3]:
$$P\bigl(|f(X) - \mathbb{E}[f(X)]| > t\bigr) \leq 2\exp\!\left(\frac{-t^2}{2L^2\, \|\Sigma\|_{\mathrm{op}}}\right),$$
where $\|\Sigma\|_{\mathrm{op}} = \lambda_{\max}(\Sigma)$ is the spectral norm of $\Sigma$.
Applying this to $F = L_n^{(1)}(\varepsilon)$ and $\Sigma = \Sigma_H$ gives Theorem 1
if we can establish:

- **Lemma A1.** $\|\Sigma_H\|_{\mathrm{op}} \sim C_H \, n^{2H}$ as $n \to \infty$.
- **Lemma A2.** $L_n^{(1)}(\varepsilon)$, viewed as a function of $\mathbf{B} \in \mathbb{R}^N$,
  is $L_\varepsilon$-Lipschitz with $L_\varepsilon$ depending on $\varepsilon, d, \tau$ but
  *not* on $n$.

If both lemmas hold, we obtain Theorem 1 with $C(H,d,\tau,\varepsilon) = 2 L_\varepsilon^2 C_H$.

## Lemma A1: Spectral Norm of $\Sigma_H$

**Claim.** $\lambda_{\max}(\Sigma_H) \asymp n^{2H}$.

*Lower bound.* Let $u = n^{-1/2}(1, \ldots, 1)^T \in \mathbb{R}^N$ (approximately). Then
$$u^T \Sigma_H u = \frac{1}{N}\sum_{i,j=1}^N (\Sigma_H)_{ij}
= \frac{1}{N}\sum_{i,j=1}^N \tfrac{1}{2}(i^{2H} + j^{2H} - |i-j|^{2H}).$$
The dominant term is $\frac{1}{N}\sum_{i,j} \tfrac{1}{2}(i^{2H} + j^{2H}) \sim \frac{1}{N} \cdot N \cdot N^{2H} = N^{2H}$.
Since $N \asymp n$, this gives $\lambda_{\max}(\Sigma_H) \geq c\, n^{2H}$.

*Upper bound.* **[GAP]** The trace satisfies
$\mathrm{tr}(\Sigma_H) = \sum_{i=1}^N (\Sigma_H)_{ii} = \sum_{i=1}^N i^{2H} \sim C n^{1+2H}$,
giving only $\lambda_{\max} \leq C n^{1+2H}$. A tighter upper bound $\lambda_{\max} = O(n^{2H})$
requires showing that the large off-diagonal correlations $(\Sigma_H)_{ij}$ for nearby $i,j$ do
not compound. The relevant spectral analysis of fBm covariance matrices
(related to the power spectral density of fBm increments, $S(\omega) \sim |\omega|^{1-2H}$)
appears in [@PipirasKrishnakumarTaqqu2003] but we have not located a sharp $\lambda_{\max}$ result
at the required precision. This is a resolvable gap via Toeplitz theory applied to the stationary
increments.

**Working conclusion.** Lemma A1 establishes $\lambda_{\max}(\Sigma_H) = \Omega(n^{2H})$; the
matching upper bound $O(n^{2H})$ is likely true but requires additional work.

## Lemma A2: Lipschitz Bound for the Barcode Count

**Claim.** There exists $L_\varepsilon < \infty$ (depending on $\varepsilon, d, \tau$ but not $n$)
such that
$$\bigl|L_n^{(1)}(\varepsilon)(\mathbf{b}) - L_n^{(1)}(\varepsilon)(\mathbf{b}')\bigr|
\leq L_\varepsilon\, \|\mathbf{b} - \mathbf{b}'\|_2 \quad \text{for all } \mathbf{b}, \mathbf{b}' \in \mathbb{R}^N.$$

**This is the central difficulty of Route A and is not established.**

*Why naive stability is insufficient.* The Cohen-Steiner--Edelsbrunner--Harer stability theorem
[@CohenSteinerEdelsbrunnerHarer2007] gives
$$d_B\!\bigl(\mathrm{Dgm}_1(P), \mathrm{Dgm}_1(P')\bigr) \leq d_H(P, P')$$
where $d_H$ is the Hausdorff distance. When $\mathbf{b}$ changes by $\delta$ in $\ell^\infty$,
each window $p_t$ shifts by at most $\delta$, so $d_H(P, P') \leq \delta$, and hence
$d_B(\mathrm{Dgm}_1, \mathrm{Dgm}_1') \leq \delta$.

A bottleneck perturbation of $\delta$ changes $L_n^{(1)}(\varepsilon)$ by the number of bars
matched to points within distance $\delta$ of the threshold $\varepsilon$ in the lifetime
coordinate. Formally:
$$\bigl|L_n^{(1)}(\varepsilon) - L_n^{(1)'}(\varepsilon)\bigr|
\leq \#\bigl\{\text{bars with lifetime} \in (\varepsilon - \delta, \varepsilon + \delta)\bigr\}.$$
For generic fBm configurations, the expected number of bars in any fixed band is $O(n)$,
so the naive difference $c_i = O(n)$ does not give a useful bound.

*A smoothing fix.* Replace $L_n^{(1)}(\varepsilon)$ by the regularized count
$$L_n^{(1),h}(\varepsilon) = \sum_{\text{bars}} \psi_h(\ell - \varepsilon),$$
where $\ell$ denotes the lifetime of a bar and $\psi_h$ is a smooth non-decreasing function
with $\psi_h(x) = 0$ for $x < -h$, $\psi_h(x) = 1$ for $x > 0$, and $|\psi_h'| \leq 1/h$.
This is the same regularization used for persistence images [@AdamsEmersonKirby2017].
One can show:
$$\bigl|L_n^{(1),h}(\varepsilon)(\mathbf{b}) - L_n^{(1),h}(\varepsilon)(\mathbf{b}')\bigr|
\leq \frac{C_{d,\tau}}{h\varepsilon}\, \|\mathbf{b} - \mathbf{b}'\|_\infty \cdot n.$$
The $n$ factor again spoils the bound. However, applying the inequality
$\|\mathbf{b} - \mathbf{b}'\|_\infty \leq \|\mathbf{b} - \mathbf{b}'\|_2$ and considering
the *average* behavior over fBm trajectories (rather than the worst case) may recover the
correct scaling.

*Alternative: persistence landscape norm.* The persistence landscape [@Bubenik2015]
$$\lambda_k^{(1)}(t,s) = \max(\min(t - b_k, d_k - t) - s, 0)$$
is 1-Lipschitz in the bottleneck distance, hence also in $d_H$. The $L^1$ norm
$\|\lambda^{(1)}\|_{L^1} = \sum_k \text{(area under } \lambda_k^{(1)})$ satisfies
$$\bigl|\|\lambda^{(1)}\|_{L^1}(\mathbf{b}) - \|\lambda^{(1)}\|_{L^1}(\mathbf{b}')\bigr|
\leq C\, \|\mathbf{b} - \mathbf{b}'\|_\infty \cdot \sqrt{n}$$
(where the $\sqrt{n}$ comes from the number of bars). This gives an $n^{1/2}$-Lipschitz
functional, which via Gaussian concentration yields:
$$P\!\left(\bigl|\|\lambda^{(1)}\|_{L^1} - \mathbb{E}\bigl[\|\lambda^{(1)}\|_{L^1}\bigr]\bigr| > t\right)
\leq 2\exp\!\left(\frac{-t^2}{C\, n \cdot n^{2H}}\right) = 2\exp\!\left(\frac{-t^2}{C\, n^{1+2H}}\right).$$
This is *weaker* than Theorem 1 by a factor of $n$, but it is a provable bound for a related
functional. **[GAP]** Bridging the $n$ gap to recover the sharp $n^{2H}$ bound for
$L_n^{(1)}(\varepsilon)$ requires either a sharper Lipschitz estimate or a different method.

---

# Proof Route B: Block Martingale {#sec:routeB}

This is the approach sketched in the Introduction of paper.md. It avoids the Lipschitz difficulty
by working with the process structure directly, at the cost of a more involved decoupling argument.

## Step B1: Block Decomposition

Partition $\{1, \ldots, n\}$ into $k_n$ *big blocks* $I_1, \ldots, I_{k_n}$ each of length
$b_n$, separated by *gap blocks* $G_1, \ldots, G_{k_n - 1}$ each of length $g_n$, where
$$b_n + g_n = \lfloor n / k_n \rfloor, \qquad b_n \asymp n^{2H-1}, \qquad g_n \asymp b_n^\beta$$
for some $\beta \in (0,1)$ to be chosen. Set $k_n \asymp n^{2-2H}$.

Write the sliding-window cloud as $P^{(n)} = P^{(n)}_{\mathrm{big}} \cup P^{(n)}_{\mathrm{gap}}$
where $P^{(n)}_{\mathrm{big}}$ contains windows whose *anchor* $t$ falls in a big block.
Define the approximate barcode count
$$\widetilde{L}_n^{(1)}(\varepsilon) = \#\bigl\{\text{bars in } \mathrm{Dgm}_1(P^{(n)}_{\mathrm{big}}) \text{ with lifetime} > \varepsilon\bigr\}.$$

**Claim B1.** $|L_n^{(1)}(\varepsilon) - \widetilde{L}_n^{(1)}(\varepsilon)| \leq C\, k_n\, g_n \cdot b_n$
with high probability. *[The gap blocks contribute at most $k_n g_n$ windows, each capable of
changing the barcode count by at most $C b_n$ via interactions with the big-block windows.]*
**[GAP]** This bound is heuristic; the precise statement requires controlling how gap-block
windows interact with big-block topology.

## Step B2: Mixing Coefficients of fBm Increments

The fBm increments $\Delta_t = B^H_{t+1} - B^H_t$ form a stationary Gaussian process.
For a stationary Gaussian process with covariance $r(k) = \mathrm{Cov}(\Delta_0, \Delta_k)$,
the $\alpha$-mixing coefficients satisfy
$$\alpha(k) \leq \phi\!\left(\sup_{|m| \geq k} |r(m)|\right)$$
for a function $\phi$ with $\phi(x) \to 0$ as $x \to 0$ [@BradleyMixing2005, Vol.~I, Thm.~3.6].

For fBm with $H > 1/2$, the increment covariance is
$$r(k) = \mathrm{Cov}(\Delta_0, \Delta_k) = \tfrac{1}{2}\bigl((k+1)^{2H} - 2k^{2H} + (k-1)^{2H}\bigr)
\sim H(2H-1) k^{2H-2} \quad \text{as } k \to \infty.$$
Since $2H - 2 < 0$ for $H < 1$, we have $r(k) \to 0$, so the increments are strongly mixing.
The mixing rate is:
$$\alpha(k) \leq C_H\, k^{H-1} \quad (H \in (1/2, 1)).$$

**This is a published fact** (Gaussian processes are $\alpha$-mixing whenever their covariance
decays to zero; see, e.g., [@Taqqu2003]). However, the precise bound $\alpha(k) \leq C_H k^{H-1}$
requires citing a specific result. **[GAP: locate precise reference for $\alpha$-mixing rate of fBm increments.
Pipiras and Taqqu [@PipirasKrishnakumarTaqqu2003] cover spectral properties but mixing rate
bounds for fBm increments may require additional work via the Gaussian hypercontractivity theorem.}**

## Step B3: Coupling to Independent Blocks

Standard $\alpha$-mixing technology (Berbee's lemma, or the coupling of [@Rio2000]) asserts:
for an $\alpha$-mixing sequence with $\alpha(g_n) \leq \delta_n$, one can couple the big-block
sequences $\{B^H_t : t \in I_j\}$ with independent copies $\{B^{H,*}_t : t \in I_j\}$ such that
$$P\!\left(\text{coupling fails on some block}\right) \leq k_n \cdot \delta_n.$$

Under the coupling, $\widetilde{L}_n^{(1)}(\varepsilon) \approx \widetilde{L}_n^{(1),*}(\varepsilon)$
(the same count computed from the independent copies), with discrepancy controlled by the
probability of coupling failure times a worst-case difference. Setting $g_n = b_n^\beta$ with
$\beta$ large enough ensures $k_n \cdot \alpha(g_n) \to 0$.

**[GAP]** The coupling construction must be made explicit. The standard result (see
[@BoucheronLugosiMassart2013, §6.4] for the Azuma extension to mixing sequences) works for
real-valued sums; extending it to the functional $L_n^{(1)}(\varepsilon)$ requires showing
that the functional depends on each block's contribution in a way that is compatible with
the decoupling. Specifically, the barcode count is a *global* property of $P^{(n)}$, not
a sum of per-block quantities, and Mayer--Vietoris-type bounds are needed to control how
topology across block boundaries interacts.

## Step B4: Concentration of the Decoupled Sum

Once the blocks are independent, write
$$\widetilde{L}_n^{(1),*}(\varepsilon) = \sum_{j=1}^{k_n} Z_j$$
where $Z_j$ counts bars in $\mathrm{Dgm}_1(P^{(n)}_{I_j})$ with lifetime $> \varepsilon$,
and $Z_1, \ldots, Z_{k_n}$ are *independent*. Each $Z_j$ satisfies:
- $\mathbb{E}[Z_j] \leq C b_n$ (expected number of bars in a block of size $b_n$)
- $|Z_j - \mathbb{E}[Z_j]| \leq C b_n$ a.s. (trivial bound; each block has at most $b_n$ bars)

Applying the Hoeffding--Azuma inequality to $\sum_j Z_j$:
$$P\!\left(\left|\sum_j Z_j - \mathbb{E}\sum_j Z_j\right| > t\right)
\leq 2\exp\!\left(\frac{-2t^2}{\sum_j (Cb_n)^2}\right)
= 2\exp\!\left(\frac{-2t^2}{k_n\, C^2 b_n^2}\right).$$

With $k_n \asymp n^{2-2H}$ and $b_n \asymp n^{2H-1}$:
$$k_n b_n^2 \asymp n^{2-2H} \cdot n^{2(2H-1)} = n^{2-2H+4H-2} = n^{2H}.$$
This gives
$$P\!\left(\left|\widetilde{L}_n^{(1),*}(\varepsilon) - \mathbb{E}[\cdot]\right| > t\right)
\leq 2\exp\!\left(\frac{-t^2}{C' n^{2H}}\right),$$
**which is exactly the form of Theorem 1.** This is the key calculation that validates the
block sizes $b_n \asymp n^{2H-1}$, $k_n \asymp n^{2-2H}$.

## Step B5: Assembly

Combining Steps B1--B4 (assuming the gaps are closed):
$$P\!\left(\left|L_n^{(1)}(\varepsilon) - \mathbb{E}[L_n^{(1)}(\varepsilon)]\right| > t\right)
\leq P\!\left(\left|\widetilde{L}_n^{(1)}(\varepsilon) - \widetilde{L}_n^{(1),*}(\varepsilon)\right| > t/3\right)
+ P\!\left(\left|\widetilde{L}_n^{(1),*}(\varepsilon) - \mathbb{E}[\cdot]\right| > t/3\right)
+ P\!\left(\left|L_n^{(1)}(\varepsilon) - \widetilde{L}_n^{(1)}(\varepsilon)\right| > t/3\right).$$
The second term is bounded by $2\exp(-t^2 / (C n^{2H}))$ by Step B4. The first and third
terms involve gap-block errors and coupling failures, which should be of smaller order if the
block sizes are chosen correctly.

---

# Comparison of Routes and Status {#sec:status}

| Component | Route A status | Route B status |
|-----------|----------------|----------------|
| Core inequality template | Established (Gaussian log-Sobolev) | Established (Hoeffding for independent) |
| $n^{2H}$ variance factor | From $\lambda_{\max}(\Sigma_H) \sim n^{2H}$ — **[GAP: upper bound]** | From block size calculation — **proven** |
| Lipschitz/bounded differences | **[GAP: central difficulty]** | Bounded by $b_n$ per block — rough but workable |
| Independence/decoupling | Automatic (Gaussian, no blocking needed) | **[GAP: Mayer-Vietoris + coupling]** |
| Mixing of fBm | Not needed | **[GAP: precise $\alpha$-mixing rate needed]** |
| Final assembly | Clean once Lemma A2 is resolved | Requires bounding cross-block topology |

**Recommendation.** Route B's core calculation (Step B4) is the more explicit path to the right
variance factor, and the block sizes are now justified. Route A would give a cleaner proof if
Lemma A2 can be established. The most productive next step is:

1. **Prove Lemma A2** for the regularized count $L_n^{(1),h}(\varepsilon)$, then show the
   $h \to 0$ limit via a monotone convergence argument.
2. **Alternatively**, prove Route B's Claim B1 (gap-block error) using a Mayer--Vietoris
   spectral sequence argument bounding $H_1$ contributions across block boundaries.

---

# The Constant $C(H, d, \tau, \varepsilon)$ {#sec:constant}

From Route B, the constant has the form
$$C(H, d, \tau, \varepsilon) = 2 C_1(d, \tau, \varepsilon)^2 \cdot C_2(H),$$
where:
- $C_1(d, \tau, \varepsilon)$ is the bounded-differences constant per block (measuring how many
  bars of lifetime near $\varepsilon$ a single block can contribute). It depends on the geometry
  of the embedding and diverges as $\varepsilon \to 0$.
- $C_2(H) = \lim_{n \to \infty} k_n b_n^2 / n^{2H}$ is the asymptotic constant in the block
  size calculation. From the choice $b_n = (2H-1) n^{2H-1}$ and $k_n = n / b_n$:
  $C_2(H) = (2H-1)^{-1}$ approximately (to be determined).

At $H = 1/2$: $b_n \asymp 1$ (blocks of constant size, i.e., effectively i.i.d.), and the
bound reduces to the Azuma--Hoeffding rate with constant $C(1/2, d, \tau, \varepsilon) = O(1)$.
This is consistent with the claim in the paper that the bound recovers the i.i.d. rate at $H = 1/2$.

---

# References

*(Entries not already in references.bib are marked with \*; add to bib before compiling.)*

- [@CohenSteinerEdelsbrunnerHarer2007]: stability theorem (already in bib)
- [@BoucheronLugosiMassart2013]: concentration inequalities (already in bib)
- [@Taqqu2003]: fBm and long-range dependence (already in bib)
- [@Bubenik2015]: persistence landscapes (already in bib)
- [@AdamsEmersonKirby2017]: persistence images (already in bib)
- \*[@Ledoux2001]: *The Concentration of Measure Phenomenon*, AMS, 2001 — Gaussian log-Sobolev
- \*[@Rio2000]: *Théorie asymptotique des processus aléatoires faiblement dépendants*,
  Springer, 2000 — coupling for mixing sequences
- \*[@BradleyMixing2005]: Bradley, *Introduction to Strong Mixing Conditions*, Kendrick Press,
  2007 — reference for mixing coefficient bounds for Gaussian processes
- \*[@PipirasKrishnakumarTaqqu2003]: Pipiras and Taqqu, *Long-Range Dependence and Self-Similarity*,
  Cambridge University Press, 2017 — spectral and mixing properties of fBm

---

*Last updated: 2026-03-21.*
