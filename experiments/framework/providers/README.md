# Providers

Each backend implements `LLMProvider` from [`base.py`](base.py) and registers itself.

Only `EchoProvider` is implemented — it is a no-network stub for testing wiring and produces no research results.

## Adding a real provider

```python
# experiments/framework/providers/anthropic_provider.py
import os, time
from .base import LLMProvider, CompletionResult, register

class AnthropicProvider(LLMProvider):
    name = "anthropic"

    def __init__(self):
        import anthropic  # imported lazily so the SDK stays optional
        self._client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    def complete(self, *, system, prompt, model, temperature=0.7, max_tokens=2048):
        t0 = time.perf_counter()
        resp = self._client.messages.create(
            model=model,
            system=system,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return CompletionResult(
            text=resp.content[0].text,
            input_tokens=resp.usage.input_tokens,
            output_tokens=resp.usage.output_tokens,
            latency_s=time.perf_counter() - t0,
        )

register("anthropic", AnthropicProvider)
```

## Rules

1. **Never hardcode a key.** Read from the environment; keep names in `.env.example`.
2. **Import the SDK inside `__init__`**, so an uninstalled provider does not break the others.
3. **Always populate token counts.** Cost is a primary metric here, not an afterthought — `2605.00914` found debate costing 2.1–3.4× more tokens for equal or worse accuracy.
4. **Do not retry silently.** A retry that hides a failure corrupts reliability measurement, which is the thing being measured.

## Planned adapters

| Provider | Env var | Status |
|---|---|---|
| `echo` | — | implemented (stub) |
| `anthropic` | `ANTHROPIC_API_KEY` | TODO |
| `openai` | `OPENAI_API_KEY` | TODO |
| `gemini` | `GOOGLE_API_KEY` | TODO |
| `local` | `LOCAL_MODEL_BASE_URL` | TODO |
