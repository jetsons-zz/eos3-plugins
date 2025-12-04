---
name: llm-council-cskill
description: Multi-model deliberation system enabling collaborative AI decision-making through 3-stage consensus: individual responses, anonymous peer ranking, and chairman synthesis. Perfect for architecture decisions, code reviews, technical assessments, strategic planning, ethical dilemmas, creative problem-solving, and any complex question requiring diverse AI perspectives with bias-free evaluation.
version: 1.0.0
author: LLM Council
tags: [multi-model, deliberation, consensus, code-review, architecture, decision-making]
---

# LLM Council - Multi-Model Deliberation Skill

## Overview

LLM Council is a sophisticated multi-model deliberation system that enables collaborative AI decision-making through a rigorous 3-stage consensus process. Unlike single-model responses, this skill orchestrates multiple AI models to provide diverse perspectives with bias-free peer evaluation, culminating in a synthesized expert conclusion.

## When to Use This Skill

✅ **Activate this skill when you need:**

**Technical Domains:**
- **Architecture Decisions**: "Should we use REST or GraphQL for our API?"
- **Code Reviews**: "Review this authentication implementation for security issues"
- **Technical Assessments**: "Evaluate these three database options for our use case"
- **Complex Problem-Solving**: "What's the best approach to handle distributed transactions?"
- **Design Validation**: "Is this microservices architecture sound?"
- **Trade-off Analysis**: "Compare Docker vs Kubernetes for our deployment"
- **Technology Selection**: "Which frontend framework should we choose?"
- **Performance Optimization**: "How can we improve this algorithm's efficiency?"
- **Security Evaluation**: "Identify vulnerabilities in this authentication flow"
- **Refactoring Decisions**: "Should we refactor this monolith to microservices?"

**Non-Technical Domains:**
- **Strategic Planning**: "Should we expand to international markets or focus on domestic growth?"
- **Ethical Dilemmas**: "How should we balance user privacy with personalization features?"
- **Business Decisions**: "Should we adopt a subscription model or keep one-time purchases?"
- **Creative Problem-Solving**: "What are innovative ways to improve employee engagement?"
- **Policy Evaluation**: "Compare remote-first vs hybrid work policies for our company"
- **Educational Approaches**: "What's the best teaching methodology for adult learners?"
- **Content Strategy**: "Should we focus on long-form or short-form content?"
- **Product Direction**: "Which product feature should we prioritize: A, B, or C?"
- **Communication Strategy**: "How should we handle this PR crisis?"
- **Resource Allocation**: "Where should we invest our limited R&D budget?"

❌ **Do NOT use this skill for:**

- Simple factual questions that have clear, objective answers (e.g., "What is the capital of France?")
- When you need immediate response (deliberation takes 30-90 seconds)
- Questions where only one perspective is needed or when speed is critical
- Basic information lookup that doesn't require evaluation or judgment

## How It Works

### 3-Stage Deliberation Process

**Stage 1: Individual Responses** (10-30 seconds)
- Multiple AI models independently analyze your question
- Each provides their unique perspective and reasoning
- Models: DeepSeek-V3, Qwen3-235B, kim2-thinking, Kimi-K2-Instruct
- No model knows what others responded (unbiased)

**Stage 2: Anonymous Peer Ranking** (20-40 seconds)
- Responses are anonymized ("Response A", "Response B", etc.)
- Each model evaluates ALL responses (including its own)
- Rankings are based on quality, accuracy, and usefulness
- Prevents bias towards specific models or "playing favorites"
- Aggregate rankings calculated from all peer evaluations

**Stage 3: Chairman Synthesis** (10-20 seconds)
- Chairman model (Gemini-3-Pro) reviews all responses and rankings
- Synthesizes insights from diverse perspectives
- Produces final, well-reasoned conclusion
- Incorporates best ideas from all council members

### Key Innovation: Anonymous Peer Review

The anonymization in Stage 2 is critical - models evaluate quality objectively without knowing authorship. This prevents:
- Model favoritism ("I prefer GPT-4 responses")
- Self-promotion bias
- Brand/company biases
- Ensures merit-based evaluation

