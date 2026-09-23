# Results Changelog

Before/after record for every fix that moves reported numbers (ROADMAP 1.1
acceptance requirement). All figures are OOS (2018–2024) net Sharpe / annualized
return unless noted. Numbers remain PROVISIONAL until the Phase 1 lookahead
fixes (P3-1, P3-6) and survivorship mitigation (G-3) land.

## 2026-08-23 · Full reproduction from a lock-rebuilt environment

Incident: a folder rename (Documents/Academic → Documents/Quant) broke the
venv's absolute-path shebangs; all three notebook runs silently no-op'd and
the stale-output discipline (Writing-line + mtime + freshness-print proofs)
caught the false matches. The environment was rebuilt from requirements.lock
in ~2 minutes and all three projects re-executed end to end.

Reproduction result: **P1 exact (8/8 goldens), P2 exact (11/11), P3 9/11
exact** — the two P3 deltas are the documented EM-fragile quantities and are
float-level: strategy OOS 8.30%/0.478 vs published 8.32%/0.479 (≤2 bp /
0.001 Sharpe), band [0.281..0.479] vs [0.282..0.479], mean/std identical at
0.406/0.064. The fresh point lies inside the published band; every citable
claim stands unchanged. Threaded-BLAS EM path sensitivity is hereby a
*measured* reproducibility bound, not a hypothesis — and the reason P3's
Sharpe is cited as a band.

## 2026-07-21 · ROADMAP 3.3 — OOS discipline pass · **PHASES 0–3 COMPLETE**

Commit: 4e037d2. No numbers changed. Per-project OOS-discipline statements in
each notebook + results/OOS_DISCIPLINE.md with the five-point evidence trail;
the 3.3 sweep verified IS/OOS labeling in every results/ table (p2/p3 metric
files gained their IS tables; the P2 grid file is footnoted OOS-only-by-
design). **With this, Phases 0–3 are complete: the roadmap's applications
bar — 'applications go out with Phases 0–3 complete at minimum' — is met.**
The three projects exist as executed, tested, self-honest research artifacts:
citable baselines, published surfaces, measured limitations, and written
discipline statements an interviewer can check line by line.

## 2026-07-21 · ROADMAP 3.2 (P2 portion) — window×universe grid: the q study

Commits: grid cells + run, artifacts. 15 full backtests, T ∈ {126,252,504} ×
n ∈ {50,100,151}, q spanning 0.099–1.198 (visiting the design target 0.794
and the singular q>1 corner). Base numbers unchanged; 0/669 non-optimal
solves even on singular sample matrices.

**Verdict (question pre-stated in-notebook):** the RMT ≈ LW ≈ raw tie
SURVIVES the entire q range — max spread 0.023, occurring at the design-
target q=0.794 cell itself (twin seed: 0.007); singular corner spread 0.009.
Where cleaning should matter most in theory, it still doesn't separate the
estimators on this universe/period. Combined with 1.6's survival-profile
sweep, the tie is now established across composition AND the (T, n) design
space. ROADMAP 3.2 COMPLETE (P1 + P2 + P3 portions).

## 2026-07-21 · ROADMAP 3.2 (P1 portion) — the κ×γ trade-off surface

Commits: 1705e3e (run), 527adcd (artifacts). Grid: κ ∈ {0, 5bp, 10bp, 20bp,
0.5%, 1%, 2%} × γ ∈ {1, 2, 5}, each a full 227-rebalance backtest; cached at
results/cache/; 4,767/4,767 solves optimal; base numbers unchanged.

**Findings (no retuning — baseline stays κ=0.005 as documented):**
- Freeze boundary κ* = 0.005 at every γ: the baseline sits exactly on the
  trade/no-trade cliff. Below it the optimizer trades (turnover up to
  ~0.11/mo at κ=0).
- Costs barely bite at realized turnover (gross−net OOS gap ≤ 0.003 Sharpe) —
  but trading still doesn't pay: only 2/12 trading cells beat equal-weight
  net OOS (0.785), none by more than noise against CIs.
- The IS-selected cell (max net IS Sharpe) is ITSELF a frozen cell (γ=1,
  κ=2%: IS 0.723 → OOS 0.850, reported never selected on) — in-sample data
  independently concludes trading isn't worth it.
- **The honest paragraph:** monthly FF3-forecast rebalancing does not clear
  real costs at any sane κ on this universe — not because costs are large,
  but because the forecasts are weak; the optimizer's near-zero-trading
  policy is the correct optimum, not a calibration accident (consistent with
  DeMiguel et al. 2009). The 1.5 'freeze finding' is hereby upgraded from
  'suspicious behavior' to 'the result.'

## 2026-07-20 · ROADMAP 3.2 (P3 portion) — corrected BIC, K re-selection, fragility band

