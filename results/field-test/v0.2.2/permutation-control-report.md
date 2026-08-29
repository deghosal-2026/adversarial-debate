# Permutation Control Report (v0.2.2)

Rows: 3440 | Shuffles: 500 | Seed: 42

| Metric | Real (LLM) | Real (deterministic) | Null mean | Null std | 95% CI | Z-score |
|--------|-----------|---------------------|-----------|----------|--------|---------|
| Match rate | 0.874 | 0.072 | 0.003 | 0.001 | 0.001-0.005 | 77.8 |
| Partial rate | 0.126 | 0.217 | 0.034 | 0.003 | 0.029-0.041 | - |
| No_match rate | 0.000 | 0.710 | 0.963 | 0.003 | 0.956-0.968 | - |

## Interpretation

The null distribution (vocabulary overlap alone) has a mean match rate of 0.3% (95% CI: 0.1%-0.5%).
This is the corpus-specific vocabulary floor.

The real LLM match rate (87.4%) sits 77.8 standard
deviations above this floor. The matcher is discriminating well.