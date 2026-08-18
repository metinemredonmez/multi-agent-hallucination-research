"""Reliability metrics for multi-agent trajectories.

Every metric here is defined in research/research-map.md with its source paper.
Where a metric comes from a specific paper, the arXiv ID is cited in the
docstring.

Design rule: these functions return `None` rather than a fabricated number when
the trajectory lacks the labels needed to compute them. A metric that silently
returns 0.0 for "no data" is how misleading results get published.
"""

from __future__ import annotations

from .types import Claim, Trajectory

# --------------------------------------------------------------------------
# Accuracy
# --------------------------------------------------------------------------


def factual_accuracy(traj: Trajectory) -> float | None:
    """Fraction of labelled claims that are correct.

    Returns None if no claim carries a ground-truth label.
    """
    labelled = [c for c in traj.all_claims() if c.is_correct is not None]
    if not labelled:
        return None
    return sum(1 for c in labelled if c.is_correct) / len(labelled)


def task_completion_accuracy(traj: Trajectory) -> bool | None:
    """Did the system produce the correct final answer?

    Distinct from factual accuracy: 2606.07937 observed hallucination scores
    falling while factual accuracy *also* fell, so the two must be reported
    separately.
    """
    if traj.final_answer is None or traj.ground_truth is None:
        return None
    return traj.final_answer.strip().lower() == traj.ground_truth.strip().lower()


# --------------------------------------------------------------------------
# Propagation  (2603.04474, 2608.03421, 2606.07937)
# --------------------------------------------------------------------------


def _hallucination_score(claims: list[Claim]) -> float | None:
    """Fraction of labelled claims that are incorrect."""
    labelled = [c for c in claims if c.is_correct is not None]
    if not labelled:
        return None
    return sum(1 for c in labelled if not c.is_correct) / len(labelled)


def hallucination_amplification_rate(traj: Trajectory) -> float | None:
    """Final hallucination score / initial hallucination score.

    >1 means the cascade amplified error; <1 means it attenuated.

    Source: 2606.07937, which measured 0.644 (net ATTENUATION) across 3-agent
    chains. Do not assume this metric exceeds 1 by default -- the direction is
    an empirical question, and the corpus contains both outcomes.
    """
    if not traj.outputs:
        return None
    first = _hallucination_score(traj.outputs[0].claims)
    last = _hallucination_score(traj.outputs[-1].claims)
    if first is None or last is None or first == 0:
        return None
    return last / first


def error_propagation_rate(traj: Trajectory) -> float | None:
    """P(a downstream agent restates an injected false claim).

    The adoption probability of 2608.03421, where false testimony was adopted
    *more* readily than truthful testimony.

    Uses substring containment as a deliberately crude proxy. Replace with
    entailment or claim-matching before reporting anything real.
    """
    seeds = traj.seed_claims()
    if not seeds or len(traj.outputs) < 2:
        return None

    seed_hops = {s.hop_introduced for s in seeds if s.hop_introduced is not None}
    if not seed_hops:
        return None
    earliest = min(seed_hops)
    downstream = [o for o in traj.outputs if o.hop > earliest]
    if not downstream:
        return None

    adopted = 0
    for out in downstream:
        text = out.raw_text.lower()
        if any(s.text.lower() in text for s in seeds):
            adopted += 1
    return adopted / len(downstream)


def propagation_depth(traj: Trajectory) -> int | None:
    """Number of consecutive hops an injected error survives.

    Source: 2603.04474.
    """
    seeds = traj.seed_claims()
    if not seeds:
        return None
    seed_hops = {s.hop_introduced for s in seeds if s.hop_introduced is not None}
    if not seed_hops:
        return None
    earliest = min(seed_hops)

    depth = 0
    for out in sorted(traj.outputs, key=lambda o: o.hop):
        if out.hop <= earliest:
            continue
        if any(s.text.lower() in out.raw_text.lower() for s in seeds):
            depth += 1
        else:
            break  # the chain of contamination is broken
    return depth


def recovery_rate(traj: Trajectory) -> float | None:
    """Fraction of injected seeds marked CONTRADICTED by the end of the run."""
    seeds = traj.seed_claims()
    if not seeds:
        return None
    from .types import ClaimStatus

    corrected = sum(1 for s in seeds if s.status is ClaimStatus.CONTRADICTED)
    return corrected / len(seeds)


# --------------------------------------------------------------------------
# Consensus  (2605.00914, 2602.09341)
# --------------------------------------------------------------------------


def oracle_gap(traj: Trajectory) -> float | None:
    """pass@N minus final group accuracy.

    Measures CONSENSUS COLLAPSE: a correct answer was present in the candidate
    pool and the aggregation step discarded it.

    Source: 2605.00914, which reported an oracle gap up to 32.3 percentage
    points. This is the single most diagnostic consensus metric, because it
    separates aggregation failure from generation failure.
    """
    if traj.ground_truth is None:
        return None
    gt = traj.ground_truth.strip().lower()
    answers = [o.answer.strip().lower() for o in traj.outputs if o.answer]
    if not answers:
        return None

    any_correct = 1.0 if gt in answers else 0.0
    final_correct = 1.0 if (traj.final_answer or "").strip().lower() == gt else 0.0
    return any_correct - final_correct


