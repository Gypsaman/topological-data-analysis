# TDA Research Frontiers and Open Problems

## Overview

This document maps the current research landscape of TDA (as of 2025–2026), covering active theoretical directions, open problems, the TDA+deep learning intersection, and emerging application frontiers. This is the foundation for identifying potential research contributions.

---

## 1. The Most Active Theoretical Frontiers

### 1.1 Multiparameter Persistence — The Central Open Problem

**Background:** Single-parameter persistence (filtrations over $\mathbb{R}$) has a complete algebraic classification: every persistence module decomposes into interval modules (the Structure Theorem). But for filtrations over $\mathbb{R}^n$ ($n \geq 2$), no such clean classification exists.

**Why it matters:** Many scientific problems naturally have multiple filtration parameters:
- Filtering by both scale AND density (outlier-robust topology)
- Filtering molecular data by both covalent-bond structure AND van der Waals interactions
- Filtering time-series data by both time AND frequency

**Core difficulty (Carlsson & Zomorodian, DCG 2009):** 2-parameter persistence modules are of **wild representation type** — infinitely many indecomposable types, no finite classification. The module structure over $\mathbb{k}[x, y]$ (a bivariate polynomial ring) cannot be summarized by a finite set of intervals.

**Key recent progress:**

| Result | Authors | Year | Significance |
|--------|---------|------|-------------|
| Signed barcodes via rank decompositions | Botnan, Oppermann, Oudot | 2024 | Virtual indecomposables as signed barcodes — major theoretical breakthrough |
| Stability of 2-parameter PH | Blumberg & Lesnick | FCM 2022 | First stability results for 2-parameter modules |
| Probabilistic analysis: interval-decomposable modules are rare | Loiseaux et al. | SoCG 2024 | Confirms hardness is generic, not exceptional |
| Differentiability of multiparameter PH | Carrière et al. | ICML 2024 | Gradient computation for 2-parameter persistence |
| Multi-parameter module approximation | Various | JACT 2025 | Tractable approximations with robustness guarantees |

**Current practical tools:** RIVET (fibered barcodes via 1D line slices), bigraded Betti numbers (via minimal free resolutions), Hilbert function.

**Open questions:**
- Is there a polynomial-time algorithm for any complete multiparameter invariant?
- Which partial invariants are most informative in practice?
- Can signed barcodes be computed efficiently?

---

### 1.2 Sheaf Theory Approaches

Sheaf theory provides a principled framework for encoding local-to-global consistency on data over a topological space. It generalizes persistent homology by assigning richer data (not just a scalar) to each cell of a complex.

**Foundational work:**
- **Ghrist & Curry:** "Sheaves, Cosheaves and Applications" (arXiv:1303.3255) — cellular sheaves and cosheaves for distributed TDA, sensor networks, network coding.
- **Hansen & Ghrist (2019):** "Toward a Spectral Theory of Cellular Sheaves" (JACT) — introduced the **sheaf Laplacian** $L_{\mathcal{F}}$, whose spectrum encodes consistency properties of the sheaf.

**Neural Sheaf Diffusion (NeurIPS 2022):**

**Bodnar, C., Di Giovanni, F. et al.** "Neural Sheaf Diffusion: A Topological Perspective on Heterophily and Oversmoothing in GNNs." *NeurIPS* 2022 (arXiv:2202.04579).

Assigns a local vector space to each node and a linear restriction map to each edge. The sheaf Laplacian then drives transport-aware diffusion. Key result: explains why standard GNNs fail on heterophilic graphs — the scalar sheaf Laplacian collapses to a standard graph Laplacian, which only works for homophilic data. Replacing it with a learned sheaf enables heterophilic message passing.

**Recent extensions (2024–2025):**
- Polynomial Neural Sheaf Diffusion (arXiv:2512.00242, 2024): adds polynomial spectral filters on sheaf Laplacians; long-range mixing in a single layer
- "Sheaf theory: from deep geometry to deep learning" (arXiv:2502.15476, 2025): comprehensive survey

