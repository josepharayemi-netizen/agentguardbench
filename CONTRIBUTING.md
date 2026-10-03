# Contributing

Contributions that improve test coverage, add safely constructed scenarios, or
extend evaluation adapters are welcome.

## Development setup

```bash
python -m pip install -e .
python scripts/generate_dataset.py
python -m unittest discover -s tests -v
agentguardbench --policy both
```

## Scenario requirements

New scenarios must:

- avoid real personal data, credentials, malware, and live exploit instructions;
- identify language, sector, risk category, expected action, and standards mapping;
- include a short rationale that a reviewer can audit;
- preserve balanced coverage or document why the distribution changes.

Open an issue before making a major schema or scoring change. Pull requests
should include tests and an explanation of any change to benchmark results.
