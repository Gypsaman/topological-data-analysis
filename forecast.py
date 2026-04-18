
"""
Dow Jones TDA Forecasting with N-BEATS (PyTorch)
------------------------------------------------
Implementation of the methodology from:
"Enhancing financial time series forecasting through topological data analysis"
de Jesus Jr., Fernández-Navarro, Carbonero-Ruz (2025)

What this script does:
  1) Downloads Dow Jones (^DJI) data from Yahoo Finance
  2) Preprocesses following Section 3.2 of the paper:
       a) Cubic spline interpolation for missing values
       b) Compute log returns
       c) Outlier clipping at [0.02, 0.98] quantile bounds (Z-score method)
       d) ADF stationarity test (verification only)
       e) MinMaxScaler normalization to [-1, 1]
       f) MODWT denoising (Daubechies-2, 5 levels, approximation retained)
  3) Builds sliding-window TDA features on each local segment (Section 2.3):
       - Takens embedding (k=2, tau=3)
       - Vietoris-Rips persistent homology
       - persistent entropy H(D), amplitude A(D), point count N(D)
  4) Concatenates v=(H(D), A(D), N(D)) to the signal input of each N-BEATS block
     (Section 2.4.2, Eq. 8)
  5) Trains an N-BEATS-style forecaster with paper's hyperparameters (Section 3.4):
       T=7, H=1, 2 layers × 512 units, batch_size=16, epochs=100
  6) Reports test metrics and a latest one-step-ahead forecast

Dependencies:
  pip install yfinance pandas numpy matplotlib scikit-learn ripser torch pywavelets statsmodels

Run:
  python dow_jones_tda_nbeats_forecast.py
"""

from __future__ import annotations

import copy
import math
import os
import random
import warnings
from dataclasses import dataclass
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyotp
import pywt
import torch
import torch.nn as nn
import yfinance as yf
from dotenv import load_dotenv
from ripser import ripser
from scipy.interpolate import CubicSpline
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from statsmodels.tsa.stattools import adfuller
from tastytrade import Session
from tastytrade.instruments import NestedOptionChain

load_dotenv()
warnings.filterwarnings("ignore")


# -----------------------------
# Reproducibility
# -----------------------------
def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


# -----------------------------
# Configuration
# -----------------------------
@dataclass
class Config:
    ticker: str = "^DJI"
    start: str = "2015-01-01"
    end: str = ""   # empty = today

    # Forecast setup — paper Section 3.4: T=7, H=1

    input_chunk_length: int = 7
    forecast_horizon: int = 1

    # TDA setup — paper Section 3.3: tau in {3,7}, L in {2,3,4,6 weeks}
    # Using tau=3, L=21 (3 weeks) as defaults for daily DJI data
    tda_window_length: int = 21
    takens_delay: int = 3
    takens_dimension: int = 2   # paper Fig.1 shows k=2
    homology_maxdim: int = 1
    combine_h0_h1: bool = True

    # Train / test split
    test_fraction: float = 0.2

    # Training — paper Section 3.4: batch=16, epochs=100
    batch_size: int = 16
    epochs: int = 100
    learning_rate: float = 1e-3
    weight_decay: float = 1e-5
    random_state: int = 42

    # N-BEATS architecture — paper Section 3.4: 2 layers × 512 units
    n_blocks: int = 4
    hidden_width: int = 512
    n_layers: int = 2
    dropout: float = 0.1

    # Early stopping
    val_fraction_within_train: float = 0.15
    patience: int = 20

    # MODWT denoising — paper Section 3.2
    wavelet: str = "db2"
    wavelet_level: int = 5

    # Runtime
    device: str = "cuda" if torch.cuda.is_available() else "cpu"
    show_plot: bool = False

    # Options chain (tastytrade)
    options_symbol: str = ""     # tastytrade symbol to fetch options for, e.g. 'SPY'
    options_width: float = 0.02  # ± fraction around forecasted price