---

### 1.3 Magnitude and Magnitude Homology

**Magnitude** is a numerical invariant of metric spaces introduced by Leinster, categorifying the Euler characteristic. **Magnitude homology** (Hepworth & Willerton, 2017; Leinster & Shulman, AGT 2021) categorifies it further.

**Key result:** Magnitude homology is a form of Hochschild homology whose graded Euler characteristic is the magnitude. It detects geometric information such as convexity.

**Active research thread (2024–2026):**
- "Magnitude homology equivalence of Euclidean sets" (arXiv:2406.11722, 2024): two closed Euclidean subsets are magnitude-homology equivalent iff their "cores" are isometric
- "Magnitude meets persistence" (seminar at MPI MIS Leipzig): connecting magnitude homology with persistent homology
- "The magnitude of categories of texts enriched by language models" (arXiv:2501.06662, 2025): applying magnitude to NLP

**Potential unification:** Magnitude homology and persistent homology are currently independent theories — finding their common structure is an active open problem.

---

## 2. TDA + Deep Learning

### 2.1 Differentiable Persistent Homology

Making PH differentiable enables it to be embedded directly in gradient-based learning pipelines.

**Key papers:**

**Gabrielsson et al. — "A Topology Layer for Machine Learning"** (*AISTATS* 2020; arXiv:1905.12200)
- PyTorch-compatible layer for level-set and edge filtrations
- Supports topological regularization, generative network topology priors, adversarial attacks

**Carrière et al. — "Optimizing Persistent Homology Based Functions"** (*ICML* 2021; arXiv:2010.08356)
- Unified framework with explicit gradient computation via real analytic geometry
- Proves convergence of stochastic subgradient methods for persistence-based losses
- Encompasses essentially all prior constructions in a single framework

**Hofer et al. (ICML 2020):** End-to-end learning of graph filtrations surpasses fixed filtrations + PH baselines.

**Differentiable Mapper** (arXiv:2402.12854; Nature Machine Intelligence 2023): Extends topological optimization to the Mapper algorithm.

---

### 2.2 Topological Loss Functions for Deep Learning

Enforce prior topological knowledge in neural network outputs without requiring labeled topology.

| Paper | Venue | Application | Key method |
|-------|-------|-------------|-----------|
| Hu et al. "Topology-Preserving Deep Image Segmentation" | NeurIPS 2019 | Binary segmentation | PH-based topological loss |
| Clough et al. | IEEE TPAMI 2022 | Cardiac MRI segmentation | Critical simplex gradient |
| Moor et al. "Topological Autoencoders" | ICML 2020 | Dimensionality reduction | Wasserstein PH loss |
| Nigmetov & Morozov | arXiv 2022 | General topology | "Topological Optimization with Big Steps" |

---

### 2.3 Topological Deep Learning Beyond Graphs

**Hajij et al. — "Topological Deep Learning: Going Beyond Graph Data"** (*arXiv:2206.00606*, 2022)

A unifying framework for deep learning on higher-order combinatorial structures: simplicial complexes, cell complexes, hypergraphs, combinatorial complexes. Defines message-passing operators on each cell type using boundary/coboundary maps.

**TopoX suite (2024):** Python packages TopoNetX, TopoEmbedX, TopoModelX implementing topological neural networks.

**TOGL: Topological Graph Neural Networks** (*ICLR* 2022): Computes topological features per GNN layer and adds them back to node embeddings.

---

### 2.4 Persistent Homology of Neural Network Loss Landscapes

Topological analysis of optimization landscapes provides theoretical insight into why certain architectures and optimizers work better:

- H0 features = connected components of sublevel sets (basins of attraction)
- Persistence = depth of basins
- Topological Obstructions Score = quantifies how many/deep local minima exist
- Empirical result: simpler loss topology → better generalization

