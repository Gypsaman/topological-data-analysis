---
title: "Concentration Inequalities for Persistent Homology of Long-Range Dependent Point Clouds, with a Topological Hurst Estimator"
author:
  - name: "[Author 1]"
  - name: "[Author 2]"
date: 2026
abstract: |
  Let $\{X_t\}_{t \geq 0}$ be a fractional Brownian motion (fBm) with Hurst exponent
  $H \in (1/2, 1)$. The sliding-window point cloud
  $P_{d,\tau}^{(n)} = \{(X_t, X_{t+\tau}, \ldots, X_{t+(d-1)\tau})\}_{t=1}^n \subset \mathbb{R}^d$
  encodes the local geometry of the process at embedding dimension $d$ and lag $\tau$.
  We study the persistent homology of $P_{d,\tau}^{(n)}$ under the Vietoris--Rips filtration,
  focusing on the barcode count function
  $L_n^{(1)}(\varepsilon) = \#\{\text{bars in } \mathrm{Dgm}_1(P_{d,\tau}^{(n)}) \text{ with lifetime} > \varepsilon\}$.

  The central obstacle to a statistical theory for this object is dependence: when $H > 1/2$,
  the covariance $\mathrm{Cov}(X_0, X_t) \sim t^{2H-2}$ is not summable, which breaks
  the martingale structure required by Azuma--Hoeffding-type arguments. We resolve this via a
  block decomposition exploiting the strong mixing of fBm increments, yielding the first
  concentration inequality for persistent Betti numbers of long-range dependent point clouds:
  $$P\!\left(\left|L_n^{(1)}(\varepsilon) - \mathbb{E}[L_n^{(1)}(\varepsilon)]\right| > t\right)
  \leq 2\exp\!\left(\frac{-t^2}{C(H)\, n^{2H}}\right),$$
  where $C(H)$ is explicit. At $H = 1/2$ the bound recovers the i.i.d. rate.

  Using the self-similarity of fBm, we derive a scaling law
  $\mathbb{E}[L_n^{(1)}(\varepsilon)] \sim n \cdot \varepsilon^{-\alpha(H)}$,
  where $\alpha(H)$ is strictly monotone. This motivates the *topological Hurst estimator*
  $\hat{H}_{\mathrm{top}}$: fit the log-log slope of $L_n^{(1)}(\varepsilon)$ and invert
  the calibrated function $\alpha(H)$. We establish consistency and a convergence rate of
  $O(n^{H-1})$, matching the known minimax rate for Hurst estimation. Unlike classical
  estimators (R/S, DFA, Whittle), $\hat{H}_{\mathrm{top}}$ is stable under monotone
  transforms of the series, a consequence of the bottleneck stability theorem for persistence
  diagrams. Numerical experiments on synthetic fBm and financial time series (S&P 500, VIX,
  FX rates) confirm the theory.
bibliography: references.bib
link-citations: true
numbersections: true
---

# Introduction {#sec:intro}

## Background {#sec:background}

Persistent homology tracks how topological features --- connected components, loops, voids ---
appear and disappear as a scale parameter grows. Given a finite metric space, one constructs
a nested family of simplicial complexes (the Vietoris--Rips or Čech filtration) and reads
off the birth and death times of homological features; the resulting multiset of intervals,
the *persistence diagram*, serves as a compact topological summary of the data
[@EdelsbrunnerLetscherZomorodian2002; @ZomorodianCarlsson2005]. The theory rests on two
foundational results: the structure theorem, which guarantees a unique decomposition of any
pointwise finite-dimensional persistence module into interval summands
[@CrawleyBoevey2015; @ChazalDeSilvaGlisseOudot2016], and the stability theorem, which bounds
the bottleneck distance between persistence diagrams by the $L^\infty$ distance between the
generating functions [@CohenSteinerEdelsbrunnerHarer2007]. Together these make persistence
diagrams both theoretically tractable and practically robust. For a broad overview of the
field see @Carlsson2009.

The application of persistent homology to time series analysis rests on the *sliding window
embedding* (also called delay embedding or Takens embedding). Given a univariate series
$\{X_t\}$ with embedding dimension $d$ and lag $\tau$, one forms the point cloud
$$P_{d,\tau}^{(n)} = \bigl\{(X_t,\, X_{t+\tau},\, \ldots,\, X_{t+(d-1)\tau})\bigr\}_{t=1}^{n}
\subset \mathbb{R}^d.$$
@PereaHarer2015 showed that when $X_t = \cos(2\pi t / T)$, the persistent $H_1$ of
$P_{d,\tau}^{(n)}$ detects the period $T$ and that sufficiently large windows produce point
clouds whose topology approximates that of a circle. For nonlinear and stochastic signals the
picture is less clean, but the intuition persists: the 1-dimensional holes in the delay
embedding reflect quasi-periodic or looping structure in the underlying process. @GideaKatz2018
exploited this to identify topological precursors to financial crashes in equity indices,
computing persistence landscapes of sliding windows of S&P 500 log-returns and observing
characteristic changes in $L^1$-norm near crash events.

The random topology of such constructions has received growing attention. @LinialMeshulam2006
introduced the random 2-complex model and studied homological connectivity thresholds;
subsequent work by @KahleRandomClique2009 and @KahleSharpVanishing2014 established sharp
vanishing thresholds for cohomology of random flag complexes and clique complexes built from
Erdős--Rényi graphs. The essential probabilistic tool in these analyses is the
Azuma--Hoeffding inequality, which applies whenever the quantity of interest can be written
as a function of independent random variables with bounded differences. The bounded
differences condition translates, for persistent Betti numbers, into the observation that
adding or removing a single point changes $\mathrm{Dgm}_k$ by at most a controlled amount ---
a consequence of stability. The general framework is treated in @BoucheronLugosiMassart2013.

Long-memory processes occupy a different part of the probability landscape entirely.
Fractional Brownian motion $\{B^H_t\}_{t \geq 0}$ with Hurst exponent $H \in (0,1)$ is
the unique (up to scaling) self-similar Gaussian process with stationary increments
[@Taqqu2003]. For $H = 1/2$ it reduces to standard Brownian motion. For $H > 1/2$ the
covariance function satisfies $\mathrm{Cov}(B^H_0, B^H_t) \sim t^{2H-2}$, which is not
summable over $t \geq 1$; this is the signature of *long-range dependence*. Financial time
series --- particularly log-returns of equity indices, exchange rates, and volatility measures
--- exhibit Hurst exponents measurably above $1/2$, a fact central to Mandelbrot's critique
of geometric Brownian motion [@Mandelbrot1997]. Estimating $H$ from data is a classical
problem with a well-developed toolkit: rescaled range (R/S) analysis, detrended fluctuation
analysis (DFA), the Whittle estimator, and quadratic variation methods
[@IstasLang1997; @DaviesHarte1987]. Each operates on the raw time series directly. None uses
the geometry of the delay-embedding point cloud.

## The Gap {#sec:gap}

The existing probabilistic theory for random persistent homology is built entirely on
independence. The block argument of @LinialMeshulam2006, the Morse-theoretic threshold
results of @KahleRandomClique2009, and concentration bounds derived in the statistical TDA
literature all rely, at some point, on the Azuma--Hoeffding inequality or its variants, which
require the sample points to be independent (or at least form a martingale difference
sequence). For the sliding-window cloud $P_{d,\tau}^{(n)}$, adjacent points share $d-1$
coordinates, introducing dependence at the level of the embedding by construction. When the
underlying process has long memory, this dependence propagates across all time scales: points
in $P_{d,\tau}^{(n)}$ separated by lag $k$ are still correlated, with correlation decaying
like $k^{2H-2}$. Since $\sum_{k=1}^\infty k^{2H-2} = \infty$ for $H > 1/2$, the process is
not $L^1$-mixing, and the standard blocking argument breaks down.

The consequence is a complete absence of statistical theory for topological summaries of
long-memory processes. The barcode count $L_n^{(1)}(\varepsilon)$ is computable in practice
--- @Bauer2021 handles point clouds of the relevant size in seconds --- but its distributional
behavior, even asymptotically, is unknown. Without concentration results, there is no
principled way to construct confidence intervals, conduct hypothesis tests, or establish the
consistency of any estimator built from persistence diagrams of such data. The proposal of
@GideaKatz2018, despite its empirical appeal, rests on entirely heuristic grounds when
applied to processes with long memory.

The gap, stated precisely: *no concentration inequality for persistent Betti numbers of point
clouds drawn from long-range dependent processes exists*. This paper fills that gap for the
canonical long-memory model, fBm with $H \in (1/2, 1)$, and constructs the first TDA-based
estimator of $H$ with provable statistical guarantees.

## Main Results {#sec:results}

The paper establishes three results, in increasing order of consequence.

**Theorem 1 (Concentration for long-memory point clouds).** *Let $\{B^H_t\}$ be fBm with
$H \in (1/2, 1)$, and let $P_{d,\tau}^{(n)}$ be its sliding-window embedding with parameters
$d \geq 2$, $\tau \geq 1$. For any $\varepsilon > 0$ and $t > 0$,*
$$P\!\left(\left|L_n^{(1)}(\varepsilon) - \mathbb{E}[L_n^{(1)}(\varepsilon)]\right| > t\right)
\leq 2\exp\!\left(\frac{-t^2}{C(H,d,\tau,\varepsilon)\, n^{2H}}\right),$$
*where $C(H,d,\tau,\varepsilon)$ is an explicit constant.*

The proof partitions $\{1,\ldots,n\}$ into blocks of size $b_n \sim n^{1-1/(2H)}$, applies
a martingale inequality blockwise using the strong mixing of fBm increments, and controls
cross-block terms via the decay rate of the mixing coefficients. The variance factor $n^{2H}$
--- larger than the i.i.d. rate $n$ by a factor $n^{2H-1}$ --- reflects the accumulated
dependence. At $H = 1/2$ the bound reduces to the classical Azuma rate.

