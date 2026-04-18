# Topological Data Analysis — Research Repository

A deep research collection on Topological Data Analysis (TDA): theory, algorithms, software, applications, and research frontiers. Built for learning, exploration, and eventual research paper development.

---

## What is TDA?

**Topological Data Analysis** is a mathematical framework that extracts *shape-based features* from data using tools from algebraic topology. The central insight: the **topology** of a dataset — its connected components, loops, voids, and higher-dimensional holes — carries structural information that classical statistical methods cannot access.

The main tool is **persistent homology**: a multi-scale summary of topological features that:
- Is stable under noise (small data perturbations → small diagram changes)
- Requires no assumptions about the underlying data distribution
- Works across diverse data types (point clouds, images, networks, time series)
- Captures structure at all scales simultaneously

---

## Repository Structure

```
topological_data_analysis/
├── README.md                    ← This file
├── CLAUDE.md                    ← Context for AI-assisted research
├── forecast.py                  ← TDA + N-BEATS financial forecaster (see Usage below)
├── .env                         ← Credentials (not committed)
└── research/
    ├── 01_foundations.md        ← Mathematical foundations
    ├── 02_persistent_homology.md← Core theory: persistence, stability
    ├── 03_algorithms_and_software.md ← Algorithms and tools
    ├── 04_applications.md       ← Applications across domains
    ├── 05_research_frontiers.md ← Open problems and emerging directions
    ├── 06_bibliography.md       ← Complete bibliography (76 entries)
    ├── 07_research_directions.md← Candidate research topics (low-resource, math-focused)
    ├── 08_research_direction_financial_memory.md ← Direction 8: topological Hurst estimator
    └── 09_research_direction_unified.md          ← Direction 9: unified theory (6 + 8), leading candidate
```

---

## Financial Forecaster (`forecast.py`)

Implements the methodology from *"Enhancing financial time series forecasting through topological data analysis"* (de Jesus Jr., Fernández-Navarro, Carbonero-Ruz, 2025). Combines **Vietoris-Rips persistent homology** on Takens-embedded windows with an **N-BEATS** neural network to produce one-step-ahead price forecasts.

### Setup

```bash
pip install yfinance tastytrade pyotp pandas numpy matplotlib \
            scikit-learn ripser torch pywavelets statsmodels python-dotenv
```

Create a `.env` file in the project root:

```
TASTYTRADE_LOGIN=your@email.com
TASTYTRADE_PASSWORD=yourpassword
TASTYTRADE_TOTP_SECRET=YOUR_BASE32_TOTP_SECRET   # from your 2FA setup
```

### Usage

**Basic forecast (Dow Jones, no chart):**
```bash
python forecast.py
```

**Forecast a different ticker:**
```bash
python forecast.py --ticker SPY
python forecast.py --ticker QQQ
```

**Show actual vs predicted chart:**
```bash
python forecast.py --ticker SPY --plot
```

**Fetch live options chain from tastytrade around the forecasted price:**
```bash
# ±2% range (default)
python forecast.py --ticker SPY --options SPY

# Tighter ±1% range
python forecast.py --ticker SPY --options SPY --width 0.01
```

**Forecast for a specific past date** (backtesting):
```bash
python forecast.py --ticker SPY --forecast 2026-01-15
```

**All flags together:**
```bash
python forecast.py --ticker SPY --options SPY --width 0.02 --plot
```

### Output

```
===== Results =====
Test  MAE:  0.003948
Test  MAPE: 5.07%
Test  directional accuracy: 100.00%

===== Price Forecast =====
Data through:         2026-04-06
Last available close: 657.09
Predicted log return: -0.000106
Forecasted price:     657.02

===== Options Chain: SPY | Target $657.02 ±2% [$644.09 – $670.00] =====
Expiration: 2026-04-06  (0 DTE)

Type    Strike      Bid      Ask      Mid  Symbol
-----------------------------------------------------------------
CALL    655.00     1.94     1.99     1.96  SPY   260406C00655000
PUT     655.00     0.97     0.95     0.96  SPY   260406P00655000
...
```

### How it works

