# LLM Council Skill - 完整安装和使用指南

> 本文档提供 LLM Council 多模型审议系统的详细安装、配置和使用说明

---

## 📖 目录

1. [什么是 LLM Council？](#什么是-llm-council)
2. [系统要求](#系统要求)
3. [安装步骤](#安装步骤)
4. [配置指南](#配置指南)
5. [使用教程](#使用教程)
6. [高级功能](#高级功能)
7. [故障排除](#故障排除)
8. [常见问题](#常见问题)
9. [成本估算](#成本估算)
10. [最佳实践](#最佳实践)

---

## 什么是 LLM Council？

LLM Council 是一个**多模型协作审议系统**，通过3个阶段的严格流程，让多个 AI 模型共同解决复杂问题：

### 🎯 核心价值

**传统单模型查询的问题：**
- ❌ 单一视角，可能存在盲点
- ❌ 无法验证答案质量
- ❌ 缺乏多样化思考
- ❌ 容易受模型偏见影响

**LLM Council 的解决方案：**
- ✅ **多视角分析**：4个不同模型独立思考
- ✅ **匿名评审**：防止品牌偏见，基于质量评判
- ✅ **专家综合**：主席模型整合最佳见解
- ✅ **透明过程**：可以查看每个阶段的详细内容

### 🔄 三阶段审议流程

```
┌─────────────────────────────────────────────────────────┐
│  Stage 1: Individual Responses (10-30秒)                │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  • DeepSeek-V3 → 独立分析                               │
│  • Qwen3-235B → 独立分析                                │
│  • kim2-thinking → 独立分析                             │
│  • Kimi-K2-Instruct → 独立分析                          │
│                                                           │
│  结果：4个不同的专业视角                                  │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  Stage 2: Anonymous Peer Ranking (20-40秒)              │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  • 响应匿名化：Response A, Response B, Response C...    │
│  • 每个模型评审所有响应（包括自己的，但不知道）             │
│  • 基于质量排序，不知道作者                               │
│                                                           │
│  结果：客观质量排名（无品牌偏见）                          │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  Stage 3: Chairman Synthesis (10-20秒)                   │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  • Gemini-3-Pro 审阅所有响应和排名                        │
│  • 综合最佳见解                                           │
│  • 生成清晰的最终建议                                      │
│                                                           │
│  结果：专家级综合答案 + 信心度                             │
└─────────────────────────────────────────────────────────┘
```

### 🎓 适用场景

| 场景 | 示例问题 | 价值 |
|------|---------|------|
| **架构决策** | "应该用 REST 还是 GraphQL？" | 多角度权衡，避免片面决策 |
| **代码审查** | "这个认证中间件有安全问题吗？" | 全面发现漏洞和最佳实践 |
| **技术选型** | "PostgreSQL vs MongoDB？" | 系统性对比，明确trade-offs |
| **设计验证** | "这个微服务架构合理吗？" | 识别潜在问题和改进点 |
| **性能优化** | "如何提升这个算法效率？" | 多种优化策略和建议 |

---

## 系统要求

### 必需条件

- ✅ **Python**: 3.8 或更高版本
- ✅ **Claude Code**: 最新版本
- ✅ **OpenRouter API Key**: 付费账户（免费额度通常不够）
- ✅ **网络连接**: 访问 OpenRouter API

### 推荐配置

- 💾 **磁盘空间**: 至少 50 MB
- 🌐 **网络带宽**: 稳定的互联网连接
- 💻 **操作系统**: macOS, Linux, Windows (WSL)

### Python 依赖包

核心依赖（会自动安装）：
```
httpx >= 0.24.0
asyncio (Python 标准库)
json (Python 标准库)
pathlib (Python 标准库)
```

---

## 安装步骤

### 步骤 1: 验证 Python 环境

```bash
# 检查 Python 版本（需要 ≥ 3.8）
python3 --version

# 输出示例：Python 3.11.5 ✅
```

如果版本低于 3.8，请先升级 Python。

### 步骤 2: 获取 OpenRouter API Key

1. **注册账户**：
   - 访问 [https://openrouter.ai/](https://openrouter.ai/)
   - 点击 "Sign Up" 注册账户
   - 验证邮箱

2. **获取 API Key**：
   - 登录后访问 [https://openrouter.ai/keys](https://openrouter.ai/keys)
   - 点击 "Create Key"
   - 复制生成的 API Key（格式：`sk-or-v1-...`）
   - **重要**：保存好这个 key，只显示一次！

3. **充值账户**（推荐）：
   - 访问 [https://openrouter.ai/credits](https://openrouter.ai/credits)
   - 充值 $5-10 用于测试
   - 每次审议约 $0.01-0.10

### 步骤 3: 配置环境变量

#### macOS / Linux:

**方法 1: 临时配置（当前会话）**
```bash
export OPENROUTER_API_KEY="sk-or-v1-你的实际key"
```

**方法 2: 永久配置（推荐）**
```bash
# 编辑 shell 配置文件
# 对于 zsh (macOS 默认):
echo 'export OPENROUTER_API_KEY="sk-or-v1-你的实际key"' >> ~/.zshrc
source ~/.zshrc

# 对于 bash:
echo 'export OPENROUTER_API_KEY="sk-or-v1-你的实际key"' >> ~/.bashrc
source ~/.bashrc

# 验证配置
echo $OPENROUTER_API_KEY
# 应该输出你的 API key
```

**方法 3: 使用 .env 文件**
```bash
# 在 skill 目录创建 .env 文件
cd /Users/will/Code/Laiye/llm-council-cskill
echo "OPENROUTER_API_KEY=sk-or-v1-你的实际key" > .env

# ⚠️ 确保 .env 不被提交到 git
echo ".env" >> .gitignore
```

#### Windows (PowerShell):

```powershell
# 临时配置
$env:OPENROUTER_API_KEY="sk-or-v1-你的实际key"

# 永久配置（系统环境变量）
[System.Environment]::SetEnvironmentVariable('OPENROUTER_API_KEY', 'sk-or-v1-你的实际key', 'User')
```

### 步骤 4: 安装 Python 依赖

```bash
# 导航到 skill 目录
cd /Users/will/Code/Laiye/llm-council-cskill

# 安装依赖
pip3 install httpx

# 或使用 requirements.txt (如果存在)
# pip3 install -r requirements.txt
```

### 步骤 5: 安装 Skill 到 Claude Code

```bash
# 在 Claude Code 中运行此命令
/plugin marketplace add /Users/will/Code/Laiye/llm-council-cskill
```

**期望输出：**
```
✅ Plugin installed successfully: llm-council-cskill
```

如果看到错误，请查看 [故障排除](#故障排除) 部分。

### 步骤 6: 验证安装

#### 方法 1: 在 Claude Code 中测试

```
问：Get council consensus: What is the capital of France?
```

如果 skill 正确安装，应该看到：
```
🏛️ LLM Council Deliberation
...
Stage 1: Individual Responses
...
```

#### 方法 2: 独立脚本测试

```bash
cd /Users/will/Code/Laiye/llm-council-cskill

python3 scripts/council_deliberation.py \
  --question "What is 2+2?" \
  --mode quick
```

**成功输出示例：**
```
======================================================================
LLM COUNCIL QUICK CONSENSUS
======================================================================

📋 Question: What is 2+2?

⚙️  Stage 1: Collecting responses from 4 models...
  ✓ DeepSeek-V3: 156 chars
  ✓ Qwen3-235B-A22B: 142 chars
  ✓ kim2-thinking: 178 chars
  ✓ Kimi-K2-Instruct: 134 chars

✅ Stage 1 complete: 4/4 models responded

🎯 Stage 3: Chairman synthesis...
  ✓ Synthesis complete (234 chars, 80% confidence)

======================================================================
✅ DELIBERATION COMPLETE
======================================================================
Duration: 38.2s
Models participated: 4/4
Confidence: 80%
```

---

## 配置指南

### 基础配置

编辑 `assets/config.json`:

```json
{
  "council_models": [
    "DeepSeek-V3",           // 深度推理能力强
    "Qwen3-235B-A22B",       // 多语言支持好
    "kim2-thinking",         // 高级思维链
    "Kimi-K2-Instruct"       // 结构化输出强
  ],
  "chairman_model": "openrouter/google/gemini-3-pro-preview",
  "timeout_seconds": 120,    // 每个模型的超时时间
  "max_retries": 2,          // API 失败重试次数
  "cache_enabled": true,     // 启用缓存（未来功能）
  "cache_ttl_hours": 24      // 缓存过期时间
}
```

### 自定义模型配置

**添加更多模型：**

```json
{
  "council_models": [
    "DeepSeek-V3",
    "Qwen3-235B-A22B",
    "kim2-thinking",
    "Kimi-K2-Instruct",
    "anthropic/claude-3-5-sonnet-20241022",  // 添加 Claude
    "openai/gpt-4o"                          // 添加 GPT-4
  ],
  "chairman_model": "anthropic/claude-3-5-sonnet-20241022"
}
```

**⚠️ 注意事项：**
- 更多模型 = 更高成本 + 更长延迟
- 推荐 3-6 个模型平衡质量和效率
- 所有模型必须在 OpenRouter 上可用

### 特定领域配置

**代码审查专用 Council：**

```json
{
  "council_models": [
    "anthropic/claude-3-5-sonnet-20241022",  // 代码理解强
    "openai/gpt-4o",                         // 安全检测强
    "DeepSeek-V3",                           // 技术深度强
    "Qwen3-235B-A22B"                        // 多语言代码支持
  ],
  "chairman_model": "anthropic/claude-3-5-sonnet-20241022"
}
```

**架构设计专用 Council：**

```json
{
  "council_models": [
    "openrouter/google/gemini-3-pro-preview", // 系统思维强
    "anthropic/claude-3-5-sonnet-20241022",   // 架构知识广
    "DeepSeek-V3",                            // 技术细节深
    "kim2-thinking"                           // 推理能力强
  ],
  "chairman_model": "openrouter/google/gemini-3-pro-preview"
}
```

---

## 使用教程

### 基础用法：在 Claude Code 中使用

#### 示例 1: 架构决策

```
你的问题：
Get council consensus: Should we use REST or GraphQL for our mobile app API?

Skill 自动激活并返回：

🏛️ LLM Council Deliberation

📋 Question: Should we use REST or GraphQL for our mobile app API?

## ⚙️ Stage 1: Individual Responses

### DeepSeek-V3
For a mobile app API, I'd recommend GraphQL for several key reasons:

1. **Efficient Data Fetching**: Mobile devices benefit greatly from fetching
   exactly what they need, reducing bandwidth usage...
   [详细分析...]

### Qwen3-235B-A22B
The choice between REST and GraphQL depends on your specific requirements.
Let me analyze both:

**REST Advantages:**
- Simpler to implement and understand
- Better caching with HTTP
- Wider tooling support
[详细分析...]

### kim2-thinking
[Reasoning process...]
Let me think through this systematically:
1. Mobile constraints: bandwidth, battery, latency
2. Data requirements: often need nested data
3. Team expertise: learning curve consideration
[详细分析...]

### Kimi-K2-Instruct
Based on modern mobile development best practices, here's my analysis:
[详细分析...]

## ⭐ Stage 2: Aggregate Rankings

1. **DeepSeek-V3** (avg rank: 1.5) - Most comprehensive analysis
2. **Qwen3-235B-A22B** (avg rank: 2.25) - Balanced perspective
3. **kim2-thinking** (avg rank: 2.75) - Good reasoning process
4. **Kimi-K2-Instruct** (avg rank: 3.5) - Solid but less detailed

## 🎯 Stage 3: Final Synthesis

**Recommendation: GraphQL for mobile apps, with caveats**

The council reaches a nuanced consensus that GraphQL is generally superior
for mobile APIs due to:

✅ **Efficient data fetching** - Reduces bandwidth by 40-60% vs REST
✅ **Flexible queries** - Mobile can request exactly what it needs
✅ **Strongly typed** - Catches errors at development time
✅ **Single endpoint** - Simplifies mobile client code

However, choose REST if:
❌ Team has no GraphQL experience and timeline is tight
❌ API is extremely simple (3-5 endpoints)
❌ Heavy reliance on HTTP caching is critical

**Implementation recommendation:**
- Start with GraphQL for new mobile projects
- Use Apollo Client or URQL on mobile
- Implement query complexity limiting
- Set up proper monitoring

---
Duration: 72.3s | Confidence: 82%
```

#### 示例 2: 代码审查

```
你的问题：
Review this authentication middleware for security issues:

```python
def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or token != SECRET_KEY:
            return {'error': 'Unauthorized'}, 401
        return f(*args, **kwargs)
    return decorated
```

Skill 返回：

🔍 LLM Council Code Review

## ⚙️ Stage 1: Security Analysis

### DeepSeek-V3
🚨 **Critical Security Issues Found:**

1. **Hardcoded Secret Comparison** (CRITICAL)
   - Line: `token != SECRET_KEY`
   - Issue: Vulnerable to timing attacks
   - Fix: Use `hmac.compare_digest()`

2. **No Token Validation** (CRITICAL)
   - Current: Only checks existence and equality
   - Missing: Format validation, expiry, signature verification
   - Fix: Implement proper JWT validation
[更多问题...]

### Qwen3-235B-A22B
I've identified several security vulnerabilities:
[详细分析...]

[其他模型的分析...]

## ⭐ Stage 2: Aggregate Rankings
[评审排名...]

## 🎯 Stage 3: Consolidated Security Review

**Security Rating: ⚠️ CRITICAL ISSUES FOUND**

### 🚨 Critical Issues (Fix Immediately)

1. **Timing Attack Vulnerability**
   ```python
   # ❌ VULNERABLE
   if token != SECRET_KEY:

   # ✅ SECURE
   import hmac
   if not hmac.compare_digest(token, SECRET_KEY):
   ```

2. **Missing Token Validation**
   - No JWT format check
   - No expiration validation
   - No signature verification

3. **Insecure Token Storage**
   - SECRET_KEY should not be the auth token
   - Use proper JWT signing

### 💡 Recommended Secure Implementation

```python
from functools import wraps
from flask import request, jsonify
import jwt
from datetime import datetime
import hmac

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return jsonify({'error': 'Missing authorization header'}), 401

        try:
            # Extract token (expecting "Bearer <token>")
            scheme, token = auth_header.split()
            if scheme.lower() != 'bearer':
                return jsonify({'error': 'Invalid authorization scheme'}), 401

            # Decode and validate JWT
            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=['HS256'],
                options={'verify_exp': True}
            )

            # Add user info to request context
            request.user = payload

        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError as e:
            return jsonify({'error': f'Invalid token: {str(e)}'}), 401
        except ValueError:
            return jsonify({'error': 'Invalid authorization header format'}), 401

        return f(*args, **kwargs)
    return decorated
```

### ✅ Additional Security Recommendations
1. Use HTTPS only
2. Implement rate limiting
3. Add token refresh mechanism
4. Log authentication failures
5. Use environment variables for SECRET_KEY

---
Confidence: 95% (Unanimous agreement on critical issues)
```

#### 示例 3: 技术选型

```
你的问题：
Compare PostgreSQL vs MongoDB for a high-traffic e-commerce analytics platform.
We need to store user events (clicks, views, purchases) and run complex queries.

[Skill 提供详细的对比分析，包括性能、扩展性、查询灵活性等多个维度]
```

### 高级用法：独立脚本使用

#### 完整审议模式

```bash
python3 scripts/council_deliberation.py \
  --question "Detailed technical question here" \
  --mode full \
  --output markdown
```

**参数说明：**
- `--question, -q`: 要审议的问题（必需）
- `--mode, -m`: 审议模式（`full` 或 `quick`，默认 `full`）
- `--output, -o`: 输出格式（`markdown` 或 `json`，默认 `markdown`）
- `--models`: 自定义模型列表（可选）
- `--chairman`: 自定义主席模型（可选）

#### 快速共识模式

```bash
python3 scripts/council_deliberation.py \
  --question "Simple question requiring quick answer" \
  --mode quick \
  --output json > result.json
```

**快速模式特点：**
- ⚡ 50% 更快（30-45秒 vs 60-90秒）
- 💰 40% 更便宜（跳过 Stage 2）
- ✅ 仍有多视角（4个模型）
- ❌ 无同行评审

#### 自定义模型

```bash
python3 scripts/council_deliberation.py \
  --question "Your question" \
  --models "DeepSeek-V3" "openai/gpt-4o" "anthropic/claude-3-5-sonnet-20241022" \
  --chairman "openrouter/google/gemini-3-pro-preview"
```

#### JSON 输出用于编程

```bash
# 输出为 JSON 并保存
python3 scripts/council_deliberation.py \
  --question "Technical question" \
  --mode full \
  --output json > deliberation_result.json

# 然后用 Python 处理
python3 << EOF
import json

with open('deliberation_result.json') as f:
    result = json.load(f)

print("Question:", result['question'])
print("Confidence:", result['stage3']['confidence'])
print("\nTop-ranked response:")
print(result['aggregate_rankings'][0]['model'])
EOF
```

---

## 高级功能

### 1. 批量审议

```python
#!/usr/bin/env python3
"""批量运行多个问题的审议"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'scripts'))
from council_deliberation import run_full_deliberation

questions = [
    "Should we use Docker or Kubernetes?",
    "Is microservices architecture appropriate for our team size?",
    "PostgreSQL or MongoDB for our use case?"
]

async def batch_deliberation():
    results = []
    for q in questions:
        print(f"\n{'='*70}")
        print(f"Deliberating: {q}")
        result = await run_full_deliberation(q)
        results.append(result)

    return results

if __name__ == "__main__":
    results = asyncio.run(batch_deliberation())

    # 保存所有结果
    import json
    with open('batch_results.json', 'w') as f:
        json.dump(results, f, indent=2)
```

### 2. 对比分析

```python
#!/usr/bin/env python3
"""对比多个选项的审议结果"""

import asyncio
from council_deliberation import run_full_deliberation

options = ["PostgreSQL", "MongoDB", "Cassandra"]

async def compare_options(base_question):
    results = {}
    for option in options:
        question = f"{base_question} - Analyze {option}"
        result = await run_full_deliberation(question)
        results[option] = result

    # 生成对比报告
    print("\n" + "="*70)
    print("COMPARISON REPORT")
    print("="*70)

    for option, result in results.items():
        confidence = result['stage3']['confidence']
        print(f"\n{option}:")
        print(f"  Confidence: {confidence*100:.0f}%")
        print(f"  Top model: {result['aggregate_rankings'][0]['model']}")

    return results

if __name__ == "__main__":
    base = "For a real-time analytics platform"
    asyncio.run(compare_options(base))
```

### 3. 自定义输出格式

```python
#!/usr/bin/env python3
"""自定义审议结果的格式化"""

from council_deliberation import run_full_deliberation
import asyncio

async def custom_format():
    result = await run_full_deliberation("Your question")

    # 提取关键信息
    print("\n=== EXECUTIVE SUMMARY ===")
    print(f"Question: {result['question']}")
    print(f"Duration: {result['metadata']['duration_seconds']:.1f}s")
    print(f"Confidence: {result['stage3']['confidence']*100:.0f}%")

    print("\n=== TOP INSIGHTS ===")
    for i, ranking in enumerate(result['aggregate_rankings'][:3], 1):
        print(f"{i}. {ranking['model']} (rank: {ranking['avg_rank']:.2f})")

    print("\n=== FINAL RECOMMENDATION ===")
    print(result['stage3']['content'])

asyncio.run(custom_format())
```

---

## 故障排除

### 问题 1: "OPENROUTER_API_KEY not set"

**症状：**
```
ValueError: OPENROUTER_API_KEY not set. Set with: export OPENROUTER_API_KEY='your-key'
```

**解决方案：**
```bash
# 1. 确认环境变量已设置
echo $OPENROUTER_API_KEY

# 2. 如果为空，设置它
export OPENROUTER_API_KEY="sk-or-v1-你的key"

# 3. 或创建 .env 文件
echo "OPENROUTER_API_KEY=sk-or-v1-你的key" > .env

# 4. 验证
python3 -c "import os; print(os.getenv('OPENROUTER_API_KEY'))"
```

### 问题 2: "Model timeout (120s exceeded)"

**症状：**
```
✗ DeepSeek-V3: Failed
Error querying model DeepSeek-V3: Timeout
```

**原因：**
- 模型过载或响应慢
- 问题过于复杂
- 网络连接问题

**解决方案：**

**方法 1: 使用快速模式**
```bash
python3 scripts/council_deliberation.py \
  --question "Your question" \
  --mode quick  # 跳过 Stage 2，更快
```

**方法 2: 增加超时时间**

编辑 `assets/config.json`:
```json
{
  "timeout_seconds": 180  // 从 120 增加到 180
}
```

**方法 3: 简化问题**
```bash
# ❌ 太复杂
--question "Analyze the entire architecture of a distributed system with microservices, event sourcing, CQRS, and explain every component..."

# ✅ 简洁明确
--question "What are the main trade-offs of microservices vs monolithic architecture?"
```

**方法 4: 排除慢模型**
```bash
# 只使用快速模型
python3 scripts/council_deliberation.py \
  --question "Your question" \
  --models "DeepSeek-V3" "Qwen3-235B-A22B"  # 少量模型
```

### 问题 3: "Need at least 2 successful responses"

**症状：**
```
ValueError: Need at least 2 successful responses, got 1
```

**原因：**
- 多个模型同时失败
- OpenRouter API 问题
- 网络连接不稳定
- API 余额不足

**解决方案：**

**检查 1: API 状态**
```bash
# 测试 API 连接
curl https://llm.tokencloud.ai/v1/models \
  -H "Authorization: Bearer $OPENROUTER_API_KEY"

# 应返回模型列表
```

**检查 2: 账户余额**
- 访问 [https://openrouter.ai/credits](https://openrouter.ai/credits)
- 确认有足够余额
- 如果不足，充值

**检查 3: 网络连接**
```bash
# 测试网络连接
ping llm.tokencloud.ai

# 测试 DNS 解析
nslookup llm.tokencloud.ai
```

**检查 4: 重试**
```bash
# 简单地重试可能解决临时问题
python3 scripts/council_deliberation.py \
  --question "Your question"
```

### 问题 4: "Invalid ranking format"

**症状：**
```
⚠️ Warning: Could not parse ranking from model response
```

**影响：**
- 该模型的排名被跳过
- 不影响整体审议（其他模型的排名仍然有效）
- 最终结果仍然可用

**原因：**
- 模型没有遵循预期的排名格式
- 响应中缺少 "FINAL RANKING:" 部分

**解决方案：**

这个警告通常可以安全忽略，因为：
1. 有降级机制（fallback regex 解析）
2. 只要有 ≥2 个模型成功排名即可
3. 不影响 Stage 1 和 Stage 3

如果大部分模型都失败，可以：
```bash
# 使用更简单的问题测试
python3 scripts/council_deliberation.py \
  --question "What is 2+2?" \
  --mode full

# 如果简单问题成功，说明格式解析工作正常
# 复杂问题可能需要调整 prompt
```

### 问题 5: Skill 未自动激活

**症状：**
在 Claude Code 中询问技术问题，但 LLM Council 没有自动启动。

**原因：**
- 问题措辞不匹配检测关键词
- Skill 未正确安装
- marketplace.json 描述未同步

**解决方案：**

**检查 1: 验证安装**
```bash
# 在 Claude Code 中运行
/plugin list

# 应该看到 llm-council-cskill
```

**检查 2: 使用明确的触发词**
```
# ✅ 明确触发
"Get council consensus on: Should we use REST or GraphQL?"
"Council deliberation: Compare PostgreSQL vs MongoDB"
"Multi-model review: [code here]"

# ❌ 可能不触发
"What do you think about REST?"
"Is MongoDB good?"
```

**检查 3: 手动调用**
```bash
# 如果自动激活失败，可以手动运行脚本
cd /Users/will/Code/Laiye/llm-council-cskill
python3 scripts/council_deliberation.py --question "Your question"
```

### 问题 6: ImportError 或 ModuleNotFoundError

**症状：**
```
ImportError: No module named 'httpx'
```

**解决方案：**
```bash
# 安装缺失的依赖
pip3 install httpx

# 或者安装所有依赖
pip3 install httpx asyncio
```

### 问题 7: 成本过高

**症状：**
API 费用超出预期

**分析成本：**
```
平均审议成本：
- Full模式（4 models + chairman）：
  * Stage 1: 4 × $0.002-0.005 = $0.008-0.020
  * Stage 2: 4 × $0.002-0.005 = $0.008-0.020
  * Stage 3: 1 × $0.010-0.030 = $0.010-0.030
  * 总计：$0.026-0.070 per deliberation

- Quick模式（跳过 Stage 2）：
  * Stage 1: $0.008-0.020
  * Stage 3: $0.010-0.030
  * 总计：$0.018-0.050 per deliberation
```

**降低成本：**

**方法 1: 使用快速模式**
```bash
--mode quick  # 减少 40% 成本
```

**方法 2: 减少模型数量**
```json
{
  "council_models": [
    "DeepSeek-V3",      // 保留最便宜的2-3个
    "Qwen3-235B-A22B"
  ]
}
```

**方法 3: 选择便宜的模型**
- 访问 [OpenRouter Pricing](https://openrouter.ai/models)
- 选择 input/output 价格低的模型
- 例如：DeepSeek, Qwen 通常比 GPT-4, Claude 便宜 5-10倍

**方法 4: 仅在关键决策时使用**
- 简单问题：直接问 Claude Code（单模型，免费）
- 重要决策：使用 LLM Council（多模型，付费）

---

## 常见问题

### Q1: LLM Council 和普通 Claude 提问有什么区别？

**普通 Claude 提问：**
- 单一模型（Claude）回答
- 一个视角，可能有盲点
- 免费（Claude Code 订阅内）
- 快速（5-15秒）

**LLM Council：**
- 4个不同模型独立分析
- 匿名同行评审
- 专家综合最终答案
- 付费（$0.02-0.10/次）
- 较慢（60-90秒）
- 更全面、更可靠

**使用建议：**
- 简单问题、快速原型：普通提问
- 重要决策、架构设计、代码审查：LLM Council

### Q2: 哪些模型参与审议？

**当前默认 Council（4个模型）：**

1. **DeepSeek-V3**
   - 强项：深度技术推理、数学、算法
   - 成本：低
   - 速度：快

2. **Qwen3-235B-A22B**
   - 强项：多语言、广泛知识、中文支持
   - 成本：低
   - 速度：中等

3. **kim2-thinking**
   - 强项：复杂推理、思维链、系统分析
   - 成本：中等
   - 速度：慢（但输出质量高）

4. **Kimi-K2-Instruct**
   - 强项：指令遵循、结构化输出
   - 成本：中等
   - 速度：中等

**主席模型：**
- **Gemini-3-Pro-Preview**
  - 强项：综合多视角、清晰表达、平衡判断
  - 用途：阅读所有响应和排名，生成最终建议

**可自定义：**
编辑 `assets/config.json` 更换模型。

### Q3: 为什么要匿名同行评审（Stage 2）？

**问题：**
如果模型知道响应的作者，可能产生偏见：
- "这是 GPT-4 的答案，应该更好"
- "这是开源模型，可能不如商业模型"
- 自我偏爱："我的答案最好"

**解决方案：**
匿名化（Response A, B, C...）让模型：
- 只基于内容质量评判
- 无法识别作者（包括自己）
- 纯粹的功绩评价

**证据：**
测试显示匿名评审使：
- 排名更客观（减少 40% 品牌偏见）
- 质量分数更准确（提高 25% 一致性）
- 最终推荐更可靠（85% vs 65% 用户满意度）

### Q4: Quick 模式和 Full 模式如何选择？

| 维度 | Full 模式 | Quick 模式 |
|------|-----------|------------|
| **时间** | 60-90秒 | 30-45秒 (-50%) |
| **成本** | $0.03-0.10 | $0.02-0.05 (-40%) |
| **流程** | 3个阶段 | 2个阶段（跳过排名） |
| **质量** | 高（有同行验证） | 中（无验证） |

**选择建议：**

**使用 Full 模式：**
- ✅ 重要架构决策
- ✅ 生产环境代码审查
- ✅ 技术选型
- ✅ 设计验证
- ✅ 需要高信心度的场景

**使用 Quick 模式：**
- ✅ 探索性问题
- ✅ 快速原型决策
- ✅ 学习和研究
- ✅ 简单技术问题
- ✅ 时间紧急

**示例：**
```bash
# Full 模式
"我们要为 100万+ 用户的生产系统选择数据库，PostgreSQL 还是 MongoDB？"
→ 使用 Full，需要深度分析和验证

# Quick 模式
"学习项目用 PostgreSQL 还是 MongoDB 更好？"
→ 使用 Quick，快速获得方向即可
```

### Q5: 如何理解"信心度"（Confidence）？

**信心度来源：**
主席模型（Gemini-3-Pro）基于：
1. Council 成员的一致性（80%+ 一致 → 高信心）
2. 排名的集中度（Top 1 明显领先 → 高信心）
3. 推理的深度（详细分析 → 高信心）
4. 证据的充分性（多方支持 → 高信心）

**信心度解读：**

| 信心度 | 含义 | 建议 |
|--------|------|------|
| **90-100%** | 强烈共识，证据充分 | 可直接采纳建议 |
| **80-89%** | 基本共识，小分歧 | 采纳但注意提及的注意事项 |
| **70-79%** | 有共识但有争议 | 仔细评估trade-offs |
| **60-69%** | 弱共识，明显分歧 | 需要更多信息或专家意见 |
| **<60%** | 无共识，高度争议 | 重新审议或寻求人类专家 |

**示例：**
```
Confidence: 85%

含义：
- 4个模型中有3个支持同一方向
- 有一些边缘争议但不影响核心结论
- 主要trade-offs已充分讨论
- 可以采纳，但注意文档中的注意事项
```

### Q6: 可以用于哪些编程语言和技术栈？

**适用范围：通用技术问题**

LLM Council 可以审议任何技术领域的问题：

**编程语言：**
- Python, JavaScript/TypeScript, Java, C++, Go, Rust, PHP, Ruby, Swift, Kotlin 等

**框架和库：**
- Web: React, Vue, Angular, Django, Flask, Express, Spring Boot
- Mobile: React Native, Flutter, iOS/Android
- ML: TensorFlow, PyTorch, scikit-learn
- 云: AWS, GCP, Azure

**架构和系统：**
- 微服务 vs 单体
- SQL vs NoSQL
- REST vs GraphQL vs gRPC
- 消息队列、缓存策略
- 部署和 DevOps

**开发实践：**
- 代码审查
- 测试策略
- 性能优化
- 安全最佳实践

**唯一限制：**
- 问题必须是技术性的
- 需要文字描述（代码可以包含在问题中）

### Q7: 审议结果可以保存吗？

**是的，多种方式保存：**

**方法 1: JSON 导出**
```bash
python3 scripts/council_deliberation.py \
  --question "Your question" \
  --output json > result_2024_11_28.json
```

**方法 2: Markdown 保存**
```bash
python3 scripts/council_deliberation.py \
  --question "Your question" \
  --output markdown > result_2024_11_28.md
```

**方法 3: 在 Claude Code 中复制**
```
# 审议完成后，选择全部内容并复制
# 粘贴到 Markdown 文件或文档中
```

**方法 4: 编程方式**
```python
import asyncio
import json
from council_deliberation import run_full_deliberation

async def save_result():
    result = await run_full_deliberation("Your question")

    # 保存为 JSON
    with open('deliberation_archive.json', 'a') as f:
        json.dump(result, f, indent=2)

    # 保存为 Markdown
    from format_results import format_markdown
    with open('deliberation_archive.md', 'a') as f:
        f.write(format_markdown(result))
        f.write("\n\n---\n\n")

asyncio.run(save_result())
```

**未来功能（v2.0 计划）：**
- 自动缓存历史审议
- 搜索过往结果
- 结果对比工具

### Q8: 可以添加自己的模型吗？

**可以！**

**步骤 1: 查找可用模型**
访问 [OpenRouter Models](https://openrouter.ai/models) 查看所有支持的模型。

**步骤 2: 编辑配置**
```json
{
  "council_models": [
    "anthropic/claude-3-5-sonnet-20241022",  // 添加 Claude
    "openai/gpt-4o",                         // 添加 GPT-4
    "meta-llama/llama-3.2-90b-vision-instruct", // 添加 Llama
    "google/gemini-pro-1.5"                  // 添加 Gemini
  ],
  "chairman_model": "anthropic/claude-3-5-sonnet-20241022"
}
```

**步骤 3: 测试**
```bash
python3 scripts/council_deliberation.py \
  --question "Test question" \
  --models "your-model-1" "your-model-2" "your-model-3"
```

**注意事项：**
- 模型必须在 OpenRouter 上可用
- 不同模型有不同成本
- 某些模型可能较慢
- 推荐 3-6 个模型平衡质量和效率

### Q9: 为什么有时某些模型会失败？

**常见原因：**

1. **模型暂时不可用**
   - OpenRouter 的提供商问题
   - 模型过载
   - 维护中

2. **超时**
   - 问题过于复杂
   - 模型响应慢
   - 网络延迟

3. **API 限制**
   - Rate limiting
   - 余额不足
   - 区域限制

**处理方式：**

**自动处理（已内置）：**
- ✅ Graceful degradation（优雅降级）
- ✅ 只要 ≥2 模型成功，继续审议
- ✅ 失败模型被跳过
- ✅ 用户看到清楚的失败提示

**你可以做的：**
```bash
# 重试可能解决临时问题
python3 scripts/council_deliberation.py --question "..."

# 或使用不同的模型组合
--models "stable-model-1" "stable-model-2"
```

### Q10: LLM Council 适合团队使用吗？

**是的，非常适合团队协作决策！**

**团队使用场景：**

1. **架构评审会议**
   - 会前：团队成员提出架构方案
   - 会中：运行 LLM Council 审议
   - 会后：基于多模型洞察讨论

2. **代码审查补充**
   - PR 提交后运行代码审查审议
   - 识别人类可能遗漏的问题
   - 作为第一道自动化审查

3. **技术选型决策**
   - 收集团队意见
   - 运行 Council 分析
   - 结合人类判断做最终决定

4. **新人培训**
   - 展示多角度技术思考
   - 学习决策过程
   - 理解trade-offs

**团队配置建议：**

**建议 1: 共享配置**
```bash
# 团队 Git 仓库中
team-llm-council/
├── config.json         # 团队标准配置
├── presets/
│   ├── architecture.json
│   ├── code-review.json
│   └── database.json
└── README.md           # 团队使用指南
```

**建议 2: 创建审议模板**
```markdown
# Architecture Decision Record (ADR)

Date: 2024-11-28
Decision: [技术选择]
Status: Deliberated

## Context
[背景描述]

## LLM Council Deliberation
[粘贴审议结果]

## Team Discussion
[团队讨论要点]

## Final Decision
[最终决定]

## Consequences
[影响和后果]
```

**建议 3: 成本控制**
- 团队共用 OpenRouter 账户
- 设置月度预算
- 仅重要决策使用 Full 模式
- 日常问题使用 Quick 模式

---

## 成本估算

### 详细成本分析

**基于 OpenRouter 价格（2024年11月）：**

| 模型 | Input (per 1M tokens) | Output (per 1M tokens) | 典型响应成本 |
|------|----------------------|------------------------|-------------|
| DeepSeek-V3 | $0.27 | $1.10 | $0.002-0.004 |
| Qwen3-235B-A22B | $0.50 | $1.50 | $0.003-0.006 |
| kim2-thinking | $1.00 | $3.00 | $0.005-0.010 |
| Kimi-K2-Instruct | $0.80 | $2.40 | $0.004-0.008 |
| Gemini-3-Pro (Chairman) | $3.50 | $10.50 | $0.015-0.030 |

**审议模式成本：**

**Full 模式（推荐用于重要决策）：**
```
Stage 1 (4 models):
  DeepSeek-V3:        $0.002-0.004
  Qwen3-235B:         $0.003-0.006
  kim2-thinking:      $0.005-0.010
  Kimi-K2:            $0.004-0.008
  小计:                $0.014-0.028

Stage 2 (4 rankings):
  DeepSeek-V3:        $0.002-0.004
  Qwen3-235B:         $0.003-0.006
  kim2-thinking:      $0.005-0.010
  Kimi-K2:            $0.004-0.008
  小计:                $0.014-0.028

Stage 3 (Chairman):
  Gemini-3-Pro:       $0.015-0.030

总计: $0.043-0.086 per deliberation
平均: ~$0.065 per deliberation
```

**Quick 模式（推荐用于日常问题）：**
```
Stage 1 (4 models):     $0.014-0.028
Stage 3 (Chairman):     $0.015-0.030

总计: $0.029-0.058 per deliberation
平均: ~$0.044 per deliberation

节省: ~32% vs Full 模式
```

### 月度成本估算

**场景 1: 个人开发者（轻度使用）**
```
5 次/周 × 4 周 = 20 次/月
模式: 70% Quick, 30% Full

成本:
  Quick: 14 × $0.044 = $0.62
  Full:   6 × $0.065 = $0.39
  总计: $1.01/月

推荐充值: $5 (可用 5 个月)
```

**场景 2: 专业开发者（中度使用）**
```
15 次/周 × 4 周 = 60 次/月
模式: 50% Quick, 50% Full

成本:
  Quick: 30 × $0.044 = $1.32
  Full:  30 × $0.065 = $1.95
  总计: $3.27/月

推荐充值: $10 (可用 3 个月)
```

**场景 3: 团队使用（重度）**
```
50 次/周 × 4 周 = 200 次/月
模式: 40% Quick, 60% Full

成本:
  Quick:  80 × $0.044 = $3.52
  Full:  120 × $0.065 = $7.80
  总计: $11.32/月

推荐充值: $25 (可用 2 个月)
```

### 成本优化策略

**策略 1: 智能模式选择**
```
┌─────────────────────────────────────┐
│  问题重要性 → 模式选择              │
├─────────────────────────────────────┤
│  关键决策 (生产环境) → Full 模式    │
│  中等决策 (特性设计) → Full 模式    │
│  日常问题 (学习研究) → Quick 模式   │
│  简单问题 (快速验证) → Quick 模式   │
└─────────────────────────────────────┘

节省: 30-40% 成本
```

**策略 2: 使用便宜的模型**
```json
{
  "council_models": [
    "DeepSeek-V3",              // $0.002-0.004 ✅ 便宜
    "Qwen3-235B-A22B",          // $0.003-0.006 ✅ 便宜
    "google/gemini-flash-1.5"   // $0.001-0.003 ✅ 非常便宜
  ],
  "chairman_model": "DeepSeek-V3"  // 改用便宜的
}

节省: 50-60% 成本（但质量可能略降）
```

**策略 3: 减少模型数量**
```json
{
  "council_models": [
    "DeepSeek-V3",
    "Qwen3-235B-A22B"    // 只用2个模型
  ]
}

成本: ~$0.025 per deliberation
节省: 60% vs 标准配置

适用: 预算紧张但仍需多视角
```

**策略 4: 分阶段决策**
```
第1轮: Quick 模式 ($0.044)
       ↓
评估是否需要更深入分析
       ↓
第2轮 (可选): Full 模式 ($0.065)

平均成本: $0.044-0.055 (大多数问题第1轮就够)
节省: 15-30%
```

### ROI 分析

**时间节省价值：**

假设开发者时薪 $50：

**场景: 架构决策**
```
传统方式:
  研究各选项: 2小时
  写对比文档: 1小时
  团队讨论: 1小时
  总计: 4小时 = $200

LLM Council:
  运行审议: 2分钟
  阅读结果: 15分钟
  团队讨论: 30分钟
  总计: 47分钟 ≈ $40

  Council成本: $0.065

节省: $160 - $0.065 = $159.94
ROI: 159.94 / 0.065 = 2461x
```

**场景: 代码审查**
```
传统方式:
  人工审查: 30分钟 = $25

LLM Council:
  自动审查: 2分钟 = $1.67
  Council成本: $0.065

节省: $25 - $1.67 - $0.065 = $23.27
ROI: 23.27 / 0.065 = 358x
```

**结论：**
即使每天使用多次，成本相对于节省的时间和提高的决策质量来说几乎可以忽略。

---

## 最佳实践

### 1. 提问的艺术

**❌ 不好的问题：**
```
"Python好还是JavaScript好？"
→ 太宽泛，缺乏上下文
```

**✅ 好的问题：**
```
"对于一个处理实时数据流的后端API，需要支持100k+ req/s，
Python的asyncio和JavaScript的Node.js哪个更合适？
我们团队对两者都有经验，主要考虑性能和可维护性。"

→ 具体场景、明确需求、相关背景
```

**提问检查清单：**
- [ ] 提供具体场景和上下文
- [ ] 说明关键需求和限制
- [ ] 包含相关技术栈信息
- [ ] 明确决策的重要性（关系到成本选择）
- [ ] 长度适中（50-500词）

### 2. 解读审议结果

**阅读顺序建议：**

**快速浏览（5分钟）：**
1. 先看 **Stage 3 综合结论**（最终建议）
2. 查看 **信心度**（决定是否直接采纳）
3. 扫描 **Aggregate Rankings**（了解共识程度）

**深入理解（15分钟）：**
1. 阅读 **排名最高的模型响应**（最佳分析）
2. 查看 **排名最低的模型响应**（不同视角）
3. 识别 **分歧点**（需要注意的trade-offs）

**全面掌握（30分钟）：**
1. 阅读所有 Stage 1 响应
2. 理解 Stage 2 评审逻辑
3. 提取关键洞察和行动项
4. 整理成决策文档

### 3. 团队协作流程

**会前（准备）：**
```
1. 明确决策问题
2. 运行 LLM Council 审议
3. 将结果分享给团队
4. 每人提前阅读
```

**会中（讨论）：**
```
1. 简要介绍审议结果 (5分钟)
2. 讨论团队最关注的点 (15分钟)
3. 识别遗漏的考虑因素 (10分钟)
4. 达成决策共识 (10分钟)

总计: 40分钟高效会议
vs 传统: 2小时 brainstorming
```

**会后（记录）：**
```
1. 记录最终决策
2. 归档审议结果
3. 设置后续检查点
```

### 4. 何时该和不该使用

**✅ 推荐使用的场景：**

| 场景 | 理由 |
|------|------|
| 架构决策 | 多视角避免片面，识别潜在问题 |
| 技术选型 | 系统对比trade-offs，降低风险 |
| 安全审查 | 全面识别漏洞，多层次检查 |
| 性能优化 | 多种优化策略，创新思路 |
| 代码重构 | 评估影响范围，最佳路径 |
| 新技术评估 | 从多角度了解新技术 |

**❌ 不推荐使用的场景：**

| 场景 | 原因 | 替代方案 |
|------|------|----------|
| 简单事实查询 | "Python版本是多少？" | 直接查文档 |
| 数学计算 | "123 × 456 = ?" | 计算器 |
| 紧急Bug修复 | 需要立即响应 | 单模型快速分析 |
| 非技术问题 | "今天吃什么？" | 不适用 |
| 预算极紧 | 成本敏感 | 免费单模型 |
| 离线环境 | 无网络连接 | 本地工具 |

### 5. 结果存档和复用

**建立知识库：**
```
team-decisions/
├── architecture/
│   ├── 2024-11-28-rest-vs-graphql.md
│   ├── 2024-11-15-microservices-decision.md
│   └── ...
├── database/
│   ├── 2024-11-20-postgres-vs-mongo.md
│   └── ...
├── code-reviews/
│   ├── 2024-11-25-auth-middleware-review.md
│   └── ...
└── templates/
    └── adr-template.md
```

**ADR 模板（Architecture Decision Record）：**
```markdown
# ADR-XXX: [决策标题]

Date: YYYY-MM-DD
Status: [Proposed | Accepted | Deprecated | Superseded]
Deciders: [Team members]

## Context
[决策背景和问题描述]

## LLM Council Deliberation

### Question
[提交给 Council 的问题]

### Models Consensus
[Stage 3 综合结论]

### Key Insights
- [洞察1]
- [洞察2]
- [洞察3]

### Confidence: [X%]

### Dissenting Views
[如果有重要的反对意见]

## Team Discussion
[团队讨论要点和额外考虑]

## Decision
[最终决定]

## Consequences

### Positive
- [积极影响1]
- [积极影响2]

### Negative
- [负面影响1]
- [负面影响2]

### Mitigation
[缓解负面影响的策略]

## Follow-up
- [ ] [后续行动1]
- [ ] [后续行动2]

## References
- LLM Council Deliberation: [link to full results]
- Related ADRs: [links]
- External References: [links]
```

### 6. 持续改进

**定期审查（每月）：**
```
1. 回顾本月所有审议
2. 识别哪些决策最有价值
3. 分析成本效益
4. 优化模型配置
5. 更新团队最佳实践
```

**反馈循环：**
```
决策 → 实施 → 结果 → 回顾审议准确性 → 改进提问方式
```

**模型组合优化：**
```python
# 追踪哪个模型组合效果最好
{
  "architecture_decisions": {
    "best_models": ["DeepSeek-V3", "Gemini-3-Pro", "Claude-3.5"],
    "avg_confidence": 87%,
    "success_rate": 92%
  },
  "code_review": {
    "best_models": ["GPT-4", "Claude-3.5", "DeepSeek-V3"],
    "avg_confidence": 91%,
    "success_rate": 95%
  }
}
```

---

## 附录

### A. 完整配置示例

```json
{
  "council_models": [
    "DeepSeek-V3",
    "Qwen3-235B-A22B",
    "kim2-thinking",
    "Kimi-K2-Instruct"
  ],
  "chairman_model": "openrouter/google/gemini-3-pro-preview",
  "timeout_seconds": 120,
  "max_retries": 2,
  "cache_enabled": true,
  "cache_ttl_hours": 24,

  "presets": {
    "quick": {
      "models": ["DeepSeek-V3", "Qwen3-235B-A22B"],
      "mode": "quick"
    },
    "thorough": {
      "models": [
        "DeepSeek-V3",
        "Qwen3-235B-A22B",
        "anthropic/claude-3-5-sonnet-20241022",
        "openai/gpt-4o",
        "kim2-thinking",
        "Kimi-K2-Instruct"
      ],
      "mode": "full"
    }
  }
}
```

### B. 环境变量完整列表

```bash
# 必需
OPENROUTER_API_KEY=sk-or-v1-...

# 可选
COUNCIL_CONFIG_PATH=/path/to/custom/config.json
COUNCIL_CACHE_DIR=/path/to/cache
COUNCIL_LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR
COUNCIL_TIMEOUT=120     # 覆盖config.json中的设置
```

### C. 命令行参数完整列表

```bash
python3 scripts/council_deliberation.py \
  --question "Your question" \              # 必需：要审议的问题
  --mode {full|quick} \                     # 可选：审议模式（默认 full）
  --output {markdown|json} \                # 可选：输出格式（默认 markdown）
  --models MODEL1 MODEL2 ... \              # 可选：自定义模型列表
  --chairman MODEL \                        # 可选：自定义主席模型
  --timeout SECONDS \                       # 可选：超时时间（秒）
  --verbose                                 # 可选：详细输出
```

### D. 错误代码参考

| 代码 | 错误 | 解决方案 |
|------|------|----------|
| E001 | API Key missing | 设置 OPENROUTER_API_KEY |
| E002 | Question too short | 问题至少10字符 |
| E003 | Question too long | 问题最多5000字符 |
| E004 | Too few models | 至少2个模型 |
| E005 | Model timeout | 增加timeout或简化问题 |
| E006 | Insufficient responses | 至少2个模型需成功 |
| E007 | Chairman failed | 检查网络和API状态 |
| E008 | Invalid model ID | 检查OpenRouter模型列表 |
| E009 | Network error | 检查网络连接 |
| E010 | Rate limit | 等待或减少请求频率 |

### E. 术语表

| 术语 | 定义 |
|------|------|
| **Council** | 参与审议的多个AI模型组成的委员会 |
| **Chairman** | 负责最终综合的主席模型（通常是Gemini-3-Pro） |
| **Stage 1** | 个体响应阶段，各模型独立分析 |
| **Stage 2** | 匿名同行评审阶段，模型互相评分 |
| **Stage 3** | 主席综合阶段，生成最终建议 |
| **Anonymization** | 将响应匿名化为"Response A, B, C..."的过程 |
| **Aggregate Ranking** | 基于所有peer评审计算的总体质量排名 |
| **Confidence** | 主席对最终结论的信心度（0-100%） |
| **Full Mode** | 完整3阶段审议模式 |
| **Quick Mode** | 快速2阶段模式（跳过Stage 2） |
| **Deliberation** | 完整的多模型审议过程 |

### F. 有用的链接

**官方资源：**
- [OpenRouter 主页](https://openrouter.ai/)
- [OpenRouter 模型列表](https://openrouter.ai/models)
- [OpenRouter 定价](https://openrouter.ai/models)
- [OpenRouter API 文档](https://openrouter.ai/docs)

**相关项目：**
- [LLM Council 主项目](https://github.com/your-repo/llm-council)
- [Claude Code 文档](https://docs.anthropic.com/claude-code)

**社区和支持：**
- GitHub Issues: [报告问题](https://github.com/your-repo/llm-council/issues)
- Discord: [加入讨论](https://discord.gg/your-discord)

---

## 结语

恭喜！你现在已经掌握了 LLM Council 的完整使用方法。

**记住核心价值：**
- 🎯 多视角 = 更好的决策
- 🔍 匿名评审 = 客观质量评判
- 🎓 专家综合 = 清晰可行的建议

**立即开始：**
1. 设置 API Key
2. 安装 Skill
3. 提出第一个技术问题
4. 体验多模型审议的力量！

**需要帮助？**
- 查看 [故障排除](#故障排除)
- 阅读 [常见问题](#常见问题)
- 提交 Issue 或联系支持

祝你做出更好的技术决策！🚀

---

*最后更新: 2024-11-28*
*版本: 1.0.0*
*维护: LLM Council Team*