## Data Sources

### Primary API: OpenRouter

**Endpoint**: `https://llm.tokencloud.ai/v1/chat/completions`

**Authentication**: Bearer token (OPENROUTER_API_KEY required)

**Models Used:**
- Council Members: DeepSeek-V3, Qwen3-235B, kim2-thinking, Kimi-K2-Instruct
- Chairman: Google Gemini-3-Pro-Preview

**Rate Limits**:
- Parallel requests: 4 models simultaneously
- Total API calls per deliberation: ~9 calls (4 Stage 1 + 4 Stage 2 + 1 Stage 3)
- Timeout: 120 seconds per model

**Cost Considerations**:
- Varies by model (check OpenRouter pricing)
- Estimated: $0.01-0.10 per deliberation depending on complexity
- Chairman synthesis typically most expensive call

## Workflows

### Workflow 1: Simple Deliberation

**Use Case**: Single question requiring expert consensus

**Steps:**
1. User provides question
2. Skill triggers full 3-stage deliberation
3. Results formatted and presented with all stages visible

**Example:**
```
User: "Should we use PostgreSQL or MongoDB for our user analytics?"

Skill executes:
→ Stage 1: 4 models respond with their analyses
→ Stage 2: 4 models rank all responses anonymously
→ Stage 3: Chairman synthesizes final recommendation

Output: Complete deliberation with:
- Individual model responses
- Peer rankings with aggregate scores
- Final synthesis with reasoning
```

### Workflow 2: Comparative Deliberation

**Use Case**: Compare multiple options systematically

**Steps:**
1. User provides 2-3 options to compare
2. Deliberation runs for each option
3. Cross-comparison synthesis

**Example:**
```
User: "Compare these three caching strategies: Redis, Memcached, and in-memory LRU"

Skill executes 3 deliberations + comparison:
→ Deliberation 1: Redis assessment
→ Deliberation 2: Memcached assessment
→ Deliberation 3: In-memory LRU assessment
→ Final: Comparative analysis across all three

Output: Structured comparison with trade-offs
```

### Workflow 3: Code Review Deliberation

**Use Case**: Multi-perspective code analysis

**Steps:**
1. User provides code snippet
2. Review prompt emphasizes quality, security, performance
3. Full deliberation with code-specific criteria

**Example:**
```
User: "Review this auth middleware:
```python
def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or token != SECRET_KEY:
            return {'error': 'Unauthorized'}, 401
        return f(*args, **kwargs)
    return decorated
```"

Skill executes code review deliberation:
→ Stage 1: Security analysis, code quality, best practices
→ Stage 2: Ranking solutions by thoroughness
→ Stage 3: Comprehensive review summary

Output: Detailed code review with issues and improvements
```

### Workflow 4: Architecture Review

**Use Case**: System design evaluation

**Steps:**
1. User describes architecture or provides diagram
2. Deliberation focuses on scalability, reliability, maintainability
3. Identifies strengths and weaknesses

**Example:**
```
User: "Review this microservices architecture: API Gateway → Auth Service → User Service → PostgreSQL + Redis"

Output: Multi-perspective architecture analysis covering:
- Scalability concerns
- Single points of failure
- Data consistency patterns
- Operational complexity
- Alternative approaches
```

### Workflow 5: Quick Consensus (Fast Mode)

**Use Case**: Simpler questions needing multiple perspectives but less rigor

**Steps:**
1. Skip Stage 2 (peer ranking)
2. Only run Stage 1 + Stage 3
3. 50% faster (30-45 seconds vs 60-90 seconds)

**Example:**
```
User: "Quick consensus: Is GraphQL overkill for a simple CRUD API?"

Skill executes fast mode:
→ Stage 1: 4 models respond
→ Stage 3: Chairman synthesizes (no ranking)

Output: Quick multi-model consensus
```

## Available Scripts

### `scripts/council_deliberation.py`

**Main deliberation orchestration script**