This line of work suggests topology-aware architecture and optimizer design.

---

## 3. Statistical TDA

### 3.1 Bootstrap Methods

**Chazal et al. (2018):** Bootstrap confidence bands for persistence diagrams via subsampling. Computationally expensive (requires $B \sim 20,000$ bootstrap samples for tight bands).

**Roycraft et al. (2021):** Establishes CLTs and bootstrap validity for stabilizing statistics of persistent homology — rigorous statistical foundations for hypothesis testing.

### 3.2 Hypothesis Testing

**Two-group permutation tests:** Use bottleneck or Wasserstein distance between persistence diagrams as test statistic, permute group labels to get null distribution.

**"Vector summaries for permutation-based hypothesis testing"** (AIMS FoDS, 2024): Uses Betti curves, landscapes, and silhouettes as loss functions. Avoids the non-Euclidean structure of diagram space.

### 3.3 Kernel Methods for Persistence Diagrams

| Kernel | Properties | Reference |
|--------|-----------|-----------|
| Sliced Wasserstein (SWK) | Positive definite; stable; tractable | Carrière et al., ICML 2017 |
| Persistence Fisher | Positive definite; Fisher information metric | Le & Yamada, NeurIPS 2018 |
| Persistence scale-space | Stable; heat kernel on diagrams | Reininghaus et al., CVPR 2015 |
| RKHS on diagram groups | Theoretical framework | arXiv:2602.15153, 2026 |

**Open problem:** Does the Wasserstein distance on persistence diagrams define a negative definite kernel? This would directly yield positive definite kernels without approximation.

### 3.4 Vectorization Landscape (2024–2026)

**Persistence Spheres** (arXiv:2603.15384, 2026): bi-continuous linear representation via partial optimal transport; competitive with persistence images, landscapes, and splines.

**Comparative study (Frontiers in AI, 2021):** Persistence Landscapes, Adcock-Carlsson Coordinates, and Template Systems are most accurate and fast; Adaptive Template Systems achieve highest accuracy overall. No single vectorization dominates all tasks.

---

## 4. Emerging Application Frontiers

### 4.1 TDA for LLM Interpretability

Among the most exciting emerging directions (2023–2026):

**Persistent homology of activation spaces:**
- Zigzag PH across transformer layers reveals distinct representational phases
- H1 features detect cyclic structures in attention patterns
- Extended PH of attention heads reveals hierarchical information flow

**Key papers:**
- "Persistent Topological Features in Large Language Models" (Gardinazzi et al., ICML 2025): topology-guided layer pruning
- "Understanding Chain-of-Thought in LLMs via TDA" (arXiv:2512.19135, 2024)
- "The Shape of Reasoning: Topological Analysis of Reasoning Traces in LLMs" (arXiv:2510.20665, 2025)
- "Short-PHD: Detecting LLM-generated Text with TDA" (COLM 2025)

**Survey:** "Unveiling Topological Structures from Language: A Comprehensive Survey of TDA Applications in NLP" (arXiv:2411.10298, 2024)

