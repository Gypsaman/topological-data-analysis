# Candidate Research Directions for a TDA Paper

## Constraints and Guiding Principles

These directions are selected with the following constraints:

- **No large-scale compute:** No GPU clusters, no training large models, no processing terabyte datasets.
- **Minimal cost:** Relies on publicly available datasets, open-source software (Ripser, GUDHI, giotto-tda), and at most modest cloud compute (a single CPU-heavy VM for a few hours).
- **Mathematically rigorous:** Both researchers have strong mathematical foundations — directions that are primarily theoretical or analytical are preferred. Computational validation is supportive, not central.
- **Novel contribution path:** Each direction has a realistic gap that two researchers can plausibly fill at the level of a journal paper or strong conference submission.

---

## Direction 1: Magnitude Homology and Persistent Homology — A Comparative Framework

**Summary:**
Magnitude homology (Leinster & Shulman, AGT 2021) and persistent homology (Edelsbrunner et al., DCG 2002) are two independent topological theories that both extract structure from metric spaces, yet their relationship is poorly understood. This direction proposes a *comparative theoretical framework* that maps their similarities and differences using concrete families of metric spaces.

**The gap:**
The "Magnitude meets Persistence" research thread (MPI MIS Leipzig seminar series, 2024–2025) is active but has produced no unifying theorem. Specific comparisons on well-understood metric spaces (finite graphs, lattices, Euclidean point clouds with known topology) have not been systematically carried out.

**Proposed contribution:**
1. For a family of metric spaces (e.g., finite metric trees, cycle graphs $C_n$, product spaces), compute both the magnitude function $|X_t|$ (as a function of scale $t$) and the persistent Betti numbers $\beta_k^{s,t}$.
2. Investigate whether critical scales of magnitude (points where $|X_t|$ changes slope) correspond to birth/death events in the persistent homology filtration.
3. Prove or disprove a correspondence theorem for specific classes of spaces.

**Why it fits your constraints:**
- **Compute:** Both invariants can be computed exactly for small finite metric spaces with pen and paper or simple Python scripts. No large datasets needed.
- **Math intensity:** High. Requires fluency in homological algebra, enriched category theory (for magnitude), and persistence module theory.
- **Data:** None required. The metric spaces are constructed analytically.
- **Novelty path:** A positive correspondence result for even one non-trivial class of spaces would be publishable in *Journal of Applied and Computational Topology* or *Algebraic & Geometric Topology*.

**Starting references:**
- Leinster & Shulman, "Magnitude homology of enriched categories and metric spaces," AGT 2021 (arXiv:1711.00802)
- Hepworth & Willerton, "Categorifying the magnitude of a graph," Homology, Homotopy and Applications 2017
- Seminar notes from MPI MIS Leipzig "Magnitude meets Persistence" series

---

## Direction 2: Topological Characterization of Persistence Diagram Spaces — A Geometric Study

**Summary:**
Persistence diagrams themselves form a metric space under the bottleneck distance $d_B$ and Wasserstein distances $W_p$. The geometric and topological properties of this space of diagrams are not fully understood. This direction studies the *topology of the space of persistence diagrams* arising from specific families of filtrations.

**The gap:**
The Fréchet mean of persistence diagrams is known to be non-unique in general (Turner et al., 2014). But for *restricted* families of diagrams (e.g., diagrams arising from sublevel-set filtrations of functions on a fixed simplicial complex, or diagrams with bounded total persistence), the geometry may be far more tractable. The curvature, geodesics, and contractibility of these restricted spaces have not been systematically studied.

**Proposed contribution:**
1. Fix a parameterized family of functions on a simple complex (e.g., piecewise-linear functions on a triangulated surface of genus $g$).
2. Study the induced map from function space (a finite-dimensional vector space) to persistence diagram space.
3. Characterize the fiber (preimage of a diagram), identify when the map is locally injective, and describe the topology of diagram space as seen through this map.
4. Specifically: determine conditions under which a persistence diagram has a *unique Fréchet mean* within the image of this map.

**Why it fits your constraints:**
- **Compute:** Exploratory computations on small triangulated surfaces (e.g., the torus triangulated with 7 vertices) are feasible with GUDHI on a laptop.
- **Math intensity:** Very high. Requires Morse theory, optimal transport theory, and functional analysis.
- **Data:** None external. All spaces are constructed analytically.
- **Novelty path:** Uniqueness-of-Fréchet-mean results for restricted diagram spaces would directly address an open problem in statistical TDA.