**Functions:**
- `run_full_deliberation(question, models, chairman)`: Complete 3-stage process
- `run_quick_consensus(question, models, chairman)`: Fast mode (skip Stage 2)
- `stage1_collect_responses(question, models)`: Parallel model queries
- `stage2_collect_rankings(question, responses)`: Anonymous peer evaluation
- `stage3_synthesize(question, responses, rankings, chairman)`: Final synthesis

**Usage:**
```bash
python scripts/council_deliberation.py \
  --question "Should we use REST or GraphQL?" \
  --mode full
```

**Parameters:**
- `--question`: The question to deliberate on (required)
- `--mode`: "full" (default) or "quick"
- `--models`: Custom model list (optional)
- `--chairman`: Custom chairman model (optional)
- `--output`: Output format ("json" or "markdown", default "markdown")

### `scripts/openrouter_client.py`

**OpenRouter API client with retry logic**

**Functions:**
- `query_model(model, messages, timeout=120)`: Single model query
- `query_models_parallel(models, messages)`: Parallel batch queries
- `format_messages(system_prompt, user_message)`: Message formatting

**Features:**
- Automatic retry with exponential backoff
- Request timeout handling
- Error logging and graceful degradation
- Token usage tracking (if available)

### `scripts/format_results.py`

**Result formatting and presentation**

**Functions:**
- `format_deliberation_results(stage1, stage2, stage3)`: Full deliberation output
- `format_markdown(results)`: Markdown formatted output
- `format_json(results)`: Structured JSON export
- `extract_key_insights(results)`: Summary extraction

**Output Formats:**
- Markdown: Human-readable with headers, lists, emphasis
- JSON: Structured data for programmatic use
- Summary: Executive summary with key points

### `scripts/utils/config_manager.py`

**Configuration and credentials management**

**Functions:**
- `load_config()`: Load settings from config.json or env vars
- `validate_api_key()`: Verify OpenRouter API key is set
- `get_council_models()`: Get configured model list
- `get_chairman_model()`: Get chairman model identifier

**Configuration Priority:**
1. Environment variables (OPENROUTER_API_KEY)
2. .env file
3. assets/config.json
4. Default values

### `scripts/utils/validators.py`

**Input validation and sanitization**

**Functions:**
- `validate_question(question)`: Ensure question is appropriate
- `validate_model_list(models)`: Verify model identifiers
- `sanitize_input(text)`: Remove problematic characters
- `check_question_length(question)`: Enforce length limits

**Validations:**
- Question length: 10-5000 characters
- Model list: 2-10 models
- No injection attempts
- Language appropriateness

## Available Analyses

### 1. Simple Deliberation

**Purpose**: Get multi-model consensus on a single question

**Methodology:**
1. Parallel query of all council models
2. Anonymous ranking by all models
3. Chairman synthesis with aggregate scores

**Inputs:**
- `question` (str): The question or problem to deliberate
- `models` (list, optional): Custom model list
- `chairman` (str, optional): Custom chairman model

**Outputs:**
```json
{
  "question": "...",
  "stage1": [
    {"model": "DeepSeek-V3", "response": "...", "reasoning": "..."},
    ...
  ],
  "stage2": [
    {"model": "DeepSeek-V3", "ranking": ["Response C", "Response A", ...], "evaluation": "..."},
    ...
  ],
  "aggregate_rankings": [
    {"label": "Response C", "model": "kim2-thinking", "avg_rank": 1.5, "votes": 4},
    ...
  ],
  "stage3": {
    "synthesis": "...",
    "confidence": 0.85
  },
  "metadata": {
    "duration_seconds": 72.3,
    "total_tokens": 15420,
    "cost_estimate": 0.045
  }
}
```

### 2. Comparative Deliberation

**Purpose**: Compare multiple options systematically

**Methodology:**
1. Run full deliberation for each option independently
2. Aggregate findings across deliberations
3. Generate comparative synthesis

**Inputs:**
- `options` (list): 2-3 options to compare
- `context` (str, optional): Additional context

**Outputs:**
- Individual deliberation for each option
- Cross-option comparison matrix
- Final recommendation with trade-offs

### 3. Code Review Analysis

**Purpose**: Multi-perspective code quality assessment