Commits: 5faac89 (fix+test), 39acf04/858b31e (grid+elbow), 1624292 (run).

**The citable regime-count answer:** corrected Gaussian-emission BIC
decreases monotonically through K=12 — no interior minimum on any grid
tried. Vanilla BIC does not identify a finite K on 25y of daily data (fat
tails reward extra Gaussian components); a credible count requires
heavier-tailed emissions (Student-t, Phase 4 Ext-1). The strategy uses a
pre-stated pragmatic elbow K=11, explicitly labeled rule-driven (and the
rule inherits the non-turning pathology — arbitrary-but-fixed, not learned).

| P3 OOS quantity | 3.1 baseline (K=5, defective BIC) | 3.2 final (elbow K=11) |
|---|---|---|
| HMM Sharpe (point) | 0.403 | 0.479 |
| HMM Sharpe (band, 11 runs) | n/a | **0.406 ± 0.064 [0.282, 0.479]** |
| HMM Return | 7.42% | 8.32% |
| Latency GFC / COVID / 2022 | +0d / +3d / missed | +4d / +11d / missed |
| Crisis alpha GFC / COVID / 2022 | +52.2% / +5.7% / −9.0% | +41.8% / +15.7% / −7.9% |
| Benchmarks | unchanged | unchanged (B&H 0.640) |
| BIC magnitude | 79.3M (defective) | 13,685 (sane) |

Note the point run sits at the band MAX — cite the band. The honest headline
stands at every K tried: the regime strategy trails buy-and-hold OOS.

## 2026-07-20 · ROADMAP 3.1 — CITABLE BASELINE + causal winsorization

Commits: 8667706 (fix), 5805b25 (runs), 591d774 (results tree). **These are
the study's citable numbers** (survivor-universe baseline, final by the
2026-07-20 framing decision; a CRSP/PIT version would be a separate P2b
extension). Full tables: results/tables/; figures: results/figures/.

Winsorization fix (last known lookahead closed — expanding-window causal
quantiles, exact delete-the-future invariance now test-pinned):

| P3 OOS quantity | Before | After (citable) |
|---|---|---|
| HMM Switching Sharpe / Return | 0.238 / 5.49% | **0.403 / 7.42%** |
| HMM MaxDD | -30.85% | -29.52% |
| Benchmarks (B&H/60-40/VIX/vol) | 0.640/0.482/0.199/0.256 | unchanged |
| Forecast RMSE (filt/smooth) | 0.1040/0.1032 | 0.1039/0.1030 |
| Latency (GFC/COVID/2022) | +0d/+3d/missed | unchanged |
| Crisis alpha (GFC/COVID/2022) | +52.21%/+5.07%/-9.09% | +52.21%/+5.72%/-8.95% |
| Selected K (defective BIC, 3.2 owns) | 5 | 5 |

Note the asymmetry: feature perturbation was tiny (bulk < 5e-3) but the
strategy Sharpe moved 0.165 — EM regime assignment is discontinuous, so a
few flipped rebalances compound. Recorded as a fragility flag for 3.2's
K/feature sensitivity grids. P1 and P2 reruns: every golden identical.

## 2026-07-20 · ROADMAP 2.3 — config extraction (zero number movement)

Commits: aa236c9 (loader + generated yamls), driver commit. All three
notebooks now load schema-validated config.yaml; parity verified with
freshness proofs — every golden identical, as required for pure plumbing.
Finding: P2's ticker list holds 180 names, not 200 (the [:200] slice was a
no-op); denominator claims corrected in LIMITATIONS/DESIGN/AUDIT — all
data-derived numbers unaffected. PHASE 2 COMPLETE.

## 2026-07-19 · ROADMAP 1.7 — spec reconciliation (G-5)

Commits: docs/SPEC_RECONCILIATION.md (list), 6f858a0 (edits). No numbers
changed — documents were corrected to match reality (never the reverse).
Headline corrections: P1's 'fixed historical date' universe claim (false →
survivor universe documented), FF5→FF3, PyPortfolioOpt/Qlib marked NOT USED;
P2's 'RMT beats LW/raw' Key Result replaced with the measured
indistinguishability finding; P3's 'outperforms GARCH' and '3 states' claims
corrected, hand-rolled status made precise (forward pass done+validated, rest
Phase 4.1), phantom 50-asset correlation feature marked NOT IMPLEMENTED and
AUDIT G-3 corrected. Ownership: P3-2+P3-7 → 3.2; Baum-Welch → 4.1;
GARCH → 4.2; κ-freeze → 3.2. **Phase 1 complete** (1.6(d) gated on WRDS).

## 2026-07-19 · ROADMAP 1.6 — survivorship mitigations a/b/c/e (G-3)

Commits: 624bcd1 (options memo), bce6c39 (implementation). Tests:
`tests/test_survivorship_analysis.py`. No strategy numbers changed — this
session changed CLAIMS and added measurements.