**Starting references:**
- Turner, Mileyko, Mukherjee, Harer, "Fréchet Means for Distributions of Persistence Diagrams," DCG 2014
- Chazal, de Silva, Glisse, Oudot, *The Structure and Stability of Persistence Modules*, Springer 2016
- Mémoli, "Some properties of Gromov-Hausdorff distances," DCG 2012

---

## Direction 3: Persistent Homology of Cayley Complexes and Finitely Presented Groups

**Summary:**
Given a finitely presented group $G = \langle S \mid R \rangle$, its Cayley complex $\text{Cay}(G, S)$ is a 2-dimensional CW complex encoding both the group structure and relators. This direction proposes computing and classifying persistent homology of Cayley complexes under natural filtrations, connecting geometric group theory with TDA.

**The gap:**
The persistent homology of Cayley graphs (1-dimensional) is studied, but the persistent homology of the full Cayley *2-complex* (including 2-cells from relations) under filtrations by word length or presentation complexity has received minimal attention. The relationship between group-theoretic properties (amenability, hyperbolicity, property T) and topological features of the Cayley complex filtration is unexplored.

**Proposed contribution:**
1. Define a natural filtration on Cayley complexes: attach cells in order of word length of the relators.
2. Compute $H_0$, $H_1$, $H_2$ persistence for families of groups: free groups, surface groups $\pi_1(\Sigma_g)$, hyperbolic groups, small cancellation groups.
3. Investigate whether group-theoretic invariants (e.g., hyperbolicity $\delta$, cohomological dimension) correlate with specific persistence features.

**Why it fits your constraints:**
- **Compute:** Cayley complexes of small groups (order < 100 or small rank) are finite and computable by hand or with GAP/SageMath + GUDHI.
- **Math intensity:** Very high. Requires geometric group theory, CW complex topology, and persistent homology theory.
- **Data:** None. All spaces are algebraically defined.
- **Novelty path:** Any provable relationship between group-theoretic properties and persistence invariants would be new and publishable in a topology or algebra journal.

**Starting references:**
- Bridson & Haefliger, *Metric Spaces of Non-Positive Curvature*, Springer 1999
- Edelsbrunner & Harer, *Computational Topology*, AMS 2010 (Ch. IV on CW complexes)
- Kahle, "Topology of random clique complexes," DCG 2009 (for probabilistic extensions)

---

## Direction 4: Stability of Persistence Under Graph Coarsening and Simplification

**Summary:**
Many real datasets are naturally modeled as graphs. A common preprocessing step is *graph coarsening* (merging nodes, pooling) used in GNNs and network analysis. This direction asks: how stable is the persistent homology of a graph under coarsening operations? Can we bound the bottleneck distance between the original and coarsened graph's persistence diagrams?