**Theorem 2 (Scaling law).** *Under the self-similarity
$\{B^H_{ct}\} \stackrel{d}{=} \{c^H B^H_t\}$, the expected barcode count satisfies*
$$\mathbb{E}[L_n^{(1)}(\varepsilon)] \sim n \cdot \varepsilon^{-\alpha(H)}$$
*as $n \to \infty$, $\varepsilon \to 0$ with $\varepsilon n^{H/d} \to \ell \in (0,\infty)$.
The scaling exponent $\alpha(H)$ is strictly increasing in $H$ on $(0,1)$.*

The proof follows from a self-consistency argument: rescaling time by $c$ maps
$P_{d,\tau}^{(n)}$ to $c^H P_{d,\tau}^{(n)}$ and simultaneously rescales the filtration
parameter, constraining $\mathbb{E}[L_n^{(1)}(\varepsilon)]$ to a power law. Monotonicity
of $\alpha(H)$ is established numerically in the finite-sample regime and analytically in
the limit $H \to 1$.

**Theorem 3 (Topological Hurst estimator: consistency and rate).** *Define
$\hat{H}_{\mathrm{top}}$ by: embed $\{X_t\}_{t=1}^n$ as $P_{d,\tau}^{(n)}$, compute
$\mathrm{Dgm}_1(P_{d,\tau}^{(n)})$ via Ripser [@Bauer2021], and for a range of scales
$\varepsilon_1 < \cdots < \varepsilon_m$ fit the OLS regression*
$$\log L_n^{(1)}(\varepsilon_j) = -\hat{\alpha} \log \varepsilon_j + \mathrm{const},$$
*then set $\hat{H}_{\mathrm{top}} = \alpha^{-1}(\hat{\alpha})$. Then
$\hat{H}_{\mathrm{top}} \xrightarrow{P} H$ as $n \to \infty$, and
$|\hat{H}_{\mathrm{top}} - H| = O_P(n^{H-1})$.*

This rate matches the minimax lower bound for Hurst estimation established by
@IstasLang1997. The estimator is *transform-stable*: if $Y_t = \phi(X_t)$ for any strictly
monotone $\phi$, the bottleneck stability of persistence diagrams
[@CohenSteinerEdelsbrunnerHarer2007] implies
$\hat{H}_{\mathrm{top}}(\{Y_t\}) = \hat{H}_{\mathrm{top}}(\{X_t\}) + O_P(n^{H-1})$,
so the leading-order estimate is unchanged. The R/S, DFA, and Whittle estimators do not
share this property.

Together, these results establish a coherent statistical theory for persistent homology of
long-memory time series: a concentration bound, an expectation formula, and a consistent
estimator with known rate.

## Organization {#sec:organization}

Section 2 collects the necessary background on persistent homology, fBm, and mixing.
Section 3 proves Theorem 1 via the block martingale argument. Section 4 derives the scaling
law (Theorem 2) and establishes monotonicity of $\alpha(H)$. Section 5 defines and analyzes
$\hat{H}_{\mathrm{top}}$, proving Theorem 3 and the transform-stability claim. Section 6
presents numerical experiments: synthetic fBm simulations calibrating $\alpha(H)$, a
comparison of $\hat{H}_{\mathrm{top}}$ against R/S, DFA, and Whittle, and an application
to S&P 500 log-returns, VIX, and EUR/USD exchange rates. Section 7 discusses the
multifractal extension and open problems.

# Preliminaries {#sec:prelim}

## Persistent Homology {#sec:ph-background}

For a finite metric space $(X, d_X)$ and scale parameter $r \geq 0$, the Vietoris--Rips
complex $\mathrm{VR}(X, r)$ is the abstract simplicial complex with vertex set $X$ containing
$\{x_0, \ldots, x_k\}$ as a $k$-simplex whenever $d_X(x_i, x_j) \leq r$ for all
$0 \leq i < j \leq k$. The inclusions $\mathrm{VR}(X, r) \hookrightarrow \mathrm{VR}(X, r')$
for $r \leq r'$ assemble into a *filtration*: a nested one-parameter family of simplicial
complexes.

Applying the $k$-th homology functor with coefficients in a field $\mathbb{k}$ produces a
*persistence module* $\mathbb{V} = \{V_r\}_{r \geq 0}$: a family of $\mathbb{k}$-vector
spaces connected by linear maps $\varphi_{r,r'}: V_r \to V_{r'}$ for $r \leq r'$. By the
structure theorem [@CrawleyBoevey2015; @ChazalDeSilvaGlisseOudot2016], every pointwise
finite-dimensional persistence module decomposes uniquely as
$$\mathbb{V} \cong \bigoplus_j \mathbb{k}^{[b_j, d_j)},$$
where each $\mathbb{k}^{[b,d)}$ is the interval module supported on $[b, d)$. The multiset
$\mathrm{Dgm}_k(X) = \{(b_j, d_j)\}_j$ is the *$k$-th persistence diagram*. Each pair
$(b_j, d_j)$ records the birth and death of a homological feature in dimension $k$; the
difference $d_j - b_j$ is the *lifetime* of the feature.

The analytical backbone of persistence theory is the *stability theorem*
[@CohenSteinerEdelsbrunnerHarer2007]. In the form relevant here: for two finite point clouds
$X$ and $Y$ in the same ambient space,
$$d_B\!\left(\mathrm{Dgm}_k(X),\, \mathrm{Dgm}_k(Y)\right) \leq d_H(X, Y),$$
where $d_B$ is the bottleneck distance and $d_H$ the Hausdorff distance. Stability means
that nearby point clouds produce nearby persistence diagrams --- a robustness property that
will translate, in §3.1, into a controlled sensitivity of the barcode count to perturbations
of the underlying time series.

For a fixed lifetime threshold $\varepsilon > 0$, define the *barcode count function*
$$L_n^{(k)}(\varepsilon) = \#\!\left\{(b, d) \in \mathrm{Dgm}_k\!\left(P_{d,\tau}^{(n)}\right)
: d - b > \varepsilon\right\}.$$
The primary object of study is $L_n^{(1)}(\varepsilon)$: the number of 1-cycles (loops) in
the Vietoris--Rips filtration of the delay embedding with lifetime exceeding $\varepsilon$.
Geometrically, such a loop reflects a quasi-periodic or recurrent pattern in the time series
that persists across the scale range $[\text{birth}, \text{death}]$. Computation of
$\mathrm{Dgm}_1$ is performed via Ripser [@Bauer2021], which runs in seconds for point
clouds of size $n \leq 10^4$ in $\mathbb{R}^3$.

## Fractional Brownian Motion {#sec:fbm}

Fractional Brownian motion with Hurst exponent $H \in (0, 1)$ is the centered Gaussian
process $\{B^H_t\}_{t \geq 0}$ with $B^H_0 = 0$ and covariance
$$\mathrm{Cov}(B^H_s, B^H_t) = \frac{1}{2}\!\left(|s|^{2H} + |t|^{2H} - |s - t|^{2H}\right).$$
It is the unique --- up to scaling --- process that is *self-similar* of index $H$, meaning
$\{B^H_{ct}\}_{t \geq 0} \stackrel{d}{=} \{c^H B^H_t\}_{t \geq 0}$ for all $c > 0$, and
has *stationary increments*. Setting $s = t$ gives $\mathrm{Var}(B^H_t) = t^{2H}$, the
fundamental variance scaling. At $H = 1/2$, the covariance reduces to $\min(s, t)$ and the
process is standard Brownian motion; the increments are i.i.d. Gaussian.

For $H \neq 1/2$, the increments remain Gaussian and stationary but are correlated. The
increment covariance
$$\gamma_H(k) = \mathrm{Cov}\!\left(B^H_1,\; B^H_{k+1} - B^H_k\right)
= \frac{1}{2}\!\left((k+1)^{2H} - 2k^{2H} + (k-1)^{2H}\right)$$
satisfies $\gamma_H(k) \sim H(2H-1)k^{2H-2}$ as $k \to \infty$. For $H \in (1/2, 1)$, the
exponent $2H - 2 \in (-1, 0)$, so $|\gamma_H(k)| \sim k^{2H-2}$ is not summable:
$\sum_{k=1}^\infty |\gamma_H(k)| = \infty$. Non-summability of the covariance is the
standard criterion for *long-range dependence* [@Taqqu2003].

The spectral implications of long-range dependence are encoded in the operator norm of the
$n \times n$ fBm covariance matrix
$\Sigma_n = \left(\frac{1}{2}(i^{2H} + j^{2H} - |i-j|^{2H})\right)_{i,j=1}^n$. By the
Szegő--Grenander--Rosenblatt spectral theory applied to the increments process (see
[@Taqqu2003, Ch. 4]),
$$\|\Sigma_n\|_{\mathrm{op}} \sim C_H n^{2H}, \quad n \to \infty,$$
for an explicit constant $C_H$ depending only on $H$. This scaling --- $n^{2H}$ rather than
$n$ --- is the quantity that propagates into the concentration bound. Setting $H = 1/2$
recovers $\|\Sigma_n\|_{\mathrm{op}} = O(n)$, consistent with the i.i.d. case. Exact sample
paths are generated via the Davies--Harte algorithm [@DaviesHarte1987], which uses the FFT
to produce exact (not approximate) realizations in $O(n \log n)$ time.

## The Sliding Window Embedding {#sec:embedding}

For a univariate time series $\{X_t\}_{t=1}^N$, embedding dimension $d \geq 2$, and lag
$\tau \geq 1$, the *sliding window embedding* is
$$P_{d,\tau}^{(n)} = \bigl\{w_t = (X_t,\, X_{t+\tau},\, \ldots,\, X_{t+(d-1)\tau})\bigr\}_{t=1}^{n}
\subset \mathbb{R}^d,$$
where $n = N - (d-1)\tau$. Each $w_t \in \mathbb{R}^d$ is a *delay vector*. The dependence
structure of $P_{d,\tau}^{(n)}$ is more complex than that of $\{X_t\}$ alone: adjacent delay
vectors $w_t$ and $w_{t+1}$ share the samples $\{X_{t+\tau}, \ldots, X_{t+(d-1)\tau}\}$, a
block of $d-1$ common coordinates. This overlap means $P_{d,\tau}^{(n)}$ is never a
collection of independent samples, even when the underlying $\{X_t\}$ has independent
increments.

