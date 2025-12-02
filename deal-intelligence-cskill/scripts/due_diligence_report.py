"""
Due Diligence Report Module - 尽调报告模块
生成各类尽职调查报告
"""

from datetime import datetime
from typing import Dict, List, Optional
from .company_info import get_company_profile, get_company_financials, get_executive_team
from .funding_analyzer import get_funding_history, analyze_funding_trajectory, estimate_valuation
from .hiring_tracker import analyze_growth_signals, get_hiring_activity
from .news_aggregator import sentiment_analysis, get_company_news
from .risk_scanner import get_risk_score, scan_legal_risks


def generate_quick_profile(company_name: str) -> str:
    """
    生成快速公司概况（一句话版本）

    Args:
        company_name: 公司名称

    Returns:
        简洁概况
    """
    profile = get_company_profile(company_name)

    if profile.get("status") != "success":
        return f"❌ 未找到 {company_name} 的信息"

    data = profile.get("data", {})

    if profile.get("is_public"):
        # 上市公司
        name = data.get("name", company_name)
        ticker = data.get("ticker", "")
        market_cap = data.get("market_cap_formatted", "N/A")
        industry = data.get("industry", "N/A")
        return f"📊 {name} ({ticker}) | {industry} | 市值: {market_cap}"
    else:
        # 私有公司
        name = data.get("name", company_name)
        valuation = data.get("valuation", "N/A")
        industry = data.get("industry", "N/A")
        return f"🏢 {name} | {industry} | 估值: {valuation} | 私有公司"


