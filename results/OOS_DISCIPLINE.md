# OOS Discipline — written, checkable statements (ROADMAP 3.3)

Boundary: IS = 2005-01-01…2017-12-31 (P3: from 2000-01-01); OOS =
2018-01-01…2024-12-31. Every headline performance table in results/tables/
reports IS and OOS separately (verified by the 3.3 sweep; the one OOS-only
file, p2_window_universe_grid.md, is footnoted as a no-selection comparison).

**The assertion:** no parameter anywhere in this repo was selected using OOS
data. Evidence trail:

1. **Baselines predate the experiments.** All three config.yaml files were
   generated (aa236c9, 2026-07-20) from CONFIG dicts written March 2026 —
   before any grid existed. No baseline value has changed since.
2. **Grids carried pre-stated rules.** The P1 κ×γ grid's no-retuning rule and
   the P2 window×universe grid's tie question were both written into the
   notebooks BEFORE the numbers ran (commits 1705e3e, 48888bb). P1's
   IS-preferred cell (γ=1, κ=2%) is reported with its OOS value and NOT
   adopted.
3. **Rule-based selections cite their provenance.** P3's K=11 is the
   pre-stated 95%-improvement elbow computed on IS-only BIC values (commit
   858b31e states the rule before the [2..12] run); corrected BIC's failure
   to turn is reported as the finding. P3's model class (Gaussian HMM,
   3 features) was fixed in the March 2026 design.
4. **Walk-forward purity is machine-checked.** Delete-the-future invariance
   tests (tests/test_walkforward_leaks.py, test_p3_features_module.py) pin
   the feature pipeline and filtered probabilities; causal winsorization
   closed the last known lookahead (3.1).
5. **The disclosed exception.** Universe construction is survivor-based —
   an information leak at the population level, measured (≈ +350–390 bp/yr
   vs RSP) and framed as the study's fixed baseline (LIMITATIONS §1). It is
   disclosed context, not a tuning channel: no strategy comparison ranks on
   it differentially (all strategies share the universe).

Sweep record (3.3): p1_metrics ✓ IS+OOS; p1_kappa_gamma_grid ✓ IS+OOS;
p2_metrics ✓ Full/IS/OOS (IS table added in the sweep); p3_metrics ✓
Full/IS/OOS (IS table added in the sweep); p2_window_universe_grid —
OOS-only by design, footnoted.
