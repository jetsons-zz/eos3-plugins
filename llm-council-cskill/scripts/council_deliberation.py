#!/usr/bin/env python3
"""
LLM Council Deliberation - Core orchestration script.

Implements the 3-stage multi-model deliberation process:
- Stage 1: Individual responses from multiple models
- Stage 2: Anonymous peer ranking
- Stage 3: Chairman synthesis

Usage:
    python council_deliberation.py --question "Your question here"
    python council_deliberation.py --question "Compare X vs Y" --mode quick
"""

import asyncio
import json
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import os

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from openrouter_client import query_model, query_models_parallel
    from format_results import format_deliberation_results, format_markdown
    from utils.config_manager import load_config, validate_api_key, get_council_models, get_chairman_model
    from utils.validators import validate_question, validate_model_list
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all required modules are in the scripts directory")
    sys.exit(1)


async def stage1_collect_responses(
    question: str,
    models: List[str]
) -> List[Dict[str, Any]]:
    """
    Stage 1: Collect individual responses from all council models.

    Args:
        question: The question to deliberate on
        models: List of OpenRouter model identifiers

    Returns:
        List of response dicts with 'model' and 'content' keys
    """
    print(f"\n⚙️  Stage 1: Collecting responses from {len(models)} models...")

    messages = [
        {
            "role": "system",
            "content": "You are participating in a multi-model council deliberation. Provide your independent analysis and perspective on the question."
        },
        {
            "role": "user",
            "content": question
        }
    ]

    # Query all models in parallel
    results = await query_models_parallel(models, messages)

    # Format responses
    responses = []
    for model, response in results.items():
        if response and response.get('content'):
            responses.append({
                'model': model,
                'content': response['content'],
                'reasoning': response.get('reasoning_details')
            })
            print(f"  ✓ {model}: {len(response['content'])} chars")
        else:
            print(f"  ✗ {model}: Failed")

    if len(responses) < 2:
        raise ValueError(f"Need at least 2 successful responses, got {len(responses)}")

    print(f"\n✅ Stage 1 complete: {len(responses)}/{len(models)} models responded")
    return responses


async def stage2_collect_rankings(
    question: str,
    responses: List[Dict[str, Any]],
    models: List[str]
) -> Tuple[List[Dict[str, Any]], Dict[str, str]]:
    """
    Stage 2: Collect anonymous peer rankings from all models.

    Responses are anonymized as "Response A", "Response B", etc.
    Each model ranks all responses (including its own, anonymized).

    Args:
        question: Original question
        responses: Stage 1 responses
        models: List of model identifiers

    Returns:
        Tuple of (rankings_list, label_to_model_mapping)
    """
    print(f"\n⭐ Stage 2: Collecting anonymous peer rankings...")

    # Create anonymized responses
    labels = [f"Response {chr(65+i)}" for i in range(len(responses))]
    label_to_model = {label: resp['model'] for label, resp in zip(labels, responses)}

    # Create ranking prompt
    anonymized_text = "\n\n".join([
        f"{label}:\n{resp['content']}"
        for label, resp in zip(labels, responses)
    ])

    ranking_prompt = f"""You are evaluating responses to this question:

Question: {question}

Here are the anonymized responses:

{anonymized_text}

Evaluate each response based on:
- Accuracy and correctness
- Depth of analysis
- Practical value
- Clarity of explanation

Provide your ranking in this EXACT format:

EVALUATION:
[Your evaluation of each response]

FINAL RANKING:
1. Response X
2. Response Y
3. Response Z
...

Use only the response labels (Response A, Response B, etc.) in your ranking.
"""

    messages = [
        {
            "role": "system",
            "content": "You are a neutral evaluator in a peer review process. Rank the responses objectively based on quality."
        },
        {
            "role": "user",
            "content": ranking_prompt
        }
    ]

    # Query all models for rankings
    ranking_results = await query_models_parallel(models, messages)

    # Parse rankings
    rankings = []
    for model, result in ranking_results.items():
        if result and result.get('content'):
            ranking_text = result['content']
            parsed_ranking = parse_ranking(ranking_text, labels)

            rankings.append({
                'model': model,
                'ranking': parsed_ranking,
                'evaluation': ranking_text
            })
            print(f"  ✓ {model}: Ranked {len(parsed_ranking)} responses")
        else:
            print(f"  ✗ {model}: Failed to rank")

    print(f"\n✅ Stage 2 complete: {len(rankings)}/{len(models)} models provided rankings")
    return rankings, label_to_model