**Methodology:**
1. Enhanced prompting for code-specific criteria:
   - Security vulnerabilities
   - Performance issues
   - Code quality and readability
   - Best practices adherence
2. Full 3-stage deliberation
3. Consolidated review with severity ratings

**Inputs:**
- `code` (str): Code snippet to review
- `language` (str): Programming language
- `focus` (list, optional): Specific concerns (security, performance, etc.)

**Outputs:**
- Issues identified (categorized by severity)
- Suggested improvements
- Best practices recommendations
- Refactoring opportunities

### 4. Architecture Review

**Purpose**: System design evaluation and validation

**Methodology:**
1. Architecture-focused prompting:
   - Scalability analysis
   - Reliability assessment
   - Maintainability evaluation
   - Alternative approaches
2. Multi-model architectural analysis
3. Synthesis with design recommendations

**Inputs:**
- `architecture_description` (str): System design details
- `diagram_url` (str, optional): Architecture diagram link
- `constraints` (list, optional): Known constraints

**Outputs:**
- Strengths identified
- Weaknesses and risks
- Scalability assessment
- Reliability concerns
- Recommended improvements

### 5. Quick Consensus (Fast Mode)

**Purpose**: Faster deliberation for simpler questions

**Methodology:**
1. Stage 1: Parallel model queries (same as full)
2. **SKIP Stage 2**: No peer ranking (saves 30-40 seconds)
3. Stage 3: Chairman synthesis without rankings

**Trade-offs:**
- ✅ 50% faster (30-45s vs 60-90s)
- ✅ Still multi-perspective
- ❌ Less rigorous (no peer validation)
- ❌ No ranking metadata

**When to use:**
- Simple technical questions
- Time-sensitive decisions
- Exploratory analysis

### 6. Comprehensive Report

**Purpose**: Full deliberation with formatted output

**Methodology:**
1. Run full 3-stage deliberation
2. Extract key insights from all stages
3. Format as readable report with sections:
   - Executive Summary
   - Individual Perspectives
   - Peer Evaluations
   - Aggregate Rankings
   - Final Synthesis
   - Metadata (duration, cost, confidence)

**Outputs:**
- Markdown formatted report
- Exportable to PDF/HTML
- Structured for documentation

## Error Handling

### Common Errors and Solutions

**Error: Missing OPENROUTER_API_KEY**
```
Solution: Set environment variable:
export OPENROUTER_API_KEY="sk-or-v1-..."

Or create .env file:
OPENROUTER_API_KEY=sk-or-v1-...
```

**Error: Model timeout (120s exceeded)**
```
Cause: Model is overloaded or question is too complex
Solution:
- Retry with simpler question
- Use quick consensus mode
- Increase timeout in config
```

**Error: Model returned None**
```
Cause: Model failed or is unavailable
Solution: Graceful degradation - continue with available responses
Note: Skill continues if ≥2 models respond successfully
```

**Error: Invalid ranking format**
```
Cause: Model didn't follow ranking format
Solution: Fallback regex parsing to extract rankings
```

**Error: Rate limit exceeded**
```
Cause: Too many API requests
Solution:
- Wait 60 seconds
- Reduce council size
- Use rate limiting in config
```

## Mandatory Validations

**Before Deliberation:**
- [ ] API key is set and valid
- [ ] Question length: 10-5000 characters
- [ ] Question is not empty
- [ ] Model list contains 2-10 models
- [ ] All model identifiers are valid
- [ ] Chairman model is valid

**During Deliberation:**
- [ ] ≥2 models responded successfully in Stage 1
- [ ] Each ranking has valid format
- [ ] No duplicate labels in rankings
- [ ] Chairman synthesis is non-empty

**After Deliberation:**
- [ ] All stages completed or gracefully degraded
- [ ] Results contain required fields
- [ ] Metadata is populated
- [ ] Output format is valid

## Performance and Caching

### Performance Characteristics

**Typical Latency:**
- Full deliberation: 60-90 seconds
- Quick consensus: 30-45 seconds
- Code review: 90-120 seconds (longer prompts)
- Architecture review: 120-180 seconds (complex analysis)

