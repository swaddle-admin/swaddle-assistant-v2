import time
from typing import Any

import anthropic

from app.config import settings


def build_benchmark(
    start: float,
    usage: anthropic.types.Usage,
) -> dict[str, Any]:
    return {
        "latency_ms": round(
            (time.perf_counter() - start) * 1000
        ),
        "input_tokens": usage.input_tokens,
        "output_tokens": usage.output_tokens,
        "model": settings.model_name,
    }