# -----------------------------
# Data download
# -----------------------------
def download_close_prices(ticker: str, start: str, end: str) -> pd.Series:
    """Download daily close prices from Yahoo Finance.

    If end is empty the download runs through today's latest available close.
    """
    kwargs = dict(start=start, auto_adjust=True, progress=False)
    if end:
        kwargs["end"] = end
    df = yf.download(ticker, **kwargs)
    if df.empty:
        raise RuntimeError(f"No data downloaded for ticker {ticker}.")
    close = df["Close"].squeeze().copy()
    close.name = "close"
    return close


# -----------------------------
# Tastytrade session + options
# -----------------------------
def _tastytrade_session() -> Session:
    """Login automatically using TOTP secret from .env (no manual code entry)."""
    login = os.environ.get("TASTYTRADE_LOGIN")
    password = os.environ.get("TASTYTRADE_PASSWORD")
    totp_secret = os.environ.get("TASTYTRADE_TOTP_SECRET")
    if not login or not password or not totp_secret:
        raise RuntimeError("Set TASTYTRADE_LOGIN, TASTYTRADE_PASSWORD, TASTYTRADE_TOTP_SECRET in .env")
    otp = pyotp.TOTP(totp_secret).now()
    s = Session(login, password, two_factor_authentication=otp, remember_me=True)
    return s


def fetch_options_near_target(tt_symbol: str, target_price: float, width: float = 0.02) -> float | None:
    """
    Fetch the nearest-expiry options chain from tastytrade for strikes within
    ±width of target_price. Prints the chain and returns the mid price of the
    ATM call (strike closest to target_price). Returns None on failure.
    """
    import asyncio
    from tastytrade.streamer import DXLinkStreamer
    from tastytrade.dxfeed import Quote

    lo = target_price * (1 - width)
    hi = target_price * (1 + width)

    print(f"\n===== Options Chain: {tt_symbol} | Target ${target_price:.2f} ±{width*100:.0f}% "
          f"[${lo:.2f} – ${hi:.2f}] =====")

    session = _tastytrade_session()

    chains = NestedOptionChain.get_chain(session, tt_symbol)
    if not chains:
        print("No chain data returned.")
        return None
    chain = chains[0]

    # Prefer ≤1 DTE; fall back to nearest expiration
    expirations = sorted(chain.expirations, key=lambda e: e.expiration_date)
    if not expirations:
        print("No expirations found.")
        return None
    one_dte = [e for e in expirations if e.days_to_expiration <= 1]
    exp = one_dte[-1] if one_dte else expirations[0]
    print(f"Expiration: {exp.expiration_date}  ({exp.days_to_expiration} DTE)\n")

    rows = []
    for strike in exp.strikes:
        strike_price = float(strike.strike_price)
        if lo <= strike_price <= hi:
            for side, streamer_sym, tt_sym in [
                ("CALL", strike.call_streamer_symbol, strike.call),
                ("PUT",  strike.put_streamer_symbol,  strike.put),
            ]:
                rows.append({
                    "type": side,
                    "strike": strike_price,
                    "streamer_sym": streamer_sym,
                    "tt_sym": tt_sym,
                })

    if not rows:
        print(f"No strikes found between ${lo:.2f} and ${hi:.2f}.")
        return None

    streamer_symbols = [r["streamer_sym"] for r in rows]

    async def get_quotes():
        quotes: dict = {}
        async with DXLinkStreamer(session) as streamer:
            await streamer.subscribe(Quote, streamer_symbols)
            for _ in streamer_symbols:
                event = await asyncio.wait_for(streamer.get_event(Quote), timeout=10)
                quotes[event.event_symbol] = event
        return quotes

    quotes = asyncio.run(get_quotes())

    print(f"{'Type':<5} {'Strike':>8} {'Bid':>8} {'Ask':>8} {'Mid':>8}  Symbol")
    print("-" * 65)
    for r in sorted(rows, key=lambda x: (x["strike"], x["type"])):
        q = quotes.get(r["streamer_sym"])
        if q:
            bid = float(q.bid_price or 0)
            ask = float(q.ask_price or 0)
            mid = (bid + ask) / 2
            print(f"{r['type']:<5} {r['strike']:>8.2f} {bid:>8.2f} {ask:>8.2f} {mid:>8.2f}  {r['tt_sym']}")
        else:
            print(f"{r['type']:<5} {r['strike']:>8.2f} {'N/A':>8} {'N/A':>8} {'N/A':>8}  {r['tt_sym']}")

    # Return mid of the ATM call (strike closest to target_price)
    call_rows = [r for r in rows if r["type"] == "CALL"]
    if not call_rows:
        return None
    atm_row = min(call_rows, key=lambda r: abs(r["strike"] - target_price))
    q = quotes.get(atm_row["streamer_sym"])
    if q and q.bid_price is not None and q.ask_price is not None:
        return (float(q.bid_price) + float(q.ask_price)) / 2
    return None


