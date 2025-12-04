#!/usr/bin/env python3
"""Configuration management for LLM Council."""

import os
import json
from pathlib import Path
from typing import Dict, Any, List


def load_config() -> Dict[str, Any]:
    """Load configuration from file or environment."""
    config_path = Path(__file__).parent.parent.parent / 'assets' / 'config.json'

    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)

    # Default config
    return {
        'council_models': [
            "DeepSeek-V3",
            "Qwen3-235B-A22B",
            "kim2-thinking",
            "Kimi-K2-Instruct"
        ],
        'chairman_model': "openrouter/google/gemini-3-pro-preview"
    }


def validate_api_key() -> bool:
    """Validate OpenRouter API key is set."""
    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        raise ValueError(
            "OPENROUTER_API_KEY not set. "
            "Set with: export OPENROUTER_API_KEY='your-key'"
        )
    return True


def get_council_models(config: Dict[str, Any]) -> List[str]:
    """Get council model list from config."""
    return config.get('council_models', [])


def get_chairman_model(config: Dict[str, Any]) -> str:
    """Get chairman model from config."""
    return config.get('chairman_model', 'openrouter/google/gemini-3-pro-preview')
