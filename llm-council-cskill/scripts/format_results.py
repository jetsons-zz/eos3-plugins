#!/usr/bin/env python3
"""Result formatting for LLM Council deliberations."""

from typing import Dict, Any


def format_markdown(results: Dict[str, Any]) -> str:
    """Format deliberation results as markdown."""
    lines = []

    lines.append(f"# 🏛️ LLM Council Deliberation\n")
    lines.append(f"**Question**: {results['question']}\n")

    # Stage 1
    lines.append(f"## ⚙️ Stage 1: Individual Responses\n")
    for resp in results.get('stage1', []):
        lines.append(f"### {resp['model']}\n")
        lines.append(f"{resp['content']}\n")

    # Stage 2 (if present)
    if 'aggregate_rankings' in results:
        lines.append(f"## ⭐ Stage 2: Aggregate Rankings\n")
        for i, agg in enumerate(results['aggregate_rankings'], 1):
            lines.append(f"{i}. **{agg['model']}** (avg rank: {agg['avg_rank']:.2f})")

    # Stage 3
    lines.append(f"\n## 🎯 Stage 3: Final Synthesis\n")
    lines.append(f"{results['stage3']['content']}\n")

    # Metadata
    meta = results.get('metadata', {})
    lines.append(f"\n---")
    lines.append(f"Duration: {meta.get('duration_seconds', 0):.1f}s")
    lines.append(f"Confidence: {results['stage3'].get('confidence', 0)*100:.0f}%")

    return "\n".join(lines)


def format_deliberation_results(stage1, stage2, stage3):
    """Format complete deliberation results."""
    return {
        'stage1': stage1,
        'stage2': stage2,
        'stage3': stage3
    }