**Reading list:** [AwesomeTDA4NLP](https://github.com/AdaUchendu/AwesomeTDA4NLP)

---

### 4.2 Drug Discovery and Molecular Sciences

One of the most mature application domains:

**Wei group (Michigan State):**
- **ToDD** (NeurIPS 2022): Topological compound fingerprints via multiparameter PH, partitioning compounds into chemical substructures
- **Top-DTI**: Drug-target interaction prediction integrating TDA with LLMs
- **hERG cardiotoxicity screening:** TDA-integrated ML identified 227 potential blockers from DrugBank
- **AlphaFold integration:** Persistent spectral theory on predicted protein structures

**Review:** "A Review of TDA and Topological Deep Learning in Molecular Sciences" (arXiv:2509.16877; ACS JCIM, 2025)

---

### 4.3 Quantum Topology

TDA is a leading candidate for genuine quantum advantage:

**Hayakawa, R.** "Quantum algorithm for persistent Betti numbers and topological data analysis." *Quantum*, 6:873, 2022.

First quantum algorithm able to compute persistent Betti numbers (prior quantum algorithms for homology could not). Potentially exponential speedup over classical algorithms for certain inputs.

**Ameneyro, B., Maroulas, V., Siopsis, G.** "Quantum persistent homology." *JACT*, 2024.

Uses a persistent Dirac operator whose spectrum relates to persistent combinatorial Laplacians.

**Key question:** Which TDA computations are genuinely quantum-advantaged vs. classically efficient? Analysis (2024) suggests true quantum advantage requires careful problem specification.

---

## 5. Key Researchers and Venues

### 5.1 Leading Researchers

| Researcher | Affiliation | Key Contributions |
|-----------|-------------|------------------|
| Gunnar Carlsson | Stanford (emeritus) / Ayasdi | Persistence barcodes, Mapper, founded TDA |
| Herbert Edelsbrunner | ISTA Klosterneuburg | Alpha complexes, persistence theory, extended persistence |
| Robert Ghrist | Penn | Sheaf theory, sensor networks, barcodes |
| Steve Oudot | INRIA Saclay | Stability theory, multiparameter persistence, signed barcodes |
| Frédéric Chazal | INRIA Saclay | Statistical TDA, bootstrap, GUDHI |
| Peter Bubenik | U. Florida | Persistence landscapes, statistical topology |
| Michael Lesnick | Albany | 2-parameter persistence, RIVET |
| Magnus Botnan | VU Amsterdam | Multiparameter persistence, signed barcodes |
| Mathieu Carrière | INRIA | Differentiable TDA, PersLay, sliced Wasserstein |
| Guo-Wei Wei | Michigan State | Molecular TDA, drug discovery, persistent Laplacians |
| Tom Leinster | U. Edinburgh | Magnitude, magnitude homology |
| Matthew Kahle | Ohio State | Random topology, stochastic PH |
| Omer Bobrowski | Technion | Random topology, statistical TDA |
| Kathryn Hess | EPFL | Topological neuroscience, directed complexes |
| Henry Adams | Colorado State | Persistence images, Ripser |
| Théo Lacombe | INRIA | Optimal transport + TDA |

### 5.2 Key Venues

**Conferences:**
- **SoCG** (Symposium on Computational Geometry): Premier theory venue; SoCG 2025 in Kanazawa
- **NeurIPS**: Recurring TDA workshops + main track topological DL
- **ICML**: Growing TDA presence (Carrière 2021, TOGL 2022, Gardinazzi 2025)
- **ICLR**: Topological GNNs
- **AISTATS**: PersLay, TopologyLayer
- **ATMCS** (Algebraic Topology: Methods, Computation and Science): Specialized meeting

**Journals:**
- **Journal of Applied and Computational Topology** (Springer JACT): Dedicated TDA journal
- **Foundations of Computational Mathematics**: High-prestige theory (stability, multiparameter)
- **SIAM J. Mathematics of Data Science (SIMODS)**: Statistical and applied TDA
- **Discrete & Computational Geometry**: Classical venue (stability theorem, Edelsbrunner)
- **Algebraic & Geometric Topology**: Magnitude homology

---

## 6. Synthesis: Most Promising Research Directions

Based on the current state of the field, the following directions represent high-impact opportunities:

### High-Impact Directions (Theoretical)

1. **Efficient invariants for multiparameter persistence**
   - Signed barcodes are theoretically powerful but algorithms are nascent
   - Connection to sheaf cohomology may yield tractable invariants
   - Interval approximations with stability bounds

2. **Magnitude meets persistence**
   - Two currently independent theories with deep connections
   - Unification could yield new invariants combining both

3. **Statistical foundations**
   - Optimal hypothesis tests for topological features
   - RKHS embeddings of persistence diagrams without approximation

### High-Impact Directions (Applied/Interdisciplinary)

4. **TDA for LLM mechanistic interpretability**
   - Very new, fast-moving, high-impact area
   - Topology of attention patterns, residual stream, and reasoning traces
   - Connection to safety-relevant questions (circuit analysis, hallucination detection)

5. **TDA + AlphaFold / protein language models**
   - Persistent topology of predicted protein structures at scale
   - Multiparameter persistence for molecular property prediction

6. **Topological deep learning (higher-order networks)**
   - Sheaf neural networks beyond graphs
   - Unifying framework via combinatorial complexes

7. **Quantum TDA**
   - Identifying genuine quantum advantage cases
   - Quantum algorithms for specific persistence problems

### Medium-Term Directions

8. **Differentiable multiparameter persistence**
   - Theoretical foundations (Carrière et al. 2024) exist; practical implementations needed

9. **Topology-aware training dynamics**
   - Using topological loss landscape analysis to guide architecture search and hyperparameter tuning

10. **Domain-specific TDA pipelines**
    - Climate data, materials informatics, genomics with multi-scale multiparameter PH

---

## 6. Topics from Dey & Wang (CTDA, 2022) Not Covered in Our Notes

*Added 2026-03-20 after reviewing "Computational Topology for Data Analysis" by Tamal Krishna Dey and Yusu Wang (Cambridge University Press, 2022, 375 pp.). This book is the most algorithmically comprehensive TDA reference available. The sections below document topics it covers that are absent or thin in our existing notes. These are potential theoretical targets.*

---

### 6.1 Optimal Homology Generators (Chapter 5)

**What the book covers:** Computing *minimum-weight* homology representatives — the "most efficient" cycle that generates a homology class. Distinct from column reduction, which yields *some* generator, not the optimal one.

The key results:
- **Greedy algorithm for optimal H_p(K)-basis** (§5.1.1): A greedy algorithm on edge weights finds an optimal basis for H_p in polynomial time under specific conditions.
- **Optimal H₁-basis and independence check** (§5.1.2): For H₁, minimum spanning tree ideas extend to homology.
- **Localization via LP** (§5.2): Optimal generators can be computed by linear programming over $\mathbb{Z}$ when the complex is *totally unimodular* — a condition satisfied by surfaces and planar graphs.
- **Persistent cycles** (§5.3): For PL-functions on pseudomanifolds, the persistent cycle (the specific cycle born at a birth event) can be computed explicitly in $O(n^3)$.

**Why this matters for research:** The minimum-weight representative of a homology class has interpretive value — in network analysis it is the "most efficient loop," in materials science the "tightest ring." No concentration results exist for optimal generators of random complexes. Combining Chapter 5 with probabilistic methods is open.

**Open question from the book:** For 2-pseudomanifolds embedded in $\mathbb{R}^3$, the persistent cycles corresponding to *infinite* bars (essential classes) can be computed efficiently (§5.3.3). Whether this extends to higher dimensions with better than $O(n^3)$ complexity is open.

---

### 6.2 Reeb Graph Distances and the Universality Problem (Chapter 7)

**What the book covers:** Two distances on Reeb graphs with rigorous stability theorems:

- **Interleaving distance** $\mathsf{d}_I(\mathbb{F}, \mathbb{G})$: Defined via $\varepsilon$-smoothings of Reeb graphs (thickened versions); the smallest $\varepsilon$ for which $\varepsilon$-interleaved maps exist. Generalizes persistence module interleaving to the graph setting.
- **Functional distortion distance** $\mathsf{d}_{FD}(\mathbb{F}, \mathbb{G})$: A function-adapted Gromov–Hausdorff distance using the function-induced metric on each Reeb graph.

**Key theorem (Bi-Lipschitz equivalence, Thm 7.6):** $\mathsf{d}_{FD} \leq 3\mathsf{d}_I \leq 3\mathsf{d}_{FD}$. Both distances are stable: $\mathsf{d}_R((\mathbb{F},f), (\mathbb{G}, g)) \leq \|f - g\|_\infty$.

**Universality (Definition 7.10):** A Reeb graph distance $\mathsf{d}_U$ is *universal* if it is stable and for every other stable distance $\mathsf{d}_S$, we have $\mathsf{d}_S \leq \mathsf{d}_U$. The universal distance exists (via pullback to a common space, Bauer-Landi-Mémoli 2020) but:

> **Open question (stated explicitly in §7.4):** *"It remains an interesting open question whether the interleaving distance (and thus functional distortion distance) is within a constant factor of the universal Reeb graph distance."*

This is a well-posed, hard open problem. A positive answer would unify all stable Reeb graph distances. A counterexample would show the interleaving distance is fundamentally incomplete.

**Computational note:** Computing $\mathsf{d}_I$ between general Reeb graphs is at least as hard as graph isomorphism (NP-hard for merge trees, Agarwal et al. 2018). A fixed-parameter tractable algorithm exists for merge trees.

---

### 6.3 Path Homology for Directed Graphs (Chapter 8)

**What the book covers:** The Grigor'yan-Lin-Muranov-Yau construction assigns homology groups to directed graphs via *allowed paths* — sequences of directed edges that survive the boundary operator. This is fundamentally different from the clique complex / Vietoris–Rips construction, which symmetrizes the graph.

Key points:
- The **path complex** $\mathcal{P}(G)$ of a digraph $G$ is built from all elementary paths; the **allowed subcomplex** $\Omega_*(G)$ consists of paths whose boundary is also a linear combination of allowed paths.
- Path homology detects directed cycles (closed directed walks) that have no undirected analogue.
- **Persistent path homology** is defined by filtration of digraphs by edge weight and has an $O(n^3)$ algorithm (Dey-Li-Wang, SODA 2018).
- Application: Reimann et al. (2017) found that biological neural networks (connectome data) have vastly more directed cliques than random graphs of similar density — a topological signature of biological organization.

**What the book does NOT prove:** A stability theorem for persistent path homology. The Cohen-Steiner stability result does not transfer directly because small edge-weight perturbations can create or destroy allowed paths. This is the primary open problem for persistent path homology.

**Our notes' gap:** Path homology is absent from [01_foundations.md](01_foundations.md) through [04_applications.md](04_applications.md). It is a fully developed theory with software support in GUDHI, targeting a different class of data (directed networks) than standard TDA.

**See:** [10_research_direction_path_homology.md](10_research_direction_path_homology.md) for the full research direction built on this.

---

### 6.4 Statistical Treatment: The Confirmed Gap (Chapter 13.3)

**What the book covers:** Section 13.3 (3 pages) briefly surveys:
- Fréchet means/variance in persistence diagram spaces $\mathbb{D}^p_q$ (Turner et al., Mileyko et al.)
- Concentration and convergence of persistence landscapes under i.i.d. sampling (Chazal et al. refs [85, 86])
- Confidence sets via bootstrapping [35, 84, 160]
- Distance-to-measures (DTM) for robustness when the sampling distribution deviates from the target [80]

**What the book explicitly does NOT cover:**
- Concentration for persistent Betti numbers of random simplicial complexes: *"We will not describe this interesting line of work in this book."* (refs [36, 37, 38, 202–204], the Bobrowski-Kahle program)
- Any result for **dependent** or **long-range-dependent** samples

**From the preface:** *"there is an emerging sub-area of TDA which centers more around statistical aspects. This book does not deal with these developments."*

This is textbook-level confirmation that the statistical gap addressed by Direction 9 is real, acknowledged, and unsolved as of 2021. The i.i.d. boundary is the frontier of the published literature in the most comprehensive available reference.

---

*Previous: [04_applications.md](04_applications.md) | Next: [06_bibliography.md](06_bibliography.md)*
