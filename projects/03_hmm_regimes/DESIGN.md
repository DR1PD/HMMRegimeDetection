HMM Regime Detection  |  D. Colindres

PROJECT SPECIFICATION

**Hidden Markov Model Regime Detection**

Identifying Latent Volatility and Liquidity States in Financial Markets

**David Colindres**

B.S./M.S. Industrial & Systems Engineering

University of Oklahoma

*Prepared for MFE / MSCF / MSFE Admissions Portfolio — Project 3 of 3*

March 2026

# A. Project Title

***Hidden Markov Model Regime Detection: Identifying Latent Volatility and Liquidity States in Financial Markets***

# B. Project Thesis

Financial markets do not behave the same way all the time. Volatility clusters, correlations spike during crises, and the statistical properties of returns shift between distinct regimes — calm vs. turbulent, risk-on vs. risk-off, expansion vs. contraction. These regime changes are not directly observable; they are latent states that must be inferred from the data.

This project implements a Gaussian Hidden Markov Model (HMM) calibrated via the Expectation-Maximization (EM) algorithm to detect latent volatility and liquidity regimes in equity market returns. The model estimates the number of regimes, their statistical parameters (mean return, volatility, persistence), and the probability of being in each regime at any point in time. The central question is whether HMM-detected regimes are economically meaningful — do they correspond to recognizable market conditions, do they predict future volatility, and can regime-aware portfolio strategies outperform regime-agnostic baselines?

# C. Why This Project Is Admissions-Relevant

**Stochastic processes. **The HMM is a state-space model grounded in Markov chains, conditional distributions, and latent variable inference. This is exactly the material tested in probability and stochastic processes courses at top MFE programs.

**The EM algorithm. **Calibrating the HMM requires the Baum-Welch algorithm (a special case of EM), touching maximum likelihood estimation, iterative optimization, convergence guarantees, and latent variable machinery.

**Time-series econometrics. **Regime-switching models (Hamilton, 1989) are a cornerstone of financial econometrics. This connects directly to courses in time-series analysis where Markov-switching GARCH and state-space models are standard.

**Financial relevance. **Understanding non-stationarity — that the data-generating process itself changes — is one of the most important insights in quantitative finance. Regime detection is used for risk management, portfolio allocation, derivatives pricing, and signal generation.

**ISE alignment. **HMMs leverage core ISE competencies: stochastic modeling, statistical inference, optimization (EM), and systems-level thinking about processes that evolve through discrete states. Quality control and reliability engineering use similar frameworks.

**Portfolio integration. **This project directly connects to Projects 1 and 2. Regime probabilities can condition the portfolio optimizer (Project 1) and explain dynamic dimensionality in the eigenvalue spectrum (Project 2: during crises, correlations spike and the number of signal eigenvalues collapses).

# D. Research Question

*Do Gaussian Hidden Markov Models fitted to multivariate market observables identify economically meaningful latent regimes that (a) align with recognized market conditions, (b) predict future volatility and drawdown risk out of sample, and (c) enable regime-conditional portfolio strategies that outperform regime-agnostic baselines in net risk-adjusted returns?*

# E. Quant Finance Concepts Involved

- Hidden Markov Models (discrete latent states, continuous emissions)

- Markov chains: transition matrices, stationary distributions, persistence

- Expectation-Maximization (Baum-Welch) algorithm for parameter estimation

- Gaussian mixture emissions (multivariate normal per regime)

- Forward-backward algorithm for state probability inference

- Viterbi algorithm for most-likely state sequence (dynamic programming)

- Regime-switching models (Hamilton, 1989)

- Realized volatility estimation and forecasting

- Correlation dynamics as regime features

- Regime-conditioned VaR and CVaR

- Volatility forecasting: HMM vs GARCH benchmarks

- Model selection: BIC/AIC for optimal number of regimes

- Rolling-window out-of-sample evaluation

- Volatility clustering, fat tails, mean reversion, regime shifts