# -----------------------------
# Preprocessing (Section 3.2)
# -----------------------------
def cubic_spline_interpolate(close: pd.Series) -> pd.Series:
    """Fill missing values with cubic spline interpolation."""
    if close.isna().sum() == 0:
        return close
    x_full = np.arange(len(close))
    mask = ~close.isna()
    cs = CubicSpline(x_full[mask], close.values[mask])
    filled = cs(x_full)
    return pd.Series(filled, index=close.index, name=close.name)


def compute_log_returns(close: pd.Series) -> pd.Series:
    """Log return: ln(P_t / P_{t-1})."""
    log_returns = np.log(close / close.shift(1)).dropna()
    log_returns.name = "log_return"
    return log_returns


def clip_outliers(returns: pd.Series) -> pd.Series:
    """
    Outlier detection via Z-score, adjusted to [0.02, 0.98] quantile bounds
    (paper Section 3.2).
    """
    lo = returns.quantile(0.02)
    hi = returns.quantile(0.98)
    clipped = returns.clip(lower=lo, upper=hi)
    return clipped


def check_stationarity(returns: pd.Series) -> None:
    """ADF test for stationarity (paper Section 3.2). Reports result."""
    result = adfuller(returns.dropna(), autolag="AIC")
    p_value = result[1]
    stationary = p_value < 0.05
    print(f"ADF test p-value: {p_value:.4f} → series is "
          f"{'stationary' if stationary else 'NON-stationary (consider differencing)'}")


def modwt_denoise(series: np.ndarray, wavelet: str = "db2", level: int = 5) -> np.ndarray:
    """
    MODWT denoising via stationary wavelet transform (SWT).
    Keeps only the approximation coefficients (low-pass), zeroes all detail
    coefficients, then reconstructs — matching paper Section 3.2.

    The SWT requires length to be a multiple of 2^level; we pad and trim.
    """
    n = len(series)
    required = 2 ** level
    pad_len = (required - n % required) % required
    padded = np.pad(series, (0, pad_len), mode="edge")

    coeffs = pywt.swt(padded, wavelet=wavelet, level=level)
    # Zero out all detail coefficients; keep approximations only
    denoised_coeffs = [(cA, np.zeros_like(cD)) for cA, cD in coeffs]
    reconstructed = pywt.iswt(denoised_coeffs, wavelet=wavelet)
    return reconstructed[:n]


def preprocess(close: pd.Series, cfg: Config) -> tuple[np.ndarray, pd.Index, MinMaxScaler]:
    """
    Full preprocessing pipeline following paper Section 3.2.
    Returns (normalized_denoised_returns, dates, signal_scaler).
    """
    print("  [1/5] Cubic spline interpolation for missing values...")
    close = cubic_spline_interpolate(close)

    print("  [2/5] Computing log returns...")
    returns = compute_log_returns(close)

    print("  [3/5] Outlier clipping at [0.02, 0.98] quantile bounds...")
    returns = clip_outliers(returns)

    print("  [4/5] ADF stationarity test...")
    check_stationarity(returns)

    print("  [5/5] MODWT denoising (db2, 5 levels) + MinMaxScaler to [-1, 1]...")
    raw = returns.to_numpy(dtype=float)
    denoised = modwt_denoise(raw, wavelet=cfg.wavelet, level=cfg.wavelet_level)

    scaler = MinMaxScaler(feature_range=(-1, 1))
    normalized = scaler.fit_transform(denoised.reshape(-1, 1)).ravel()

    return normalized, returns.index, scaler


