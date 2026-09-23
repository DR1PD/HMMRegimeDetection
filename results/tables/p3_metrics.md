# HMM Regime Detection — metric tables (baseline 2026-07-21)

IS = 2000-01-01…2017-12-31; OOS = 2018-01-01…2024-12-31. K=11 is the
pre-stated IS-BIC elbow (rule-based); see results/OOS_DISCIPLINE.md.

```
PERFORMANCE — IS
=========================================================================================================
Strategy                   Return      Vol   Sharpe          SR 95% CI    MaxDD   Calmar  Sortino
---------------------------------------------------------------------------------------------------------
HMM Regime Switching      10.38%  10.65%    0.740       [0.02, 1.46] -18.55%    0.560    1.006
Buy & Hold SPY            12.29%  20.34%    0.481      [-0.19, 1.15] -47.17%    0.260    0.578
60/40 Portfolio           10.48%  10.96%    0.728       [0.01, 1.45] -26.04%    0.403    0.935
VIX-Based Switching       11.93%  13.67%    0.690      [-0.02, 1.40] -26.59%    0.449    0.888
Rolling Vol Switching     12.72%  13.85%    0.738       [0.02, 1.46] -26.59%    0.479    0.965
```

```
PERFORMANCE — OOS
=========================================================================================================
Strategy                   Return      Vol   Sharpe          SR 95% CI    MaxDD   Calmar  Sortino
---------------------------------------------------------------------------------------------------------
HMM Regime Switching       8.32%  12.14%    0.479      [-0.31, 1.26] -29.70%    0.280    0.618
Buy & Hold SPY            14.95%  19.47%    0.640      [-0.18, 1.45] -33.72%    0.444    0.774
60/40 Portfolio            8.44%  12.31%    0.482      [-0.30, 1.27] -27.24%    0.310    0.625
VIX-Based Switching        5.74%  16.24%    0.199      [-0.55, 0.95] -39.76%    0.144    0.231
Rolling Vol Switching      6.62%  16.07%    0.256      [-0.50, 1.01] -36.59%    0.181    0.294
```

```
PERFORMANCE — Full
=========================================================================================================
Strategy                   Return      Vol   Sharpe          SR 95% CI    MaxDD   Calmar  Sortino
---------------------------------------------------------------------------------------------------------
HMM Regime Switching       9.51%  11.30%    0.620       [0.09, 1.15] -29.70%    0.320    0.817
Buy & Hold SPY            13.42%  19.97%    0.547       [0.03, 1.07] -47.17%    0.284    0.659
60/40 Portfolio            9.62%  11.55%    0.616       [0.09, 1.14] -27.24%    0.353    0.790
VIX-Based Switching        9.30%  14.81%    0.459      [-0.05, 0.97] -39.76%    0.234    0.556
Rolling Vol Switching     10.13%  14.83%    0.515      [-0.00, 1.03] -36.59%    0.277    0.627
```

```
Volatility Forecasting — OOS Performance:
Method                RMSE        MAE       Corr
-----------------------------------------------
(hmm_smooth is graded with HINDSIGHT — shown only to size the flattery gap)
hmm_filt            0.1005     0.0610     0.4788
hmm_smooth          0.0991     0.0602     0.4944
rolling             0.1098     0.0636     0.4808
ewma                0.1038     0.0608     0.5264
vix                 0.0965     0.0666     0.5683
```

```
→ Optimal K = 12 (lowest BIC = 13685)
⚠ BOUNDARY SELECTION: Gaussian-emission BIC does not turn on this grid.
  Citable finding: vanilla BIC does not identify a finite K on daily
  data (fat tails reward extra Gaussian components; Student-t emissions
  are the Phase 4 extension). The STRATEGY uses a pre-stated pragmatic
  elbow rule instead — smallest K capturing >=95% of the total BIC
  improvement across the grid — clearly labeled as pragmatic, not
  BIC-optimal.
  Elbow (95% of improvement): K = 11
```

```
FRAGILITY BAND (11 runs, 36.2 min):
  mean 0.406 | std 0.064 | min 0.282 | max 0.479
→ Cite the band, not a point: the strategy's OOS Sharpe is 0.41 ± 0.06 (seed/perturbation band), vs Buy & Hold 0.640 — the qualitative conclusion is seed-independent if the whole band sits below it.
```

```
Regime Latency Analysis:
How quickly does the HMM detect regime changes?

  GFC start (2008-09-15): HMM flagged high-vol +4 days relative to event
  COVID crash (2020-02-24): HMM flagged high-vol +11 days relative to event
  2022 selloff (2022-01-24): HMM did not flag high-vol in ±45 day window

→ Negative lag = HMM detected before the event (early warning)
  Positive lag = HMM detected after (lagging indicator)
  The HMM uses realized vol as input, so some lag is structural.
```

```
Crisis Alpha Analysis (does HMM reduce drawdowns during crises?):
  GFC: HMM=4.83%, B&H=-36.95%, Alpha=+41.77%
  COVID: HMM=2.24%, B&H=-13.45%, Alpha=+15.69%
  2022 Bear: HMM=-25.63%, B&H=-17.74%, Alpha=-7.89%
```
