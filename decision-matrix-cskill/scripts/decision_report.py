"""
Decision Report Module - 决策报告模块
生成各类决策分析报告
"""

from datetime import datetime
from typing import Dict, List, Optional
from .decision_framer import DECISION_STORE
from .scoring_engine import calculate_weighted_scores, rank_options, get_recommendation
from .analysis_tools import pros_cons_analysis, risk_assessment


def generate_quick_summary(decision_id: str) -> str:
    """
    生成快速摘要（一句话版本）

    Args:
        decision_id: 决策ID

    Returns:
        一句话摘要
    """
    if decision_id not in DECISION_STORE:
        return f"❌ 未找到决策: {decision_id}"

    decision = DECISION_STORE[decision_id]
    recommendation = get_recommendation(decision_id)

    if recommendation.get("status") != "success":
        return f"📋 {decision.get('title', '决策')} - 待完成评分"

    rec = recommendation.get("recommendation", {})
    choice = rec.get("choice", "N/A")
    score = rec.get("score", 0)
    confidence = rec.get("confidence_emoji", "")

    return f"{confidence} {decision.get('title', '决策')}: 建议选择「{choice}」(得分: {score})"


def generate_decision_matrix(decision_id: str) -> str:
    """
    生成决策矩阵表格

    Args:
        decision_id: 决策ID

    Returns:
        格式化的决策矩阵
    """
    if decision_id not in DECISION_STORE:
        return f"❌ 未找到决策: {decision_id}"

    decision = DECISION_STORE[decision_id]
    options = decision.get("options", [])
    criteria = decision.get("criteria", [])
    scores = decision.get("scores", {})

    if not options or not criteria:
        return "⚠️ 需要先添加选项和标准"

    lines = []
    lines.append("=" * 70)
    lines.append(f"📊 决策矩阵: {decision.get('title', '未命名决策')}")
    lines.append("=" * 70)
    lines.append("")

    # 表头
    header = "| 标准 (权重) |"
    for opt in options:
        header += f" {opt['name'][:8]:^10} |"
    lines.append(header)
    lines.append("|" + "-" * 14 + "|" + ("-" * 12 + "|") * len(options))

    # 数据行
    for criterion in criteria:
        crit_name = criterion["name"]
        weight = criterion["weight"]
        crit_type = criterion.get("type", "benefit")
        type_mark = "↑" if crit_type == "benefit" else "↓"

        row = f"| {crit_name[:8]:8} ({weight:.2f}){type_mark} |"

        for opt in options:
            opt_id = opt["id"]
            if opt_id in scores and crit_name in scores[opt_id]:
                score = scores[opt_id][crit_name]
                row += f" {score:^10} |"
            else:
                row += f" {'--':^10} |"

        lines.append(row)

    lines.append("|" + "-" * 14 + "|" + ("-" * 12 + "|") * len(options))

    # 加权得分
    weighted = calculate_weighted_scores(decision_id)
    if weighted.get("status") == "success":
        results = {r["option_id"]: r["normalized_score"] for r in weighted.get("results", [])}

        score_row = "| **加权得分** |"
        for opt in options:
            opt_id = opt["id"]
            if opt_id in results:
                score_row += f" {results[opt_id]:^10.1f} |"
            else:
                score_row += f" {'--':^10} |"
        lines.append(score_row)

    lines.append("")
    lines.append("↑ = 越高越好 (benefit)  ↓ = 越低越好 (cost)")
    lines.append("=" * 70)

    return "\n".join(lines)