# -----------------------------
# TDA feature extraction (Section 2.3)
# -----------------------------
def takens_embedding(series_window: np.ndarray, delay: int, dimension: int) -> np.ndarray:
    """Single Takens embedding. Eq. from Section 2.3."""
    if delay <= 0:
        raise ValueError("delay must be > 0")
    if dimension <= 1:
        raise ValueError("dimension must be > 1")
    L = len(series_window)
    J = L - (dimension - 1) * delay
    if J <= 1:
        raise ValueError(
            f"Window too short for Takens embedding: length={L}, delay={delay}, dimension={dimension}"
        )
    cloud = np.empty((J, dimension), dtype=float)
    for i in range(J):
        cloud[i, :] = [series_window[i + j * delay] for j in range(dimension)]
    return cloud


def collect_finite_lifetimes(diagrams: List[np.ndarray], combine_h0_h1: bool = True) -> np.ndarray:
    """Collect finite lifetimes r_i = d_i - b_i from persistence diagrams."""
    lifetimes = []
    dims_to_use = range(len(diagrams)) if combine_h0_h1 else ([1] if len(diagrams) > 1 else [0])
    for d in dims_to_use:
        for birth, death in diagrams[d]:
            if np.isfinite(death):
                lifetime = death - birth
                if lifetime > 0:
                    lifetimes.append(float(lifetime))
    return np.asarray(lifetimes, dtype=float)


def persistent_entropy(lifetimes: np.ndarray) -> float:
    """H(D) = -Σ p_i log(p_i), p_i = r_i / R. Eq. (1)."""
    if lifetimes.size == 0:
        return 0.0
    total = lifetimes.sum()
    if total <= 0:
        return 0.0
    probs = lifetimes / total
    probs = probs[probs > 0]
    return float(-np.sum(probs * np.log(probs)))


def amplitude(lifetimes: np.ndarray) -> float:
    """A(D) = max_i r_i. Eq. (2)."""
    return float(np.max(lifetimes)) if lifetimes.size > 0 else 0.0


def point_count(lifetimes: np.ndarray) -> float:
    """N(D) = |I_q|. Eq. (3)."""
    return float(lifetimes.size)


def tda_features_for_window(
    series_window: np.ndarray,
    delay: int,
    dimension: int,
    homology_maxdim: int,
    combine_h0_h1: bool,
) -> np.ndarray:
    """Compute v_q = (H(D_q), A(D_q), N(D_q)) for one segment."""
    cloud = takens_embedding(series_window, delay=delay, dimension=dimension)
    dgms = ripser(cloud, maxdim=homology_maxdim)["dgms"]
    lifetimes = collect_finite_lifetimes(dgms, combine_h0_h1=combine_h0_h1)
    return np.asarray([
        persistent_entropy(lifetimes),
        amplitude(lifetimes),
        point_count(lifetimes),
    ], dtype=float)