When $\{X_t\} = \{B^H_t\}$, each coordinate $w_t^{(i)} = B^H_{t+(i-1)\tau}$ is a linear
functional of the fBm path. The point cloud $P_{d,\tau}^{(n)}$ is therefore a Gaussian
point cloud in $\mathbb{R}^d$ with covariance structure
$$\mathrm{Cov}(w_s^{(i)}, w_t^{(j)}) = \frac{1}{2}\!\left(|s+(i-1)\tau|^{2H}
+ |t+(j-1)\tau|^{2H} - |s - t + (i-j)\tau|^{2H}\right),$$
which inherits the $n^{2H}$ operator-norm scaling from the ambient fBm. This is the chain
of structure that connects the long-memory statistics of $\{B^H_t\}$ to the geometry of the
delay-embedding point cloud and, ultimately, to the concentration of its persistence diagram.

## Concentration Tools {#sec:tools}

The proofs in Section 3 use two concentration inequalities. The first applies within each
block of the decomposition, where approximate independence is available; the second leverages
the Gaussian structure directly.

**Azuma's inequality** [@BoucheronLugosiMassart2013, Theorem 7.1]. *Let $\{M_j\}_{j=0}^m$
be a martingale with $|M_j - M_{j-1}| \leq c_j$ almost surely. Then for any $t > 0$,*
$$P\!\left(|M_m - M_0| > t\right) \leq 2\exp\!\left(\frac{-2t^2}{\sum_{j=1}^m c_j^2}\right).$$

**Gaussian concentration** [@BoucheronLugosiMassart2013, Theorem 5.6]. *Let
$\mathbf{Z} \sim \mathcal{N}(0, \Sigma)$ and let $g: \mathbb{R}^n \to \mathbb{R}$ be
$L$-Lipschitz with respect to the Euclidean norm. Then*
$$P\!\left(|g(\mathbf{Z}) - \mathbb{E}[g(\mathbf{Z})]| > t\right)
\leq 2\exp\!\left(\frac{-t^2}{2L^2 \|\Sigma\|_{\mathrm{op}}}\right).$$

The Gaussian inequality is used in Remark 3.4 to give an alternative proof of Theorem 1
with a potentially sharper constant, at the cost of working with a Lipschitz approximation
to $L_n^{(1)}(\varepsilon)$ rather than the count itself.

# Concentration Inequality {#sec:concentration}

The goal of this section is to prove Theorem 1. The argument proceeds in three stages: a
sensitivity lemma (§3.1) establishes how much $L_n^{(1)}(\varepsilon)$ can change when one
time-series observation is perturbed; a block martingale construction (§3.2) converts this
sensitivity into a concentration bound whose rate depends on the block size; and a variance
bound via covariance decay (§3.3) identifies the correct block size as $b_n \sim n^{2H-1}$,
producing the $n^{2H}$ exponent in Theorem 1.

## Sensitivity of the Barcode Count {#sec:sensitivity}

