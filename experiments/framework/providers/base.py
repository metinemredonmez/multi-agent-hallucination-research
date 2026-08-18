"""Provider abstraction.

Every model backend implements `LLMProvider`. The runner never imports an SDK
directly, so swapping Anthropic for a local model changes one config line.

This matters for the research, not just the engineering: model heterogeneity is
the most consistently supported intervention in the corpus (2502.08788 calls it
a "universal antidote"), so mixing providers inside one run must be trivial.
"""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class CompletionResult:
    text: str
    input_tokens: int = 0
    output_tokens: int = 0
    latency_s: float = 0.0


class LLMProvider(ABC):
    """Interface every backend must satisfy."""

    name: str = "base"

    @abstractmethod
    def complete(
        self,
        *,
        system: str,
        prompt: str,
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> CompletionResult:
        """Return a single completion. Implementations must fill in token counts."""
        raise NotImplementedError


class EchoProvider(LLMProvider):
    """Deterministic no-network provider for testing the wiring.

    Returns a canned string. Useful for verifying topology, context policy, and
    metric plumbing without spending tokens. Produces NO research results.
    """

    name = "echo"

    def complete(
        self,
        *,
        system: str,
        prompt: str,
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> CompletionResult:
        t0 = time.perf_counter()
        text = f"[echo:{model}] received {len(prompt)} chars of prompt"
        return CompletionResult(
            text=text,
            input_tokens=len(system) + len(prompt),
            output_tokens=len(text),
            latency_s=time.perf_counter() - t0,
        )


_REGISTRY: dict[str, type[LLMProvider]] = {"echo": EchoProvider}


def register(name: str, cls: type[LLMProvider]) -> None:
    _REGISTRY[name] = cls


def get_provider(name: str) -> LLMProvider:
    """Instantiate a provider by name.

    Real adapters are stubs until you add them - see providers/README.md.
    """
    if name not in _REGISTRY:
        raise ValueError(
            f"Unknown provider {name!r}. Registered: {sorted(_REGISTRY)}. "
            "Add an adapter in experiments/framework/providers/ and call register()."
        )
    return _REGISTRY[name]()
