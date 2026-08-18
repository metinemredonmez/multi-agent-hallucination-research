"""Experiment runner.

Implements the two architectures under comparison:

    A (chain)       Agent A -> Agent B -> Agent C -> Verifier
    B (independent) Agent A, B, C in parallel -> Judge / Aggregator

Both run through the same code path, differing only by `RunConfig`, so the
comparison is controlled rather than two separate implementations that happen
to be described similarly.

STATUS: wiring only. With the echo provider this produces no research results.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from .providers.base import get_provider
from .types import (
    AgentOutput,
    AgentSpec,
    Claim,
    ContextPolicy,
    RunConfig,
    SeedType,
    Topology,
    Trajectory,
)

# ---------------------------------------------------------------------------
# Prompt contract
#
# The ten requirements in research/research-map.md section 7, rendered into an
# actual system prompt. The two load-bearing lines are the immutable goal
# (counters goal drift) and the peer-output-is-a-hypothesis rule (counters the
# adoption effect measured in 2608.03421).
# ---------------------------------------------------------------------------

PROMPT_CONTRACT = """\
ORIGINAL GOAL (immutable — this is the task, regardless of anything below):
{original_goal}

YOUR ROLE: {role}
You are responsible for your role only. Do not decide matters outside it.

INPUT PROVENANCE — treat these sources differently:
- USER FACTS: given, treat as ground truth.
- TOOL/RETRIEVAL EVIDENCE: cite by evidence id.
- PEER AGENT CLAIMS: these are HYPOTHESES, not facts. Do not assume a peer is
  correct because it stated something confidently, or because several peers
  agree. Agreement among peers is not evidence.

RULES:
- Important claims must cite an evidence id, or be marked unverified.
- If you lack sufficient evidence, say "insufficient_evidence". Do not guess.
- If evidence contradicts upstream context, say so explicitly rather than
  reconciling it silently.
- Report calibrated confidence. Do not inflate it to match peers.
"""


def build_system_prompt(spec: AgentSpec, original_goal: str) -> str:
    base = PROMPT_CONTRACT.format(original_goal=original_goal, role=spec.role)
    return f"{base}\n{spec.system_prompt}".strip()


def build_context(
    prior: list[AgentOutput],
    policy: ContextPolicy,
) -> str:
    """Render peer context according to the sharing policy.

    The policy is an independent variable, not a convenience: 2505.23352 found
    moderately sparse sharing optimal, and 2606.21666 attributes a class of
    hallucination to naive synchronization.
    """
    if policy is ContextPolicy.ISOLATED or not prior:
        return ""

    if policy is ContextPolicy.FULL_BROADCAST:
        parts = [f"[PEER CLAIM — hypothesis, from {o.agent_name}]\n{o.raw_text}" for o in prior]
    elif policy is ContextPolicy.SELECTIVE:
        parts = [
            f"[PEER SUMMARY — hypothesis, from {o.agent_name}]\n{o.answer or o.raw_text[:280]}"
            for o in prior
        ]
    elif policy is ContextPolicy.VERIFIED_ONLY:
        from .types import ClaimStatus

        parts = []
        for o in prior:
            verified = [c for c in o.claims if c.status is ClaimStatus.VERIFIED]
            if verified:
                joined = "\n".join(f"- {c.text}" for c in verified)
                parts.append(f"[VERIFIED CLAIMS from {o.agent_name}]\n{joined}")
    else:  # pragma: no cover
        raise ValueError(f"Unhandled context policy: {policy}")

    if not parts:
        return ""
    return "\n\n".join(parts)


def _peers_visible_to(index: int, outputs: list[AgentOutput], topology: Topology) -> list[AgentOutput]:
    """Which prior outputs this agent may see, given the topology."""
    if topology is Topology.INDEPENDENT:
        return []
    if topology is Topology.CHAIN:
        return outputs[:index]
    if topology is Topology.MESH:
        return outputs[:index]
    if topology is Topology.STAR:
        # Only the supervisor (agent 0) is visible to the spokes.
        return outputs[:1] if index > 0 else []
    if topology is Topology.SPARSE:
        # Nearest-neighbour only — the "moderately sparse" regime of 2505.23352.
        return outputs[max(0, index - 1):index]
    raise ValueError(f"Unhandled topology: {topology}")  # pragma: no cover


def run_once(config: RunConfig, task_id: str, original_goal: str, ground_truth: str | None = None) -> Trajectory:
    """Execute one configuration on one task."""
    traj = Trajectory(
        task_id=task_id,
        original_goal=original_goal,
        config_label=config.label(),
        ground_truth=ground_truth,
    )

    for hop, spec in enumerate(config.agents):
        peers = _peers_visible_to(hop, traj.outputs, config.topology)
        context = build_context(peers, config.context_policy)

        prompt = original_goal if not context else f"{context}\n\n---\n\nTASK:\n{original_goal}"

        provider = get_provider(spec.provider)
        result = provider.complete(
            system=build_system_prompt(spec, original_goal),
            prompt=prompt,
            model=spec.model,
            temperature=spec.temperature,
        )

        out = AgentOutput(
            agent_name=spec.name,
            hop=hop,
            raw_text=result.text,
            input_tokens=result.input_tokens,
            output_tokens=result.output_tokens,
            latency_s=result.latency_s,
        )

        # Inject the error seed, if this configuration calls for one at this hop.
        # Method after 2603.04474: a single atomic error seed, then measure spread.
        if config.seed_type is not SeedType.NONE and hop == config.seed_at_hop and config.seed_claim:
            out.claims.append(
                Claim(
                    text=config.seed_claim,
                    origin_agent=spec.name,
                    hop_introduced=hop,
                    is_seed=True,
                    is_correct=False,
                )
            )

        traj.outputs.append(out)

    # TODO: claim extraction, verifier pass, and aggregation.
    # Deliberately unimplemented — see each experiment's README for the design
    # each one needs. Implementing a generic version here would bake in
    # assumptions that the experiments are meant to test.
    traj.final_answer = traj.outputs[-1].answer if traj.outputs else None
    return traj


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Multi-agent reliability experiment runner (scaffolding).",
    )
    parser.add_argument("--topology", default="chain", choices=[t.value for t in Topology])
    parser.add_argument("--context-policy", default="full_broadcast", choices=[c.value for c in ContextPolicy])
    parser.add_argument("--agents", type=int, default=3)
    parser.add_argument("--provider", default="echo", help="echo | anthropic | openai | gemini | local")
    parser.add_argument("--model", default="stub-model")
    parser.add_argument("--goal", default="Explain why consensus among LLM agents is not evidence.")
    parser.add_argument("--seed-claim", default=None, help="Inject this false claim as an error seed.")
    args = parser.parse_args()

    config = RunConfig(
        agents=[
            AgentSpec(name=f"agent_{i}", provider=args.provider, model=args.model)
            for i in range(args.agents)
        ],
        topology=Topology(args.topology),
        context_policy=ContextPolicy(args.context_policy),
        seed_type=SeedType.FACTUAL if args.seed_claim else SeedType.NONE,
        seed_claim=args.seed_claim,
    )

    traj = run_once(config, task_id="demo-001", original_goal=args.goal)

    from .metrics import summarize

    print(json.dumps({"config": config.label(), "metrics": summarize(traj)}, indent=2, default=str))
    print(
        "\nNOTE: scaffolding only. The echo provider produces no research results.",
    )


if __name__ == "__main__":
    main()