def false_consensus_rate(trajectories: list[Trajectory]) -> float | None:
    """Fraction of runs where agents agreed and the group was wrong."""
    usable = [t for t in trajectories if t.ground_truth and t.final_answer]
    if not usable:
        return None

    bad = 0
    for t in usable:
        answers = [o.answer.strip().lower() for o in t.outputs if o.answer]
        if not answers:
            continue
        agreed = len(set(answers)) == 1
        wrong = t.final_answer.strip().lower() != t.ground_truth.strip().lower()
        if agreed and wrong:
            bad += 1
    return bad / len(usable)


def inter_agent_error_correlation(trajectories: list[Trajectory]) -> dict | None:
    """Pairwise agreement on WHICH ITEMS each agent got wrong.

    This is the quantity behind RQ15 -- whether agents from the same foundation
    model are genuinely independent sources. 2602.09341 names the failure
    (confabulation consensus) and 2608.00243 documents it, but NO paper in this
    corpus reports the coefficient directly, despite it being cheap.

    Returns {(agent_a, agent_b): jaccard_of_error_sets}.
    """
    errors: dict[str, set[str]] = {}
    for t in trajectories:
        if t.ground_truth is None:
            continue
        gt = t.ground_truth.strip().lower()
        for o in t.outputs:
            if o.answer is None:
                continue
            if o.answer.strip().lower() != gt:
                errors.setdefault(o.agent_name, set()).add(t.task_id)

    if len(errors) < 2:
        return None

    names = sorted(errors)
    out: dict = {}
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            union = errors[a] | errors[b]
            if not union:
                continue
            out[(a, b)] = len(errors[a] & errors[b]) / len(union)
    return out or None


# --------------------------------------------------------------------------
# Drift  (2606.21666, 2601.04170)
# --------------------------------------------------------------------------


def context_divergence_score(
    traj: Trajectory,
    embed_fn=None,
) -> float | None:
    """Mean pairwise divergence between agents' stated knowledge states.

    A CDS-style metric, after 2606.21666. Requires an embedding function; the
    paper's own definition spans spatial, temporal, and task dimensions, which
    this simplification does not reproduce.

    NOT VALIDATED. CDS appears in one paper and has not been independently
    replicated -- see open-research-questions.md RQ13.
    """
    if embed_fn is None or len(traj.outputs) < 2:
        return None
    raise NotImplementedError(
        "Supply embed_fn and a cosine-distance implementation. Validate against "
        "human judgment before reporting -- see research/open-research-questions.md RQ13."
    )


def semantic_distance_from_goal(
    traj: Trajectory,
    embed_fn=None,
) -> list[float] | None:
    """Distance between the original goal and each hop's operative objective.

    This repository's proposed goal-drift metric. No corpus paper defines
    "goal drift" under that name -- the nearest sourced concept is semantic
    drift (2601.04170, simulation-based). Treat as UNVALIDATED.
    """
    if embed_fn is None:
        return None
    raise NotImplementedError(
        "Supply embed_fn. This metric is proposed, not validated -- see "
        "research/terminology.md section 6."
    )


# --------------------------------------------------------------------------
# Verification  (2606.27409, 2603.24579)
# --------------------------------------------------------------------------


def verifier_correction_rate(traj: Trajectory) -> float | None:
    """Fraction of genuinely-false claims the verifier flagged."""
    from .types import ClaimStatus

    false_claims = [c for c in traj.all_claims() if c.is_correct is False]
    if not false_claims:
        return None
    caught = sum(1 for c in false_claims if c.status is ClaimStatus.CONTRADICTED)
    return caught / len(false_claims)


def verifier_failure_rate(traj: Trajectory) -> float | None:
    """Fraction of genuinely-false claims the verifier MISSED.

    The metric for RQ9 -- the corpus's largest gap. 2603.24579 identifies
    verifier confirmation bias, where an LLM-as-judge reproduces the errors of
    the generation it checks. To study that, run this metric under two
    conditions: verifier WITH the generator's context, and verifier with
    deliberately asymmetric information.
    """
    rate = verifier_correction_rate(traj)
    return None if rate is None else 1.0 - rate


# --------------------------------------------------------------------------
# Cost  (2605.00914)
# --------------------------------------------------------------------------


def cost_summary(traj: Trajectory) -> dict:
    """Token cost, latency, and agent turns.

    Always report these next to any accuracy claim. 2605.00914 found debate
    consuming 2.1-3.4x more tokens (up to 28,631 per problem) for equal or
    worse accuracy than isolated self-correction.
    """
    return {
        "total_tokens": traj.total_tokens(),
        "input_tokens": sum(o.input_tokens for o in traj.outputs),
        "output_tokens": sum(o.output_tokens for o in traj.outputs),
        "latency_s": round(traj.total_latency(), 3),
        "agent_turns": traj.agent_turns(),
    }


def summarize(traj: Trajectory) -> dict:
    """All single-trajectory metrics. None means 'not computable', never 0."""
    return {
        "task_id": traj.task_id,
        "config": traj.config_label,
        "factual_accuracy": factual_accuracy(traj),
        "task_completion_accuracy": task_completion_accuracy(traj),
        "hallucination_amplification_rate": hallucination_amplification_rate(traj),
        "error_propagation_rate": error_propagation_rate(traj),
        "propagation_depth": propagation_depth(traj),
        "recovery_rate": recovery_rate(traj),
        "oracle_gap": oracle_gap(traj),
        "verifier_correction_rate": verifier_correction_rate(traj),
        "verifier_failure_rate": verifier_failure_rate(traj),
        **cost_summary(traj),
    }