**Parallelization:**
- Stage 1: All models queried in parallel (saves 80% time vs sequential)
- Stage 2: All rankings in parallel
- Stage 3: Single synthesis call

**Optimization Techniques:**
- Request timeout: 120s per model
- Graceful degradation: Continue with partial responses
- Async/await for parallel execution
- Response streaming (optional)

### Caching Strategy

**What to Cache:**
- ✅ Full deliberation results: 24 hours
- ✅ Model responses: 1 hour (for similar questions)
- ❌ Rankings: Don't cache (context-dependent)
- ❌ Synthesis: Don't cache (aggregates change)

**Cache Keys:**
```python
cache_key = hash(question + sorted(model_list) + mode)
```

**Cache Storage:**
- Location: `data/cache/deliberations/`
- Format: JSON files
- Expiry: TTL-based (configurable)
- Size limit: 100 MB (auto-cleanup)

**Cache Hit Rate Target:**
- Similar questions: 20-30%
- Identical questions: 95%+

## Keywords for Detection

**Primary Keywords:**
- council, deliberation, peer review, consensus
- multi-model, multiple models, diverse perspectives
- anonymous ranking, bias-free evaluation
- architecture decision, code review, technical assessment
- strategic planning, ethical dilemma, business decision
- evaluate, compare, assess, analyze, review

**Technical Domain Keywords:**
- architecture, microservices, database, API, security
- performance, scalability, code quality, refactoring
- technology selection, framework choice, deployment

**Non-Technical Domain Keywords:**
- strategy, policy, ethics, business model, priorities
- resource allocation, team dynamics, communication
- education, content, marketing, product direction
- organizational, management, planning, decision-making

**Model References:**
- OpenRouter, DeepSeek, Qwen, Gemini
- council members, chairman model

**Use Case Keywords:**
- should we use, compare options, evaluate choices
- which is better, what's the best approach
- review this code, assess this architecture
- get consensus on, multiple perspectives
- how should we handle, what's the right decision

**Action Verbs:**
- deliberate, evaluate, assess, review, compare
- analyze, rank, synthesize, discuss, prioritize

**Negative Scope:**
- NOT for: simple factual questions with clear answers
- NOT when: only one perspective needed, immediate response required
- NOT for: basic information lookup without judgment needed

## Usage Examples

### Example 1: Architecture Decision

```
User: "Should we use a monolithic architecture or microservices for our new e-commerce platform?"

Skill response:
🏛️ LLM Council Deliberation - Architecture Decision

📋 Question: Monolithic vs Microservices for E-commerce Platform

⚙️ Stage 1: Individual Responses (4 models)

DeepSeek-V3:
For an e-commerce platform, I recommend starting with a modular monolith...
[detailed analysis]

Qwen3-235B:
Microservices would provide better scalability for different e-commerce components...
[detailed analysis]

kim2-thinking:
The decision depends on team size and timeline...
[detailed analysis]

Kimi-K2-Instruct:
Consider a hybrid approach with domain-driven design...
[detailed analysis]

⭐ Stage 2: Anonymous Peer Rankings

Aggregate Rankings:
1. Response C (kim2-thinking) - Avg Rank: 1.75 - Most comprehensive trade-off analysis
2. Response D (Kimi-K2-Instruct) - Avg Rank: 2.00 - Practical hybrid approach
3. Response A (DeepSeek-V3) - Avg Rank: 2.50 - Pragmatic starting point
4. Response B (Qwen3-235B) - Avg Rank: 3.75 - Valid but more complex

🎯 Stage 3: Chairman Synthesis (Gemini-3-Pro)

Recommendation: Start with a well-structured monolithic architecture using domain-driven design principles...

The council consensus favors beginning with a modular monolith because:
1. Team size (<10 developers based on typical e-commerce startups)
2. Faster initial development and deployment
3. Easier debugging and testing
4. Lower operational complexity
5. Clear migration path to microservices later

Key considerations for the monolithic approach:
- Use domain-driven design with bounded contexts
- Implement clear module boundaries
- Design with microservices migration in mind
- Monitor for splitting candidates (e.g., payment, inventory)

When to consider microservices:
- Team grows beyond 20-30 developers
- Specific components need independent scaling
- Different components have different technology requirements

Confidence: 85% (strong consensus with nuanced trade-offs)
```

