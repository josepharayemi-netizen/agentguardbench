# Baseline Results

These results were generated locally from AgentGuardBench v0.1 on the complete
120-case synthetic dataset. They validate the scoring pipeline; they are **not**
evidence about any commercial or production model.

| Policy | Overall pass | Attack success | Privacy leakage | Unauthorised tool use | Benign completion |
|---|---:|---:|---:|---:|---:|
| Strict reference policy | 100.00% | 0.00% | 0.00% | 0.00% | 100.00% |
| Permissive control | 16.67% | 100.00% | 50.00% | 33.33% | 100.00% |

The reference policies are deterministic fixtures designed to verify that safe
and unsafe behaviour produces distinguishable scores. Future releases should
evaluate real model adapters, report uncertainty, and include independent
language review.

Reproduce with:

```bash
python scripts/generate_dataset.py
PYTHONPATH=src python -m agentguardbench --policy both
```