def generate_full_report(decision_id: str) -> str:
    """
    生成完整决策报告

    Args:
        decision_id: 决策ID

    Returns:
        完整决策报告
    """
    if decision_id not in DECISION_STORE:
        return f"❌ 未找到决策: {decision_id}"

    decision = DECISION_STORE[decision_id]

    lines = []

    # 封面
    lines.append("╔" + "═" * 68 + "╗")
    lines.append("║" + "📋 决策分析报告".center(64) + "║")
    lines.append("║" + f"{decision.get('title', '未命名决策')}".center(66) + "║")
    lines.append("║" + f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}".center(60) + "║")
    lines.append("╚" + "═" * 68 + "╝")
    lines.append("")

    # 1. 决策概述
    lines.append("## 1. 决策概述")
    lines.append("")
    lines.append(f"**决策问题**: {decision.get('title', 'N/A')}")
    lines.append(f"**描述**: {decision.get('description', '无')}")
    lines.append(f"**截止日期**: {decision.get('deadline', '未设置')}")
    lines.append(f"**利益相关者**: {', '.join(decision.get('stakeholders', [])) or '未设置'}")
    lines.append(f"**状态**: {decision.get('status', 'draft')}")
    lines.append("")

    # 2. 选项概述
    lines.append("## 2. 决策选项")
    lines.append("")
    options = decision.get("options", [])
    for i, opt in enumerate(options, 1):
        lines.append(f"### 选项 {i}: {opt.get('name', 'N/A')}")
        if opt.get("description"):
            lines.append(f"  描述: {opt['description']}")
        if opt.get("estimated_cost"):
            lines.append(f"  预估成本: {opt['estimated_cost']}")
        if opt.get("estimated_time"):
            lines.append(f"  预估时间: {opt['estimated_time']}")
        if opt.get("pros"):
            lines.append(f"  优势: {', '.join(opt['pros'])}")
        if opt.get("cons"):
            lines.append(f"  劣势: {', '.join(opt['cons'])}")
        lines.append("")

    # 3. 评估标准
    lines.append("## 3. 评估标准")
    lines.append("")
    criteria = decision.get("criteria", [])
    lines.append("| 标准 | 权重 | 类型 |")
    lines.append("|------|------|------|")
    for c in criteria:
        type_name = "正向(越高越好)" if c.get("type") == "benefit" else "负向(越低越好)"
        lines.append(f"| {c['name']} | {c['weight']:.2f} | {type_name} |")
    lines.append("")

    # 4. 决策矩阵
    lines.append("## 4. 决策矩阵")
    lines.append("")
    lines.append(generate_decision_matrix(decision_id))
    lines.append("")

    # 5. 排名结果
    lines.append("## 5. 排名结果")
    lines.append("")
    ranking = rank_options(decision_id)
    if ranking.get("status") == "success":
        for r in ranking.get("rankings", []):
            medal = ["🥇", "🥈", "🥉"][r["rank"]-1] if r["rank"] <= 3 else f"{r['rank']}."
            lines.append(f"{medal} {r['option_name']}: {r['score']:.1f}分")
            lines.append(f"   {r['score_bar']}")
        lines.append("")

    # 6. 风险评估
    lines.append("## 6. 风险评估")
    lines.append("")
    risk = risk_assessment(decision_id)
    if risk.get("status") == "success":
        for assessment in risk.get("assessments", []):
            lines.append(f"**{assessment['option_name']}**: {assessment['overall_emoji']} {assessment['overall_level']} (风险得分: {assessment['overall_risk_score']})")
            lines.append(f"  建议: {assessment['recommendation']}")
        lines.append("")
    else:
        lines.append("  风险评估不可用")
        lines.append("")

    # 7. 优劣势对比
    lines.append("## 7. 优劣势对比")
    lines.append("")
    pros_cons = pros_cons_analysis(decision_id)
    if pros_cons.get("status") == "success":
        for analysis in pros_cons.get("analysis", []):
            lines.append(f"### {analysis['option_name']} ({analysis['balance']})")
            if analysis.get("strengths"):
                lines.append("  ✅ 优势:")
                for s in analysis["strengths"]:
                    lines.append(f"    - {s['criterion']}: {s['score']}/10 ({s['note']})")
            if analysis.get("weaknesses"):
                lines.append("  ❌ 劣势:")
                for w in analysis["weaknesses"]:
                    lines.append(f"    - {w['criterion']}: {w['score']}/10 ({w['note']})")
            lines.append("")

    # 8. 建议
    lines.append("## 8. 决策建议")
    lines.append("")
    recommendation = get_recommendation(decision_id)
    if recommendation.get("status") == "success":
        rec = recommendation.get("recommendation", {})
        lines.append(f"**推荐选择**: {rec.get('confidence_emoji', '')} {rec.get('choice', 'N/A')}")
        lines.append(f"**得分**: {rec.get('score', 0):.1f}/100")
        lines.append(f"**置信度**: {rec.get('confidence', 'N/A')}")
        lines.append(f"**建议**: {rec.get('advice', 'N/A')}")

        comp = recommendation.get("comparison", {})
        if comp.get("runner_up"):
            lines.append("")
            lines.append(f"与第二名「{comp['runner_up']}」相差 {comp['score_gap']} 分")
    else:
        lines.append("  建议不可用，请确保完成评分")

    lines.append("")
    lines.append("=" * 70)
    lines.append("报告结束")

    return "\n".join(lines)


def generate_executive_summary(decision_id: str) -> str:
    """
    生成执行摘要

    Args:
        decision_id: 决策ID

    Returns:
        执行摘要
    """
    if decision_id not in DECISION_STORE:
        return f"❌ 未找到决策: {decision_id}"

    decision = DECISION_STORE[decision_id]
    recommendation = get_recommendation(decision_id)

    lines = []
    lines.append("┌" + "─" * 58 + "┐")
    lines.append("│" + "📋 执行摘要".center(54) + "│")
    lines.append("├" + "─" * 58 + "┤")

    # 决策问题
    title = decision.get("title", "未命名决策")[:40]
    lines.append(f"│ 决策问题: {title:48} │")

    # 选项数量
    opt_count = len(decision.get("options", []))
    lines.append(f"│ 评估选项: {opt_count}个{' '*47}│")

    # 推荐结果
    if recommendation.get("status") == "success":
        rec = recommendation.get("recommendation", {})
        choice = rec.get("choice", "N/A")[:20]
        score = rec.get("score", 0)
        confidence = rec.get("confidence_emoji", "")

        lines.append("├" + "─" * 58 + "┤")
        lines.append(f"│ {confidence} 推荐选择: {choice:36} │")
        lines.append(f"│ 综合得分: {score:.1f}/100{' '*41}│")
        lines.append(f"│ 置信度: {rec.get('confidence', 'N/A')}{' '*45}│"[:61] + "│")

        # 关键理由
        lines.append("├" + "─" * 58 + "┤")
        lines.append(f"│ 结论: {rec.get('advice', 'N/A')[:50]:50} │")
    else:
        lines.append("├" + "─" * 58 + "┤")
        lines.append("│ ⚠️  评分未完成，无法生成建议                              │")

    lines.append("└" + "─" * 58 + "┘")

    return "\n".join(lines)