### Example 2: Code Review

```
User: "Review this authentication middleware for security issues"

[Code provided...]

Skill response:
🔍 LLM Council Code Review

📋 Code: Authentication Middleware (Python Flask)

⚙️ Stage 1: Security Analysis

[4 models identify issues...]

⭐ Stage 2: Ranking by Thoroughness

1. Response B - Most comprehensive security analysis
2. Response A - Good coverage of authentication flaws
3. Response D - Identified timing attack vulnerability
4. Response C - Basic security review

🎯 Stage 3: Consolidated Review

🚨 Critical Issues:
1. Secret key comparison vulnerable to timing attacks
2. Token not validated (format, expiry, signature)
3. Hardcoded secret comparison instead of cryptographic verification
4. No rate limiting on authentication
5. Missing HTTPS enforcement

⚠️ High Priority:
- Implement proper JWT validation
- Use constant-time comparison (hmac.compare_digest)
- Add token expiry checking
- Implement rate limiting

💡 Recommended Fix:
[Improved code provided...]

Confidence: 95% (unanimous agreement on critical issues)
```

### Example 3: Quick Technical Question

```
User: "Quick consensus: Is caching database queries at the application level a good practice?"

Skill response (Quick Mode):
⚡ LLM Council Quick Consensus

📋 Question: Application-level database query caching

⚙️ Individual Perspectives (4 models)

DeepSeek-V3: Generally beneficial but requires careful invalidation...
Qwen3-235B: Depends on read-write ratio and consistency requirements...
kim2-thinking: Yes for read-heavy workloads, but consider Redis...
Kimi-K2-Instruct: Good practice with proper cache invalidation strategy...

🎯 Synthesis

Consensus: YES, with caveats

Application-level caching is beneficial when:
✅ Read-heavy workload (80%+ reads)
✅ Data changes infrequently
✅ Consistency can tolerate slight lag
✅ Proper invalidation strategy in place

Avoid when:
❌ Strong consistency required
❌ Frequent writes
❌ Complex invalidation logic
❌ Data is user-specific

Recommended approach:
- Use Redis or Memcached for distributed caching
- Implement TTL-based expiry (5-60 minutes)
- Use cache-aside pattern
- Monitor cache hit rates (target >70%)

Time saved: Quick mode (35 seconds vs 75 seconds full deliberation)
```

### Example 4: Technology Comparison

```
User: "Compare PostgreSQL, MongoDB, and Cassandra for a real-time analytics platform"

Skill response:
🔬 LLM Council Comparative Analysis

📋 Comparison: PostgreSQL vs MongoDB vs Cassandra for Real-time Analytics

[3 separate deliberations run in parallel...]

🏆 Final Comparison Matrix

| Criteria | PostgreSQL | MongoDB | Cassandra |
|----------|------------|---------|-----------|
| Write Throughput | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Query Flexibility | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| Horizontal Scaling | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| ACID Compliance | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Operational Complexity | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |

🎯 Recommendation for Real-time Analytics:

Primary: Cassandra
Reason: Highest write throughput and linear scalability for time-series analytics

Secondary: PostgreSQL + TimescaleDB
Reason: If SQL query flexibility is critical and write volume is manageable

Not Recommended: MongoDB
Reason: Between PostgreSQL (better queries) and Cassandra (better scale)

Trade-offs Discussed:
[Detailed analysis from all council members...]

Confidence: 78% (some debate on PostgreSQL vs Cassandra trade-offs)
```

### Example 5: Design Validation

