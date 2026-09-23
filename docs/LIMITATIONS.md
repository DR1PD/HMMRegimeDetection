# Limitations

Living document, seeded by ROADMAP 1.6 (G-3). Each limitation states what is
affected, what was measured, what was mitigated, and what the correct fix is.

## 1 · Survivorship / selection in the equity universes (G-3)

**Design fact.** P1 (50 names) and P2 (200 names) use 2024-era large caps
traded back to 2005. Two filters: *selection* (chosen because they became
large) and *censoring* (the dead and delisted are absent — Yahoo carries no
usable history for most casualties). Realized universes: P1 46/50, P2 151 names.
*[CORRECTION 2026-07-20 (found generating config.yaml): P2's hand-picked
list contains 180 tickers, not the designed 200 — the `[:200]` slice was
always a no-op. True funnel: 180 targeted → 172 with Yahoo data (8 failed,
not 28) → 151 after cleaning. The q = 0.599 realized value and every
data-derived number are unaffected; only the denominator claims were wrong.]*
P2's core parameter sits at q = 0.599 vs the 0.79 design premise.

**Population reframe (mitigation a).** All results are estimates for the
population *"firms that became and remained large-cap through 2024"*, not the
investable 2005 opportunity set. Notebook headers say so explicitly.

**Measured selection premium (mitigation b).** Survivors-EW vs investable
benchmarks, annualized (P2 §16.1):

| Period | Survivors EW | SPY | RSP | vs SPY | vs RSP |
|---|---|---|---|---|---|
| IS 2005–2017 | 14.72% | 9.86% | 10.80% | +486 bp | +392 bp |
| OOS 2018–2024 | 15.14% | 14.84% | 11.69% | +30 bp | +345 bp |
| Full | 14.88% | 11.79% | 11.15% | +310 bp | +374 bp |

The vs-RSP column strips the equal-weight factor and is the cleanest free
measure of selection: **≈ +350–390 bp/yr, roughly stable across periods** —
it does *not* decay, because the 2024-selected winners did much of their
winning in 2018–2024. The naive "foreknowledge decays" story (visible in the
vs-SPY column, +486 → +30 bp) is mostly the equal-weight factor flipping sign
(RSP−SPY: +94 bp IS, −315 bp OOS). Interpretation: every long-only level in
P1/P2 carries an order-of-350-bp/yr selection inflation; strategy *rankings*
within the shared universe are less affected but not immune.

**Censoring, unmeasurable here.** The 2008 casualties are precisely the
extreme-vol/correlation observations. Consequences we cannot quantify with
free data: crisis-window eigenvalue spectra are too calm; min-var's GFC-era
drawdown (−28%) is a survivors-only number (2007's low-vol cohort included
the banks that died — a real min-var would have held them); levels miss
delisting returns (average ≈ −30% for performance delistings, Shumway 1997).

**Sensitivity of the headline finding (mitigation c).** The RMT ≈ Ledoit-Wolf
≈ raw-sample tie was rerun on survival-profile cohorts — near-death survivors
(76 names with worse-than-median max drawdown; threshold −61%; 82 of 151
names drew down ≥60% at some point) vs smooth survivors (75) — and on six
random sub-universes (n = 50, 100). **Max OOS Sharpe spread across all eight
subsets: 0.009.** The tie is robust to the composition dimension of
survivorship. [EXTENDED 2026-07-21 (3.2): also robust across the (T, n)
design space — 15-cell window×universe grid, q 0.099–1.198 incl. the design
target 0.794 and the singular q>1 corner; max spread 0.023. See
results/tables/p2_window_universe_grid.md.] It remains untested against true
censoring (dead names), which requires point-in-time data.

**Literature anchors (mitigation e).** Fund-universe survivorship ≈ 0.9%/yr
(Carhart 1997; Elton–Gruber–Blake 1996); delisting returns ≈ −30% average
for performance delistings (Shumway 1997); delisting bias concentrated in
small caps (Shumway & Warther 1999). Our measured ≈ +350–390 bp/yr sits well
above the fund number, consistent with hand-picking index winners rather
than sampling a fund universe.

**The correct fix, and its status — FRAMING DECIDED 2026-07-20 (David).**
The survivor universe is the FINAL BASELINE for this study: results are and
remain estimates for the survivor population, with the measured ≈ +350–390
bp/yr selection premium as their disclosed context. A CRSP/point-in-time
version — if WRDS access comes through — becomes a separate **P2b extension**
(new universe, new baseline, cross-referenced results), NOT a re-baseline of
this study. This converts the data limitation into a fixed, documented scope
boundary; the free half-measure (2005-fixed membership) is retired as
superseded by that framing.

## 2 · Other standing limitations (pointers)

- ~~P1's optimizer freeze~~ MEASURED AND RESOLVED AS A FINDING 2026-07-21
  (3.2): the freeze boundary is exactly κ*=0.005 at every γ; trading cells
  below it don't beat equal-weight net OOS (2/12, within noise), and even
  IS selection picks a frozen cell. Near-zero trading is the optimizer's
  correct policy at this forecast quality — the multi-period machinery is
  demonstrated, and its optimal use here is restraint.
- ~~P3's winsorization~~ FIXED 2026-07-20 (3.1): causal expanding-window
  quantiles; exact delete-the-future invariance test-pinned. The regime-
  latency analysis still reads smoothed probabilities (revisit with 4.1).
- P3's HMM strategy Sharpe is FRAGILE — now measured (3.2): OOS Sharpe band
  0.406 ± 0.064, range [0.282, 0.479] across 8 EM seeds + 3 feature
  perturbations at K=11. Cite the band, never a point (the single-run point,
  0.479, sits at the band maximum). Whole band < B&H 0.640.
- ~~P3's K selection~~ RESOLVED AS A FINDING 2026-07-20 (3.2): corrected BIC
  never turns through K=12 — Gaussian-emission BIC does not identify finite
  K on daily data. Strategy K=11 is a labeled pragmatic elbow choice.
  Credible counting needs Student-t emissions (Phase 4).
- Yahoo Finance adjusted prices mutate over time; all results are pinned to
  the parquet snapshots in `data/` (see decision log 2026-07-18).
