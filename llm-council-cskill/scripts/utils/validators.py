#!/usr/bin/env python3
"""Input validation for LLM Council."""

from typing import List


def validate_question(question: str) -> bool:
    """Validate question is appropriate for deliberation."""
    if not question or not question.strip():
        raise ValueError("Question cannot be empty")

    if len(question) < 10:
        raise ValueError("Question too short (minimum 10 characters)")

    if len(question) > 5000:
        raise ValueError("Question too long (maximum 5000 characters)")

    return True


def validate_model_list(models: List[str]) -> bool:
    """Validate model list is appropriate."""
    if not models:
        raise ValueError("Model list cannot be empty")

    if len(models) < 2:
        raise ValueError("Need at least 2 models for deliberation")

    if len(models) > 10:
        raise ValueError("Maximum 10 models allowed")

    return True