**The gap:**
The stability theorem guarantees that PH is stable under *continuous* perturbations of a function. But graph coarsening is a *discrete* structural change — it alters the vertex set and edge structure, not just function values. Existing stability bounds do not apply. There are no known tight bounds on $d_B(\text{Dgm}(G), \text{Dgm}(G'))$ when $G'$ is a coarsening of $G$.

**Proposed contribution:**
1. Define a family of graph coarsening operations (edge contraction, quotient graphs, spectral coarsening).
2. For the lower-star filtration and the Vietoris-Rips filtration on graphs, derive upper bounds on $d_B(\text{Dgm}(G), \text{Dgm}(G'))$ in terms of the coarsening ratio and spectral properties of $G$.
3. Show the bounds are tight (or find counterexamples showing they cannot be improved).
4. As a corollary: identify which coarsening operations *preserve* topological features and which destroy them.

**Why it fits your constraints:**
- **Compute:** Small graphs (50–200 nodes) suffice for all experiments. Fully feasible on a laptop with NetworkX + Ripser.
- **Math intensity:** High. Requires spectral graph theory, persistence stability theory, and some functional analysis.
- **Data:** Experiments can use standard benchmark graphs (Karate Club, MUTAG molecular graphs) — all freely available.
- **Novelty path:** This directly addresses a gap relevant to GNN theory and TDA-on-graphs, making it attractive to both topology and ML communities (*NeurIPS*, *ICLR*, *JACT*).

**Starting references:**
- Cohen-Steiner, Edelsbrunner, Harer, "Stability of persistence diagrams," DCG 2007
- Loukas, "Graph Reduction with Spectral and Cut Guarantees," JMLR 2019 (spectral coarsening)
- Hofer, Graf, Rieck, Niethammer, Kwitt, "Graph Filtration Learning," ICML 2020

---

## Direction 5: Extended Persistence and Morse Theory on Surfaces — Algorithmic and Structural Results

**Summary:**
Extended persistence (Cohen-Steiner, Edelsbrunner, Harer, FoCM 2009) augments standard persistence by using Lefschetz duality to pair essential classes — capturing the full topology of a manifold. For surfaces (compact 2-manifolds), extended persistence of Morse functions is well-defined but the combinatorial structure of the extended diagram (especially the pairing of $H_1$ "up" vs. $H_1$ "down" features) has not been fully characterized.

**The gap:**
For Morse functions on surfaces of genus $g$, the extended persistence diagram encodes $2g$ essential classes. The relationship between the *topology of the Reeb graph* of the Morse function and the extended persistence diagram is partially understood but not complete. In particular: which Reeb graph topologies correspond to which extended persistence pairing structures?

**Proposed contribution:**
1. Enumerate all Reeb graph topologies for Morse functions on $\Sigma_g$ (genus-$g$ surface) for small $g$ (e.g., $g = 1, 2, 3$).
2. For each Reeb graph type, characterize the structure of the extended persistence diagram.
3. Prove a correspondence theorem: the extended persistence diagram of a Morse function on $\Sigma_g$ is determined (up to symmetry) by the combinatorial type of its Reeb graph.
4. As a byproduct: classify which extended diagrams are *realizable* by Morse functions on $\Sigma_g$.

**Why it fits your constraints:**
- **Compute:** All computations are on compact surfaces with small triangulations. Feasible with GUDHI.
- **Math intensity:** Very high. Requires Morse theory, surface topology, and extended persistence theory.
- **Data:** None. All objects are analytically defined.
- **Novelty path:** A complete correspondence theorem for genus-2 or higher surfaces would be new. Publishable in *Discrete & Computational Geometry* or *Algebraic & Geometric Topology*.

**Starting references:**
- Cohen-Steiner, Edelsbrunner, Harer, "Extending persistence using Poincaré and Lefschetz duality," FoCM 2009
- Biasotti, Giorgi, Spagnuolo, Falcidieno, "Reeb graphs for shape analysis and applications," Theoretical Computer Science 2008
- Edelsbrunner, Harer, *Computational Topology*, AMS 2010 (Ch. VII on Morse theory)

---

## Direction 6: Persistent Homology of Random Simplicial Complexes — Concentration Inequalities

**Summary:**
The Erdős–Rényi random graph $G(n, p)$ has a well-known phase transition for connectivity. The Linial–Meshulam random 2-complex $Y(n, p)$ (2-simplices added independently with probability $p$ on the complete graph) has a phase transition for the vanishing of $H_1$. This direction aims to establish *concentration inequalities* for persistent Betti numbers of random complexes, going beyond phase transitions to quantitative rates.

**The gap:**
Phase transition thresholds are known (Linial–Meshulam 2006, Meshulam–Wallach 2009). But concentration results — how tightly the persistent Betti numbers concentrate around their expectation at a given $(n, p)$ — are only known for $H_0$ (classical random graph theory). For $H_1$ and higher, concentration results are largely open.

**Proposed contribution:**
1. Use martingale methods (Azuma–Hoeffding or entropy methods) to establish concentration inequalities for $\beta_1(Y(n,p))$ as a function of $n$ and $p$.
2. Extend to persistent Betti numbers: for the filtration $Y(n, p_1) \subseteq Y(n, p_2) \subseteq \ldots$, bound the variance of $\beta_1^{i,j}$.
3. Compare theoretical bounds with simulations on moderate-size random complexes ($n \leq 100$, feasible on a laptop).

**Why it fits your constraints:**
- **Compute:** Simulations of $Y(n, p)$ for $n \leq 100$ are very fast with GUDHI/Ripser.
- **Math intensity:** Very high. Requires probability theory (concentration inequalities, Doob martingales), combinatorics, and algebraic topology.
- **Data:** No real data. All experiments use generated random complexes.
- **Novelty path:** Any sharp concentration inequality for $H_1$ of random complexes would be new, filling a gap noted explicitly in Kahle's survey (Bull. AMS 2014). Natural venue: *Random Structures & Algorithms* or *Combinatorica*.

**Starting references:**
- Linial, Meshulam, "Homological connectivity of random 2-complexes," Combinatorica 2006
- Kahle, "Topology of random clique complexes," DCG 2009
- Kahle, "Sharp vanishing thresholds for cohomology of random flag complexes," Annals of Math 2014
- Boucheron, Lugosi, Massart, *Concentration Inequalities: A Nonasymptotic Theory of Independence*, Oxford 2013

---

## Direction 7: Topological Analysis of Discrete Morse Pairings — Complexity and Optimality

**Summary:**
A discrete Morse function (Forman 1998) on a simplicial complex pairs simplices into gradient pairs, reducing the complex to a Morse complex with far fewer cells but the same homology. The *optimal* discrete Morse function (minimizing the number of critical cells) is NP-hard to compute in general. This direction studies the persistent homology of sub-optimal discrete Morse functions and asks: how close to optimal can a greedy algorithm get, and how does sub-optimality manifest in the persistence diagram?

**The gap:**
The connection between discrete Morse theory and persistent homology is well-established (Mischaikow & Nanda, DCG 2013): Morse pairings correspond exactly to persistence pairs in the boundary matrix. But the *persistence diagram of a sub-optimal Morse function* — one with extra critical cells — has never been characterized in terms of the excess complexity. Specifically: if a Morse function has $k$ excess critical cells beyond the minimum, what is the worst-case total persistence of the spurious features it introduces?

**Proposed contribution:**
1. Define a measure of sub-optimality for a discrete Morse function on a given complex.
2. Prove bounds on the total persistence of features introduced by the excess critical cells.
3. Characterize for which complex topologies greedy algorithms achieve or fail to achieve optimality.
4. Numerical experiments on random triangulations of surfaces.

**Why it fits your constraints:**
- **Compute:** Random triangulated surfaces of moderate size (up to ~5,000 triangles) are feasible. Morse pairings computable with Perseus or GUDHI.
- **Math intensity:** Very high. Requires discrete Morse theory, algorithmic complexity, and persistence theory.
- **Data:** None external. All test objects are synthetically generated.
- **Novelty path:** Bounds connecting Morse sub-optimality to persistence features are new and bridge two active TDA subfields. Natural venue: *DCG*, *SoCG*, or *FoCM*.

**Starting references:**
- Forman, "Morse theory for cell complexes," Advances in Mathematics 1998
- Mischaikow, Nanda, "Morse theory for filtrations and efficient computation of persistent homology," DCG 2013
- Joswig, Pfetsch, "Computing optimal Morse matchings," SIAM J. Discrete Mathematics 2006

---

## Comparison Table

| # | Direction | Primary Discipline | Compute Need | Data Need | Novelty Risk | Recommended If… |
|---|-----------|-------------------|-------------|-----------|-------------|-----------------|
| 1 | Magnitude vs. Persistence correspondence | Algebra / Category Theory | Very low | None | Medium | You enjoy enriched category theory |
| 2 | Fréchet mean uniqueness in restricted diagram spaces | Functional analysis / Morse theory | Low | None | Medium–High | You want to address statistical TDA foundations |
| 3 | PH of Cayley complexes | Geometric group theory | Low | None | Medium | You have group theory background |
| 4 | Stability under graph coarsening | Spectral graph theory / PH theory | Low | Benchmark graphs | Low–Medium | You want ML-relevant theory with clear experiments |
| 5 | Extended persistence and Reeb graphs on surfaces | Morse theory / Surface topology | Low | None | Medium | You prefer pure topology |
| 6 | Concentration inequalities for random complexes | Probability / Combinatorics | Very low | None | Medium | You have strong probability background |
| 7 | Discrete Morse sub-optimality and persistence | Discrete Morse theory / Algorithms | Low | None | Medium | You enjoy algorithmic topology |

---

## Recommended Starting Point

**For a team with strong pure math backgrounds and minimal compute:**

**Direction 6 (Concentration inequalities)** or **Direction 1 (Magnitude meets Persistence)** are the most self-contained and require no data collection. Direction 6 has the clearest open problem statement and a concrete technical path. Direction 1 has the highest potential impact if a positive result is found.

**For a team wanting some empirical validation alongside theory:**

**Direction 4 (Graph coarsening stability)** is the most immediately relevant to active ML research, has the clearest gap, and experiments fit easily on a laptop. It also has the broadest potential audience spanning TDA and ML.

---

*Document created: 2026-03-18. Based on literature survey in `01_foundations.md` through `06_bibliography.md`.*
