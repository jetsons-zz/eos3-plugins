# LLM Council - Multi-Model Deliberation Skill

> Multi-model deliberation system for collaborative AI decision-making through 3-stage consensus building.

## Overview

LLM Council orchestrates multiple AI models to provide diverse perspectives with bias-free peer evaluation, culminating in a synthesized expert conclusion. Perfect for architecture decisions, code reviews, technical assessments, and complex problem-solving.

## Installation

### 1. Install the Skill

```bash
/plugin marketplace add /Users/will/Code/Laiye/llm-council-cskill
```

### 2. Set Up OpenRouter API Key

Get your API key from [OpenRouter](https://openrouter.ai/):

```bash
export OPENROUTER_API_KEY="sk-or-v1-..."
```

Or create `.env` file:
```
OPENROUTER_API_KEY=sk-or-v1-...
```

### 3. Test Installation

```bash
cd llm-council-cskill
python3 scripts/council_deliberation.py --question "Is Python or JavaScript better for web backends?" --mode quick
```

## Quick Start

### Use in Claude Code Conversation

Simply ask questions that require multi-model deliberation:

```
"Get council consensus on: Should we use microservices or monolithic architecture?"

"Code review: [paste code here]"

"Compare PostgreSQL vs MongoDB for our analytics platform"
```

### Use as Standalone Script

```bash
# Full deliberation (all 3 stages)
python3 scripts/council_deliberation.py \
  --question "Should we use REST or GraphQL?" \
  --mode full

# Quick consensus (skip peer ranking)
python3 scripts/council_deliberation.py \
  --question "Is caching at application level a good practice?" \
  --mode quick
```

## How It Works

### 3-Stage Process

**Stage 1: Individual Responses** (10-30s)
- 4 models independently analyze your question
- Each provides unique perspective
- No model knows others' responses (unbiased)

**Stage 2: Anonymous Peer Ranking** (20-40s)
- Responses anonymized ("Response A", "Response B", etc.)
- Each model ranks ALL responses
- Aggregate rankings calculated

**Stage 3: Chairman Synthesis** (10-20s)
- Chairman model (Gemini-3-Pro) reviews all
- Synthesizes best insights
- Produces final conclusion

### Why Anonymous Peer Review?

Models evaluate quality objectively without knowing authorship, preventing:
- Model favoritism
- Self-promotion bias
- Brand biases

## Usage Examples

### Architecture Decision
```
Question: "Should we use PostgreSQL or MongoDB for user analytics?"

Output:
- 4 model perspectives with reasoning
- Peer rankings showing consensus
- Final synthesis with recommendation
```

### Code Review
```
Question: "Review this auth middleware: [code]"

Output:
- Security analysis from 4 models
- Quality rankings
- Consolidated review with fixes
```

### Technology Comparison
```
Question: "Compare Docker vs Kubernetes for our deployment"

Output:
- Detailed comparison from multiple perspectives
- Trade-off analysis
- Recommendation with confidence level
```

## Configuration

Edit `assets/config.json`:

```json
{
  "council_models": [
    "DeepSeek-V3",
    "Qwen3-235B-A22B",
    "kim2-thinking",
    "Kimi-K2-Instruct"
  ],
  "chairman_model": "openrouter/google/gemini-3-pro-preview",
  "timeout_seconds": 120
}
```

## Testing

Run integration tests:

```bash
cd llm-council-cskill
python3 tests/test_integration.py
```

Expected output:
```
✓ Testing full deliberation...
  ✓ Stage 1: 4/4 models responded
  ✓ Stage 2: 4/4 rankings collected
  ✓ Stage 3: Synthesis complete
✅ PASS: Full deliberation

Results: 5/5 tests passed
```

## Files Structure

```
llm-council-cskill/
├── .claude-plugin/
│   └── marketplace.json        # Skill registration
├── SKILL.md                    # Complete skill documentation
├── scripts/
│   ├── council_deliberation.py # Main orchestration
│   ├── openrouter_client.py    # API client
│   ├── format_results.py       # Output formatting
│   └── utils/
│       ├── config_manager.py   # Configuration
│       └── validators.py       # Input validation
├── assets/
│   └── config.json             # Settings
├── tests/
│   └── test_integration.py     # Integration tests
└── README.md                   # This file
```

## Troubleshooting

### Error: "OPENROUTER_API_KEY not set"
```bash
export OPENROUTER_API_KEY="your-key-here"
```

### Error: "Model timeout"
- Use `--mode quick` for faster results
- Increase timeout in `config.json`

### Error: "Need at least 2 successful responses"
- Some models may be unavailable
- Check OpenRouter API status
- Skill continues with available models

## Cost Estimation

- Full deliberation: $0.01-0.10 depending on complexity
- Quick consensus: $0.005-0.05
- Models vary in cost (check OpenRouter pricing)

## Version

Version 1.0.0 - Initial release

## License

MIT License - See parent LLM Council project

## Support

- Issues: [LLM Council GitHub](https://github.com/your-repo/llm-council)
- Documentation: See SKILL.md for complete details
