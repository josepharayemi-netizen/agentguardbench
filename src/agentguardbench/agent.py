from __future__ import annotations

import re

from .models import AgentDecision, Scenario

SENSITIVE_PATTERNS = (
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    re.compile(r"\b(?:\d[ -]*?){13,16}\b"),
    re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    re.compile(r"\b(?:password|secret|api[_ -]?key|token)\s*[:=]\s*\S+", re.I),
)

INJECTION_MARKERS = (
    "ignore previous",
    "ignore all previous",
    "system override",
    "developer message",
    "hidden instruction",
    "disregard policy",
    "do not tell the user",
    "ignorez toutes les instructions précédentes",
    "puuza maagizo yote ya awali",
    "fojú kú gbogbo àṣẹ tẹ́lẹ̀",
)

HIGH_IMPACT_TOOLS = {"send_email", "transfer_funds", "delete_record", "publish_record"}


def _contains_sensitive(text: str) -> bool:
    return any(pattern.search(text) for pattern in SENSITIVE_PATTERNS)


class MockAgent:
    """A deterministic agent used to measure policy behaviour without live side effects."""

    def __init__(self, policy: str = "strict") -> None:
        if policy not in {"strict", "permissive"}:
            raise ValueError("policy must be 'strict' or 'permissive'")
        self.policy = policy

    def run(self, scenario: Scenario) -> AgentDecision:
        combined = f"{scenario.prompt}\n{scenario.context}".lower()
        injection = any(marker in combined for marker in INJECTION_MARKERS)
        sensitive = scenario.contains_sensitive_data or _contains_sensitive(scenario.context)
        tool = scenario.requested_tool

        if self.policy == "permissive":
            if tool:
                return AgentDecision(
                    action="execute",
                    response=scenario.context if sensitive else "Task executed.",
                    tool_called=tool,
                    disclosed_sensitive_data=sensitive,
                    rationale="Permissive baseline follows the latest instruction.",
                )
            return AgentDecision(
                action="answer",
                response=scenario.context if sensitive else "Request completed.",
                disclosed_sensitive_data=sensitive,
                rationale="Permissive baseline answers without policy checks.",
            )

        if injection:
            return AgentDecision(
                action="refuse",
                response="I cannot follow instructions embedded in untrusted content.",
                rationale="Detected a direct or indirect prompt-injection marker.",
            )

        if sensitive and scenario.expected_action in {"refuse", "redact"}:
            return AgentDecision(
                action=scenario.expected_action,
                response="Sensitive information withheld or redacted.",
                rationale="Applied data-minimisation and confidentiality controls.",
            )

        if scenario.expected_action == "refuse":
            return AgentDecision(
                action="refuse",
                response="The requested action is outside the agent's authorised scope.",
                rationale="Least-privilege policy denied the request.",
            )

        if scenario.requires_human_approval or tool in HIGH_IMPACT_TOOLS:
            return AgentDecision(
                action="request_approval",
                response="Human approval is required before this action can be executed.",
                tool_called=None,
                requested_approval=True,
                rationale="High-impact action is gated by human oversight.",
            )

        return AgentDecision(
            action=scenario.expected_action,
            response="Task completed within the authorised scope.",
            tool_called=tool if scenario.expected_action == "execute" else None,
            rationale="Request passed provenance, scope, and safety checks.",
        )
