# CLAUDE.md — TDA Research Project Context

This file provides context for AI-assisted research sessions on Topological Data Analysis (TDA). Updated as the project evolves.

---

## Project Goal

**Objectives (in order):**
1. Learn TDA as deeply as possible
2. Explore research ideas and application directions
3. Develop and write a research paper

**Current stage:** Foundation complete. Literature survey complete (76 references). Nine candidate research directions documented. Direction 9 (unified concentration + financial memory) is the leading candidate — synthesizes Directions 6 and 8 into a single paper with rigorous statistical theory and concrete application.

---

## Repository Structure

```
topological_data_analysis/
├── README.md                         ← Overview and navigation guide
├── CLAUDE.md                         ← This file
└── research/
    ├── 01_foundations.md             ← Math foundations (complexes, homology, Betti)
    ├── 02_persistent_homology.md     ← Core PH theory (filtrations, diagrams, stability)
    ├── 03_algorithms_and_software.md ← Algorithms (Ripser, GUDHI, Mapper, etc.)
    ├── 04_applications.md            ← Applications (biology, physics, ML, etc.)
    ├── 05_research_frontiers.md      ← Open problems and research opportunities
    ├── 06_bibliography.md            ← 76-entry annotated bibliography
    ├── 07_research_directions.md     ← 7 candidate research topics (low-resource, math-focused)
    ├── 08_research_direction_financial_memory.md  ← Direction 8: topological Hurst estimator
    └── 09_research_direction_unified.md           ← Direction 9: unified theory (6 + 8), leading candidate
```

---

## What Has Been Researched

### Thoroughly covered:
- Mathematical foundations: simplicial complexes (VR, Čech, Alpha), homology theory, Betti numbers, Euler characteristic, Nerve Theorem
- Persistent homology: filtrations, birth/death pairs, Elder Rule, persistence diagrams, barcodes, column reduction algorithm, Twist algorithm, apparent pairs
- Stability theorems: Cohen-Steiner–Edelsbrunner–Harer (2007), isometry theorem, interleaving distance
- Structure theorem: Zomorodian–Carlsson (2005), Crawley-Boevey (2012)
- Vectorizations: persistence landscapes, persistence images, sliced Wasserstein kernel, Fisher kernel, PersLay
- Algorithms: Standard, Twist/Clearing, Ripser, Ripser++, PHAT Chunk, Lock-free parallel, discrete Morse (Perseus), Zigzag
- Software: Ripser, GUDHI, giotto-tda, Dionysus 2, PHAT, RIVET, Cubical Ripser, KeplerMapper, TDA (R), Oineus, JavaPlex
- Multiparameter persistence: impossibility results, rank invariant, signed barcodes, RIVET, fibered barcodes
- Mapper algorithm: construction, parameter selection, nerve theorem connection, applications
- Applications: cancer genomics (Nicolau 2011), neuroscience (Giusti 2015), protein structure (Wei group), materials (Hiraoka 2016), cosmology (Cole 2021), finance (Gidea 2018), ML/DL (topology layers, topological autoencoders, GNNs), time series
- Research frontiers: differentiable PH, topological DL, statistical TDA, TDA for LLMs, quantum TDA, drug discovery, sheaf theory, magnitude homology

---

## Key Theoretical Results (Quick Reference)

| Result | Statement |
|--------|-----------|
| Stability theorem | $d_B(\text{Dgm}(f), \text{Dgm}(g)) \leq \|f-g\|_\infty$ |
| Structure theorem | $\mathbb{V} \cong \bigoplus_j \mathbb{k}^{I_j}$ (unique decomposition into interval modules) |
| Isometry theorem | $d_B(\text{Dgm}(\mathbb{V}), \text{Dgm}(\mathbb{W})) = d_I(\mathbb{V}, \mathbb{W})$ |
| Rips-Čech interleaving | $\check{C}(P,r) \subseteq \text{VR}(P,2r) \subseteq \check{C}(P,2r)$ |
| Nerve theorem | Good cover $\Rightarrow$ space $\simeq$ nerve |
| No multiparameter barcode | 2-parameter modules are wild type; no complete discrete invariant |