def generate_investment_memo(company_name: str) -> str:
    """
    生成投资备忘录

    Args:
        company_name: 公司名称

    Returns:
        投资备忘录（Markdown格式）
    """
    # 收集数据
    profile = get_company_profile(company_name)
    funding = analyze_funding_trajectory(company_name)
    growth = analyze_growth_signals(company_name)
    sentiment = sentiment_analysis(company_name)
    risk = get_risk_score(company_name)

    memo = []

    # 标题
    memo.append("=" * 60)
    memo.append(f"📋 投资备忘录: {company_name}")
    memo.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    memo.append("=" * 60)
    memo.append("")

    # 执行摘要
    memo.append("## 📌 执行摘要")
    if profile.get("status") == "success":
        data = profile.get("data", {})
        if profile.get("is_public"):
            memo.append(f"- **公司**: {data.get('name', company_name)} ({data.get('ticker', '')})")
            memo.append(f"- **行业**: {data.get('industry', 'N/A')}")
            memo.append(f"- **市值**: {data.get('market_cap_formatted', 'N/A')}")
        else:
            memo.append(f"- **公司**: {data.get('name', company_name)}")
            memo.append(f"- **行业**: {data.get('industry', 'N/A')}")
            memo.append(f"- **估值**: {data.get('valuation', 'N/A')}")
            memo.append(f"- **状态**: 私有公司")

    # 投资建议
    memo.append("")
    memo.append("### 投资建议")
    overall_score = calculate_overall_score(risk, growth, sentiment)
    if overall_score >= 75:
        memo.append("✅ **建议**: 积极关注，适合深入接洽")
    elif overall_score >= 50:
        memo.append("🟡 **建议**: 可以接触，需完成详细尽调")
    else:
        memo.append("⚠️ **建议**: 谨慎评估，存在较多风险因素")
    memo.append("")

    # 融资情况
    memo.append("## 💰 融资情况")
    if funding.get("status") == "success":
        summary = funding.get("summary", {})
        memo.append(f"- **累计融资**: {summary.get('total_raised', 'N/A')}")
        memo.append(f"- **最新估值**: {summary.get('latest_valuation', 'N/A')}")
        memo.append(f"- **最新轮次**: {summary.get('latest_round', 'N/A')} ({summary.get('latest_date', '')})")
        memo.append(f"- **融资节奏**: {funding.get('trajectory_analysis', {}).get('funding_velocity', 'N/A')}")
        memo.append(f"- **发展阶段**: {funding.get('trajectory_analysis', {}).get('stage', 'N/A')}")

        if funding.get("notable_investors"):
            memo.append(f"- **知名投资人**: {', '.join(funding['notable_investors'][:5])}")
    else:
        memo.append("- 融资信息不可用")
    memo.append("")

    # 增长信号
    memo.append("## 📈 增长信号")
    if growth.get("status") == "success":
        assessment = growth.get("overall_assessment", {})
        memo.append(f"- **信号强度**: {assessment.get('signal', 'N/A')}")
        memo.append(f"- **招聘规模**: {assessment.get('total_openings', 0)}个岗位")
        memo.append(f"- **同比变化**: {assessment.get('yoy_change', 'N/A')}")

        if growth.get("strategic_focus"):
            memo.append(f"- **战略重点**: {', '.join(growth['strategic_focus'][:3])}")
    else:
        memo.append("- 增长信号数据不可用")
    memo.append("")

    # 舆情分析
    memo.append("## 📰 舆情分析")
    if sentiment.get("status") == "success":
        sent_summary = sentiment.get("sentiment_summary", {})
        memo.append(f"- **舆情评分**: {sent_summary.get('score', 50)}/100")
        memo.append(f"- **整体倾向**: {sent_summary.get('emoji', '')} {sent_summary.get('overall', 'N/A')}")

        if sentiment.get("main_topics"):
            topics = [t[0] for t in sentiment["main_topics"][:3]]
            memo.append(f"- **热点话题**: {', '.join(topics)}")
    else:
        memo.append("- 舆情数据不可用")
    memo.append("")

    # 风险评估
    memo.append("## ⚠️ 风险评估")
    if risk.get("status") == "success":
        memo.append(f"- **风险等级**: {risk.get('risk_level', 'N/A')}")
        memo.append(f"- **风险评分**: {risk.get('overall_score', 50)}/100")
        memo.append(f"- **投资建议**: {risk.get('investment_advice', 'N/A')}")

        if risk.get("top_risks"):
            memo.append("- **主要风险**:")
            for r in risk["top_risks"][:3]:
                severity_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(r.get("severity", ""), "")
                memo.append(f"  - {severity_emoji} {r.get('type', '')}: {r.get('description', '')}")
    else:
        memo.append("- 风险数据不可用")
    memo.append("")

    # 下一步行动
    memo.append("## 📋 建议下一步")
    memo.append("1. 安排管理层会面")
    memo.append("2. 获取详细财务数据")
    memo.append("3. 进行客户/用户访谈")
    memo.append("4. 聘请专业机构进行法律尽调")
    memo.append("")

    memo.append("=" * 60)
    memo.append("*此报告基于公开信息生成，仅供参考*")

    return "\n".join(memo)


def calculate_overall_score(risk: Dict, growth: Dict, sentiment: Dict) -> float:
    """计算综合评分"""
    scores = []

    # 风险评分（反向，风险低得分高）
    if risk.get("status") == "success":
        risk_score = 100 - risk.get("overall_score", 50)
        scores.append(risk_score * 0.4)  # 权重40%

    # 增长信号评分
    if growth.get("status") == "success":
        growth_score = growth.get("overall_assessment", {}).get("score", 50)
        scores.append(growth_score * 0.35)  # 权重35%

    # 舆情评分
    if sentiment.get("status") == "success":
        sent_score = sentiment.get("sentiment_summary", {}).get("score", 50)
        scores.append(sent_score * 0.25)  # 权重25%

    return sum(scores) if scores else 50