def build_dataset(values: np.ndarray, dates: pd.Index, cfg: Config):
    """
    Sliding-window dataset construction (Section 2.3, Fig. 2).
    Each sample: signal window of length T, TDA window of length L, target.
    """
    X_signal, X_tda, y, sample_dates = [], [], [], []

    min_required = max(cfg.input_chunk_length, cfg.tda_window_length)
    for t in range(min_required - 1, len(values) - cfg.forecast_horizon):
        signal_window = values[t - cfg.input_chunk_length + 1: t + 1]
        tda_window = values[t - cfg.tda_window_length + 1: t + 1]

        tda_vec = tda_features_for_window(
            tda_window,
            delay=cfg.takens_delay,
            dimension=cfg.takens_dimension,
            homology_maxdim=cfg.homology_maxdim,
            combine_h0_h1=cfg.combine_h0_h1,
        )

        target = values[t + cfg.forecast_horizon]

        X_signal.append(signal_window)
        X_tda.append(tda_vec)
        y.append(target)
        sample_dates.append(dates[t + cfg.forecast_horizon])

    return (
        np.asarray(X_signal, dtype=float),
        np.asarray(X_tda, dtype=float),
        np.asarray(y, dtype=float),
        sample_dates,
    )


def time_series_split(*arrays, test_fraction: float):
    n = len(arrays[0])
    split = int(n * (1.0 - test_fraction))
    if split <= 0 or split >= n:
        raise ValueError("Invalid test split.")
    outputs = []
    for arr in arrays:
        outputs.extend([arr[:split], arr[split:]])
    return outputs


def make_torch_loader(x_signal: np.ndarray, x_tda: np.ndarray, y: np.ndarray,
                      batch_size: int, shuffle: bool):
    dataset = torch.utils.data.TensorDataset(
        torch.tensor(x_signal, dtype=torch.float32),
        torch.tensor(x_tda, dtype=torch.float32),
        torch.tensor(y, dtype=torch.float32).unsqueeze(-1),
    )
    return torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)


# -----------------------------
# N-BEATS+TDA model (Section 2.4)
# -----------------------------
class NBeatsTDABlock(nn.Module):
    """
    N-BEATS double-residual block augmented with TDA features (Section 2.4.2).

    Input: concatenation [x^{p-1}, v] where v = (H(D), A(D), N(D)).
    Outputs backcast and forecast components (Eq. 5–6).
    """
    def __init__(
        self,
        signal_length: int,
        tda_dim: int,
        forecast_horizon: int,
        hidden_width: int,
        n_layers: int,
        dropout: float,
    ):
        super().__init__()
        in_dim = signal_length + tda_dim   # Eq. (8): x^p_TDA = (x^p, v)

        layers = []
        last_dim = in_dim
        for _ in range(n_layers):
            layers.append(nn.Linear(last_dim, hidden_width))
            layers.append(nn.ReLU())
            if dropout > 0:
                layers.append(nn.Dropout(dropout))
            last_dim = hidden_width
        self.mlp = nn.Sequential(*layers)   # S^p in paper

        self.backcast_head = nn.Linear(hidden_width, signal_length)   # U^p
        self.forecast_head = nn.Linear(hidden_width, forecast_horizon)  # V^p

    def forward(self, x_signal: torch.Tensor, x_tda: torch.Tensor):
        z = torch.cat([x_signal, x_tda], dim=-1)   # Eq. (8)
        h = self.mlp(z)
        backcast = self.backcast_head(h)
        forecast = self.forecast_head(h)
        return backcast, forecast


class NBeatsTDA(nn.Module):
    """
    Stack of P double-residual blocks (Section 2.4.2, Fig. 3 right).
    x^p = x^{p-1} - backcast^p  (Eq. 5)
    ŷ = Σ_p forecast^p           (Eq. 7)
    """
    def __init__(
        self,
        signal_length: int,
        tda_dim: int,
        forecast_horizon: int,
        n_blocks: int,
        hidden_width: int,
        n_layers: int,
        dropout: float,
    ):
        super().__init__()
        self.signal_length = signal_length
        self.forecast_horizon = forecast_horizon
        self.blocks = nn.ModuleList([
            NBeatsTDABlock(
                signal_length=signal_length,
                tda_dim=tda_dim,
                forecast_horizon=forecast_horizon,
                hidden_width=hidden_width,
                n_layers=n_layers,
                dropout=dropout,
            )
            for _ in range(n_blocks)
        ])

    def forward(self, x_signal: torch.Tensor, x_tda: torch.Tensor) -> torch.Tensor:
        residual = x_signal
        forecast_sum = torch.zeros(
            (x_signal.size(0), self.forecast_horizon),
            dtype=x_signal.dtype,
            device=x_signal.device,
        )
        for block in self.blocks:
            backcast, forecast = block(residual, x_tda)
            residual = residual - backcast      # Eq. (5)
            forecast_sum = forecast_sum + forecast  # Eq. (7)
        return forecast_sum