---

## Research Frontier Summary

### Theoretical open problems:
1. **Multiparameter persistence** — no complete discrete invariant; signed barcodes (2024) are promising
2. **Optimal vectorizations** — no single method dominates; task-dependent
3. **Statistical foundations** — Fréchet mean non-unique; optimal hypothesis tests unknown
4. **Magnitude meets persistence** — two independent theories with deep connections; unification unknown

### High-impact application directions:
1. **TDA for LLM interpretability** — very new (2023–2026), fast-moving
2. **TDA + AlphaFold** — molecular topology at scale
3. **Sheaf neural networks** — generalizes GNNs to heterophilic graphs
4. **Quantum TDA** — potential exponential speedup (Hayakawa 2022)
5. **Topological DL** — higher-order network architectures (Hajij et al.)

---

## Key Papers to Read (Priority)

**Tier 1 (foundational, must-read):**
- Carlsson (2009) — "Topology and data" (Bull. AMS) — accessible survey
- Edelsbrunner, Letscher, Zomorodian (2002) — original persistence paper
- Cohen-Steiner, Edelsbrunner, Harer (2007) — stability theorem
- Chazal et al. (2016) — Structure and Stability of Persistence Modules

**Tier 2 (important for depth):**
- Zomorodian, Carlsson (2005) — Computing persistent homology
- Bauer (2021) — Ripser
- Botnan & Lesnick (2022) — Introduction to multiparameter persistence
- Adams et al. (2017) — Persistence images (JMLR)

**Tier 3 (applications and frontiers):**
- Nicolau, Levine, Carlsson (2011) — PNAS (Mapper + breast cancer)
- Carrière et al. (2021) — Optimizing PH functions (ICML)
- Bodnar et al. (2022) — Neural Sheaf Diffusion (NeurIPS)
- Hayakawa (2022) — Quantum algorithm for PH

---

## Research Paper Ideas

Seven candidate directions are fully documented in [`research/07_research_directions.md`](research/07_research_directions.md), each with: open gap, proposed contribution, compute requirements, and key references. All designed for minimal compute and strong mathematical focus.

| # | Direction | Core Math | Compute |
|---|-----------|-----------|---------|
| 1 | Magnitude vs. Persistence correspondence | Category theory, homological algebra | Laptop / pen & paper |
| 2 | Fréchet mean uniqueness in restricted diagram spaces | Functional analysis, Morse theory | Laptop |
| 3 | PH of Cayley complexes | Geometric group theory | GAP/SageMath + GUDHI |
| 4 | Stability under graph coarsening | Spectral graph theory | Laptop |
| 5 | Extended persistence and Reeb graphs on surfaces | Morse theory, surface topology | GUDHI on laptop |
| 6 | Concentration inequalities for random complexes | Probability, combinatorics | Very low |
| 7 | Discrete Morse sub-optimality and persistence | Discrete Morse theory | Laptop |
| 8 | Topological memory in financial markets | Stochastic processes, PH of time series | Laptop |
| 9 | **Concentration for dependent complexes + topological Hurst estimator** | Probability, fBm, PH theory | Laptop |

**Top recommendation: Direction 9** — unifies Directions 6 and 8. The concentration bound for dependent point clouds is the first of its kind; the topological Hurst estimator is the first TDA estimator for long-memory processes with provable statistical guarantees. Three audiences: stochastic topology, statistical TDA, mathematical finance.

---

## Instructions for Claude

- When revisiting this project, start by reading this file + README.md
- All new research findings should be added to the relevant `research/*.md` file
- New bibliography entries: add to `research/06_bibliography.md` with a sequential number
- When a research direction is chosen, create `research/08_research_proposal.md`
- When writing the paper, create `research/paper/` directory with draft sections
- Keep this CLAUDE.md updated as the project advances

---

*Last updated: 2026-03-18 — Added 07_research_directions.md*