| Step | Method |
|------|--------|
| Data | Yahoo Finance daily close, 2015–present |
| Preprocessing | Log returns → outlier clip → ADF stationarity → MinMaxScaler → MODWT denoise (db2, 5 levels) |
| TDA features | Takens embedding (k=2, τ=3) → Vietoris-Rips PH → entropy H(D), amplitude A(D), count N(D) |
| Model | N-BEATS (2 stacks × 4 blocks × 512 units), input window T=7, horizon H=1 |
| Options data | Tastytrade API via DXLink WebSocket streamer (requires account + TOTP 2FA) |

---

## Documents

### [01 — Mathematical Foundations](research/01_foundations.md)
- Metric spaces and point cloud data
- Simplicial complexes: Vietoris-Rips, Čech, Alpha
- Homology theory: chain groups, boundary operators, homology groups
- Betti numbers and their geometric interpretation
- The Nerve Theorem

**Key formula:**
$$H_k = \ker(\partial_k) / \text{im}(\partial_{k+1}), \quad \beta_k = \dim H_k$$

---

### [02 — Persistent Homology](research/02_persistent_homology.md)
- Filtrations and persistent homology groups
- Birth/death pairs, Elder Rule
- Persistence diagrams and barcodes
- The persistence algorithm (column reduction)
- Stability theorem: $d_B(\text{Dgm}(f), \text{Dgm}(g)) \leq \|f-g\|_\infty$
- Structure theorem: $\mathbb{V} \cong \bigoplus_j \mathbb{k}^{I_j}$
- Vectorizations: persistence landscapes, persistence images, kernels

---

### [03 — Algorithms and Software](research/03_algorithms_and_software.md)
- Standard algorithm, Twist/clearing, apparent pairs (Ripser)
- Parallel algorithms: Chunk, Lock-free (giotto-ph), GPU (Ripser++)
- Zigzag persistence and multiparameter persistence
- The Mapper algorithm in detail
- Complete software guide: Ripser, GUDHI, giotto-tda, Dionysus 2, PHAT, RIVET, Cubical Ripser, and more

**Quick selection:**
| Use case | Tool |
|----------|------|
| Fastest Rips PH | Ripser |
| Full pipeline (Python/ML) | giotto-tda |
| Alpha complex | GUDHI |
| 2-parameter persistence | RIVET |
| Mapper | KeplerMapper |

---

### [04 — Applications](research/04_applications.md)
Landmark papers across six domains:

| Domain | Key result |
|--------|-----------|
| **Cancer genomics** | Mapper discovered c-MYB+ breast cancer subtype with 100% survival (Nicolau et al., PNAS 2011) |
| **Neuroscience** | Torus topology of hippocampal correlations (Giusti et al., PNAS 2015) |
| **Drug discovery** | Element-specific PH for protein-ligand binding affinity (Wei group) |
| **Materials science** | Medium-range order in glass (Hiraoka et al., PNAS 2016) |
| **Cosmology** | Primordial non-Gaussianity detection beyond power spectrum (Cole et al., PRL 2021) |
| **Finance** | 250-day early warning before 2000 and 2008 crashes (Gidea & Katz, 2018) |
| **Phase transitions** | Topology-derived order parameters (Cole et al., PRR 2021) |
| **ML / neural networks** | Topological autoencoders, topology layers, neural persistence |

---

### [05 — Research Frontiers](research/05_research_frontiers.md)
Current open problems and high-impact research directions:

**Theoretical:**
- Multiparameter persistence — no complete discrete invariant (central open problem)
- Signed barcodes (Botnan, Oppermann, Oudot 2024) — major recent breakthrough
- Sheaf theory and neural sheaf diffusion
- Magnitude homology connections to persistence

**TDA + Deep Learning:**
- Differentiable persistent homology (Gabrielsson 2020, Carrière 2021)
- Topological loss functions for segmentation
- Topological deep learning beyond graphs (Hajij et al. 2022)

**Emerging Applications:**
- TDA for LLM interpretability (Gardinazzi et al., ICML 2025)
- Drug discovery with AlphaFold structures
- Quantum algorithms for TDA (Hayakawa 2022)

---

### [06 — Bibliography](research/06_bibliography.md)
76 entries covering all papers referenced in this collection, organized by category:
- Foundational papers (persistent homology, stability, structure theorem)
- Algorithms and software
- Statistical TDA and vectorizations
- Applications (biology, physics, ML, time series)
- Research frontiers
- Textbooks and surveys