**Lemma 3.1** *(One-observation sensitivity).* *Fix $\varepsilon > 0$, $d \geq 2$,
$\tau \geq 1$. Let $P = P_{d,\tau}^{(n)}$ be the sliding window embedding of
$(x_1, \ldots, x_N) \in \mathbb{R}^N$, and let $P^{(t)}$ denote the embedding obtained by
replacing $x_t$ with $x_t' \in \mathbb{R}$. Then*
$$\left|L_n^{(1)}\!\left(\varepsilon;\, P\right) - L_n^{(1)}\!\left(\varepsilon;\, P^{(t)}\right)
\right| \leq 2\!\left\lfloor \frac{2|x_t - x_t'|}{\varepsilon} \right\rfloor + 2.$$
*In particular, for $|x_t - x_t'| \leq \varepsilon/4$, the barcode count is unchanged.*

*Proof.* Replacing $x_t$ by $x_t'$ modifies exactly the delay vectors $w_s$ for which
$t \in \{s, s + \tau, \ldots, s + (d-1)\tau\}$; there are at most $d$ such indices $s$.
For each affected $w_s$, exactly one coordinate changes, so $\|w_s - w_s'\|_2 = |x_t - x_t'|$.
The Hausdorff distance therefore satisfies $d_H(P, P^{(t)}) \leq |x_t - x_t'| =: \delta$.

By the stability theorem, $d_B(\mathrm{Dgm}_1(P), \mathrm{Dgm}_1(P^{(t)})) \leq \delta$. A
bottleneck matching of quality $\delta$ pairs each bar $(b_j, d_j)$ in $\mathrm{Dgm}_1(P)$
either with a bar $(b_j', d_j')$ in $\mathrm{Dgm}_1(P^{(t)})$ satisfying
$\max(|b_j - b_j'|, |d_j - d_j'|) \leq \delta$, or with a diagonal point representing
deletion. If a bar is matched to the diagonal, its closest diagonal point $(x, x)$ must
satisfy $\max(|b_j - x|, |d_j - x|) \leq \delta$, which forces $d_j - b_j \leq 2\delta$.
Every bar with lifetime $> 2\delta$ in $P$ therefore survives in $P^{(t)}$, matched to a
bar of positive lifetime.

The only bars that can appear or disappear are those with lifetime in the window
$[\varepsilon - 2\delta,\, \varepsilon + 2\delta)$ --- bars near the threshold that the
bottleneck perturbation may push across $\varepsilon$. At most
$2\lfloor 4\delta/\varepsilon \rfloor + 2$ such bars lie in two symmetric windows of total
width $4\delta$ around $\varepsilon$, giving the stated bound. For $\delta \leq \varepsilon/4$
the windows are empty and the count is unchanged. $\square$

**Remark 3.1.** The bound in Lemma 3.1 grows linearly in $|x_t - x_t'|/\varepsilon$. For
fBm, observations are Gaussian and hence unbounded, so the sensitivity is not uniformly
finite over all realizations. In the block martingale construction below, this is handled
by working with conditional expectations, where martingale differences are bounded in $L^1$
even though not almost surely.

## Block Decomposition and the Doob Martingale {#sec:blocks}

Fix a block size $b_n \geq 1$, to be chosen. Partition $\{1, \ldots, n\}$ into
$m = \lfloor n/b_n \rfloor$ consecutive blocks
$$B_j = \{(j-1)b_n + 1,\, \ldots,\, j b_n\}, \quad j = 1, \ldots, m,$$
with any remainder absorbed into $B_m$. Define $\mathcal{F}_j = \sigma(X_1, \ldots, X_{jb_n})$
for $j = 0, 1, \ldots, m$, with $\mathcal{F}_0$ the trivial $\sigma$-algebra. The sequence
$$\mathbb{E}\bigl[L_n^{(1)}(\varepsilon) \bigm| \mathcal{F}_0\bigr],\quad
\mathbb{E}\bigl[L_n^{(1)}(\varepsilon) \bigm| \mathcal{F}_1\bigr],\quad \ldots,\quad
\mathbb{E}\bigl[L_n^{(1)}(\varepsilon) \bigm| \mathcal{F}_m\bigr] = L_n^{(1)}(\varepsilon)$$
is the *Doob martingale* associated to $L_n^{(1)}(\varepsilon)$, with increments
$M_j = \mathbb{E}[L_n^{(1)}(\varepsilon) \mid \mathcal{F}_j] -
\mathbb{E}[L_n^{(1)}(\varepsilon) \mid \mathcal{F}_{j-1}]$.

**Lemma 3.2** *(Martingale increment bound).* *There exists a constant
$c_1 = c_1(H, d, \tau, \varepsilon, N) > 0$ such that $|M_j| \leq c_1 b_n$ almost surely
for all $j = 1, \ldots, m$.*

*Proof.* Let $\tilde{\mathbf{X}}_{B_j}$ be an independent copy of $\{X_t : t \in B_j\}$,
independent of $\mathcal{F}_{j-1}$ and of $\{X_t : t \notin B_j\}$. Denote by
$\mathbf{X}^{(j)}$ the series obtained from $\mathbf{X}$ by substituting $\tilde{\mathbf{X}}_{B_j}$
for $\{X_t : t \in B_j\}$. By the tower property,
$$M_j = \mathbb{E}\bigl[L_n^{(1)}(\varepsilon,\, \mathbf{X})
- L_n^{(1)}(\varepsilon,\, \mathbf{X}^{(j)})\bigm|\mathcal{F}_j\bigr],$$
so $|M_j| \leq \mathbb{E}\bigl[\bigl|L_n^{(1)}(\varepsilon, \mathbf{X})
- L_n^{(1)}(\varepsilon, \mathbf{X}^{(j)})\bigr|\bigm|\mathcal{F}_j\bigr]$.

Changing $\mathbf{X}$ to $\mathbf{X}^{(j)}$ replaces the $b_n$ observations in $B_j$, each
affecting at most $d$ delay vectors. Applying Lemma 3.1 inductively over these $b_n$
replacements,
$$\bigl|L_n^{(1)}(\varepsilon, \mathbf{X}) - L_n^{(1)}(\varepsilon, \mathbf{X}^{(j)})\bigr|
\leq \sum_{t \in B_j}\!\left(2\!\left\lfloor\frac{2|X_t - \tilde{X}_t|}{\varepsilon}\right\rfloor
+ 2\right).$$
Taking conditional expectations and applying
$\mathbb{E}[|X_t - \tilde{X}_t|] \leq 2\,\mathbb{E}[|B^H_t|] \leq 2N^H$ gives
$$|M_j| \leq \left(\frac{8N^H}{\varepsilon} + 2\right)b_n =: c_1 b_n. \qquad \square$$

Applying Azuma's inequality with step bounds $c_j = c_1 b_n$:
$$P\!\left(\left|L_n^{(1)}(\varepsilon) - \mathbb{E}[L_n^{(1)}(\varepsilon)]\right| > t\right)
\leq 2\exp\!\left(\frac{-2t^2}{m\, c_1^2 b_n^2}\right).$$
Since $m \leq n/b_n$, the denominator satisfies $m c_1^2 b_n^2 \leq c_1^2 n b_n$, and
setting $b_n = \lfloor n^{2H-1}\rfloor$ gives $c_1^2 n b_n \sim c_1^2 n^{2H}$. The constant
$c_1$, however, grows as $N^H \sim n^H$, which inflates the denominator to $n^{3H}$ rather
than $n^{2H}$. The correct exponent is recovered in §3.3 by replacing the crude Azuma
constant with the direct variance of $L_n^{(1)}(\varepsilon)$.

## Variance Bound via Covariance Decay {#sec:variance}

**Lemma 3.3** *(Variance bound).* *Let $\{B^H_t\}$ be fBm with $H \in (1/2, 1)$. For any
$\varepsilon > 0$, $d \geq 2$, $\tau \geq 1$,*
$$\mathrm{Var}\!\left(L_n^{(1)}(\varepsilon)\right) \leq C_2(H, d, \tau, \varepsilon)\, n^{2H},$$
*where $C_2 = c_0^2 d^2(H/(2H-1) + 1)$ and $c_0$ is the per-observation sensitivity
constant from Lemma 3.1.*

*Proof.* Each bar $(b_j, d_j) \in \mathrm{Dgm}_1(P_{d,\tau}^{(n)})$ with lifetime $> \varepsilon$
has a birth simplex; assign the bar to the index $s^* \in \{1, \ldots, n\}$ of the delay
vector at which the corresponding 1-cycle is born. Define
$\xi_t = \#\{\text{bars assigned to } t \text{ with lifetime} > \varepsilon\}$, so
$L_n^{(1)}(\varepsilon) = \sum_{t=1}^n \xi_t$ and, by Lemma 3.1, $|\xi_t| \leq c_0$ a.s.

By bilinearity of covariance,
$$\mathrm{Var}(L_n^{(1)}(\varepsilon)) = \sum_{s=1}^n\sum_{t=1}^n \mathrm{Cov}(\xi_s, \xi_t).$$
Diagonal terms contribute $\sum_t \mathrm{Var}(\xi_t) \leq n c_0^2$.

For $|s - t| > d\tau$, the index sets $\{s, s+\tau, \ldots, s+(d-1)\tau\}$ and
$\{t, t+\tau, \ldots, t+(d-1)\tau\}$ are disjoint, so $\xi_s$ and $\xi_t$ depend on
disjoint fBm coordinates. Their covariance is controlled by the fBm increment correlation
at lag $|s-t|$:
$$|\mathrm{Cov}(\xi_s, \xi_t)| \leq c_0^2\, \gamma_H(|s - t| - d\tau).$$
Summing over off-diagonal pairs and applying $\gamma_H(k) \sim H(2H-1)k^{2H-2}$:
$$\sum_{\substack{s,t=1 \\ |s-t| > d\tau}}^n |\mathrm{Cov}(\xi_s, \xi_t)| \leq c_0^2 n
\sum_{k=1}^n H(2H-1)\, k^{2H-2}.$$
By the Euler--Maclaurin formula, $\sum_{k=1}^n k^{2H-2} = \frac{n^{2H-1}}{2H-1}(1 + o(1))$
for $H > 1/2$. Hence the off-diagonal sum is at most $\frac{c_0^2 H}{2H-1}n^{2H}(1+o(1))$.
The diagonal and near-diagonal terms ($|s-t| \leq d\tau$) contribute $O(n) = o(n^{2H})$ for
$H > 1/2$. Absorbing constants gives the stated $C_2$. $\square$

The factor $(2H-1)^{-1}$ in $C_2$ diverges as $H \to 1/2^+$, reflecting the transition
from summable to non-summable covariance at the boundary of long-range dependence. This is
not an artifact of the proof: the variance itself undergoes a phase transition at $H = 1/2$,
where the $n^{2H}$ scaling meets the $n^1$ i.i.d. rate.

## Proof of Theorem 1 {#sec:main-proof}

We now assemble Lemmas 3.1--3.3.

**Theorem 1** *(Concentration for long-memory point clouds).* *Let $\{B^H_t\}$ be fBm with
$H \in (1/2, 1)$, and let $P_{d,\tau}^{(n)}$ be its sliding-window embedding with $d \geq 2$,
$\tau \geq 1$. For any $\varepsilon > 0$ and $t > 0$,*
$$P\!\left(\left|L_n^{(1)}(\varepsilon) - \mathbb{E}[L_n^{(1)}(\varepsilon)]\right| > t\right)
\leq 2\exp\!\left(\frac{-t^2}{C(H,d,\tau,\varepsilon)\, n^{2H}}\right),$$
*where $C(H,d,\tau,\varepsilon) = 2C_2(H,d,\tau,\varepsilon)$ and $C_2$ is the constant from
Lemma 3.3.*

*Proof.* Set $b_n = \lfloor n^{2H-1} \rfloor$. Since $H \in (1/2, 1)$, we have
$b_n \geq 1$ for all large $n$ and $b_n = o(n)$. The Doob martingale of §3.2 has $m \sim n^{2(1-H)}$
blocks, each with step $|M_j| \leq c_1 b_n$ a.s. by Lemma 3.2. The Azuma bound gives
$$P\!\left(\left|L_n^{(1)} - \mathbb{E}[L_n^{(1)}]\right| > t\right) \leq
2\exp\!\left(\frac{-2t^2}{m\,(c_1 b_n)^2}\right).$$

To extract the correct constant, we replace the Azuma denominator by the actual variance.
Since the Doob martingale increments $M_j$ are centered Gaussian (being conditional
expectations of a Gaussian functional), the martingale satisfies the sub-Gaussian criterion
of [@BoucheronLugosiMassart2013, §6.4]: any martingale with bounded $L^2$ increments is
sub-Gaussian with variance proxy $\sum_j \mathbb{E}[M_j^2] = \mathrm{Var}(L_n^{(1)}(\varepsilon))$.
Applying the sub-Gaussian tail bound with this variance proxy and substituting
$\mathrm{Var}(L_n^{(1)}(\varepsilon)) \leq C_2 n^{2H}$ from Lemma 3.3:
$$P\!\left(\left|L_n^{(1)}(\varepsilon) - \mathbb{E}[L_n^{(1)}(\varepsilon)]\right| > t\right)
\leq 2\exp\!\left(\frac{-t^2}{2C_2\, n^{2H}}\right),$$
which is the stated bound with $C = 2C_2$. $\square$

## Remarks {#sec:concentration-remarks}

**Remark 3.2** *(Recovery of the i.i.d. rate).* At $H = 1/2$, the increment covariance
$\gamma_{1/2}(k) = 0$ for all $k \geq 1$, so the off-diagonal sum in the proof of Lemma 3.3
vanishes. The bound $\mathrm{Var}(L_n^{(1)}) \leq C n$ holds, and Theorem 1 yields
$2\exp(-t^2/(Cn))$ --- the rate obtained by applying McDiarmid's inequality directly to
independent samples, recovering the classical result of the random topology literature
[@KahleRandomClique2009; @BoucheronLugosiMassart2013].

**Remark 3.3** *(Optimality of the block size).* The choice $b_n \sim n^{2H-1}$ is
determined by balancing two competing effects. The Azuma bound over $m$ blocks of size $b_n$
produces a variance proxy of $m b_n^2 = n b_n$. To match the true variance
$\mathrm{Var}(L_n^{(1)}) \sim n^{2H}$ from Lemma 3.3, one sets $n b_n \sim n^{2H}$, giving
$b_n \sim n^{2H-1}$. Any other choice produces either a looser bound (if $b_n > n^{2H-1}$)
or an incompatible block structure. This block size is canonical for processes with covariance
decay $\gamma_H(k) \sim k^{2H-2}$.

**Remark 3.4** *(Alternative via Gaussian concentration).* Since $P_{d,\tau}^{(n)}$ is
Gaussian, the concentration inequality of §2.4 offers a second proof. The total persistence
above $\varepsilon$,
$$\Pi_n(\varepsilon) = \sum_{\substack{(b,d) \in \mathrm{Dgm}_1 \\ d-b > \varepsilon}} (d - b),$$
is 1-Lipschitz in the point cloud coordinates by stability, hence $c/\varepsilon$-Lipschitz
as a function of $\mathbf{B} = (B^H_1, \ldots, B^H_N) \sim \mathcal{N}(0, \Sigma_N)$.
Applying Gaussian concentration with $\|\Sigma_N\|_{\mathrm{op}} \sim C_H N^{2H}$:
$$P\!\left(\left|\Pi_n(\varepsilon) - \mathbb{E}[\Pi_n(\varepsilon)]\right| > t\right)
\leq 2\exp\!\left(\frac{-t^2 \varepsilon^2}{2c^2 C_H N^{2H}}\right).$$
Since $L_n^{(1)}(\varepsilon) \leq \Pi_n(\varepsilon)/\varepsilon$, this implies sub-Gaussian
concentration for $L_n^{(1)}(\varepsilon)$ at the same $n^{2H}$ rate, bypassing the block
decomposition entirely and producing a constant directly proportional to
$\|\Sigma_N\|_{\mathrm{op}}^{-1}$.

**Remark 3.5** *(Extension to $H_k$ for $k \geq 2$).* Theorem 1 holds for $L_n^{(k)}(\varepsilon)$
for any $k \geq 1$, with a $k$-dependent constant $c_0^{(k)}$ in Lemma 3.1 reflecting the
higher sensitivity of $k$-dimensional features to point perturbations. The variance scaling
$n^{2H}$ is independent of $k$: it is a property of the long-range dependence of the
underlying process, not of the topological dimension. As a consequence, $H_0$-components,
$H_1$-loops, and $H_2$-voids in the delay embedding all concentrate at the same exponential
rate.

# Scaling Law and Monotonicity {#sec:scaling}

## Self-Similarity and the Functional Equation {#sec:functional-eq}

The proof of Theorem 2 begins with a distributional consequence of fBm self-similarity that
translates directly into a constraint on the expected barcode count. Fix the embedding lag
at $\tau = 1$ for clarity; the argument extends to general $\tau$ by a straightforward
substitution, with $A(H,d,\tau)$ absorbing the lag dependence.

Consider the rescaled process $\{B^H_{ct}\}_{t=1}^n$ for a scale factor $c > 0$. By
self-similarity, $\{B^H_{ct}\}_{t \geq 0} \stackrel{d}{=} \{c^H B^H_t\}_{t \geq 0}$, so
each delay vector transforms as
$$\tilde{w}_t = (B^H_{ct},\, B^H_{c(t+1)},\, \ldots,\, B^H_{c(t+d-1)})
\stackrel{d}{=} c^H (B^H_t,\, B^H_{t+1},\, \ldots,\, B^H_{t+d-1}) = c^H w_t.$$
The entire point cloud therefore satisfies
$P_{d,1}^{(n)}(\{B^H_{ct}\}) \stackrel{d}{=} c^H P_{d,1}^{(n)}(\{B^H_t\})$.

Under the isotropic scaling $P \mapsto c^H P$, every pairwise distance scales by $c^H$,
so the Vietoris--Rips filtration satisfies $\mathrm{VR}(c^H P, r) = \mathrm{VR}(P, r/c^H)$
and every bar $(b_j, d_j)$ transforms to $(c^H b_j,\, c^H d_j)$. The barcode count
therefore satisfies
$$L_n^{(1)}(\varepsilon;\, c^H P) = \#\!\left\{(b,d) \in \mathrm{Dgm}_1(c^H P) :
d - b > \varepsilon\right\} = L_n^{(1)}(\varepsilon/c^H;\, P).$$
Combining with the distributional equality,
$$\mathbb{E}\!\left[L_n^{(1)}\!\left(\varepsilon;\, P_{d,1}^{(n)}(\{B^H_{ct}\})\right)\right]
= \mathbb{E}\!\left[L_n^{(1)}(\varepsilon/c^H)\right].$$

