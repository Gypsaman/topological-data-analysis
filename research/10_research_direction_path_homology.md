# Direction 10: Persistent Path Homology for Directed Financial Networks

*Added: 2026-03-20. Inspired by Dey & Wang, "Computational Topology for Data Analysis" (Cambridge 2021), Chapter 8 (Topological Analysis of Graphs), which introduces path homology for directed graphs. No prior work applies this construction to financial networks, and the stability theory for persistent path homology remains open.*

---

## Summary

Standard TDA (Vietoris–Rips on symmetrized distances) is inherently undirected — it discards the direction of edges, treating a → b the same as b → a. Financial networks are fundamentally directed: money flows from buyer to seller, causal influence propagates asymmetrically, and market-impact graphs encode who moves whom. Symmetrizing such graphs throws away information that is financially meaningful.

**Path homology** (Grigor'yan, Lin, Muranov, Yau 2012–2019) is a homology theory for directed graphs that respects edge orientation. It assigns homology groups to a digraph using *allowed paths* — sequences of edges that follow the direction — rather than the symmetric simplicial structure of a clique complex. The theory is fully developed for the static case. The persistent version — persistent path homology under a filtration — has a definition and algorithm (Dey & Wang, Ch 8.3) but lacks a stability theorem analogous to Cohen-Steiner et al. (2007).

This direction has two parts: (1) prove stability of persistent path homology, filling the central theoretical gap; (2) apply it to directed financial networks to detect topological structure that undirected TDA misses.

---

## The Mathematical Setting

### Path Homology (Static)

Let $G = (V, E)$ be a directed graph. A **regular path** of length $p$ is an elementary $p$-path $e_{i_0 i_1 \ldots i_p}$ such that consecutive vertices are connected by directed edges: $(i_k, i_{k+1}) \in E$ for all $k$. The **allowed $p$-paths** $\Omega_p(G)$ are the $p$-paths that survive the boundary operator:

$$\partial e_{i_0 \ldots i_p} = \sum_{k=0}^{p} (-1)^k e_{i_0 \ldots \hat{i}_k \ldots i_p}$$

where we discard any resulting path that is not allowed. The path homology groups are:

$$\mathrm{H}_p^{\mathrm{path}}(G; \mathbb{k}) = \ker(\partial_p) / \mathrm{im}(\partial_{p+1}) \cap \Omega_p(G)$$

**Key difference from simplicial homology:** The clique complex of $G$ (treating edges as 1-simplices and triangles as 2-simplices) ignores orientation. Path homology detects directed cycles — closed directed paths — that have no undirected analogue.

### Persistent Path Homology

Given a filtration of directed graphs $G_0 \subseteq G_1 \subseteq \ldots \subseteq G_n$ (e.g., by edge weight threshold), persistent path homology tracks how allowed-path homology classes are born and die:

$$\mathrm{H}_p^{\mathrm{path}}(G_0) \to \mathrm{H}_p^{\mathrm{path}}(G_1) \to \ldots \to \mathrm{H}_p^{\mathrm{path}}(G_n)$$

The **persistent path homology diagram** $\mathrm{Dgm}_p^{\mathrm{path}}(G_\bullet)$ records birth-death pairs, exactly as in standard persistence. Dey & Wang (Ch 8.3) give an $O(n^3)$ algorithm for computing these diagrams.

---

## The Gap: No Stability Theorem

The Cohen-Steiner–Edelsbrunner–Harer stability theorem states:

$$d_B(\mathrm{Dgm}(f), \mathrm{Dgm}(g)) \leq \|f - g\|_\infty$$

for persistence diagrams induced by real-valued functions. The analogous result for **persistent path homology** is absent from the literature. Dey & Wang note the algorithm but do not prove stability.

**Why it's hard:** The standard proof uses the interpolation lemma (that $\|f - g\|_\infty \leq \varepsilon$ implies an $\varepsilon$-interleaving of persistence modules). For path homology, the boundary operator $\partial$ acting on allowed paths does not behave nicely under small perturbations of edge weights — a small perturbation can create or destroy an allowed path by changing which edges exist. The proof technique must be adapted to the discrete, directed setting.

**Conjecture (main theoretical goal):**

For two weighted directed graphs $G$ and $G'$ on the same vertex set with weight functions $w, w' : V \times V \to \mathbb{R}_{\geq 0}$, let $G_\varepsilon$ and $G'_\varepsilon$ be the subgraphs of edges with weight $\leq \varepsilon$. If $\|w - w'\|_\infty \leq \delta$, then:

$$d_B\!\left(\mathrm{Dgm}_p^{\mathrm{path}}(G_\bullet), \mathrm{Dgm}_p^{\mathrm{path}}(G'_\bullet)\right) \leq \delta$$

Proving this would establish persistent path homology as a stable, statistically trustworthy invariant.

---

## Application: Directed Financial Networks

### Why Directed Structure Matters in Finance

| Network Type | Directed Structure | What Symmetrization Loses |
|---|---|---|
| Market-impact graph | Stock $i$ moves stock $j$ with weight $w_{ij}$ | Asymmetric lead-lag relationships |
| Transaction flow | Buyer → seller in each trade | Direction of capital flow |
| Information cascade | Firm $i$ learns from firm $j$'s prices | Information hierarchy |
| Granger-causal graph | $X_t$ Granger-causes $Y_t$ with lag $\ell$ | Temporal causal direction |

Each of these is naturally a directed weighted graph on $n \approx 100$–$500$ nodes (e.g., S&P 500 constituents, major currency pairs, sectors). This size is fully accessible with the $O(n^3)$ path homology algorithm.

### Proposed Construction

1. **Build the directed graph.** For the S&P 500, compute the **Granger causality graph** at daily frequency: add directed edge $i \to j$ with weight $= 1 / p$-value of the Granger test from stock $i$ to stock $j$ at lag 1–5 days. This gives a weighted directed graph $G_t$ for each rolling window $t$.

2. **Filter by edge weight.** Use the filtration $G_\varepsilon = \{(i,j) : w_{ij} \geq 1/\varepsilon\}$ (stronger Granger links enter first). This produces a nested sequence of digraphs.

3. **Compute persistent path homology.** Apply the Dey-Wang algorithm (Ch 8.3) to obtain $\mathrm{Dgm}_0^{\mathrm{path}}$ and $\mathrm{Dgm}_1^{\mathrm{path}}$.

4. **Compare across regimes.** Compare persistence diagrams from calm periods vs. crisis periods (2008, 2020 COVID crash, 2022 rate-hike cycle). If directed topological structure changes systematically at crisis onset, this is a new early-warning signal.

5. **Complement with undirected baseline.** Run standard Vietoris–Rips on the symmetrized graph. Compare which features are detected only by path homology — these are the "directed topological anomalies."

### Research Questions

| Question | Type | Expected Difficulty |
|---|---|---|
| Do crises create new directed 1-cycles not visible undirectedly? | Empirical | Low |
| Does $\mathrm{Dgm}_1^{\mathrm{path}}$ shift significantly at market-regime changes? | Empirical + statistical | Medium |
| Does the stability theorem hold? | Theoretical | High |
| What is the relationship between path homology and the digraph's strongly connected components? | Theoretical | Medium |
| Does persistent path homology detect lead-lag relationships that Granger regression alone misses? | Empirical | Medium |

---

## Proposed Contributions (in order of difficulty)

| # | Contribution | Type | Difficulty |
|---|---|---|---|
| 1 | Empirical: compute persistent path homology on S&P 500 Granger graphs across regimes | Computational | Low |
| 2 | Comparison: directed vs. undirected TDA on the same networks | Empirical | Low |
| 3 | Theoretical: relationship between path homology and strongly connected components | Combinatorial | Medium |
| 4 | Theoretical: stability theorem for persistent path homology | Algebraic topology | High |
| 5 | Statistical: hypothesis test for regime change using path persistence diagrams | Statistical TDA | Medium |

A paper with contributions 1–3 and 5 is publishable. Contribution 4 alone is a strong theory paper.

---

## Why This Direction Is Viable

**Compute:** $O(n^3)$ algorithm, $n \leq 500$ stocks. Running all experiments takes under 1 hour on a laptop. Granger causality at daily frequency is fast.

**Data:** S&P 500 daily prices are freely available (Yahoo Finance, FRED). No proprietary data needed.

**Math intensity:** High for the stability theorem (requires understanding the path complex boundary operator and its interaction with filtrations). Moderate for the empirical and SCC relationship parts.

**Novelty:**
- No papers apply path homology to financial networks.
- The stability theorem for persistent path homology is open — Dey & Wang's textbook does not prove it.
- The comparison (directed vs. undirected TDA) on the same dataset is methodologically new.

**Lower barrier than Direction 9:** No stochastic processes, no fBm, no mixing theory. The theoretical work (stability) is algebraic topology rather than probability. For a team wanting to publish faster, this is the right choice.

---

## Relationship to Other Directions

- **Complements Direction 9:** Direction 9 analyzes *time series* with undirected VR persistence; Direction 10 analyzes *network structure* with directed path homology. Together they cover two distinct ways TDA applies to financial data.
- **Connects to Direction 4 (graph coarsening stability):** Both ask stability questions for graph-derived persistence. The techniques may partially overlap.
- **Connects to Direction 6 (random complexes):** Random directed graphs (Erdős–Rényi digraphs) have path homology that can be studied probabilistically — a natural extension once stability is established.

---

## Target Venues

| Venue | Angle |
|---|---|
| *Journal of Applied and Computational Topology* | Core TDA venue; theory + application |
| *Quantitative Finance* | If empirical results are strong and stability is proved |
| *SIAM Journal on Applied Mathematics* | If stability theorem is the main result |
| *SoCG* (Symposium on Computational Geometry) | If algorithmic improvements are included |

---

## Key References

**Path homology:**
- Grigor'yan, Lin, Muranov, Yau, "Homologies of path complexes and digraphs," arXiv:1207.2834, 2012
- Grigor'yan, Lin, Muranov, Yau, "Path complexes and their homologies," Journal of Mathematical Sciences, 2019
- Dey, Wang, *Computational Topology for Data Analysis*, Cambridge, Ch 8.3, 2022

**Persistent path homology algorithm:**
- Dey, Li, Wang, "Persistent Path Homology of Directed Networks," SODA 2018

**Directed graph topology:**
- Reimann et al., "Cliques of neurons bound into cavities provide a missing link between structure and function," Frontiers in Computational Neuroscience, 2017 (the neuroscience application in Dey & Wang Fig. 8.1)

**Stability of persistence:**
- Cohen-Steiner, Edelsbrunner, Harer, "Stability of Persistence Diagrams," DCG 2007

**Financial networks:**
- Billio et al., "Econometric measures of connectedness and systemic risk in the finance and insurance sectors," Journal of Financial Economics, 2012 (Granger-causality-based directed networks)
- Mantegna, Stanley, *An Introduction to Econophysics*, Cambridge, 2000

---

*Document created: 2026-03-20. Based on Dey & Wang CTDA Chapter 8 and financial network literature.*