Measured selection premium (survivors-EW vs RSP, the equal-weight-factor-free
control): +392 bp/yr IS, +345 bp/yr OOS, +374 bp/yr full — roughly STABLE,
overturning the naive decay story (the vs-SPY +486→+30 bp decay was mostly
the EW factor flipping sign: RSP−SPY +94 bp IS, −315 bp OOS).

Sensitivity of the headline tie: RMT≈LW≈raw holds on near-death (spread
0.006) and smooth (0.002) cohorts and six random sub-universes; max spread
0.009 OOS Sharpe. Censoring dimension untestable without PIT data.
Full framing: docs/LIMITATIONS.md. Option (d) gated on WRDS check.

## 2026-07-19 · ROADMAP 1.5 — P1 optimizer cost honesty (P1-1, P1-2, P1-3)

Commit: 8702c01. Tests: `tests/test_p1_cost_alignment.py` (objective ==
charged cost on random trades; surrogate impact overcharge documented; true
term is DCP).

| OOS quantity | Before | After |
|---|---|---|
| Optimizer Sharpe / Return | 0.846 / 18.70% | 0.846 / 18.70% (unchanged) |
| Optimizer avg turnover | 0.0000 | 0.0000 (unchanged) |
| Optimizer total cost | 0.0 bps | 0.0 bps (unchanged) |
| Solver status (opt/mvo/min-var) | optimizer only | 227/227 optimal each, 0 fallbacks |

The zero delta IS the finding: the quadratic surrogate was never the binding
constraint. The linear hurdle — κ (50 bps regularizer) + c_prop (10 bps) per
unit turnover, every month — already exceeds any alpha the FF3 forecasts
produce, so the optimizer holds its first portfolio for 19 years. The
headline 0.846 Sharpe is a frozen ~2006 allocation that never paid a cost.
Flagged for the Phase 3 κ-sensitivity grid and 1.7 spec reconciliation;
deliberately NOT retuned in a correctness session.

## 2026-07-19 · ROADMAP 1.4 — iterative Marchenko–Pastur edge (P2-3)

Commit: 48f70c3. Tests: `tests/test_mp_edge.py` (pure noise → 0; one factor →
exactly 1; 11-factor spiked case: iterative 10/11 vs naive 7/11).

| Quantity | Naive (before) | Iterative (after) |
|---|---|---|
| σ² (demo window) | 0.578 | 0.392 |
| λ₊ (demo window) | 1.819 | 1.233 |
| Retained factors, demo window | 14 / 151 | 24 / 151 |
| Retained factors, backtest range | 11–15 | 17–42 |
| Signal variance share | 56.9% | 67.1% |

| OOS Sharpe | Before → after |
|---|---|
| RMT Hard Threshold | 0.560 → 0.579 |
| RMT Targeted Shrinkage | 0.565 → 0.579 |
| RMT Constant Residual | 0.560 → 0.579 |
| Ledoit-Wolf / Raw / EW / S&P | unchanged (0.581 / 0.580 / 0.697 / 0.634) |

The classification moved a lot (10 more real factors per window); the
portfolio barely moved — RMT is now within 0.002 Sharpe of Ledoit-Wolf and
raw sample, *strengthening* the honest RMT≈LW≈raw finding. Equal weight
still leads OOS. Provisional until G-3 (survivorship).

## 2026-07-19 · ROADMAP 1.3 — P2 min-var on covariance (P2-1, P2-2, P2-5)

Commit: c684e88. Tests: `tests/test_p2_covariance.py`. Handoff: diag reset →
Σ = D·C_clean·D; Ledoit-Wolf fits raw returns; solver statuses reported
(0/217 non-optimal, all estimators).

| OOS (2018–2024) | Sharpe before → after | Vol before → after | Return before → after |
|---|---|---|---|
| RMT Hard Threshold | 0.805 → 0.560 | 17.67% → 14.27% | 16.72% → 10.49% |
| RMT Targeted Shrinkage | 0.806 → 0.565 | 17.64% → 14.29% | 16.71% → 10.58% |
| RMT Constant Residual | 0.805 → 0.560 | 17.67% → 14.27% | 16.72% → 10.49% |
| Ledoit-Wolf Min-Var | 0.812 → 0.581 | 17.58% → 14.31% | 16.78% → 10.81% |
| Raw Sample Min-Var | 0.813 → 0.580 | 17.59% → 14.32% | 16.79% → 10.80% |
| Equal Weight (unchanged) | 0.697 | 18.15% | 15.14% |
| S&P 500 (unchanged) | 0.634 | 19.46% | 14.84% |