# -----------------------------
# Training utilities
# -----------------------------
def train_model(
    model: nn.Module,
    train_loader,
    val_loader,
    cfg: Config,
) -> nn.Module:
    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=cfg.learning_rate,
        weight_decay=cfg.weight_decay,
    )
    criterion = nn.MSELoss()   # paper Section 3.4: MSE loss

    best_state = None
    best_val = float("inf")
    wait = 0

    for epoch in range(1, cfg.epochs + 1):
        model.train()
        train_losses = []
        for xb_signal, xb_tda, yb in train_loader:
            xb_signal = xb_signal.to(cfg.device)
            xb_tda = xb_tda.to(cfg.device)
            yb = yb.to(cfg.device)

            optimizer.zero_grad()
            pred = model(xb_signal, xb_tda)
            loss = criterion(pred, yb)
            loss.backward()
            optimizer.step()
            train_losses.append(loss.item())

        model.eval()
        val_losses = []
        with torch.no_grad():
            for xb_signal, xb_tda, yb in val_loader:
                xb_signal = xb_signal.to(cfg.device)
                xb_tda = xb_tda.to(cfg.device)
                yb = yb.to(cfg.device)
                pred = model(xb_signal, xb_tda)
                val_losses.append(criterion(pred, yb).item())

        mean_train = float(np.mean(train_losses))
        mean_val = float(np.mean(val_losses))
        print(f"Epoch {epoch:03d} | train_loss={mean_train:.6f} | val_loss={mean_val:.6f}")

        if mean_val < best_val:
            best_val = mean_val
            best_state = copy.deepcopy(model.state_dict())
            wait = 0
        else:
            wait += 1
            if wait >= cfg.patience:
                print(f"Early stopping at epoch {epoch}.")
                break

    if best_state is not None:
        model.load_state_dict(best_state)
    return model


def predict_model(model: nn.Module, x_signal: np.ndarray, x_tda: np.ndarray,
                  cfg: Config) -> np.ndarray:
    model.eval()
    with torch.no_grad():
        xb_signal = torch.tensor(x_signal, dtype=torch.float32, device=cfg.device)
        xb_tda = torch.tensor(x_tda, dtype=torch.float32, device=cfg.device)
        pred = model(xb_signal, xb_tda).cpu().numpy().ravel()
    return pred


