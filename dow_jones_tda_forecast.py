
"""
Dow Jones TDA forecasting demo
--------------------------------
This script implements a practical version of the methodology described in:
"Enhancing financial time series forecasting through topological data analysis"

Pipeline:
  1) Download Dow Jones Industrial Average (^DJI) data from Yahoo Finance
  2) Compute log returns
  3) For each rolling window:
       - Build a single Takens embedding
       - Compute Vietoris-Rips persistent homology
       - Summarize the persistence diagram with:
           * persistent entropy
           * amplitude (max lifetime)
           * point count
  4) Concatenate those TDA features with the raw lag window
  5) Train a neural regressor to predict the next-day log return
  6) Report metrics and the latest out-of-sample prediction

Notes:
  - This is a faithful implementation of the feature-extraction idea,
    but not an exact reproduction of the paper's N-BEATS architecture.
  - It uses an MLP regressor for portability and simplicity.
  - If you want, this can be extended to N-BEATS in PyTorch.

Dependencies:
  pip install yfinance pandas numpy scikit-learn matplotlib ripser

Usage:
  python dow_jones_tda_forecast.py
"""

from __future__ import annotations

import math
import warnings
from dataclasses import dataclass
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf
from ripser import ripser
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")


@dataclass
class Config:
    ticker: str = "^DJI"
    start: str = "2015-01-01"
    end: str = "2026-01-01"

    # Forecast setup
    input_chunk_length: int = 20      # raw lag window fed to model
    forecast_horizon: int = 1         # next-step prediction

    # TDA setup
    tda_window_length: int = 30       # window length L used for TDA
    takens_delay: int = 2             # tau
    takens_dimension: int = 3         # k
    homology_maxdim: int = 1          # compute H0 and H1
    combine_h0_h1: bool = True        # summarize across both H0/H1 finite lifetimes

    # Model setup
    test_fraction: float = 0.2
    random_state: int = 42
    hidden_layer_sizes: Tuple[int, int] = (64, 32)
    max_iter: int = 1000

    # Plot setup
    show_plot: bool = True


def download_close_prices(ticker: str, start: str, end: str) -> pd.Series:
    df = yf.download(ticker, start=start, end=end, auto_adjust=True, progress=False)
    if df.empty:
        raise RuntimeError(f"No data downloaded for ticker {ticker}.")
    if "Close" not in df.columns:
        raise RuntimeError("Downloaded data does not contain a Close column.")
    close = df["Close"].dropna().copy()
    close.name = "close"
    return close


def compute_log_returns(close: pd.Series) -> pd.Series:
    log_returns = np.log(close / close.shift(1)).dropna()
    log_returns.name = "log_return"
    return log_returns


def takens_embedding(series_window: np.ndarray, delay: int, dimension: int) -> np.ndarray:
    """
    Build a single Takens embedding for a 1D window.

    Given [x1, x2, ..., xL], produce points:
    (x_i, x_{i+delay}, ..., x_{i+(dimension-1)delay})
    """
    if delay <= 0 or dimension <= 1:
        raise ValueError("delay must be > 0 and dimension must be > 1")

    L = len(series_window)
    J = L - (dimension - 1) * delay
    if J <= 1:
        raise ValueError(
            f"Window too short for Takens embedding: length={L}, delay={delay}, dimension={dimension}"
        )

    point_cloud = np.empty((J, dimension), dtype=float)
    for i in range(J):
        point_cloud[i, :] = [series_window[i + j * delay] for j in range(dimension)]
    return point_cloud


def collect_finite_lifetimes(diagrams: List[np.ndarray], combine_h0_h1: bool = True) -> np.ndarray:
    """
    Extract finite lifetimes from persistence diagrams.
    diagrams[d] corresponds to H_d.
    """
    lifetimes = []

    dims_to_use = range(len(diagrams)) if combine_h0_h1 else [1] if len(diagrams) > 1 else [0]

    for d in dims_to_use:
        for birth, death in diagrams[d]:
            if np.isfinite(death):
                lifetime = death - birth
                if lifetime > 0:
                    lifetimes.append(float(lifetime))

    return np.array(lifetimes, dtype=float)