The honest headline moved again: true min-var minimizes variance as designed
(lowest vol and MaxDD ≈ −28% in the table) but its low-vol tilt underperformed
the 2018–2024 high-vol mega-cap era, so equal weight now leads OOS Sharpe.
The previous "min-var beats S&P" ranking was an artifact of optimizing in
equal-vol (correlation) space. RMT vs Ledoit-Wolf vs raw: still
indistinguishable (spread < 0.021 Sharpe). Provisional until G-3
(survivorship) and P2-3 (iterative MP edge).

## 2026-07-19 · ROADMAP 1.2 — P3 lookahead leaks (P3-1, P3-6)

Commits: 087c49f (P3-1), 632a44d (P3-6). Tests: `tests/test_walkforward_leaks.py`
(+ `common/hmm_filter.py`, fc42c18). Reruns isolated per fix for attribution.

### P3-1 · full-sample scaler → frozen-IS + trailing-window statistics

| OOS metric | Before | After P3-1 |
|---|---|---|
| HMM Switching Sharpe | 0.227 | 0.238 |
| HMM Switching Return | 5.31% | 5.49% |
| Regime latency (GFC / COVID / 2022) | +0d / +3d / missed | unchanged |
| Selected K (IS) | 5 (BIC = 76.2M) | 5 (BIC = 79.0M) |

The leak's practical effect was small — as AUDIT P3-1 predicted — but the
walk-forward purity claim is now true instead of false. Benchmarks unmoved.
Residual: winsorization still uses full-sample quantiles (minor; noted for 1.7).

### P3-6 · vol forecasts graded on filtered (causal) probabilities

| OOS forecast metric | Smoothed (hindsight) | Filtered (causal) |
|---|---|---|
| HMM RMSE | 0.1032 | 0.1040 |
| HMM MAE | 0.0650 | 0.0660 |
| HMM corr w/ realized | 0.4543 | 0.4427 |

Benchmarks (causal, unchanged): rolling RMSE 0.1098, EWMA 0.1038 / best MAE
0.0608, VIX best RMSE 0.0965 / best corr 0.5683. Two honest findings: (a) the
hindsight flattery gap for this model is small; (b) with or without it, the
HMM is not the best OOS vol forecaster here — VIX and EWMA win. The smoothed
row stays in the notebook, labeled, as the measured cost of hindsight.

## 2026-07-18 · G-2 fix — portfolio aggregation log → simple returns

Commits: e62ac26 (P1), 31db3ea (P2), fc39aca (P3). Test: `tests/test_return_aggregation.py`.

### P1 — Multi-Period Portfolio Optimization (OOS)

| Strategy | Return before → after | Sharpe before → after |
|---|---|---|
| Multi-Period Optimizer | 14.35% → 18.70% | 0.618 → 0.846 |
| Single-Period MVO | 11.56% → 15.17% | 0.515 → 0.722 |
| Equal Weight (1/N) | 12.44% → 16.27% | 0.566 → 0.785 |
| S&P 500 (Buy & Hold) | — → 14.84% | 0.539 → 0.634 |

Optimizer-vs-EW Sharpe gap: 0.052 → 0.061. Ranking unchanged; levels up
~200–430 bps/yr, larger for diversified portfolios (as AUDIT G-2 predicted).

### P2 — Eigenportfolios / RMT (OOS) — **ranking reversed**

| Strategy | Return before → after | Sharpe before → after |
|---|---|---|
| RMT Hard Threshold | 10.87% → 16.72% | 0.473 → 0.805 |
| Ledoit-Wolf Min-Var | 10.96% → 16.78% | 0.480 → 0.812 |
| Raw Sample Min-Var | 10.97% → 16.79% | 0.481 → 0.813 |
| Equal Weight (1/N) | 10.54% → 15.14% | 0.442 → 0.697 |
| S&P 500 (Buy & Hold) | 12.94% → 14.84% | 0.534 → 0.634 |

Before the fix, S&P 500 appeared to beat every min-var strategy OOS; after it,
every min-var strategy beats the S&P. The bug had reversed the headline
conclusion. RMT vs Ledoit-Wolf vs raw sample remain indistinguishable
(ΔSharpe < 0.01) — that honest finding is unchanged.

### P3 — HMM Regime Switching (OOS)

| Strategy | Return before → after | Sharpe before → after |
|---|---|---|
| HMM Regime Switching | 3.88% → 5.31% | 0.111 → 0.227 |
| Buy & Hold SPY | 13.05% → 14.95% | 0.539 → 0.640 |
| 60/40 Portfolio | 6.77% → 8.44% | 0.345 → 0.482 |
| VIX-Based Switching | 4.12% → 5.74% | 0.099 → 0.199 |
| Rolling Vol Switching | 5.05% → 6.62% | 0.157 → 0.256 |

Ranking unchanged: regime switching still trails buy-and-hold OOS. Crisis
windows now compounded, not summed: GFC +52.2%, COVID +5.1%, 2022 −11.0%
(HMM minus B&H).