def signed_directional_accuracy(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return float(np.mean(np.sign(y_true) == np.sign(y_pred)))


def implied_next_close(current_close: float, predicted_log_return: float) -> float:
    return float(current_close * math.exp(predicted_log_return))


def save_to_history(
    date: str,
    last_close: float,
    forecasted_close: float,
    atm_call_cost: float | None,
    path: str = "history.json",
) -> None:
    """Append one forecast record to history.json."""
    import json

    record = {
        "date": date,
        "last_close": round(last_close, 4),
        "forecasted_close": round(forecasted_close, 4),
        "atm_call_cost": round(atm_call_cost, 4) if atm_call_cost is not None else None,
    }

    history = []
    if os.path.exists(path):
        with open(path) as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []

    # Replace existing entry for same date or append
    dates = [r["date"] for r in history]
    if date in dates:
        history[dates.index(date)] = record
    else:
        history.append(record)

    with open(path, "w") as f:
        json.dump(history, f, indent=2)

    print(f"\nSaved to {path}: {record}")


# -----------------------------
# Main
# -----------------------------
def main(cfg: Config | None = None):
    if cfg is None:
        cfg = Config()
    set_seed(cfg.random_state)

    print(f"Device: {cfg.device}")
    print(f"Downloading {cfg.ticker} data...")
    close = download_close_prices(cfg.ticker, cfg.start, cfg.end)

    print("\nPreprocessing (paper Section 3.2)...")
    values, dates, scaler = preprocess(close, cfg)

    print(f"\nPreprocessed series: {len(values)} samples")

    print("\nBuilding sliding-window TDA dataset...")
    X_signal, X_tda, y, sample_dates = build_dataset(values, dates, cfg)

    print(f"Samples: {len(y)}")
    print(f"Signal feature shape: {X_signal.shape}  (T={cfg.input_chunk_length})")
    print(f"TDA feature shape:    {X_tda.shape}     (L={cfg.tda_window_length}, tau={cfg.takens_delay}, k={cfg.takens_dimension})")

    (
        X_signal_train, X_signal_test,
        X_tda_train, X_tda_test,
        y_train, y_test,
        dates_train, dates_test,
    ) = time_series_split(
        X_signal, X_tda, y, np.array(sample_dates, dtype="datetime64[ns]"),
        test_fraction=cfg.test_fraction,
    )

    # Validation split inside training (preserving time order)
    n_train_total = len(y_train)
    n_val = max(1, int(n_train_total * cfg.val_fraction_within_train))
    n_fit = n_train_total - n_val
    if n_fit <= 10:
        raise RuntimeError("Too little data after validation split.")

    X_signal_fit, X_signal_val = X_signal_train[:n_fit], X_signal_train[n_fit:]
    X_tda_fit, X_tda_val = X_tda_train[:n_fit], X_tda_train[n_fit:]
    y_fit, y_val = y_train[:n_fit], y_train[n_fit:]

    # NOTE: The signal is already MinMaxScaled to [-1,1] (paper Section 3.2).
    # We still standardize TDA features separately (paper doesn't specify TDA scaling).
    from sklearn.preprocessing import StandardScaler
    tda_scaler = StandardScaler()
    X_tda_fit_sc = tda_scaler.fit_transform(X_tda_fit)
    X_tda_val_sc = tda_scaler.transform(X_tda_val)
    X_tda_train_sc = tda_scaler.transform(X_tda_train)
    X_tda_test_sc = tda_scaler.transform(X_tda_test)

    train_loader = make_torch_loader(
        X_signal_fit, X_tda_fit_sc, y_fit,
        batch_size=cfg.batch_size, shuffle=True,
    )
    val_loader = make_torch_loader(
        X_signal_val, X_tda_val_sc, y_val,
        batch_size=cfg.batch_size, shuffle=False,
    )

    model = NBeatsTDA(
        signal_length=cfg.input_chunk_length,
        tda_dim=3,
        forecast_horizon=cfg.forecast_horizon,
        n_blocks=cfg.n_blocks,
        hidden_width=cfg.hidden_width,    # 512 (paper Section 3.4)
        n_layers=cfg.n_layers,            # 2   (paper Section 3.4)
        dropout=cfg.dropout,
    ).to(cfg.device)

    print("\nTraining N-BEATS+TDA model (paper Section 3.4 hyperparameters)...")
    model = train_model(model, train_loader, val_loader, cfg)

    # Predictions (in normalized space — signal already in [-1,1])
    pred_train = predict_model(model, X_signal_train, X_tda_train_sc, cfg)
    pred_test = predict_model(model, X_signal_test, X_tda_test_sc, cfg)

    train_mae = mean_absolute_error(y_train, pred_train)
    test_mae = mean_absolute_error(y_test, pred_test)
    train_rmse = math.sqrt(mean_squared_error(y_train, pred_train))
    test_rmse = math.sqrt(mean_squared_error(y_test, pred_test))
    test_mda = signed_directional_accuracy(y_test, pred_test)

    # MAPE (paper's primary metric)
    eps = 1e-8
    test_mape = float(np.mean(np.abs((y_test - pred_test) / (np.abs(y_test) + eps))) * 100)

    print("\n===== Results =====")
    print(f"Train MAE:  {train_mae:.6f}")
    print(f"Test  MAE:  {test_mae:.6f}")
    print(f"Train RMSE: {train_rmse:.6f}")
    print(f"Test  RMSE: {test_rmse:.6f}")
    print(f"Test  MAPE: {test_mape:.2f}%")
    print(f"Test  directional accuracy: {100 * test_mda:.2f}%")

    # Latest forecast (on preprocessed/normalized scale)
    latest_signal = values[-cfg.input_chunk_length:].reshape(1, -1)
    latest_tda = tda_features_for_window(
        values[-cfg.tda_window_length:],
        delay=cfg.takens_delay,
        dimension=cfg.takens_dimension,
        homology_maxdim=cfg.homology_maxdim,
        combine_h0_h1=cfg.combine_h0_h1,
    ).reshape(1, -1)
    latest_tda_sc = tda_scaler.transform(latest_tda)

    latest_pred_normalized = predict_model(model, latest_signal, latest_tda_sc, cfg)[0]

    # Inverse-transform: normalized → denoised log return → price
    pred_log_return = scaler.inverse_transform([[latest_pred_normalized]])[0, 0]
    last_close = float(close.iloc[-1])
    forecasted_price = last_close * math.exp(pred_log_return)

    print("\n===== Price Forecast =====")
    print(f"Data through:         {dates[-1].date()}")
    print(f"Last available close: {last_close:.2f}")
    print(f"Predicted log return: {pred_log_return:.6f}")
    print(f"Forecasted price:     {forecasted_price:.2f}")
    print(f"TDA features [entropy, amplitude, point_count]: {latest_tda.ravel()}")

    atm_call_cost = None
    if cfg.options_symbol:
        atm_call_cost = fetch_options_near_target(cfg.options_symbol, forecasted_price, width=cfg.options_width)

    save_to_history(
        date=str(dates[-1].date()),
        last_close=last_close,
        forecasted_close=forecasted_price,
        atm_call_cost=atm_call_cost,
    )

    if cfg.show_plot:
        plot_df = pd.DataFrame({
            "date": pd.to_datetime(dates_test),
            "actual": y_test,
            "predicted": pred_test,
        }).set_index("date")

        plt.figure(figsize=(12, 5))
        plt.plot(plot_df.index, plot_df["actual"], label="Actual (normalized)")
        plt.plot(plot_df.index, plot_df["predicted"], label="Predicted (normalized)")
        plt.title("Dow Jones: Actual vs Predicted (N-BEATS+TDA, paper preprocessing)")
        plt.xlabel("Date")
        plt.ylabel("Normalized denoised log return")
        plt.legend()
        plt.tight_layout()
        plt.show()


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="TDA N-BEATS forecaster")
    parser.add_argument(
        "--ticker", metavar="SYMBOL", default=None,
        help="Yahoo Finance ticker symbol (default: ^DJI).",
    )
    parser.add_argument(
        "--forecast", metavar="DATE",
        help="Target forecast date YYYY-MM-DD. Downloads data up to this date, trains, and outputs a price forecast.",
    )
    parser.add_argument(
        "--plot", action="store_true", default=False,
        help="Show the actual vs predicted chart after training.",
    )
    parser.add_argument(
        "--options", metavar="SYMBOL", default=None,
        help="Tastytrade symbol to fetch options chain for (e.g. SPY). "
             "Prints strikes within --width of the forecasted price.",
    )
    parser.add_argument(
        "--width", metavar="FRAC", type=float, default=0.02,
        help="Fraction around forecasted price to filter strikes (default 0.02 = ±2%%).",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    cfg = Config()
    if args.ticker:
        cfg.ticker = args.ticker
    if args.forecast:
        cfg.end = args.forecast
    cfg.show_plot = args.plot
    if args.options:
        cfg.options_symbol = args.options
        cfg.options_width = args.width
    main(cfg)
