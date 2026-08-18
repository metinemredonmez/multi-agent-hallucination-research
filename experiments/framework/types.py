"""Core data types for multi-agent reliability experiments.

The central design commitment: a Claim carries its own provenance. Without
`origin_agent` and `hop_introduced`, propagation depth cannot be measured at
all, and a downstream agent cannot tell a peer's hypothesis from a user fact.

That distinction is the mechanism behind the adoption result in 2608.03421,
where false testimony was adopted more readily than truthful testimony.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ClaimStatus(str, Enum):
    """Verification state of a single claim."""

    VERIFIED = "verified"
    UNVERIFIED = "unverified"
    CONTRADICTED = "contradicted"
    #: The agent declined to assert. Permitting this is a design requirement:
    #: forced completion is itself a hallucination source (see 2604.23505).
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"


class Topology(str, Enum):
    """Inter-agent communication structure.

    2505.23352 found *moderately sparse* topologies optimal — they suppress
    error propagation while preserving beneficial information diffusion.
    """

    CHAIN = "chain"          # A -> B -> C, each sees all predecessors
    STAR = "star"            # supervisor fans out and collects
    MESH = "mesh"            # all-to-all (standard multi-agent debate)
    SPARSE = "sparse"        # partial connectivity
    INDEPENDENT = "independent"  # no peer visibility until aggregation


class ContextPolicy(str, Enum):
    """What an agent is allowed to see from its peers."""

    FULL_BROADCAST = "full_broadcast"    # entire transcript
    SELECTIVE = "selective"              # summarized state only
    VERIFIED_ONLY = "verified_only"      # only claims that passed verification
    ISOLATED = "isolated"                # nothing


class SeedType(str, Enum):
    """Category of deliberately injected error, for propagation studies.

    Injecting a known seed and measuring its spread is the method of 2603.04474.
    """

    FACTUAL = "factual"              # a false fact
    INSTRUCTION = "instruction"      # a misread constraint
    TOOL_OUTPUT = "tool_output"      # a wrong tool result
    STALE_STATE = "stale_state"      # outdated shared state (cf. 2606.21666)
    NONE = "none"                    # control condition


@dataclass
class Claim:
    """An atomic assertion with provenance attached."""

    text: str
    status: ClaimStatus = ClaimStatus.UNVERIFIED
    evidence_ids: list[str] = field(default_factory=list)
    confidence: float | None = None

    #: Provenance. Required for propagation metrics.
    origin_agent: str | None = None
    hop_introduced: int | None = None

    #: True if this claim is a deliberately injected error seed.
    is_seed: bool = False

    #: Ground-truth label, when the task provides one. None = unknown.
    is_correct: bool | None = None

    def is_peer_sourced(self) -> bool:
        """Peer output is a hypothesis, not ground truth."""
        return self.origin_agent is not None and self.hop_introduced is not None


@dataclass
class AgentSpec:
    """Declarative description of one agent. Provider-agnostic by design."""

    name: str
    provider: str            # "anthropic" | "openai" | "gemini" | "local" | "echo"
    model: str
    system_prompt: str = ""
    temperature: float = 0.7
    #: Marks a verifier/critic. 2603.24579 recommends deliberate information
    #: asymmetry so the verifier does not inherit the generator's premise.
    role: str = "solver"     # "solver" | "verifier" | "judge" | "dissenter"


@dataclass
class AgentOutput:
    """One agent's response at one hop."""

    agent_name: str
    hop: int
    raw_text: str
    claims: list[Claim] = field(default_factory=list)
    answer: str | None = None
    confidence: float | None = None

    # Cost accounting. 2605.00914 reported debate at 2.1-3.4x the tokens of
    # self-correction for equal or worse accuracy, so this is not optional.
    input_tokens: int = 0
    output_tokens: int = 0
    latency_s: float = 0.0

    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens


@dataclass
class RunConfig:
    """One cell of the experiment matrix."""

    agents: list[AgentSpec]
    topology: Topology = Topology.CHAIN
    context_policy: ContextPolicy = ContextPolicy.FULL_BROADCAST
    rounds: int = 1
    independent_first_pass: bool = False
    verifier: AgentSpec | None = None
    #: "none" | "terminal" | "per_transition"
    verification_schedule: str = "none"
    #: "majority" | "confidence_weighted" | "evidence_ledger"
    aggregation: str = "majority"
    seed_type: SeedType = SeedType.NONE
    seed_claim: str | None = None
    seed_at_hop: int = 0

    def label(self) -> str:
        """Stable identifier for this configuration."""
        return (
            f"{self.topology.value}"
            f"__n{len(self.agents)}"
            f"__{self.context_policy.value}"
            f"__verify-{self.verification_schedule}"
            f"__agg-{self.aggregation}"
            f"__seed-{self.seed_type.value}"
        )


@dataclass
class Trajectory:
    """Full record of one run. The unit of analysis is this, not the answer.

    2601.22984 argues end-to-end evaluation "obscures intermediate
    hallucinations that accumulate throughout the trajectory".
    """

    task_id: str
    original_goal: str
    config_label: str
    outputs: list[AgentOutput] = field(default_factory=list)
    final_answer: str | None = None
    ground_truth: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def all_claims(self) -> list[Claim]:
        return [c for o in self.outputs for c in o.claims]

    def seed_claims(self) -> list[Claim]:
        return [c for c in self.all_claims() if c.is_seed]

    def total_tokens(self) -> int:
        return sum(o.total_tokens() for o in self.outputs)

    def total_latency(self) -> float:
        return sum(o.latency_s for o in self.outputs)

    def agent_turns(self) -> int:
        return len(self.outputs)