def parse_ranking(text: str, valid_labels: List[str]) -> List[str]:
    """
    Parse ranking from model response.

    Looks for "FINAL RANKING:" section and extracts ordered list.
    Falls back to regex if strict parsing fails.

    Args:
        text: Model's ranking response
        valid_labels: Valid response labels (e.g., ["Response A", "Response B"])

    Returns:
        Ordered list of response labels (best to worst)
    """
    import re

    # Try to find FINAL RANKING section
    if "FINAL RANKING:" in text:
        section = text.split("FINAL RANKING:")[1]
        lines = section.strip().split("\n")

        ranking = []
        for line in lines:
            # Extract "Response X" from lines like "1. Response X"
            for label in valid_labels:
                if label in line:
                    if label not in ranking:  # Avoid duplicates
                        ranking.append(label)
                    break

        if ranking:
            return ranking

    # Fallback: Extract any mention of response labels in order
    ranking = []
    for label in valid_labels:
        if label in text:
            ranking.append(label)

    return ranking


def calculate_aggregate_rankings(
    rankings: List[Dict[str, Any]],
    label_to_model: Dict[str, str]
) -> List[Dict[str, Any]]:
    """
    Calculate aggregate rankings from all peer evaluations.

    Each position gets a score (1st place = 1 point, 2nd = 2 points, etc.)
    Lower average score = better ranking.

    Args:
        rankings: List of ranking dicts from Stage 2
        label_to_model: Mapping of labels to model names

    Returns:
        Sorted list of aggregate ranking results
    """
    from collections import defaultdict

    # Accumulate scores for each response
    scores = defaultdict(list)

    for ranking_dict in rankings:
        ranking_list = ranking_dict['ranking']
        for position, label in enumerate(ranking_list, start=1):
            scores[label].append(position)

    # Calculate averages
    aggregates = []
    for label, position_list in scores.items():
        avg_position = sum(position_list) / len(position_list)
        aggregates.append({
            'label': label,
            'model': label_to_model[label],
            'avg_rank': avg_position,
            'votes': len(position_list)
        })

    # Sort by average rank (lower is better)
    aggregates.sort(key=lambda x: x['avg_rank'])

    return aggregates


async def stage3_synthesize(
    question: str,
    responses: List[Dict[str, Any]],
    rankings: List[Dict[str, Any]],
    aggregate_rankings: List[Dict[str, Any]],
    chairman_model: str
) -> Dict[str, Any]:
    """
    Stage 3: Chairman synthesizes final answer from all responses and rankings.

    Args:
        question: Original question
        responses: Stage 1 responses
        rankings: Stage 2 rankings
        aggregate_rankings: Calculated aggregate rankings
        chairman_model: Chairman model identifier

    Returns:
        Synthesis dict with 'content' and 'confidence'
    """
    print(f"\n🎯 Stage 3: Chairman synthesis ({chairman_model})...")

    # Build synthesis prompt
    responses_text = "\n\n".join([
        f"{resp['model']}:\n{resp['content']}"
        for resp in responses
    ])

    rankings_text = "\n".join([
        f"{i+1}. {agg['model']} (avg rank: {agg['avg_rank']:.2f})"
        for i, agg in enumerate(aggregate_rankings)
    ])

    synthesis_prompt = f"""You are the chairman of a multi-model AI council. Your role is to synthesize the best final answer from the diverse perspectives provided.

Original Question:
{question}

Council Member Responses:
{responses_text}

Aggregate Quality Rankings (from peer review):
{rankings_text}

Your task:
1. Analyze all responses objectively
2. Identify common themes and disagreements
3. Synthesize the best insights from multiple perspectives
4. Provide a clear, actionable final recommendation
5. Note any important caveats or trade-offs
6. Indicate your confidence level (0-100%)

Provide your synthesis in this format:

SYNTHESIS:
[Your comprehensive final answer]

CONFIDENCE: [0-100]%
"""

    messages = [
        {
            "role": "system",
            "content": "You are an expert chairman synthesizing insights from a multi-model council deliberation."
        },
        {
            "role": "user",
            "content": synthesis_prompt
        }
    ]

    result = await query_model(chairman_model, messages, timeout=120)

    if not result or not result.get('content'):
        raise ValueError("Chairman synthesis failed")

    synthesis_text = result['content']

    # Extract confidence if present
    confidence = 0.85  # Default
    if "CONFIDENCE:" in synthesis_text:
        import re
        match = re.search(r'CONFIDENCE:\s*(\d+)%?', synthesis_text)
        if match:
            confidence = int(match.group(1)) / 100.0

    print(f"  ✓ Synthesis complete ({len(synthesis_text)} chars, {confidence*100:.0f}% confidence)")

    return {
        'content': synthesis_text,
        'confidence': confidence
    }


