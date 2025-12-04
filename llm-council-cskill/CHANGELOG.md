# Changelog

All notable changes to LLM Council Skill will be documented here.

## [1.0.0] - 2025-11-28

### Added

**Core Functionality:**
- Multi-model deliberation system with 3-stage consensus process
- Stage 1: Individual responses from 4 council models
- Stage 2: Anonymous peer ranking system
- Stage 3: Chairman synthesis from Gemini-3-Pro
- Quick consensus mode (skip Stage 2 for faster results)

**Data Sources:**
- OpenRouter API integration
- Council models: DeepSeek-V3, Qwen3-235B-A22B, kim2-thinking, Kimi-K2-Instruct
- Chairman: Google Gemini-3-Pro-Preview
- Rate limiting: 120s timeout per model

**Analysis Capabilities:**
- Simple deliberation: Single question multi-perspective analysis
- Comparative deliberation: Systematic option comparison
- Code review analysis: Security and quality assessment
- Architecture review: System design evaluation
- Quick consensus: Fast mode for simpler questions
- Comprehensive report: Formatted markdown/JSON output

**Utilities:**
- Parallel model querying for performance
- Anonymous response labeling (Response A, B, C...)
- Aggregate ranking calculation
- Error handling with graceful degradation
- Input validation (question length, model list)
- Markdown and JSON output formatting

### Data Coverage

**Metrics implemented:**
- Individual model responses with reasoning
- Peer evaluation rankings
- Aggregate quality scores (average rank position)
- Synthesis confidence levels
- Execution metadata (duration, tokens, cost estimates)

**Model coverage:** 4 council members + 1 chairman
**Question types:** Architecture, code, technology, design decisions

### Known Limitations

- Requires OpenRouter API key (not free)
- Full deliberation takes 60-90 seconds
- Cost: $0.01-0.10 per deliberation
- Limited to OpenRouter supported models
- Peer ranking format parsing may fail (has fallback)

### Planned for v2.0

- Local model support (Ollama integration)
- Streaming responses for real-time feedback
- Conversation history for follow-up questions
- Custom model pools per domain
- Result caching for similar questions
- Web UI for non-CLI users
- Multi-language support (currently English only)

## [Unreleased]

### Planned

- Add support for custom chairman models
- Improve ranking parsing reliability
- Expand to 6-8 council models
- Performance optimizations (reduce latency)
- Integration with local LLM Council backend
