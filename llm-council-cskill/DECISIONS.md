# Architecture Decisions

## Selected API: OpenRouter

**Justification:**
- ✅ **Unified Interface**: Single API for multiple LLM providers
- ✅ **Already in use**: Parent LLM Council project uses OpenRouter
- ✅ **Model Diversity**: Access to DeepSeek, Qwen, Gemini, and others
- ✅ **Parallel Execution**: Supports concurrent requests
- ✅ **Pricing Transparency**: Per-model cost tracking
- ✅ **Reliability**: Production-grade with good uptime

**Alternatives Considered:**
- Direct provider APIs (OpenAI, Anthropic, etc.): Rejected - requires multiple API keys and integration points
- Local models (Ollama): Rejected for v1.0 - slower, needs GPU, planned for v2.0
- Hugging Face Inference API: Rejected - less reliable for production use

**Conclusion**: OpenRouter is the best option for v1.0 because it's already integrated in the parent project and provides the model diversity needed for meaningful deliberation.

---

## Architecture: Standalone Python Scripts

**Justification:**
- ✅ **Portability**: No dependency on running backend service
- ✅ **Simplicity**: Direct API calls, no HTTP overhead
- ✅ **Flexibility**: Can be used as CLI tool or imported as library
- ✅ **Development Speed**: Faster iteration without service coordination
- ✅ **Testing**: Easier to unit test standalone functions