def persistent_entropy(lifetimes: np.ndarray) -> float:
    if lifetimes.size == 0:
        return 0.0
    total = lifetimes.sum()
    if total <= 0:
        return 0.0
    probs = lifetimes / total
    # numerical guard
    probs = probs[probs > 0]
    return float(-np.sum(probs * np.log(probs)))


def amplitude(lifetimes: np.ndarray) -> float:
    if lifetimes.size == 0:
        return 0.0
    return float(np.max(lifetimes))


def point_count(lifetimes: np.ndarray) -> int:
    return int(lifetimes.size)


def tda_features_for_window(
    series_window: np.ndarray,
    delay: int,
    dimension: int,
    homology_maxdim: int,
    combine_h0_h1: bool,
) -> np.ndarray:
    cloud = takens_embedding(series_window, delay=delay, dimension=dimension)
    result = ripser(cloud, maxdim=homology_maxdim)
    diagrams = result["dgms"]
    lifetimes = collect_finite_lifetimes(diagrams, combine_h0_h1=combine_h0_h1)

    H = persistent_entropy(lifetimes)
    A = amplitude(lifetimes)
    N = point_count(lifetimes)
    return np.array([H, A, float(N)], dtype=float)


def build_dataset(returns: pd.Series, cfg: Config) -> Tuple[np.ndarray, np.ndarray, List[pd.Timestamp]]:
    """
    Build supervised samples.
    Each sample uses:
      - raw lag window of length input_chunk_length
      - TDA features computed on the most recent tda_window_length observations ending at time t
    Target:
      - next-day log return
    """
    values = returns.to_numpy(dtype=float)
    dates = returns.index.to_list()

    X, y, sample_dates = [], [], []

    min_required = max(cfg.input_chunk_length, cfg.tda_window_length)
    for t in range(min_required - 1, len(values) - cfg.forecast_horizon):
        raw_window = values[t - cfg.input_chunk_length + 1 : t + 1]
        tda_window = values[t - cfg.tda_window_length + 1 : t + 1]

        tda_vec = tda_features_for_window(
            tda_window,
            delay=cfg.takens_delay,
            dimension=cfg.takens_dimension,
            homology_maxdim=cfg.homology_maxdim,
            combine_h0_h1=cfg.combine_h0_h1,
        )

        features = np.concatenate([raw_window, tda_vec], axis=0)
        target = values[t + cfg.forecast_horizon]

        X.append(features)
        y.append(target)
        sample_dates.append(dates[t + cfg.forecast_horizon])

    return np.asarray(X), np.asarray(y), sample_dates


def train_test_split_time_series(
    X: np.ndarray, y: np.ndarray, dates: List[pd.Timestamp], test_fraction: float
):
    split_idx = int(len(X) * (1.0 - test_fraction))
    if split_idx <= 0 or split_idx >= len(X):
        raise ValueError("Invalid split index. Adjust test_fraction or data size.")

    return (
        X[:split_idx], X[split_idx:],
        y[:split_idx], y[split_idx:],
        dates[:split_idx], dates[split_idx:]
    )