---

### [07 — Candidate Research Directions](research/07_research_directions.md)
Nine research directions curated for a two-person team with strong mathematical backgrounds and minimal compute/budget:

| # | Direction | Core Math | File |
|---|-----------|-----------|------|
| 1 | Magnitude vs. Persistence correspondence | Category theory, homological algebra | 07 |
| 2 | Fréchet mean uniqueness in restricted diagram spaces | Functional analysis, Morse theory | 07 |
| 3 | PH of Cayley complexes | Geometric group theory | 07 |
| 4 | Stability under graph coarsening | Spectral graph theory | 07 |
| 5 | Extended persistence and Reeb graphs on surfaces | Morse theory, surface topology | 07 |
| 6 | Concentration inequalities for random complexes | Probability, combinatorics | 07 |
| 7 | Discrete Morse sub-optimality and persistence | Discrete Morse theory | 07 |
| 8 | Topological memory in financial markets | Stochastic processes, PH of time series | 08 |
| 9 | **Concentration for dependent complexes + topological Hurst estimator** *(leading candidate)* | Probability, fBm, PH theory | 09 |

Each entry includes: the open gap, proposed contribution, compute requirements, and key references.

---

### [08 — Financial Memory via TDA](research/08_research_direction_financial_memory.md)
Applies persistent homology of delay-embedded time series to detect long-range memory in financial markets, grounded in Mandelbrot's multifractal framework. Proposes a **topological Hurst estimator** based on the scaling law $\mathbb{E}[L_n(\epsilon)] \sim n \cdot \epsilon^{-\alpha(H)}$.

---

### [09 — Unified Direction: Concentration for Dependent Complexes (Leading Candidate)](research/09_research_direction_unified.md)
Synthesizes Directions 6 and 8. Extends concentration inequalities for persistent Betti numbers from i.i.d. to mixing, long-range dependent processes. The key result: a concentration bound of the form $\exp(-t^2 / C(H) \cdot n^{2H})$ where the Hurst exponent $H$ appears explicitly — recovering Direction 6 when $H = 1/2$. Gives Direction 8 its statistical foundation. Three target communities: stochastic topology, statistical TDA, mathematical finance.

---

## Key Researchers

| Researcher | Affiliation | Key work |
|-----------|-------------|----------|
| Gunnar Carlsson | Stanford / Ayasdi | Founder of TDA, Mapper, barcodes |
| Herbert Edelsbrunner | ISTA | Alpha complexes, persistence algorithm |
| Robert Ghrist | Penn | Sheaf theory, sensor networks |
| Steve Oudot | INRIA | Stability, multiparameter, signed barcodes |
| Frédéric Chazal | INRIA | Statistical TDA, GUDHI |
| Guo-Wei Wei | Michigan State | Drug discovery, molecular TDA |

---

## Learning Path

**Beginner (start here):**
1. Carlsson (2009) — "Topology and data" (Bull. AMS survey) — accessible overview
2. Chazal & Michel (2021) — "An introduction to TDA for data scientists" (Frontiers in AI)
3. [01_foundations.md](research/01_foundations.md) + [02_persistent_homology.md](research/02_persistent_homology.md)

**Intermediate:**
4. Edelsbrunner & Harer (2010) — *Computational Topology* (textbook)
5. [03_algorithms_and_software.md](research/03_algorithms_and_software.md)
6. Otter et al. (2017) — "A roadmap for the computation of persistent homology" (software guide)

**Advanced:**
7. Chazal, de Silva, Glisse, Oudot (2016) — *The Structure and Stability of Persistence Modules*
8. [05_research_frontiers.md](research/05_research_frontiers.md)
9. Botnan & Lesnick (2022) — "An introduction to multiparameter persistence"

---

## Research Objectives

1. **Learn** TDA foundations and key results comprehensively
2. **Explore** research ideas and application directions
3. **Develop** a research paper in TDA or TDA applications

Current stage: Foundation complete. Literature survey complete (76 references). Nine candidate directions documented. Direction 9 (concentration for dependent complexes + topological Hurst estimator) is the leading candidate. Next: develop full research proposal in `10_research_proposal.md`.

---

*Last updated: 2026-04-07*