**Alternatives Considered:**
- Call local backend API (http://localhost:8001): Rejected - requires backend running, less portable
- REST API wrapper: Rejected - unnecessary complexity for v1.0
- WebSocket streaming: Rejected - overkill for current use case

**Trade-offs:**
- ❌ Can't reuse backend code directly (different structure)
- ❌ Need to duplicate some logic (OpenRouter client)
- ✅ But: Much more portable and easier to use as Claude Code skill

---

## Deliberation Process: 3-Stage Design

**Stage 1: Individual Responses**

**Decision**: Parallel query of all models simultaneously

**Justification:**
- ✅ **Performance**: 75% faster than sequential (4x models in parallel)
- ✅ **Independence**: True independent perspectives (models don't see each other's responses)
- ✅ **Scalability**: Can easily add more models without increasing latency

**Stage 2: Anonymous Peer Ranking**

**Decision**: Anonymize responses before ranking

**Justification:**
- ✅ **Bias Elimination**: Models can't favor specific brands or authors
- ✅ **Merit-Based**: Evaluation focuses on content quality, not source
- ✅ **Novel Approach**: Unique feature differentiating from simple multi-model queries
- ✅ **Better Results**: Peer review improves consensus quality

**Methodology:**
- Responses labeled "Response A", "Response B", etc.
- Each model ranks ALL responses (including its own, unknown)
- Aggregate rankings calculated from all peer evaluations
- Lower average position = better quality

**Stage 3: Chairman Synthesis**

**Decision**: Single chairman model (Gemini-3-Pro) synthesizes final answer

**Justification:**
- ✅ **Consistency**: Single synthesis voice, not committee-style output
- ✅ **Quality**: Gemini-3-Pro strong at synthesis and reasoning
- ✅ **Clarity**: Users get one clear answer, not 4 competing views
- ✅ **Metadata**: Chairman sees all responses + rankings for informed synthesis

---

## Council Composition: 4 Models

**Selected Models:**
1. **DeepSeek-V3**: Strong reasoning, technical depth
2. **Qwen3-235B-A22B**: Multilingual, broad knowledge
3. **kim2-thinking**: Advanced reasoning, chain-of-thought
4. **Kimi-K2-Instruct**: Instruction following, structured output

**Justification:**
- ✅ **Diversity**: Different architectures, training data, strengths
- ✅ **Balance**: 4 models provides good diversity without excessive cost/latency
- ✅ **Proven**: These models perform well in parent project testing
- ✅ **Cost**: Reasonable cost per deliberation (~$0.05-0.10)

**Why not more models?**
- ❌ 6-8 models: Diminishing returns, 2x cost, 50% more latency
- ❌ 2-3 models: Too few perspectives, peer ranking less valuable
- ✅ 4 models: Sweet spot for diversity vs. practicality

**Why Gemini-3-Pro as Chairman?**
- ✅ Strong synthesis capabilities
- ✅ Good at integrating multiple perspectives
- ✅ Clear, actionable output
- ✅ Reliable performance

---

## Quick Consensus Mode

**Decision**: Offer fast mode that skips Stage 2 (peer ranking)

**Justification:**
- ✅ **Speed**: 50% faster (30-45s vs 60-90s)
- ✅ **Cost**: 40% cheaper (fewer API calls)
- ✅ **Use Case**: Simple questions don't need rigorous peer review
- ✅ **Options**: Users can choose rigor vs. speed

**Trade-offs:**
- ❌ Less rigorous (no peer validation)
- ❌ No ranking metadata
- ✅ Still multi-perspective (better than single model)
- ✅ Appropriate for exploratory questions

---

## Output Formats: Markdown + JSON

**Decision**: Support both markdown (default) and JSON output

**Justification:**
- ✅ **Markdown**: Human-readable, great for Claude Code display
- ✅ **JSON**: Machine-readable, enables programmatic use
- ✅ **Flexibility**: Users choose based on need

**Markdown Format:**
- Staged sections (Stage 1, 2, 3)
- Clear headers and emphasis
- Metadata footer (duration, confidence)

**JSON Format:**
- Structured data with all fields
- Suitable for parsing, storage, analysis
- Preserves all metadata

---

## Error Handling: Graceful Degradation

**Decision**: Continue with partial responses if some models fail

**Justification:**
- ✅ **Reliability**: Don't fail entire deliberation due to one model
- ✅ **Cost**: Don't waste successful API calls
- ✅ **User Experience**: Partial result better than total failure
- ✅ **Transparency**: User sees which models succeeded/failed

**Thresholds:**
- Minimum 2 successful Stage 1 responses required
- If <50% models respond, warn user
- Chairman synthesis runs regardless (synthesizes available responses)

---

## Input Validation

**Question Length:**
- Minimum: 10 characters (prevent meaningless queries)
- Maximum: 5000 characters (API token limits, focus)

**Model List:**
- Minimum: 2 models (need diversity)
- Maximum: 10 models (cost, latency constraints)

**Rationale:** Balance between flexibility and practical constraints

---

## Performance Optimizations

**1. Parallel Execution:**
- All Stage 1 queries: Parallel (asyncio.gather)
- All Stage 2 rankings: Parallel
- Stage 3: Single call (synthesis)

**Result**: 75% latency reduction vs sequential

**2. Timeout Strategy:**
- 120s per model (generous for complex questions)
- Fail fast: Don't wait for slow models indefinitely
- Graceful degradation: Continue with timely responses

**3. (Future) Caching:**
- Cache full deliberation results: 24 hours
- Cache key: hash(question + models + mode)
- Estimated cache hit rate: 20-30%
- Not implemented in v1.0 (simple first iteration)

---

## Testing Strategy

**Integration Tests:**
- Test each stage independently
- Test full deliberation end-to-end
- Test quick consensus mode
- Test error handling (model failures)

**Why integration over unit?**
- Most logic is in API orchestration
- Integration tests validate real API behavior
- Unit tests would require extensive mocking
- Quick to run with real API (60-90s for full test suite)

---

## Documentation Structure

**SKILL.md** (~6800 words):
- Complete specification for Claude Code skill system
- When to use, workflows, examples
- Detailed API documentation

**README.md** (~1200 words):
- Quick start guide
- Installation instructions
- Basic usage examples

**CHANGELOG.md**:
- Version history
- Planned features
- Known limitations

**DECISIONS.md** (this file):
- Technical decision justifications
- Trade-off analysis
- Architecture rationale

---

## Future Enhancements (v2.0 Candidates)

**1. Local Model Support (Ollama)**
- Run models locally for privacy/cost
- Trade-off: Slower, needs GPU
- Priority: Medium

**2. Streaming Responses**
- Real-time feedback as models respond
- Better UX for long deliberations
- Priority: High

**3. Conversation History**
- Follow-up questions in context
- Multi-turn deliberations
- Priority: Medium

**4. Result Caching**
- Avoid re-querying identical questions
- 20-30% cost savings
- Priority: High

**5. Custom Model Pools**
- Domain-specific model selections
- E.g., "code-review-council" vs "architecture-council"
- Priority: Low

**6. Web UI**
- Non-CLI interface
- Visualization of rankings
- Priority: Low (Claude Code is primary interface)