# F. Math/Statistics Requirements

The following mathematics must appear explicitly as implemented computation:

> **[STATUS 2026-07-19]** Forward algorithm: **implemented and validated** against hmmlearn (`common/hmm_filter.py`; exact agreement at t = T; `tests/test_walkforward_leaks.py`) — used for all causal probabilities since ROADMAP 1.2. Backward pass, E-step/M-step (Baum-Welch), Viterbi, and log-likelihood monitoring currently run via `hmmlearn` end-to-end (AUDIT P3-3); hand-rolled implementations with 1e-6 validation are **[PLANNED — Phase 4.1]**.

## 1. Markov Chain Transition Matrix

A[i,j] = P(S_t = j | S_{t-1} = i)

Each row sums to 1. The diagonal elements A[k,k] measure regime persistence. Expected duration of regime k = 1/(1 - A[k,k]).

## 2. Gaussian Emission Distribution

P(y_t | S_t = k) = N(y_t; μ_k, Σ_k)

Each regime k has its own mean vector μ_k and covariance matrix Σ_k. For the univariate case: N(r_t; μ_k, σ_k²).

## 3. Forward Algorithm

α_t(k) = P(y_1,...,y_t, S_t=k)

α_t(j) = [Σ_i α_{t-1}(i) · A[i,j]] · P(y_t | S_t=j)

Computed recursively. Used for likelihood evaluation and as input to the E-step.

## 4. Backward Algorithm

β_t(k) = P(y_{t+1},...,y_T | S_t=k)

## 5. E-Step: Posterior State Probabilities

γ_t(k) = P(S_t=k | Y) = α_t(k) · β_t(k) / P(Y)

These are the smoothed state probabilities — the probability of being in regime k at time t, given all observed data.

## 6. M-Step: Parameter Updates

μ_k = Σ_t γ_t(k) · y_t / Σ_t γ_t(k)

Σ_k = Σ_t γ_t(k) · (y_t - μ_k)(y_t - μ_k)ᵀ / Σ_t γ_t(k)

A[i,j] = Σ_t ξ_t(i,j) / Σ_t γ_t(i)

where ξ_t(i,j) = P(S_{t-1}=i, S_t=j | Y) is the transition posterior.

## 7. Log-Likelihood and Convergence

log P(Y|θ) = log Σ_k α_T(k)

Monitored at each EM iteration. Convergence when the relative change falls below a tolerance.

## 8. Model Selection (BIC)

BIC = -2 · log L + p · log(T)

where p is the number of free parameters and T is the number of observations. Lower BIC is better. Used to select the number of regimes.