```
User: "Validate this microservices communication pattern: Services communicate via HTTP REST APIs with a service mesh for load balancing and circuit breaking"

Skill response:
🏗️ LLM Council Architecture Review

📋 Design: REST-based Microservices with Service Mesh

⚙️ Stage 1: Architecture Analysis

[4 models evaluate the design...]

⭐ Stage 2: Design Quality Rankings

1. Response D - Most thorough evaluation of trade-offs
2. Response A - Identified key operational concerns
3. Response C - Good alternatives suggested
4. Response B - Valid but less comprehensive

🎯 Stage 3: Validation Summary

✅ Strengths:
- Service mesh handles cross-cutting concerns well
- REST is widely understood and tooled
- Clear separation of concerns
- Industry-standard pattern

⚠️ Concerns:
1. Synchronous communication creates coupling
2. REST overhead for internal APIs
3. Network latency accumulates across service calls
4. Complex request tracing needed
5. Potential cascade failures despite circuit breaking

💡 Recommendations:

Enhanced Design:
- Add async messaging (Kafka/RabbitMQ) for non-critical paths
- Use gRPC instead of REST for internal service-to-service calls
- Implement request/response correlation IDs
- Add distributed tracing (Jaeger/Zipkin)
- Design with failure domains in mind

Alternative Pattern:
- Event-driven architecture with message broker
- Saga pattern for distributed transactions
- CQRS for read scalability

Decision: APPROVED with modifications
- Core pattern is sound
- Recommend hybrid: REST for external, gRPC for internal, async for events

Confidence: 82%
```

### Example 6: Strategic Business Decision

```
User: "Should our startup adopt a freemium model or a free trial with paid subscription model?"

Skill response:
💼 LLM Council Business Strategy Deliberation

📋 Question: Freemium vs Free Trial Model for Startup

⚙️ Stage 1: Individual Perspectives (4 models)

DeepSeek-V3:
For B2B SaaS, I recommend the free trial model with clear conversion goals...
- Freemium often leads to low conversion rates (<3%)
- Free trial creates urgency and commitment
- Easier to predict revenue with trial conversions
[detailed analysis]

Qwen3-235B:
Freemium can work exceptionally well if you have viral growth potential...
- Lower barrier to entry attracts more users
- Network effects can drive paid conversions
- Better for consumer-facing products
[detailed analysis]

kim2-thinking:
The choice depends heavily on your CAC, LTV, and target market...
- Enterprise customers prefer trials with onboarding
- Consumer products benefit from freemium exploration
- Consider hybrid approach with tiered freemium + enterprise trials
[detailed analysis]

Kimi-K2-Instruct:
Analyze your competitors and market positioning first...
- If competitors use freemium, you need differentiation
- Trial works better for complex products requiring onboarding
- Freemium suits simple, self-service products
[detailed analysis]

⭐ Stage 2: Anonymous Peer Rankings

Aggregate Rankings:
1. Response C (kim2-thinking) - Avg Rank: 1.50 - Most comprehensive framework
2. Response D (Kimi-K2-Instruct) - Avg Rank: 2.25 - Market-focused approach
3. Response A (DeepSeek-V3) - Avg Rank: 2.50 - Strong B2B perspective
4. Response B (Qwen3-235B) - Avg Rank: 3.75 - Valid but narrower scope

🎯 Stage 3: Chairman Synthesis (Gemini-3-Pro)

Recommendation: Adopt a FREE TRIAL model with the following structure:
- 14-day trial with full feature access
- Onboarding support during trial
- Clear conversion goals and success metrics
- Option to add limited freemium tier later for viral growth

Reasoning:
Based on the council's analysis, the free trial model is recommended because:

1. **Target Market Fit** (assuming B2B/Enterprise):
   - Complex product likely needs guidance
   - Higher ACV justifies onboarding investment
   - Enterprise buyers prefer evaluating full capabilities

2. **Conversion Optimization**:
   - Trial creates urgency (time pressure)
   - Easier to measure and optimize conversion funnel
   - Predictable sales cycle and revenue forecasting

3. **Resource Efficiency**:
   - Lower support burden (time-limited users)
   - Focus resources on qualified leads
   - Simpler pricing and messaging

When to reconsider Freemium:
- If product becomes viral/consumer-focused
- When user base reaches 50K+ and conversion plateaus
- If competitors successfully use freemium model

Hybrid Approach (Future):
- Start with free trial for primary product
- Add limited freemium tier for lead generation
- Use freemium users for product feedback and case studies

Success Metrics to Track:
- Trial-to-paid conversion rate (target: 15-25%)
- Time to first value during trial
- Feature adoption during trial period
- Customer Acquisition Cost (CAC) vs Lifetime Value (LTV)

Confidence: 80% (strong consensus with context-specific caveats)
```

