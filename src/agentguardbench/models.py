from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class Scenario:
    id: str
    category: str
    sector: str
    language: str
    prompt: str
    context: str
    requested_tool: str | None
    expected_action: str
    contains_sensitive_data: bool
    requires_human_approval: bool
    severity: str
    standard_refs: tuple[str, ...]

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "Scenario":
        value = dict(value)
        value["standard_refs"] = tuple(value.get("standard_refs", ()))
        return cls(**value)


@dataclass(frozen=True)
class AgentDecision:
    action: str
    response: str
    tool_called: str | None = None
    disclosed_sensitive_data: bool = False
    requested_approval: bool = False
    rationale: str = ""


@dataclass(frozen=True)
class Evaluation:
    scenario_id: str
    policy: str
    category: str
    sector: str
    language: str
    expected_action: str
    actual_action: str
    passed: bool
    attack_succeeded: bool
    privacy_leak: bool
    unauthorized_tool_use: bool
    approval_violation: bool
    benign_task_completed: bool
    rationale: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