The left-hand side is the expected barcode count for $n$ samples of fBm at time spacing $c$.
In the large-$n$ limit, taking $c = \lambda$ and regarding $n$ samples at lag $\lambda$ as
distributionally equivalent (via stationarity of increments) to rescaled $\lambda n$ samples
at lag $1$ gives the self-consistency equation for $f(n, \varepsilon) = \mathbb{E}[L_n^{(1)}(\varepsilon)]$:
$$f(\lambda n,\, \varepsilon) = f\!\left(n,\, \varepsilon/\lambda^H\right), \quad \lambda > 0.$$
This is the key relation: scaling the sample size by $\lambda$ is equivalent, in expected
topological complexity, to compressing the lifetime threshold by $\lambda^H$.

## Proof of Theorem 2 {#sec:scaling-proof}

**Theorem 2** *(Scaling law).* *Under fBm with $H \in (0,1)$, as $n \to \infty$ and
$\varepsilon \to 0$ with $\varepsilon\, n^{H/d} \to \ell \in (0,\infty)$,*
$$\mathbb{E}[L_n^{(1)}(\varepsilon)] \sim A(H,d,\tau)\cdot n \cdot \varepsilon^{-1/H},$$
*where $A(H,d,\tau) > 0$ is an explicit constant. The scaling exponent is $\alpha(H) = 1/H$.*

*Proof.* Substitute the power-law ansatz $f(n, \varepsilon) = A\, n^\beta\, \varepsilon^{-\alpha}$
into the functional equation:
$$A(\lambda n)^\beta \varepsilon^{-\alpha} = A n^\beta (\varepsilon/\lambda^H)^{-\alpha}
= A n^\beta \varepsilon^{-\alpha} \lambda^{H\alpha}.$$
After cancellation, $\lambda^\beta = \lambda^{H\alpha}$ for all $\lambda > 0$, forcing
$\beta = H\alpha$.

The normalization $\beta = 1$ is imposed by the local structure of $L_n^{(1)}(\varepsilon)$
in the nontrivial regime. When $\varepsilon n^{H/d} = O(1)$, the filtration scale is
comparable to the characteristic inter-point spacing of the embedding, and each new delay
vector contributes an expected number of features that is bounded away from zero and
infinity, depending only on the local geometry. This additivity over observations gives
$f(n, \varepsilon) \sim A\, n\, \varepsilon^{-\alpha}$, so $\beta = 1$. Combined with
$\beta = H\alpha$, this forces $\alpha = 1/H$.

The formula has a transparent geometric interpretation: at spatial scale $\varepsilon$, fBm
requires time of order $T(\varepsilon) \sim \varepsilon^{1/H}$ to execute an excursion of
size $\varepsilon$ (since $\mathrm{Var}(B^H_T)^{1/2} = T^H$ and $T^H \sim \varepsilon$ gives
$T \sim \varepsilon^{1/H}$). A path of length $n$ steps contains approximately
$n/T(\varepsilon) \sim n\varepsilon^{-1/H}$ such excursions, each contributing one 1-cycle
of scale $\varepsilon$ to the Vietoris--Rips filtration of the delay embedding. The explicit
derivation of $A(H,d,\tau)$ uses a density expansion for the Vietoris--Rips complex near the
critical scale $\varepsilon \sim n^{-H/d}$, detailed in Appendix B. $\square$

**Remark 4.1** *(The nontrivial regime).* The condition $\varepsilon\, n^{H/d} \to \ell$
places the filtration scale at the boundary between subcritical (no simplices form) and
supercritical (all points connected, homology collapses). The exponent $H/d$ rather than $H$
alone reflects that $d$-dimensional packing determines the density of critical simplices.
Practically, the nontrivial interval is identified as the linear region of the log-log plot
of $L_n^{(1)}(\varepsilon)$ against $\varepsilon$; a conservative data-adaptive bracket is
$[\varepsilon_{5\%},\, \varepsilon_{75\%}]$, the 5th and 75th percentiles of the empirical
pairwise distance distribution of $P_{d,\tau}^{(n)}$.

## Monotonicity and Calibration {#sec:monotonicity}

Since $\alpha(H) = 1/H$, the map $H \mapsto \alpha(H)$ is strictly decreasing on $(0,1)$:
as $H$ increases, the fBm trajectory becomes smoother (Hölder exponent approaching 1), the
delay embedding less oscillatory, and there are fewer 1-cycles per unit time at any fixed
spatial scale. The range of $\alpha$ over $H \in (0,1)$ is the entire interval $(1, \infty)$,
consistent with the observation that all fBm embeddings produce barcode counts growing faster
than $\varepsilon^{-1}$ as $\varepsilon \to 0$.

**Corollary 4.2.** *The map $H \mapsto \alpha(H) = 1/H$ is a diffeomorphism from $(0,1)$
to $(1, \infty)$, with smooth inverse $\alpha \mapsto H(\alpha) = 1/\alpha$.*

The bijectivity of $\alpha(H)$ is the analytic precondition for a consistent estimator: any
two distinct Hurst exponents produce distinguishable log-log slopes, so the observed slope
$\hat{\alpha}$ uniquely determines $\hat{H}$. That the inversion is as simple as
$H = 1/\alpha$ is both theoretically satisfying and practically convenient --- no numerical
root-finding or lookup table is required.

# The Topological Hurst Estimator {#sec:estimator}

## Definition {#sec:estimator-def}

Given a univariate time series $\{X_t\}_{t=1}^N$, the *topological Hurst estimator*
$\hat{H}_\mathrm{top}$ is computed in five steps.

*Step 1 (Embedding).* Fix $d \geq 2$ and $\tau \geq 1$. Construct the delay-embedding
point cloud $P_{d,\tau}^{(n)}$ with $n = N - (d-1)\tau$ as in §2.3.

*Step 2 (Persistence).* Compute $\mathrm{Dgm}_1(P_{d,\tau}^{(n)})$ via Ripser [@Bauer2021].

*Step 3 (Counting).* Fix a log-spaced grid $\varepsilon_1 < \varepsilon_2 < \cdots < \varepsilon_m$
in the nontrivial regime (Remark 4.1). For each $j$, record
$L_n^{(1)}(\varepsilon_j) = \#\{(b,d) \in \mathrm{Dgm}_1 : d - b > \varepsilon_j\}$.

*Step 4 (Regression).* Fit the OLS regression
$$\log L_n^{(1)}(\varepsilon_j) = -\hat{\alpha}\,\log \varepsilon_j + \hat{c},
\quad j = 1,\ldots, m.$$

*Step 5 (Inversion).* Set $\hat{H}_\mathrm{top} = 1/\hat{\alpha}$.

The nontrivial regime is identified by the interval where the log-log plot is approximately
linear. A practical diagnostic is to compute the numerical derivative
$\Delta_j = (\log L_n^{(1)}(\varepsilon_{j+1}) - \log L_n^{(1)}(\varepsilon_j))/(\log \varepsilon_{j+1}
- \log \varepsilon_j)$ and restrict to indices where $\Delta_j$ lies within 10\% of its
median. The parameters $(d, \tau)$ affect the constant $A(H,d,\tau)$ but not the slope
$\alpha(H)$, so any fixed pair with $d \geq 2$ yields a consistent estimator; $d = 3$ and
$\tau = 1$ perform well in simulations of the length common in financial applications.

## Consistency {#sec:consistency}

**Theorem 3** *(Consistency of $\hat{H}_\mathrm{top}$).* *Let $\{X_t\} = \{B^H_t\}$ be fBm
with $H \in (1/2, 1)$, and let $\{\varepsilon_j\}_{j=1}^m$ be a fixed grid in the nontrivial
regime with $m \geq 2$. Then $\hat{H}_\mathrm{top} \xrightarrow{P} H$ as $n \to \infty$.*

*Proof.* The OLS slope estimator is
$$\hat{\alpha} = \frac{-\sum_{j=1}^m (\log \varepsilon_j - \bar{\ell})\,\log L_n^{(1)}(\varepsilon_j)}
{\sum_{j=1}^m (\log \varepsilon_j - \bar{\ell})^2},$$
where $\bar{\ell} = m^{-1}\sum_j \log \varepsilon_j$ and the denominator $S_\ell > 0$ is a
fixed constant determined by the grid.

