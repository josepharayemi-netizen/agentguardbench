# Dataset Card

## Summary

AgentGuardBench v0.1 is a synthetic evaluation dataset for tool-using AI agents. It contains 120 cases generated from transparent templates across six categories, five sectors, and four languages: English, French, Swahili, and Yoruba.

## Intended uses

- Defensive security testing
- Responsible-AI evaluation
- Policy and guardrail comparison
- Classroom and reproducibility exercises

## Prohibited uses

- Unauthorised penetration testing
- Training systems to exfiltrate data or evade controls
- Claims of legal compliance based only on benchmark scores

## Limitations

The initial prompts are template-based. French, Swahili, and Yoruba text should receive independent native-speaker review before the dataset is used for cross-language research claims. The deterministic baseline is not a substitute for evaluating production models. Results should not be generalised beyond the tested configuration.

## Privacy

All data is synthetic. Email domains use `.test`, secrets are explicitly marked as demonstrations, and no real individual is represented.