def generate_full_dd_report(company_name: str) -> str:
    """
    生成完整尽调报告

    Args:
        company_name: 公司名称

    Returns:
        完整尽调报告（Markdown格式）
    """
    # 收集所有数据
    profile = get_company_profile(company_name)
    financials = get_company_financials(company_name)
    executives = get_executive_team(company_name)
    funding = analyze_funding_trajectory(company_name)
    valuation = estimate_valuation(company_name)
    growth = analyze_growth_signals(company_name)
    hiring = get_hiring_activity(company_name)
    sentiment = sentiment_analysis(company_name)
    news = get_company_news(company_name)
    risk = get_risk_score(company_name)
    legal = scan_legal_risks(company_name)

    report = []

    # 封面
    report.append("=" * 70)
    report.append("")
    report.append(f"# 📊 商业尽职调查报告")
    report.append(f"## {company_name}")
    report.append("")
    report.append(f"**报告日期**: {datetime.now().strftime('%Y年%m月%d日')}")
    report.append(f"**报告类型**: 综合尽调报告")
    report.append(f"**机密等级**: 仅供内部使用")
    report.append("")
    report.append("=" * 70)
    report.append("")

    # 目录
    report.append("## 目录")
    report.append("1. 执行摘要")
    report.append("2. 公司概况")
    report.append("3. 管理团队")
    report.append("4. 财务分析")
    report.append("5. 融资历史")
    report.append("6. 增长分析")
    report.append("7. 舆情分析")
    report.append("8. 风险评估")
    report.append("9. 投资建议")
    report.append("10. 附录")
    report.append("")

    # 1. 执行摘要
    report.append("---")
    report.append("## 1. 执行摘要")
    report.append("")

    overall_score = calculate_overall_score(risk, growth, sentiment)

    if overall_score >= 75:
        verdict = "✅ 推荐关注"
        verdict_detail = "公司基本面良好，增长势头积极，风险可控"
    elif overall_score >= 50:
        verdict = "🟡 中性评估"
        verdict_detail = "公司存在一定亮点，但也有需要关注的风险"
    else:
        verdict = "⚠️ 建议谨慎"
        verdict_detail = "公司存在较多风险因素，需仔细评估"

    report.append(f"**综合评分**: {overall_score:.0f}/100")
    report.append(f"**总体评价**: {verdict}")
    report.append(f"**评价说明**: {verdict_detail}")
    report.append("")

    # 关键发现
    report.append("### 关键发现")
    if profile.get("status") == "success":
        data = profile.get("data", {})
        report.append(f"- 行业地位: {data.get('industry', 'N/A')}")
    if funding.get("status") == "success":
        report.append(f"- 融资阶段: {funding.get('trajectory_analysis', {}).get('stage', 'N/A')}")
    if growth.get("status") == "success":
        report.append(f"- 增长信号: {growth.get('overall_assessment', {}).get('signal', 'N/A')}")
    if risk.get("status") == "success":
        report.append(f"- 风险等级: {risk.get('risk_level', 'N/A')}")
    report.append("")

    # 2. 公司概况
    report.append("---")
    report.append("## 2. 公司概况")
    report.append("")

    if profile.get("status") == "success":
        data = profile.get("data", {})
        if profile.get("is_public"):
            report.append(f"| 项目 | 内容 |")
            report.append(f"|------|------|")
            report.append(f"| 公司名称 | {data.get('name', 'N/A')} |")
            report.append(f"| 股票代码 | {data.get('ticker', 'N/A')} |")
            report.append(f"| 行业 | {data.get('industry', 'N/A')} |")
            report.append(f"| 板块 | {data.get('sector', 'N/A')} |")
            report.append(f"| 总部 | {data.get('headquarters', 'N/A')} |")
            report.append(f"| 员工数 | {data.get('employees', 'N/A')} |")
            report.append(f"| 市值 | {data.get('market_cap_formatted', 'N/A')} |")
            report.append(f"| 当前股价 | ${data.get('current_price', 0):.2f} |")
            report.append(f"| 52周最高 | ${data.get('52_week_high', 0):.2f} |")
            report.append(f"| 52周最低 | ${data.get('52_week_low', 0):.2f} |")
        else:
            report.append(f"| 项目 | 内容 |")
            report.append(f"|------|------|")
            report.append(f"| 公司名称 | {data.get('name', 'N/A')} |")
            report.append(f"| 英文名 | {data.get('name_en', 'N/A')} |")
            report.append(f"| 成立时间 | {data.get('founded', 'N/A')} |")
            report.append(f"| 总部 | {data.get('headquarters', 'N/A')} |")
            report.append(f"| 行业 | {data.get('industry', 'N/A')} |")
            report.append(f"| 员工数 | {data.get('employees', 'N/A')} |")
            report.append(f"| 估值 | {data.get('valuation', 'N/A')} |")
            report.append(f"| 创始人 | {data.get('founder', 'N/A')} |")

            if data.get("products"):
                report.append(f"| 主要产品 | {', '.join(data['products'][:5])} |")

        if data.get("description"):
            report.append("")
            report.append("**公司简介**:")
            report.append(data.get("description", ""))
    else:
        report.append("*公司基本信息不可用*")
    report.append("")

    # 3. 管理团队
    report.append("---")
    report.append("## 3. 管理团队")
    report.append("")

    if executives.get("status") == "success":
        execs = executives.get("executives", [])
        if execs:
            report.append("| 姓名 | 职位 | 年龄 | 薪酬 |")
            report.append("|------|------|------|------|")
            for exec in execs[:10]:
                report.append(f"| {exec.get('name', 'N/A')} | {exec.get('title', 'N/A')} | {exec.get('age', 'N/A')} | {exec.get('compensation', 'N/A')} |")
        else:
            report.append("*高管信息暂无*")
    else:
        report.append("*高管信息不可用*")
    report.append("")

    # 4. 财务分析
    report.append("---")
    report.append("## 4. 财务分析")
    report.append("")

    if financials.get("status") == "success":
        fin = financials.get("data", {})

        report.append("### 估值指标")
        val = fin.get("valuation", {})
        report.append(f"- 市值: {val.get('market_cap_formatted', 'N/A')}")
        report.append(f"- P/E (TTM): {val.get('pe_ratio', 'N/A')}")
        report.append(f"- P/E (Forward): {val.get('forward_pe', 'N/A')}")
        report.append(f"- P/B: {val.get('pb_ratio', 'N/A')}")
        report.append(f"- P/S: {val.get('ps_ratio', 'N/A')}")
        report.append("")

        report.append("### 盈利能力")
        prof = fin.get("profitability", {})
        report.append(f"- 营收: {prof.get('revenue_formatted', 'N/A')}")
        report.append(f"- 毛利率: {prof.get('gross_margin', 'N/A')}")
        report.append(f"- 营业利润率: {prof.get('operating_margin', 'N/A')}")
        report.append(f"- 净利率: {prof.get('profit_margin', 'N/A')}")
        report.append(f"- ROE: {prof.get('roe', 'N/A')}")
        report.append("")

        report.append("### 财务健康")
        health = fin.get("financial_health", {})
        report.append(f"- 现金: {health.get('total_cash_formatted', 'N/A')}")
        report.append(f"- 负债: {health.get('total_debt_formatted', 'N/A')}")
        report.append(f"- 资产负债率: {health.get('debt_to_equity', 'N/A')}")
        report.append(f"- 流动比率: {health.get('current_ratio', 'N/A')}")
    else:
        report.append("*财务数据不可用（可能是私有公司）*")
    report.append("")

    # 5. 融资历史
    report.append("---")
    report.append("## 5. 融资历史")
    report.append("")

    if funding.get("status") == "success":
        summary = funding.get("summary", {})
        report.append(f"- **累计融资**: {summary.get('total_raised', 'N/A')}")
        report.append(f"- **最新估值**: {summary.get('latest_valuation', 'N/A')}")
        report.append(f"- **融资轮次**: {summary.get('total_rounds', 0)}轮")
        report.append(f"- **发展阶段**: {funding.get('trajectory_analysis', {}).get('stage', 'N/A')}")
        report.append(f"- **融资节奏**: {funding.get('trajectory_analysis', {}).get('funding_velocity', 'N/A')}")
        report.append("")

        if funding.get("notable_investors"):
            report.append(f"**知名投资人**: {', '.join(funding['notable_investors'])}")
            report.append("")

        if funding.get("repeat_investors"):
            report.append(f"**多轮投资人**: {', '.join(funding['repeat_investors'])}")
    else:
        report.append("*融资历史不可用*")
    report.append("")

    # 6. 增长分析
    report.append("---")
    report.append("## 6. 增长分析")
    report.append("")

    if growth.get("status") == "success":
        assessment = growth.get("overall_assessment", {})
        report.append(f"- **增长信号**: {assessment.get('signal', 'N/A')}")
        report.append(f"- **信号得分**: {assessment.get('score', 0)}/100")
        report.append(f"- **招聘规模**: {assessment.get('total_openings', 0)}个岗位")
        report.append(f"- **同比变化**: {assessment.get('yoy_change', 'N/A')}")
        report.append("")

        if growth.get("strategic_focus"):
            report.append(f"**战略重点领域**: {', '.join(growth['strategic_focus'])}")
            report.append("")

        if growth.get("department_signals"):
            report.append("### 部门增长明细")
            for dept in growth["department_signals"][:5]:
                report.append(f"- {dept.get('signal', '')}")
    else:
        report.append("*增长数据不可用*")
    report.append("")

    # 7. 舆情分析
    report.append("---")
    report.append("## 7. 舆情分析")
    report.append("")

    if sentiment.get("status") == "success":
        sent = sentiment.get("sentiment_summary", {})
        report.append(f"- **舆情评分**: {sent.get('score', 50)}/100")
        report.append(f"- **整体倾向**: {sent.get('emoji', '')} {sent.get('overall', 'N/A')}")
        report.append(f"- **新闻数量**: {sentiment.get('total_news', 0)}条")
        report.append("")

        if sent.get("breakdown"):
            breakdown = sent["breakdown"]
            report.append("### 情感分布")
            report.append(f"- 正面: {breakdown.get('positive', 'N/A')}")
            report.append(f"- 中性: {breakdown.get('neutral', 'N/A')}")
            report.append(f"- 负面: {breakdown.get('negative', 'N/A')}")
            report.append("")

        if sentiment.get("positive_headlines"):
            report.append("### 正面报道")
            for h in sentiment["positive_headlines"][:3]:
                report.append(f"- {h}")
            report.append("")

        if sentiment.get("negative_headlines"):
            report.append("### 负面报道")
            for h in sentiment["negative_headlines"][:3]:
                report.append(f"- {h}")
    else:
        report.append("*舆情数据不可用*")
    report.append("")

    # 8. 风险评估
    report.append("---")
    report.append("## 8. 风险评估")
    report.append("")

    if risk.get("status") == "success":
        report.append(f"- **风险等级**: {risk.get('risk_level', 'N/A')}")
        report.append(f"- **风险评分**: {risk.get('overall_score', 50)}/100")
        report.append("")

        breakdown = risk.get("risk_breakdown", {})
        report.append("### 风险分布")
        report.append(f"- 法律风险: {breakdown.get('legal', 0)}/100")
        report.append(f"- 财务风险: {breakdown.get('financial', 0)}/100")
        report.append(f"- 声誉风险: {breakdown.get('reputation', 0)}/100")
        report.append("")

        if risk.get("top_risks"):
            report.append("### 主要风险项")
            for r in risk["top_risks"]:
                severity_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(r.get("severity", ""), "")
                report.append(f"- {severity_emoji} **{r.get('type', '')}**: {r.get('description', '')}")
    else:
        report.append("*风险数据不可用*")
    report.append("")

    # 9. 投资建议
    report.append("---")
    report.append("## 9. 投资建议")
    report.append("")
    report.append(f"**综合评分**: {overall_score:.0f}/100")
    report.append(f"**总体评价**: {verdict}")
    report.append("")
    report.append("### 优势")
    report.append("- [基于分析自动生成]")
    report.append("")
    report.append("### 风险")
    report.append("- [基于分析自动生成]")
    report.append("")
    report.append("### 建议下一步")
    report.append("1. 安排与管理层深度交流")
    report.append("2. 获取详细财务数据进行审计")
    report.append("3. 进行客户/用户访谈")
    report.append("4. 聘请专业机构进行法律尽调")
    report.append("5. 评估行业竞争格局")
    report.append("")

    # 10. 附录
    report.append("---")
    report.append("## 10. 附录")
    report.append("")
    report.append("### 数据来源")
    report.append("- 公开市场数据 (yfinance)")
    report.append("- 模拟融资/招聘/新闻数据")
    report.append("- 实际应用建议对接: 天眼查、Crunchbase、LinkedIn等API")
    report.append("")
    report.append("### 免责声明")
    report.append("本报告基于公开信息生成，仅供参考，不构成投资建议。")
    report.append("投资决策前请进行独立的尽职调查。")
    report.append("")
    report.append("=" * 70)

    return "\n".join(report)