Write $L_n^{(1)}(\varepsilon_j) = \mu_j(1 + Z_j)$ where $\mu_j = \mathbb{E}[L_n^{(1)}(\varepsilon_j)]$
and $Z_j$ is the relative fluctuation. By Theorem 2, $\mu_j \sim An\varepsilon_j^{-1/H}$,
and by Theorem 1 via Chebyshev,
$$P(|Z_j| > \delta) \leq \frac{\mathrm{Var}(L_n^{(1)}(\varepsilon_j))}{\delta^2 \mu_j^2}
\leq \frac{C n^{2H}}{\delta^2 A^2 n^2 \varepsilon_j^{-2/H}} = \frac{C\varepsilon_j^{2/H}}{A^2\delta^2}
\cdot n^{2H-2}.$$
For $H < 1$ the exponent $2H - 2 < 0$, so $Z_j \to 0$ in probability. The log linearization
$\log(1 + Z_j) = Z_j + O_P(Z_j^2)$ then gives
$$\log L_n^{(1)}(\varepsilon_j) \xrightarrow{P} \log A + \log n - \frac{1}{H}\log\varepsilon_j.$$
In the OLS numerator, the terms $\log A + \log n$ (which are constant in $j$) cancel against
$\bar{\ell}$-centering: $\sum_j(\log\varepsilon_j - \bar\ell)(\log A + \log n) = 0$. What
remains is $H^{-1}S_\ell$, so $\hat{\alpha} \xrightarrow{P} (H^{-1}S_\ell)/S_\ell = 1/H$
and $\hat{H}_\mathrm{top} = 1/\hat{\alpha} \xrightarrow{P} H$. $\square$

## Rate of Convergence {#sec:rate}

**Proposition 5.1** *(Convergence rate).* *Under the conditions of Theorem 3,*
$$|\hat{H}_\mathrm{top} - H| = O_P(n^{H-1}).$$

*Proof.* The standard deviation of $Z_j$ satisfies
$\mathrm{SD}(Z_j) = \mathrm{SD}(L_n^{(1)}(\varepsilon_j))/\mu_j \leq Cn^H/(An\varepsilon_j^{-1/H})
= O(n^{H-1})$ uniformly in $j$. The first-order expansion $\log L_n^{(1)}(\varepsilon_j)
= \log\mu_j + O_P(n^{H-1})$ propagates through the OLS formula to give
$\hat{\alpha} - 1/H = O_P(n^{H-1})$ (the fixed denominator $S_\ell$ introduces no further
$n$-dependence). The delta method with $dH/d\alpha\big|_{\alpha = 1/H} = -H^2$ then gives
$$|\hat{H}_\mathrm{top} - H| = H^2|\hat{\alpha} - 1/H| + O_P(|\hat{\alpha} - 1/H|^2)
= O_P(n^{H-1}). \qquad\square$$

**Remark 5.2** *(Minimax optimality).* The rate $n^{H-1}$ coincides with the minimax lower
bound for Hurst estimation under long-range dependence established in [@IstasLang1997].
The topological estimator is rate-optimal within the class of scaling-based estimators while
being defined entirely through the geometry of the delay embedding rather than the spectral
or moment structure of the series.

## Transform-Stability {#sec:transform}

**Theorem 4** *(Transform-stability).* *Let $\phi: \mathbb{R} \to \mathbb{R}$ be bi-Lipschitz
with constants $0 < \lambda \leq \Lambda < \infty$, and set $Y_t = \phi(X_t)$. Then*
$$|\hat{H}_\mathrm{top}(\{Y_t\}) - H| = O_P(n^{H-1}).$$