> **[STATUS 2026-07-19]** The current `compute_bic` has defect **P3-7** (hmmlearn's total log-likelihood scaled as if per-sample, ~4,500× inflation), so the K=5 grid-boundary selection is **unsupported as computed**. Corrected BIC + an extended K grid (until the criterion turns) is owned by **ROADMAP 3.2** together with P3-2.

## 9. Viterbi Algorithm

S* = argmax_{S_1,...,S_T} P(S_1,...,S_T | Y)

Finds the most likely sequence of hidden states via dynamic programming. Used for ex-post regime labeling.

## 10. Stationary Distribution

π = π A

The long-run probability of being in each regime. Solved as the left eigenvector of A corresponding to eigenvalue 1.

## 11. Regime-Conditioned Risk Metrics

VaR_α^(k) = μ_k + z_α · σ_k

CVaR_α^(k) = μ_k - σ_k · φ(z_α) / (1-α)

Parametric VaR and CVaR conditioned on the current regime.

# G. Data

## Primary Data Sources

| **Data** | **Source** | **Variables** | **Frequency** |
| --- | --- | --- | --- |
| S&P 500 | yfinance (SPY) | Adj close, log returns | Daily |
| Realized volatility | Computed | 21-day rolling std, annualized | Daily |
| VIX | yfinance (^VIX) | Implied volatility index | Daily |
| Yield curve slope | yfinance / FRED | 10Y - 2Y Treasury spread | Daily [NOT USED] |
| Equity universe | yfinance | 50 large-cap returns (correlation dynamics) | Daily [NOT USED] |

Period: January 2000 – December 2024 (25 years). Longer than Projects 1-2 because regime detection benefits from seeing multiple full cycles. IS: 2000–2017. OOS: 2018–2024.

# H. Modeling Pipeline

- **Step 1: Data Ingestion. **Pull SPY returns, VIX, Treasury yields. Compute realized volatility (21-day rolling std × √252). Compute rolling mean pairwise correlation of 50-asset universe as correlation dynamics feature. [NOT IMPLEMENTED — 2026-07-19: dropped; the observation vector as built is exactly (r_t, realized vol, ΔVIX). See the AUDIT G-3 correction note.]

- **Step 2: Feature Construction. **Build multivariate observation vector y_t = [r_t, σ_t^{realized}, ΔVIX_t] or extend with yield curve slope and credit spread. Standardize features to zero mean, unit variance. [As implemented since 1.2 (P3-1): scaler frozen to IS for model selection; each walk-forward window standardized by its own trailing stats. Winsorization quantiles remain full-sample — `docs/LIMITATIONS.md` §2.]

- **Step 3: Model Selection. **Fit HMMs with K = 2, 3, 4, 5 regimes. Compare via BIC, AIC, and log-likelihood. Select optimal K. Visualize BIC curve.

- **Step 4: HMM Calibration. **Fit Gaussian HMM with optimal K using EM (Baum-Welch). Multiple random initializations to avoid local optima. Record convergence diagnostics (log-likelihood per iteration).

- **Step 5: State Inference. **Compute smoothed state probabilities γ_t(k) via forward-backward. Compute Viterbi most-likely state sequence. Label regimes by their estimated volatility (Low-Vol, Medium-Vol, High-Vol, Crisis).

- **Step 6: Regime Characterization. **For each detected regime: compute mean return, volatility, Sharpe ratio, average duration, correlation level. Map regimes to known market conditions (GFC, COVID, dot-com, etc.).

- **Step 7: Volatility Forecasting. **Test whether the HMM’s current-regime volatility σ_k predicts next-period realized volatility better than (a) historical rolling vol, (b) GARCH(1,1), (c) VIX.

- **Step 8: Regime-Aware Portfolio. **Build a simple regime-switching strategy: equities in low-vol regime, defensive (cash/bonds proxy) in high-vol regime. Compare against buy-and-hold and 60/40.

- **Step 9: Rolling OOS Evaluation. **Walk-forward: at each rebalancing date, fit HMM on trailing data only. Use current regime probability for allocation decision. No future information leaks.

> **[STATUS 2026-07-19]** This claim was violated by P3-1 (full-sample scaler) and P3-6 (smoothed-probability grading) until ROADMAP 1.2; both are fixed and the discipline is enforced by `tests/test_walkforward_leaks.py` (invariance to deleting post-t data).

- **Step 10: Sensitivity & Robustness. **Vary number of regimes, feature set, lookback window, rebalancing frequency. Regime-conditioned evaluation per Project 1/2 framework.

# I. Benchmarks

| **#** | **Benchmark** | **Description** | **Purpose** |
| --- | --- | --- | --- |
| 1 | **Buy-and-Hold SPY** | 100% equity, no regime awareness | Baseline: what if you ignore regimes? |
| 2 | **60/40 Portfolio** | Static 60% equity / 40% bonds | Classic allocation benchmark |
| 3 | **VIX-Based Switching** | Equities when VIX<20, defensive when VIX>25 | Simple observable-based regime rule |
| 4 | **GARCH Vol Forecast** | Reduce equity when GARCH vol > threshold [currently an EWMA proxy — true GARCH PLANNED — Phase 4.2] | Parametric time-series benchmark |
| 5 | **Rolling Vol Switching** | Use 63-day rolling vol as regime signal | Simple historical vol benchmark |

# J. Evaluation Framework

## Regime Quality Metrics

| **Metric** | **Description** |
| --- | --- |
| **Regime persistence** | Diagonal of transition matrix A[k,k]. Higher = more stable regimes |
| **Expected duration** | 1/(1-A[k,k]) days per regime visit |
| **Within-regime Sharpe** | Sharpe ratio computed only on days classified in each regime |
| **Regime separation** | Distance between regime means in volatility space |
| **Classification stability** | % of days whose regime label changes when re-estimated on shifted window [PLANNED — Phase 3] |
| **BIC / AIC scores** | Model selection criteria across K = 2,3,4,5 |
| **Log-likelihood convergence** | EM convergence diagnostic |

## Volatility Forecasting Metrics

| **Metric** | **Description** |
| --- | --- |
| **RMSE of vol forecast** | HMM regime-vol vs realized next-period vol |
| **MAE of vol forecast** | Absolute forecast error |
| **QLIKE score** | Quasi-likelihood loss (robust to vol-of-vol) |
| **Directional accuracy** | % of times vol forecast correctly predicts vol increase/decrease |
| **Regime-conditioned VaR coverage** | Does VaR calibrated per-regime achieve correct coverage? |

## Portfolio Metrics

| **Metric** | **Description** |
| --- | --- |
| **Net Sharpe ratio** | (Net return - RF) / Volatility |
| **Maximum drawdown** | Largest peak-to-trough decline |
| **Calmar ratio** | Return / max drawdown |
| **Turnover** | Trade frequency from regime switching |
| **Crisis alpha** | Excess return specifically during bear regimes vs buy-and-hold |
| **Recovery capture** | % of post-crisis recovery captured by switching back to equities |

## Robustness Checks

- Number of regimes: K = 2, 3, 4, 5

- Feature sensitivity: returns only vs returns+vol vs full multivariate

- Lookback window: 500, 1000, 1500, 2000 trading days

- Rebalancing frequency: daily, weekly, monthly

- EM initialization: 10 random restarts, check convergence to same solution

- Regime-conditioned evaluation per bull/bear/sideways (external classification)

## Out-of-Sample Discipline

All HMM fitting uses trailing data only. Regime classification at time t uses only data up to t. No future information in any allocation decision. IS and OOS reported separately.

# K. Failure Modes

- **Regime labels may not be stable. **HMMs fitted on different windows can assign different labels to the same regime (label switching). The project must match regimes by their statistical properties, not their arbitrary label index.

- **EM converges to local optima. **The EM algorithm is not guaranteed to find the global maximum. Multiple random restarts are essential. If different initializations produce different solutions, the model is fragile.

- **Overfitting with too many regimes. **K=5 fits the in-sample data better than K=2 by construction. BIC penalizes complexity, but the selected K may still overfit, especially if some regimes are visited only a few times.

- **Regime transitions may be too slow to trade on. **If the HMM detects a crisis regime only after the drawdown has already occurred, the regime signal is useless for risk management. Latency analysis is critical.

- **Gaussian emissions are too simple. **Real returns have fat tails (excess kurtosis). A Gaussian HMM may underestimate the probability of extreme returns within each regime. Student-t emissions would be more realistic but harder to fit.

- **The HMM may just be tracking volatility. **If regime detection is just a complicated way to measure rolling volatility, the simpler VIX-based or rolling-vol benchmarks should perform equally well. This is tested explicitly.

- **Survivorship of regimes across time. **A regime identified in the 2000–2010 period may not recur in 2018–2024, or may have different characteristics when it does.

- **Transaction costs from frequent switching. **If the HMM switches regimes often, the resulting portfolio may trade excessively, eroding returns through transaction costs.

# L. Final GitHub Repository Structure

> **[STATUS 2026-07-19]** Same as P1/P2: `src/` split and results tree **[PLANNED — Phase 2/3]**; current reality is the executed notebook + `common/hmm_filter.py` + repo-level tests.

hmm-regime-detection/
├── README.md
├── requirements.txt / environment.yml / config.yaml
├── data_dictionary.md / LICENSE
├── data/ (raw/ processed/ README.md)
├── src/
│   ├── data_loader.py     │ features.py
│   ├── hmm_model.py       │ regime_analysis.py
│   ├── vol_forecasting.py │ portfolio.py
│   ├── benchmarks.py      │ metrics.py
│   └── utils.py
├── notebooks/
│   ├── 01 through 09 (exploration → conclusions)
├── results/ (figures/ tables/ logs/)
├── tests/ (test_hmm.py, test_features.py, test_metrics.py)
└── docs/ (technical_appendix.pdf, references.bib)

# M. README Outline

- 1. Title and One-Line Summary

- 2. Executive Summary: non-stationarity problem, HMM solution, key finding

- 3. Research Question

- 4. Key Results: regime characterization table + regime timeline overlay on S&P 500

- 5. Methodology: feature construction, HMM fitting, model selection, vol forecasting, portfolio

- 6. Repository Structure

- 7. How to Reproduce

- 8. Key Visualizations: regime timeline, transition matrix heatmap, regime-conditioned distributions, vol forecast comparison, cumulative returns

- 9. Assumptions and Limitations

- 10. References

- 11. Author

# N. Resume / Interview Framing

- Implemented a Gaussian Hidden Markov Model calibrated via the Expectation-Maximization algorithm to detect latent volatility regimes in 25 years of S&P 500 data, identifying statistically distinct market states [REVISED 2026-07-19: the current run selects K=5 at the boundary of its candidate grid under the defective BIC (AUDIT P3-7); the regime count is TBD pending the corrected re-selection owned by ROADMAP 3.2] with economically interpretable characteristics.

- Built a multivariate feature pipeline (returns, realized volatility, VIX changes) and applied BIC-based model selection to determine the optimal number of regimes, with convergence diagnostics from 10 random EM initializations to ensure global optimum.

- [REVISED 2026-07-19] Result with causal (filtered) grading: the HMM does **not** lead the OOS vol-forecast comparison — VIX has the best RMSE/correlation and EWMA the best MAE (`results/CHANGELOG.md` 1.2); the measured smoothed-vs-filtered flattery gap is small. The 'GARCH' benchmark is currently an EWMA proxy; true GARCH(1,1) via `arch` is [PLANNED — Phase 4.2], and that regime-aware portfolio allocation reduces maximum drawdown during detected crisis periods. [MEASURED 2026-07-19: crisis alpha GFC +52.2%, COVID +5.1%, 2022 −11.0%; OOS MaxDD 31.8% vs 33.7% buy-and-hold — but overall OOS Sharpe trails buy-and-hold (0.238 vs 0.640); honest framing in `docs/LIMITATIONS.md` and the notebook.]

- Validated all results with strict walk-forward out-of-sample evaluation, benchmarked against five regime-agnostic strategies, and documented the connection between HMM regimes and the dynamic dimensionality collapse observed in eigenvalue analysis (Project 2).

# O. Stretch Extensions

## Extension 1: Student-t Emissions for Fat-Tailed Regimes

Replace Gaussian emissions with Student-t distributions to better capture the excess kurtosis observed in financial returns. This requires modifying the EM update equations to estimate the degrees-of-freedom parameter for each regime (Bulla, 2011).

*Why this impresses: Shows understanding that Gaussian assumptions are a simplification, and willingness to implement harder but more realistic models.*

## Extension 2: Regime-Switching Factor Model (Bridge to Project 1)

Extend the portfolio optimizer from Project 1 by making expected returns and covariance regime-dependent. In the low-vol regime, tilt toward momentum and growth; in the crisis regime, tilt toward value and low-volatility. This creates a regime-switching multi-period optimizer.

*Why this impresses: Integrates all three projects into a coherent system. This is how systematic funds actually operate — regime-conditioned allocation.*

## Extension 3: Online Regime Detection for Real-Time Use

Implement an online (streaming) version of the forward algorithm that updates regime probabilities as each new data point arrives, without re-running the full forward-backward pass. This is critical for real-time risk monitoring and trading.

*Why this impresses: Moves from batch analysis to production-grade implementation. Shows awareness of the gap between research and deployment.*

# Self-Evaluation Rubric

| **Dimension** | **Score** | **Justification** |
| --- | --- | --- |
| **Finance relevance** | 5/5 | Regime detection is foundational for risk management, allocation, and understanding non-stationarity. |
| **Mathematical rigor** | 5/5 | Markov chains, EM algorithm, forward-backward, Viterbi, BIC — target end-state; see the Section F status note [forward pass implemented+validated; remainder PLANNED — Phase 4.1; BIC defect P3-7 owned by 3.2]. |
| **Programming rigor** | 5/5 | Custom HMM pipeline, multivariate features, vol forecasting, rolling backtest, publication-quality plots. |
| **Statistical validity** | 5/5 | BIC model selection, multiple EM restarts, 5 benchmarks, IS/OOS split, latency analysis. |
| **Professional presentation** | 5/5 | Regime timeline overlaid on S&P 500 is a visually striking signature plot. |
| **Interview defensibility** | 5/5 | Can explain: why regimes matter, how EM works, what transition matrix means, why Gaussian is limiting, how regimes connect to portfolio construction. |
| **Originality** | 4/5 | HMMs for regime detection are established but implementation depth and portfolio integration elevate it. |
| **Graduate readiness** | 5/5 | Directly prepares for probability, stochastic processes, econometrics, and computational finance. |

# Key Python Libraries

| **Library** | **Role** |
| --- | --- |
| **hmmlearn** | Core: Gaussian HMM fitting via EM, Viterbi decoding, state probability inference |
| **NumPy / SciPy** | Matrix operations, statistical distributions, eigenvalue computation for stationary distribution |
| **yfinance** | Data ingestion for SPY, VIX, Treasury yields |
| **QuantLib** | Optional: yield curve construction, bond pricing for fixed-income features |
| **arch** | GARCH(1,1) benchmark for volatility forecasting comparison |
| **statsmodels** | Time-series diagnostics, autocorrelation tests, statistical tests |
| **matplotlib / plotly** | Regime timelines, transition heatmaps, 3D regime surfaces, cumulative returns |
| **scikit-learn** | Preprocessing, model selection utilities |

# References

**[1] **Hamilton, J. D. (1989). A new approach to the economic analysis of nonstationary time series. Econometrica, 57(2), 357–384.

**[2] **Rydén, T., Teräsvirta, T., & Åsbrink, S. (1998). Stylized facts of daily return series and the HMM. J. Applied Econometrics, 13(3), 217–233.

**[3] **Rabiner, L. R. (1989). A tutorial on hidden Markov models. Proceedings of the IEEE, 77(2), 257–286.

**[4] **Dempster, A. P., Laird, N. M., & Rubin, D. B. (1977). Maximum likelihood from incomplete data via the EM algorithm. JRSS-B, 39(1), 1–38.

**[5] **Ang, A., & Bekaert, G. (2002). International asset allocation with regime shifts. RFS, 15(4), 1137–1187.

**[6] **Bulla, J. (2011). Hidden Markov models with t components. Quantitative Finance, 11(3), 459–475.

**[7] **Guidolin, M., & Timmermann, A. (2007). Asset allocation under multivariate regime switching. JEDyn&Ctrl, 31(11), 3503–3544.

**[8] **Lo, A. (2002). The statistics of Sharpe ratios. Financial Analysts Journal, 58(4), 36–52.