def compare_companies(company_names: List[str]) -> str:
    """
    对比多家公司

    Args:
        company_names: 公司名称列表

    Returns:
        对比报告（Markdown格式）
    """
    report = []
    report.append("=" * 60)
    report.append("# 📊 企业对比分析报告")
    report.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append("=" * 60)
    report.append("")

    # 收集各公司数据
    company_data = []
    for name in company_names:
        profile = get_company_profile(name)
        risk = get_risk_score(name)
        growth = analyze_growth_signals(name)
        funding = analyze_funding_trajectory(name)

        if profile.get("status") == "success":
            company_data.append({
                "name": name,
                "profile": profile,
                "risk": risk,
                "growth": growth,
                "funding": funding,
                "score": calculate_overall_score(risk, growth, {"status": "error"})
            })

    if not company_data:
        return "未能获取任何公司的数据"

    # 对比表格
    report.append("## 基本信息对比")
    report.append("")
    report.append("| 指标 | " + " | ".join([d["name"] for d in company_data]) + " |")
    report.append("|------" + "|------" * len(company_data) + "|")

    # 行业
    industries = []
    for d in company_data:
        data = d["profile"].get("data", {})
        industries.append(data.get("industry", "N/A"))
    report.append("| 行业 | " + " | ".join(industries) + " |")

    # 估值/市值
    valuations = []
    for d in company_data:
        data = d["profile"].get("data", {})
        if d["profile"].get("is_public"):
            valuations.append(data.get("market_cap_formatted", "N/A"))
        else:
            valuations.append(data.get("valuation", "N/A"))
    report.append("| 估值/市值 | " + " | ".join(valuations) + " |")

    # 风险评分
    risks = []
    for d in company_data:
        if d["risk"].get("status") == "success":
            risks.append(f"{d['risk'].get('overall_score', 'N/A')}/100")
        else:
            risks.append("N/A")
    report.append("| 风险评分 | " + " | ".join(risks) + " |")

    # 增长信号
    growths = []
    for d in company_data:
        if d["growth"].get("status") == "success":
            growths.append(d["growth"].get("overall_assessment", {}).get("signal", "N/A"))
        else:
            growths.append("N/A")
    report.append("| 增长信号 | " + " | ".join(growths) + " |")

    # 综合评分
    scores = []
    for d in company_data:
        scores.append(f"{d['score']:.0f}/100")
    report.append("| 综合评分 | " + " | ".join(scores) + " |")

    report.append("")

    # 排名
    report.append("## 综合排名")
    report.append("")
    ranked = sorted(company_data, key=lambda x: x["score"], reverse=True)
    for i, d in enumerate(ranked, 1):
        medal = ["🥇", "🥈", "🥉"][i-1] if i <= 3 else f"{i}."
        report.append(f"{medal} **{d['name']}** - {d['score']:.0f}分")

    report.append("")
    report.append("---")
    report.append("*此报告基于公开信息生成，仅供参考*")

    return "\n".join(report)