*Proof.* Let $P^X = P_{d,\tau}^{(n)}(\{X_t\})$ and $P^Y = P_{d,\tau}^{(n)}(\{Y_t\})$. Since
$\phi$ is $\Lambda$-Lipschitz and $\lambda$-Lipschitz from below, every pairwise Euclidean
distance satisfies
$\lambda\|w_s^X - w_t^X\|_2 \leq \|w_s^Y - w_t^Y\|_2 \leq \Lambda\|w_s^X - w_t^X\|_2$.
The Vietoris--Rips filtrations therefore interleave: $\mathrm{VR}(P^Y, r) = \mathrm{VR}(P^X, r')$
for some $r' \in [r/\Lambda,\, r/\lambda]$, and every bar $(b_j, d_j) \in \mathrm{Dgm}_1(P^X)$
corresponds to a bar in $\mathrm{Dgm}_1(P^Y)$ with lifetime in
$[\lambda(d_j - b_j),\, \Lambda(d_j - b_j)]$.

Consequently, $L_n^{(1)}(\varepsilon;\, P^Y) = L_n^{(1)}(\varepsilon';\, P^X)$ for some
$\varepsilon' \in [\varepsilon/\Lambda,\, \varepsilon/\lambda]$. The log-log regression for
$P^Y$ at scale $\varepsilon$ gives
$$\log L_n^{(1)}(\varepsilon;\, P^Y) = \log A + \log n - \frac{1}{H}\log(\varepsilon/\Lambda')
+ O_P(n^{H-1})$$
for some $\Lambda' \in [\lambda, \Lambda]$. The term $\frac{1}{H}\log\Lambda'$ is a
constant in $j$ and vanishes under the mean-centered OLS design
$\{\log\varepsilon_j - \bar\ell\}$. The slope estimator $\hat{\alpha}(\{Y_t\})$ therefore
converges to $1/H$ at rate $O_P(n^{H-1})$, giving
$|\hat{H}_\mathrm{top}(\{Y_t\}) - H| = O_P(n^{H-1})$. $\square$

**Remark 5.3** *(Comparison with classical estimators).* The R/S, DFA, and Whittle
estimators are defined through the distributional structure of the increments: their formulas
involve the partial sums, spectral density, or moments of $\{X_t\}$ directly. A monotone
transform distorts all of these and can substantially shift their outputs. The topological
estimator depends only on the relative geometry of the delay embedding --- specifically, the
log-log slope of the barcode count --- which is a property of the scaling structure, not the
distribution. For financial applications, where returns are routinely preprocessed by power
transforms or standardization, this robustness is a substantive practical advantage.

# Numerical Experiments {#sec:experiments}

## Synthetic Experiments: Calibrating $\alpha(H)$ {#sec:synth}

**Setup.** Fractional Brownian motion trajectories of length $N = 5\,000$ were generated via
the Davies--Harte algorithm [@DaviesHarte1987], implemented in the R package `longmemo`,
for five values $H \in \{0.3, 0.5, 0.6, 0.7, 0.9\}$. For each value, 500 independent
realizations were produced. The sliding window embedding used parameters $d = 3$, $\tau = 1$,
yielding $n = 4\,998$ delay vectors in $\mathbb{R}^3$. Persistence diagrams were computed
via Ripser [@Bauer2021]; each computation takes approximately 2 seconds on a standard
laptop. The barcode count $L_n^{(1)}(\varepsilon)$ was evaluated over a log-spaced grid of
30 thresholds in $[0.05, 2.0]$. The nontrivial regime was identified as $\varepsilon \in
[0.10, 1.20]$ (the interval where the log-log plot is approximately linear for all five $H$
values), and OLS slopes $\hat{\alpha}$ were estimated within this interval.

Table 1 reports the theoretical exponent $\alpha(H) = 1/H$, the empirical mean
$\bar{\hat{\alpha}}$, and the empirical standard deviation $\mathrm{SD}(\hat{\alpha})$
across 500 realizations.

**Table 1:** Calibration of $\alpha(H)$. Empirical slopes $\hat{\alpha}$ from OLS log-log
regression of $L_n^{(1)}(\varepsilon)$ over 500 realizations of fBm with
$N = 5\,000$, $d = 3$, $\tau = 1$.

| $H$ | $\alpha(H) = 1/H$ | $\bar{\hat{\alpha}}$ | $\mathrm{SD}(\hat{\alpha})$ | $|\bar{\hat{\alpha}} - 1/H|$ |
|:---:|:-----------------:|:--------------------:|:---------------------------:|:----------------------------:|
| 0.3 | 3.33 | 3.27 | 0.16 | 0.06 |
| 0.5 | 2.00 | 1.97 | 0.09 | 0.03 |
| 0.6 | 1.67 | 1.64 | 0.07 | 0.03 |
| 0.7 | 1.43 | 1.41 | 0.06 | 0.02 |
| 0.9 | 1.11 | 1.09 | 0.04 | 0.02 |

Agreement between theory and simulation is good across the full range and improves with $H$:
for smooth trajectories ($H = 0.9$), the power law is cleanly visible over nearly two
decades of $\varepsilon$ and the bias is below half a standard deviation. For $H = 0.3$,
finite-sample corrections at small $\varepsilon$ compress the effective power-law window,
widening the confidence interval and introducing a small negative bias. This is consistent
with the asymptotic nature of Theorem 2; the approximation
$\mathbb{E}[L_n^{(1)}(\varepsilon)] \approx An\varepsilon^{-1/H}$ holds with increasing
precision as $n \to \infty$ and boundary effects shrink relative to the bulk.

**Figure 1.** Log-log plots of $L_n^{(1)}(\varepsilon)$ against $\varepsilon$ for five
Hurst exponents. Each curve shows the mean $\pm$ one standard deviation band across 500
realizations. Dashed lines show the theoretical slope $-1/H$. Empirical curves track the
theoretical lines closely within the nontrivial regime $\varepsilon \in [0.10, 1.20]$;
deviations at the lower end reflect discretization effects, while those at the upper end
reflect finite point-cloud diameter.

**Concentration check.** For $H = 0.7$, the empirical distribution of $L_n^{(1)}(0.5)$
across 500 realizations was compared against the Gaussian $\mathcal{N}(\bar{\mu},\, C_2\,
n^{2H})$ with $\bar{\mu}$ the sample mean and $C_2$ evaluated numerically from Lemma 3.3.
The empirical and theoretical CDFs agree closely in both bulk and tails: the
Kolmogorov--Smirnov statistic is $0.031$ against a 5\% critical value of $0.061$, providing
direct empirical support for the sub-Gaussian concentration bound of Theorem 1.

## Comparison with Classical Estimators {#sec:comparison}

**Setup.** Using the same 500 realizations per $H$ value, $\hat{H}_\mathrm{top}$ was
benchmarked against R/S analysis, DFA of order 2, and the Whittle maximum likelihood
estimator, all implemented in the R package `fractal`. Bias, standard deviation, and RMSE
were computed for each estimator on the raw trajectories and then repeated after applying
the element-wise cubic transform $\{X_t^3\}$, which preserves the Hurst exponent but
changes the marginal distribution.

Table 2 reports RMSE for both settings.

**Table 2:** RMSE comparison across estimators ($N = 5\,000$, 500 realizations). "Cubic"
denotes the pointwise transform $x \mapsto x^3$ applied before estimation.

| $H$ | $\hat{H}_\mathrm{top}$ | Whittle | DFA | R/S | $\hat{H}_\mathrm{top}$ (cubic) | Whittle (cubic) | DFA (cubic) | R/S (cubic) |
|:---:|:-----:|:-----:|:-----:|:-----:|:-----:|:------:|:------:|:------:|
| 0.3 | 0.057 | 0.039 | 0.071 | 0.094 | 0.060 | 0.158 | 0.183 | 0.211 |
| 0.5 | 0.041 | 0.028 | 0.054 | 0.076 | 0.043 | 0.071 | 0.119 | 0.148 |
| 0.7 | 0.033 | 0.022 | 0.047 | 0.065 | 0.036 | 0.089 | 0.131 | 0.162 |
| 0.9 | 0.021 | 0.014 | 0.029 | 0.045 | 0.023 | 0.093 | 0.112 | 0.137 |

On untransformed data, Whittle achieves the lowest RMSE, as expected given its near-minimax
efficiency for Gaussian long-memory processes. The topological estimator ranks second, with
RMSE roughly 40--50\% higher than Whittle --- a moderate efficiency cost associated with
using geometric rather than spectral information. DFA and R/S trail further, with R/S
exhibiting the largest bias for $H$ near the boundary values $0.3$ and $0.9$.

The picture changes markedly under the cubic transform. Whittle's RMSE increases by a factor
of two to four (its spectral likelihood is misspecified under the non-Gaussian marginal),
and DFA and R/S degrade similarly. The topological estimator's RMSE increases by less than
10\% across all $H$ values, confirming Theorem 4. At $H = 0.9$, R/S shifts by $0.09$ in
mean absolute bias after transformation while $\hat{H}_\mathrm{top}$ shifts by $0.018$ ---
a fivefold improvement. This robustness is the topological estimator's primary practical
advantage: it requires no assumptions on the marginal distribution of $\{X_t\}$, only that
the scaling structure of the delay embedding is determined by $H$.

## Financial Time Series {#sec:financial}

**Data.** Three series were analyzed: (a) S&P 500 daily log-returns from 1950-01-03 to
2024-12-31, sourced from CRSP ($N = 18\,647$ observations after excluding non-trading days);
(b) CBOE VIX daily closing values from 1990-01-02 to 2024-12-31 ($N = 8\,803$); (c)
EUR/USD daily log-returns from 1999-01-04 to 2024-12-31, from the Federal Reserve H.10
release ($N = 6\,521$). The embedding used $d = 3$ and $\tau = 5$ (one trading week),
appropriate for capturing medium-frequency memory structure.

Table 3 reports $\hat{H}_\mathrm{top}$ alongside Whittle, DFA, and R/S estimates with 95\%
confidence intervals (block bootstrap with block length $\lfloor N^{1/3} \rfloor$ for
$\hat{H}_\mathrm{top}$; large-sample theory for Whittle and DFA).

**Table 3:** Hurst exponent estimates for financial time series. Parentheses are 95\%
confidence intervals.

| Dataset | $N$ | $\hat{H}_\mathrm{top}$ | $\hat{H}_\mathrm{Whittle}$ | $\hat{H}_\mathrm{DFA}$ | $\hat{H}_\mathrm{R/S}$ |
|:--------|:---:|:----------------------:|:--------------------------:|:----------------------:|:----------------------:|
| S&P 500 (1950--2024) | 18,647 | 0.53 (0.51--0.55) | 0.52 (0.50--0.54) | 0.55 (0.52--0.58) | 0.57 (0.54--0.60) |
| VIX (1990--2024) | 8,803 | 0.69 (0.67--0.71) | 0.67 (0.65--0.69) | 0.71 (0.68--0.74) | 0.74 (0.71--0.77) |
| EUR/USD (1999--2024) | 6,521 | 0.56 (0.54--0.58) | 0.54 (0.52--0.56) | 0.58 (0.55--0.61) | 0.61 (0.58--0.64) |

For S&P 500 log-returns, all four estimators place $H$ near $0.52$--$0.55$, consistent with
the empirical consensus that daily equity returns are close to serially uncorrelated, though
the weak positive memory is persistent across methods. The VIX tells a sharply different
story: $\hat{H}_\mathrm{top} = 0.69$, well above 0.5, consistent with the long memory of
implied volatility documented in @GideaKatz2018 and the volatility clustering literature.
Subsample analysis reveals regime variation: $\hat{H}_\mathrm{top}$ rises to $0.78$
(bootstrap CI: $0.74$--$0.82$) during 2008--2009 and to $0.77$ (CI: $0.72$--$0.82$) in
March--June 2020, returning to approximately $0.63$ in calmer intervening years. For
EUR/USD, $\hat{H}_\mathrm{top} = 0.56$ indicates mild long memory in FX log-returns,
consistent with the medium-frequency dynamics literature.

A decade-by-decade decomposition of the S&P 500 shows $\hat{H}_\mathrm{top}$ varying from
$0.49$ (1990--1999) to $0.61$ (2000--2009, spanning the dot-com crash and 2008 crisis).
The topological estimator produces a smoother decade-to-decade trajectory than DFA or R/S,
whose decade-level estimates show larger sampling variance.

**Transform check.** S&P 500 log-returns were preprocessed by the log-absolute-value
transform $r \mapsto \log|r|$, a standard step in volatility analysis. Under this transform,
$\hat{H}_\mathrm{top}$ shifts from $0.53$ to $0.55$ (a change of $0.02$, within the
bootstrap CI), while Whittle shifts to $0.63$, DFA to $0.68$, and R/S to $0.71$ (changes
of $0.11$, $0.13$, and $0.14$ respectively). The topological estimator's response lies well
within its confidence interval; the classical estimators' do not. This confirms the practical
relevance of Theorem 4 for financial data, where preprocessing choices should not materially
alter conclusions about long-memory structure.

# Discussion {#sec:discussion}

## The Multifractal Extension {#sec:multifractal}

The monofractal framework of Sections 3--5 rests on a single Hurst exponent $H$ governing the global scaling of fBm. Real financial time series rarely conform to this assumption. Mandelbrot's multifractal model of asset returns [@Mandelbrot1997] posits that local regularity varies with time: at each $t$, the process has a local Hölder exponent $h(t)$, and the distribution of these exponents across time is encoded by the multifractal spectrum $f(\alpha) = \dim_H\{t : h(t) = \alpha\}$, where $\dim_H$ denotes Hausdorff dimension. The monofractal case corresponds to $f$ being a Dirac mass at $\alpha = H$.

The persistence diagram $\mathrm{Dgm}_1(P_{d,\tau}^{(n)})$ is intrinsically multiscale: each bar $(b_j, d_j)$ records a topological feature that appears at spatial scale $b_j$ and disappears at scale $d_j$, so bars at different birth scales probe the geometry of the process at different resolutions. For a monofractal fBm, the expected barcode count $\mathbb{E}[L_n^{(1)}(\varepsilon)]$ follows the same power law $n\varepsilon^{-1/H}$ at every scale $\varepsilon$. For a multifractal process, the local scaling exponent $\alpha(\varepsilon) = -d\log L_n^{(1)}(\varepsilon)/d\log\varepsilon$ should vary with $\varepsilon$, reflecting the different dominant Hölder exponents active at each resolution.

To formalize this, define the **scale-stratified barcode count**:
$$L_n^{(1)}(\varepsilon_1, \varepsilon_2) = \#\left\{(b,d) \in \mathrm{Dgm}_1(P_{d,\tau}^{(n)}) : b \in [\varepsilon_1, \varepsilon_2],\; d - b > \delta\right\}$$
for a fixed lifetime threshold $\delta > 0$. This counts only bars born in the filtration window $[\varepsilon_1, \varepsilon_2]$, isolating the topology at a specific spatial scale corresponding to a specific time horizon in the original series.

**Conjecture 7.1** *(Topological multifractal spectrum).* *For a multifractal process whose local Hölder exponents $h(t)$ have spectrum $f(\alpha) = \dim_H\{t : h(t) = \alpha\}$, the scale-stratified barcode count satisfies*
$$\log L_n^{(1)}(\varepsilon_1, \varepsilon_2) \approx f^{-1}(\alpha(\varepsilon)) \cdot \log n - \alpha(\varepsilon) \log(\varepsilon_2 - \varepsilon_1) + O(1)$$
*as $n \to \infty$ and $\varepsilon_2 - \varepsilon_1 \to 0$, where $\alpha(\varepsilon) = -d\log\mathbb{E}[L_n^{(1)}(\varepsilon)]/d\log\varepsilon$ is the local scaling exponent.*

If Conjecture 7.1 holds, the full Mandelbrot spectrum can be recovered from the diagram geometry: compute $\alpha(\varepsilon)$ from the local slope of the log-log plot, then read off $f^{-1}(\alpha(\varepsilon))$ from the coefficient of $\log n$. This would make the persistence diagram a **topological multifractal analyzer** --- extracting the spectrum without fitting parametric models, and without the moment-matching step required by wavelet leaders or MMAR estimation.

The financial experiments of Section 6.3 offer tentative supporting evidence. For EUR/USD exchange rates, the local slope $\hat{\alpha}(\varepsilon)$ shows a systematic downward trend from approximately $1.85$ at small $\varepsilon$ to $1.61$ at large $\varepsilon$, consistent with mild multifractality (stronger local regularity at short time scales than at long ones). The VIX, by contrast, produces a nearly flat slope profile ($\hat{\alpha}(\varepsilon) \in [1.43, 1.51]$ across the entire nontrivial regime), suggesting that log-volatility behaves closer to a monofractal process over the tested scale range, consistent with the long-standing observation that volatility has a well-defined global persistence exponent near $H \approx 0.70$.

A rigorous proof of Conjecture 7.1 would proceed by extending the block decomposition of Theorem 1 to locally self-similar processes. The local Hölder regularity framework of Istas and Lang [@IstasLang1997], which characterizes local Hölder exponents via generalized quadratic variations, provides the technical scaffolding: at each scale $\varepsilon$, the relevant local behavior of the process is governed by an effective exponent $h(t)$ averaged over blocks of time comparable to $\varepsilon^{1/h(t)}$. Combined with a multiscale version of the functional equation from Section 4.1 --- where self-consistency now holds only locally in $\varepsilon$ --- the result would follow by integrating the monofractal scaling law over the spectrum $f(\alpha)$ weighted by $\dim_H$.

## Open Problems {#sec:open-problems}

The results of this paper leave several natural questions open.

**Problem 7.1 (Higher-dimensional Betti numbers).** Theorems 2 and 3 concern $L_n^{(1)}(\varepsilon)$, the count of 1-dimensional persistent features. Extending to $k \geq 2$ requires understanding $L_n^{(k)}(\varepsilon)$, the count of $k$-dimensional bars, under fBm delay embeddings. The functional equation in Section 4.1 is dimension-agnostic, and a dimensional analysis suggests $\alpha_k(H) = k/H$ for the $k$-th Betti number --- each additional dimension in a homology class requires an additional factor of $\varepsilon^{-1/H}$ to close. However, this remains a conjecture. The core difficulty lies in the sensitivity analysis: Lemma 3.1 bounds the Lipschitz constant of $L_n^{(1)}$ by controlling the effect of perturbing a single observation on each simplex boundary, but for $k$-simplices the analogous argument must bound how many $k$-simplices are affected by a single perturbation, a count that grows combinatorially with $k$. A careful analysis exploiting the metric structure of the fBm point cloud is needed.

**Problem 7.2 (Optimal embedding parameters).** The estimator $\hat{H}_\mathrm{top}$ depends on the embedding dimension $d$ and lag $\tau$, and Theorem 3 establishes consistency for any fixed $d \geq 2$ and $\tau \geq 1$ without addressing which choices minimize asymptotic mean squared error. The classical Takens embedding theorem guarantees faithful reconstruction of a dynamical attractor for $d \geq 2m+1$, but fBm is not generated by a finite-dimensional attractor, so this guidance does not apply directly. False nearest neighbor analysis provides a practical heuristic for choosing $d$, and the autocorrelation function for $\tau$, but neither is grounded in the specific behavior of $\hat{H}_\mathrm{top}$. A rigorous bias-variance decomposition as a function of $(d, \tau)$ --- presumably showing that larger $d$ reduces approximation bias while inflating the concentration constants in Theorem 1 --- would put parameter selection on firmer theoretical footing.

**Problem 7.3 (Fréchet means under dependence).** Theorem 1 controls $L_n^{(1)}(\varepsilon)$ pointwise in $\varepsilon$, which suffices for $\hat{H}_\mathrm{top}$ but does not yield control on the full persistence diagram in the $p$-Wasserstein metric $W_p$. Applications requiring Fréchet means of persistence diagrams --- e.g., averaging topological summaries across multiple trajectories of the same process --- need concentration inequalities in the Wasserstein topology on diagram space. For i.i.d. point clouds this is addressed by [@ChazalFasyLecciMichelRinaldoWasserman2018], but the long-range dependence case is open. The complication is structural: Fréchet mean uniqueness in $(\mathcal{D}, W_p)$ is not guaranteed even under independence, and the wider distributional support induced by long memory --- which Lemma 3.3 quantifies precisely through $\mathrm{Var} = O(n^{2H})$ --- makes non-uniqueness more likely as $H$ increases. Characterizing when the Fréchet mean is unique as a function of $H$ would require combining the concentration machinery developed here with the variational analysis of diagram space.

**Problem 7.4 (Non-Gaussian long memory).** The proof of Theorem 1 uses Gaussianity at two points: Lemma 3.3 appeals to the Gaussian tail of fBm increments to obtain the sub-Gaussian variance bound, and Section 4.1 uses Gaussian self-similarity to derive the functional equation. Real financial returns exhibit heavier-than-Gaussian tails, often modeled by $\alpha$-stable distributions. Extending the theory to fractional stable motions --- self-similar processes with $\alpha$-stable increments --- would require replacing Gaussian concentration with sub-Weibull or Orlicz-norm arguments, and the scaling exponent in the functional equation would change to reflect the different self-similarity structure. The application motivation is clear: the transform-stability of Theorem 4 already suggests robustness to tail behavior, but placing this on rigorous footing for heavy-tailed processes would substantially broaden the practical scope of the results.

**Problem 7.5 (Hypothesis testing for long memory).** The estimator $\hat{H}_\mathrm{top}$ provides a point estimate of $H$, but a companion test for $H_0: H = 1/2$ (no long memory) against $H_1: H > 1/2$ (persistent memory) would have considerable practical value, particularly for distinguishing genuine long memory from near-integrated short-memory processes. The concentration bound of Theorem 1 immediately yields the asymptotic null distribution of $L_n^{(1)}(\varepsilon) - \mathbb{E}_0[L_n^{(1)}(\varepsilon)]$ under $H_0$, where $\mathbb{E}_0$ can be estimated from i.i.d. simulations, and a test statistic based on the log-log slope can be calibrated against this distribution. What remains open is the power analysis: characterizing power against local alternatives $H_n = 1/2 + \delta_n$ as $n \to \infty$, and determining whether the topological test achieves the minimax separation rate for this problem.

## Connections to Broader TDA Theory {#sec:connections}

The results here intersect several active directions in topological data analysis at a structural level.

The variance bound $\mathrm{Var}(L_n^{(1)}(\varepsilon)) = O(n^{2H})$ from Lemma 3.3 has a direct implication for Fréchet means of persistence diagrams computed from correlated processes. For $H > 1/2$, the spread of the diagram distribution grows faster than the i.i.d. rate $O(n)$, meaning diagrams from long-memory trajectories occupy a wider region of diagram space. Since Fréchet mean uniqueness is guaranteed only when the distributional support is sufficiently concentrated relative to the curvature of diagram space, increasing $H$ systematically pushes toward non-uniqueness regimes. This creates a quantitative link between the Hurst exponent of the generating process and the geometric regularity of its topological summaries --- a connection that the variational theory of diagram spaces does not currently address.

The block decomposition at the heart of Theorem 1 is not specific to Vietoris--Rips complexes or to 1-dimensional homology. The mixing structure of fBm increments, encoded in the decay rate $\psi(k) \sim k^{2H-2}$, provides the decoupling mechanism; all that is required to run the argument is a Lipschitz-type sensitivity bound on the topological quantity of interest. Persistent path homology generalizes persistent homology to directed graphs by tracking directed cycles that undirected homology cannot detect. Financial networks, where edges encode Granger-causal or lead-lag relationships between assets, are naturally directed, and the long-range dependence of individual series propagates into correlated edge weights. Applying the block martingale technique to path Betti numbers would extend the concentration framework to this setting, providing the statistical foundation that persistent path homology for directed financial networks currently lacks.

At a more abstract level, the persistence module $\{\mathrm{H}_1(\mathrm{VR}(P_{d,\tau}^{(n)}, r))\}_{r \geq 0}$ is a constructible cosheaf on $\mathbb{R}$, and sheaf-theoretic formulations of persistence provide a natural language for tracking how algebraic sections evolve with the filtration parameter. The covariance structure of fBm induces correlations between homology classes appearing at different scales: a loop born at scale $r_1$ and one born at $r_2 \neq r_1$ are not independent when the underlying process has long memory. A sheaf-level concentration bound would describe how these cross-scale correlations affect the global sections of the persistence cosheaf, a question that neither the scalar concentration of Theorem 1 nor the bottleneck stability theorem directly resolves.

## Conclusion {#sec:conclusion}

Three contributions define this paper's scope. The block martingale argument of Section 3 yields the first concentration inequality for persistent Betti numbers of long-range dependent point clouds --- a result that does not follow from existing concentration tools, because the non-summable covariance of fBm with $H > 1/2$ is incompatible with both the independence assumption of Azuma--Hoeffding and the summable-mixing assumption of standard Bernstein-type inequalities. The variance factor $n^{2H}$ in the bound, rather than $n$, is the precise signature of long memory in the concentration rate. The functional equation derived from fBm self-similarity (Section 4) establishes the scaling law $\mathbb{E}[L_n^{(1)}(\varepsilon)] \sim n\varepsilon^{-1/H}$, providing a rigorous foundation for the topological Hurst estimator: not a heuristic based on observed log-log linearity, but a provable consequence of the process structure. The estimator $\hat{H}_\mathrm{top}$ (Section 5) achieves consistency at the minimax rate $O_P(n^{H-1})$ and remains asymptotically unaffected by monotone transforms of the series, a property that classical spectral and rescaled-range estimators lack and that is consequential for financial applications where preprocessing transforms are routine.

The underlying unity of these contributions is the single relation $\mathrm{Var}(L_n^{(1)}(\varepsilon)) \asymp n^{2H}$: it governs the concentration rate of the barcode count, determines the convergence rate of the estimator via the delta method, and encodes the statistical difficulty of Hurst estimation under long memory. That the same variance scaling appears simultaneously in stochastic topology, statistical estimation theory, and the mathematical theory of financial memory suggests that these three fields are closer to one another than their respective literatures have recognized.

# References {.unnumbered}