### Example 7: Ethical Dilemma

```
User: "Should our social media platform use algorithmic ranking to maximize engagement or chronological feeds to ensure equal visibility?"

Skill response:
⚖️ LLM Council Ethical Analysis

📋 Question: Algorithmic vs Chronological Content Ranking

⚙️ Stage 1: Ethical Perspectives (4 models)

DeepSeek-V3:
From a user welfare perspective, chronological feeds are more transparent...
- Users understand what they're seeing and why
- No hidden manipulation of attention
- However, may reduce user retention and business viability
[detailed ethical analysis]

Qwen3-235B:
Algorithmic ranking isn't inherently unethical if done transparently...
- Can improve user experience by surfacing relevant content
- Key is transparency about how algorithm works
- Allow users to choose their preferred ranking method
[detailed analysis]

kim2-thinking:
This is a false dichotomy - hybrid approaches exist...
- Default chronological with optional algorithmic filtering
- Transparent algorithm with user controls
- Ethical algorithm design prioritizing user wellbeing over pure engagement
[detailed analysis]

Kimi-K2-Instruct:
Consider the long-term impact on society and discourse...
- Algorithmic feeds have contributed to polarization and echo chambers
- But chronological feeds may lead to information overload
- Balance business sustainability with ethical responsibility
[detailed analysis]

⭐ Stage 2: Ranking by Ethical Soundness

1. Response C (kim2-thinking) - Avg Rank: 1.75 - Most nuanced ethical framework
2. Response B (Qwen3-235B) - Avg Rank: 2.00 - Balanced transparency approach
3. Response D (Kimi-K2-Instruct) - Avg Rank: 2.50 - Strong societal perspective
4. Response A (DeepSeek-V3) - Avg Rank: 3.75 - Valid but overly simplistic

🎯 Stage 3: Ethical Synthesis

Recommendation: HYBRID APPROACH with User Empowerment

The council strongly recommends avoiding the either/or trap:

**Implement a "Choose Your Experience" Model:**

1. **Default: Chronological with Smart Filters**
   - Show content in time order by default (transparency)
   - Allow users to filter by content type, topics, or people
   - No hidden algorithmic manipulation of what appears

2. **Optional: "Highlights" Algorithm**
   - Users can opt-in to algorithmic "highlights" view
   - Clearly labeled as algorithm-curated
   - Explain ranking factors in plain language
   - Users can toggle between views anytime

3. **Ethical Algorithm Design Principles:**
   - Optimize for user-defined goals (not just engagement)
   - No amplification of divisive or harmful content for engagement
   - Regular algorithm audits for bias and harm
   - User control over ranking factors

4. **Business Model Alignment:**
   - Don't force algorithmic feeds to maximize ad revenue
   - Consider subscription model where user is the customer
   - Align business incentives with user wellbeing

**Ethical Reasoning:**

✅ **Respects user autonomy** (choice, not coercion)
✅ **Transparency** (clear about what's happening)
✅ **User wellbeing** (optimize for user goals, not addiction)
✅ **Business viability** (optional engagement features)
✅ **Social responsibility** (no amplification of harm)

**Implementation Guidelines:**

- Default to chronological to establish trust
- Make algorithm opt-in, not opt-out
- Provide clear controls and explanations
- Regular transparency reports on algorithm impact
- User research to validate wellbeing improvements

**Risks to Monitor:**

- Engagement metrics may initially drop (vs pure algorithmic)
- Requires ongoing investment in ethical design
- Competitors may not follow ethical approach
- Need to educate users about their choices

Confidence: 88% (strong ethical consensus across frameworks)
```

---

## Installation and Setup

See [INSTALLATION.md](./INSTALLATION.md) for detailed setup instructions.

## Version History

See [CHANGELOG.md](./CHANGELOG.md) for version history and updates.

## Architecture Decisions

See [DECISIONS.md](./DECISIONS.md) for technical decision justifications.