def signed_directional_accuracy(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return float(np.mean(np.sign(y_true) == np.sign(y_pred)))


def last_price_from_return(current_price: float, predicted_log_return: float) -> float:
    return float(current_price * math.exp(predicted_log_return))


def main() -> None:
    cfg = Config()

    print("Downloading Dow Jones data...")
    close = download_close_prices(cfg.ticker, cfg.start, cfg.end)

    print("Computing log returns...")
    returns = compute_log_returns(close)

    print("Building TDA-enhanced supervised dataset...")
    X, y, sample_dates = build_dataset(returns, cfg)

    print(f"Samples: {len(X)}")
    print(f"Feature dimension: {X.shape[1]} "
          f"(raw lags={cfg.input_chunk_length} + TDA=3)")

    X_train, X_test, y_train, y_test, train_dates, test_dates = train_test_split_time_series(
        X, y, sample_dates, cfg.test_fraction
    )

    x_scaler = StandardScaler()
    y_scaler = StandardScaler()

    X_train_scaled = x_scaler.fit_transform(X_train)
    X_test_scaled = x_scaler.transform(X_test)

    y_train_scaled = y_scaler.fit_transform(y_train.reshape(-1, 1)).ravel()

    print("Training neural regressor...")
    model = MLPRegressor(
        hidden_layer_sizes=cfg.hidden_layer_sizes,
        activation="relu",
        solver="adam",
        max_iter=cfg.max_iter,
        random_state=cfg.random_state,
    )
    model.fit(X_train_scaled, y_train_scaled)

    pred_train_scaled = model.predict(X_train_scaled)
    pred_test_scaled = model.predict(X_test_scaled)

    pred_train = y_scaler.inverse_transform(pred_train_scaled.reshape(-1, 1)).ravel()
    pred_test = y_scaler.inverse_transform(pred_test_scaled.reshape(-1, 1)).ravel()

    train_mae = mean_absolute_error(y_train, pred_train)
    test_mae = mean_absolute_error(y_test, pred_test)
    train_rmse = math.sqrt(mean_squared_error(y_train, pred_train))
    test_rmse = math.sqrt(mean_squared_error(y_test, pred_test))
    test_mda = signed_directional_accuracy(y_test, pred_test)

    print("\n===== Results =====")
    print(f"Train MAE:  {train_mae:.6f}")
    print(f"Test MAE:   {test_mae:.6f}")
    print(f"Train RMSE: {train_rmse:.6f}")
    print(f"Test RMSE:  {test_rmse:.6f}")
    print(f"Test directional accuracy: {100 * test_mda:.2f}%")

    # Latest one-step-ahead forecast using the most recent available data
    latest_raw_window = returns.iloc[-cfg.input_chunk_length:].to_numpy(dtype=float)
    latest_tda_window = returns.iloc[-cfg.tda_window_length:].to_numpy(dtype=float)
    latest_tda = tda_features_for_window(
        latest_tda_window,
        delay=cfg.takens_delay,
        dimension=cfg.takens_dimension,
        homology_maxdim=cfg.homology_maxdim,
        combine_h0_h1=cfg.combine_h0_h1,
    )
    latest_features = np.concatenate([latest_raw_window, latest_tda], axis=0).reshape(1, -1)
    latest_features_scaled = x_scaler.transform(latest_features)
    next_return_scaled = model.predict(latest_features_scaled)[0]
    next_return = y_scaler.inverse_transform([[next_return_scaled]])[0, 0]

    latest_close = float(close.iloc[-1])
    implied_next_close = last_price_from_return(latest_close, next_return)

    print("\n===== Latest Forecast =====")
    print(f"Latest available close: {latest_close:.2f}")
    print(f"Predicted next log return: {next_return:.6f}")
    print(f"Implied next close: {implied_next_close:.2f}")
    print(f"Latest TDA feature vector [entropy, amplitude, point_count]: {latest_tda}")

    if cfg.show_plot:
        plot_df = pd.DataFrame({
            "date": pd.to_datetime(test_dates),
            "actual": y_test,
            "predicted": pred_test
        }).set_index("date")

        plt.figure(figsize=(12, 5))
        plt.plot(plot_df.index, plot_df["actual"], label="Actual next-day log return")
        plt.plot(plot_df.index, plot_df["predicted"], label="Predicted next-day log return")
        plt.title("Dow Jones: Actual vs Predicted Next-Day Log Return (TDA-enhanced model)")
        plt.xlabel("Date")
        plt.ylabel("Log return")
        plt.legend()
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    main()
