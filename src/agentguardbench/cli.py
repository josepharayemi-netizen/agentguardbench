from __future__ import annotations

import argparse
import json
from pathlib import Path

from .evaluator import evaluate, load_scenarios, summarise, write_results


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run AgentGuardBench.")
    parser.add_argument("--dataset", default="data/scenarios.jsonl")
    parser.add_argument("--policy", choices=("strict", "permissive", "both"), default="both")
    parser.add_argument("--output", default="results")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    scenarios = load_scenarios(Path(args.dataset))
    policies = ("strict", "permissive") if args.policy == "both" else (args.policy,)
    summaries = []
    for policy in policies:
        results = evaluate(scenarios, policy)
        write_results(results, args.output)
        summaries.append(summarise(results))
    print(json.dumps(summaries, indent=2))
    return 0