async def run_full_deliberation(
    question: str,
    models: Optional[List[str]] = None,
    chairman: Optional[str] = None
) -> Dict[str, Any]:
    """
    Run complete 3-stage deliberation process.

    Args:
        question: Question to deliberate on
        models: Council models (None = use config defaults)
        chairman: Chairman model (None = use config default)

    Returns:
        Complete deliberation results with all stages and metadata
    """
    start_time = datetime.now()

    # Load config
    config = load_config()
    models = models or get_council_models(config)
    chairman = chairman or get_chairman_model(config)

    # Validate
    validate_api_key()
    validate_question(question)
    validate_model_list(models)

    print(f"\n{'='*70}")
    print(f"LLM COUNCIL DELIBERATION")
    print(f"{'='*70}")
    print(f"\n📋 Question: {question}")
    print(f"\n👥 Council: {len(models)} models")
    print(f"🎩 Chairman: {chairman}")

    try:
        # Stage 1: Individual responses
        stage1_responses = await stage1_collect_responses(question, models)

        # Stage 2: Peer rankings
        stage2_rankings, label_to_model = await stage2_collect_rankings(
            question, stage1_responses, models
        )

        # Calculate aggregate rankings
        aggregate_rankings = calculate_aggregate_rankings(
            stage2_rankings, label_to_model
        )

        # Stage 3: Synthesis
        stage3_synthesis = await stage3_synthesize(
            question, stage1_responses, stage2_rankings,
            aggregate_rankings, chairman
        )

        # Calculate metadata
        duration = (datetime.now() - start_time).total_seconds()

        results = {
            'question': question,
            'stage1': stage1_responses,
            'stage2': stage2_rankings,
            'aggregate_rankings': aggregate_rankings,
            'stage3': stage3_synthesis,
            'metadata': {
                'duration_seconds': duration,
                'models_used': len(stage1_responses),
                'chairman_model': chairman,
                'timestamp': datetime.now().isoformat()
            }
        }

        print(f"\n{'='*70}")
        print(f"✅ DELIBERATION COMPLETE")
        print(f"{'='*70}")
        print(f"Duration: {duration:.1f}s")
        print(f"Models participated: {len(stage1_responses)}/{len(models)}")
        print(f"Confidence: {stage3_synthesis['confidence']*100:.0f}%")

        return results

    except Exception as e:
        print(f"\n❌ Deliberation failed: {e}")
        import traceback
        traceback.print_exc()
        raise


async def run_quick_consensus(
    question: str,
    models: Optional[List[str]] = None,
    chairman: Optional[str] = None
) -> Dict[str, Any]:
    """
    Run quick consensus (skip Stage 2 peer ranking).

    Faster but less rigorous - only collects responses and synthesizes.
    Use for simpler questions or when time is critical.

    Args:
        question: Question to deliberate on
        models: Council models (None = use defaults)
        chairman: Chairman model (None = use default)

    Returns:
        Deliberation results (no Stage 2)
    """
    start_time = datetime.now()

    config = load_config()
    models = models or get_council_models(config)
    chairman = chairman or get_chairman_model(config)

    print(f"\n{'='*70}")
    print(f"LLM COUNCIL QUICK CONSENSUS")
    print(f"{'='*70}")
    print(f"\n📋 Question: {question}")

    # Stage 1: Individual responses
    stage1_responses = await stage1_collect_responses(question, models)

    # Stage 3: Synthesis (skip Stage 2)
    print(f"\n🎯 Stage 3: Chairman synthesis (skipping peer ranking)...")

    responses_text = "\n\n".join([
        f"{resp['model']}:\n{resp['content']}"
        for resp in stage1_responses
    ])

    synthesis_prompt = f"""Synthesize the best answer from these perspectives:

Question: {question}

Responses:
{responses_text}

Provide a clear final answer incorporating the best insights."""

    messages = [
        {"role": "system", "content": "Synthesize insights from multiple AI perspectives."},
        {"role": "user", "content": synthesis_prompt}
    ]

    result = await query_model(chairman, messages)
    stage3_synthesis = {'content': result['content'], 'confidence': 0.80}

    duration = (datetime.now() - start_time).total_seconds()

    return {
        'question': question,
        'stage1': stage1_responses,
        'stage3': stage3_synthesis,
        'metadata': {
            'mode': 'quick_consensus',
            'duration_seconds': duration,
            'models_used': len(stage1_responses),
            'chairman_model': chairman
        }
    }


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="LLM Council Multi-Model Deliberation System"
    )
    parser.add_argument(
        '--question', '-q',
        required=True,
        help='Question to deliberate on'
    )
    parser.add_argument(
        '--mode', '-m',
        choices=['full', 'quick'],
        default='full',
        help='Deliberation mode (default: full)'
    )
    parser.add_argument(
        '--output', '-o',
        choices=['markdown', 'json'],
        default='markdown',
        help='Output format (default: markdown)'
    )
    parser.add_argument(
        '--models',
        nargs='+',
        help='Custom council models (space-separated)'
    )
    parser.add_argument(
        '--chairman',
        help='Custom chairman model'
    )

    args = parser.parse_args()

    # Run deliberation
    if args.mode == 'full':
        results = asyncio.run(run_full_deliberation(
            args.question,
            models=args.models,
            chairman=args.chairman
        ))
    else:
        results = asyncio.run(run_quick_consensus(
            args.question,
            models=args.models,
            chairman=args.chairman
        ))

    # Format output
    if args.output == 'json':
        print("\n" + json.dumps(results, indent=2))
    else:
        print("\n" + format_markdown(results))


if __name__ == "__main__":
    main()
