#!/usr/bin/env python3
"""
Skill CLI - Claude Code Skill 管理命令行工具
用于生成、验证、测试 Skills

用法:
    python skill_cli.py validate [skill_path]    - 验证 Skill 格式
    python skill_cli.py test [skill_path]        - 运行 Skill 测试
    python skill_cli.py generate <spec_file>     - 从规格文件生成 Skill
    python skill_cli.py check-all                - 检查所有 Skills
"""

import os
import sys
import json
import argparse

# 添加 core 目录到路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from core.validators.format_validator import validate_skill, validate_all_skills
from core.validators.code_validator import validate_code, validate_all_code
from core.generator.skill_generator import generate_skill_from_spec
from core.tests.test_runner import run_skill_tests, run_all_skill_tests


def cmd_validate(args):
    """验证 Skill 格式"""
    if args.path:
        skill_path = os.path.abspath(args.path)
        if os.path.isdir(skill_path):
            # 单个 Skill
            print(f"验证 Skill: {skill_path}\n")

            format_result = validate_skill(skill_path)
            code_result = validate_code(skill_path)

            # 显示格式验证结果
            print("📋 格式验证:")
            status = "✅" if format_result["passed"] else "❌"
            print(f"  {status} {format_result['skill_name']}")
            for err in format_result["errors"]:
                print(f"     ❌ {err}")
            for warn in format_result["warnings"]:
                print(f"     ⚠️  {warn}")

            # 显示代码验证结果
            print("\n💻 代码验证:")
            status = "✅" if code_result["passed"] else "❌"
            print(f"  {status} {code_result['skill_name']}")
            for err in code_result["errors"]:
                print(f"     ❌ {err}")
            for warn in code_result["warnings"][:5]:
                print(f"     ⚠️  {warn}")
            if len(code_result["warnings"]) > 5:
                print(f"     ... 还有 {len(code_result['warnings']) - 5} 个警告")

            # 总结
            passed = format_result["passed"] and code_result["passed"]
            print(f"\n{'='*50}")
            print(f"结果: {'✅ 验证通过' if passed else '❌ 验证失败'}")

            return 0 if passed else 1
        else:
            print(f"❌ 路径不存在: {skill_path}")
            return 1
    else:
        # 验证所有
        print(f"验证所有 Skills: {SCRIPT_DIR}\n")

        format_results = validate_all_skills(SCRIPT_DIR)
        code_results = validate_all_code(SCRIPT_DIR)

        # 合并结果
        all_passed = True
        total_errors = 0
        total_warnings = 0

        for fr in format_results:
            cr = next((c for c in code_results if c["skill_name"] == fr["skill_name"]), None)

            passed = fr["passed"] and (cr["passed"] if cr else True)
            status = "✅" if passed else "❌"
            print(f"{status} {fr['skill_name']}")

            for err in fr["errors"]:
                print(f"   ❌ [格式] {err}")
                total_errors += 1

            if cr:
                for err in cr["errors"]:
                    print(f"   ❌ [代码] {err}")
                    total_errors += 1

            total_warnings += fr["warning_count"]
            if cr:
                total_warnings += cr["warning_count"]

            if not passed:
                all_passed = False

        print(f"\n{'='*50}")
        print(f"总计: {len(format_results)} 个 Skills")
        print(f"错误: {total_errors}, 警告: {total_warnings}")
        print(f"结果: {'✅ 全部通过' if all_passed else '❌ 存在问题'}")

        return 0 if all_passed else 1


def cmd_test(args):
    """运行 Skill 测试"""
    if args.path:
        skill_path = os.path.abspath(args.path)
        if os.path.isdir(skill_path):
            result = run_skill_tests(skill_path)
            print(result["summary"])
            return 0 if result["passed"] else 1
        else:
            print(f"❌ 路径不存在: {skill_path}")
            return 1
    else:
        results = run_all_skill_tests(SCRIPT_DIR)

        passed_count = 0
        for result in results:
            print(result["summary"])
            print()
            if result["passed"]:
                passed_count += 1

        print("=" * 50)
        print(f"总计: {passed_count}/{len(results)} 个 Skill 测试通过")

        return 0 if passed_count == len(results) else 1


def cmd_generate(args):
    """从规格文件生成 Skill"""
    spec_file = args.spec_file

    if not os.path.isfile(spec_file):
        print(f"❌ 规格文件不存在: {spec_file}")
        return 1

    try:
        with open(spec_file, 'r', encoding='utf-8') as f:
            spec = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析错误: {e}")
        return 1

    output_path = args.output or SCRIPT_DIR

    print(f"生成 Skill: {spec.get('name', 'unknown')}")
    print(f"输出目录: {output_path}\n")

    result = generate_skill_from_spec(spec, output_path)

    if result["status"] == "success":
        print(f"✅ 生成成功!")
        print(f"   路径: {result['skill_path']}")
        print(f"   文件数: {result['files_created']}")

        if "validation" in result:
            v = result["validation"]
            print(f"\n验证结果:")
            print(f"   格式: {'✅' if v['format']['passed'] else '❌'}")
            print(f"   代码: {'✅' if v['code']['passed'] else '❌'}")

        return 0
    else:
        print(f"⚠️  {result.get('message', '生成完成但有问题')}")
        return 1


def cmd_check_all(args):
    """检查所有 Skills（验证 + 测试）"""
    print("🔍 开始全面检查...\n")

    # 1. 格式验证
    print("=" * 50)
    print("📋 步骤 1: 格式验证")
    print("=" * 50)

    format_results = validate_all_skills(SCRIPT_DIR)
    format_passed = sum(1 for r in format_results if r["passed"])
    print(f"格式验证: {format_passed}/{len(format_results)} 通过\n")

    # 2. 代码验证
    print("=" * 50)
    print("💻 步骤 2: 代码验证")
    print("=" * 50)

    code_results = validate_all_code(SCRIPT_DIR)
    code_passed = sum(1 for r in code_results if r["passed"])
    print(f"代码验证: {code_passed}/{len(code_results)} 通过\n")

    # 3. 功能测试
    print("=" * 50)
    print("🧪 步骤 3: 功能测试")
    print("=" * 50)

    test_results = run_all_skill_tests(SCRIPT_DIR)
    test_passed = sum(1 for r in test_results if r["passed"])
    print(f"功能测试: {test_passed}/{len(test_results)} 通过\n")

    # 汇总
    print("=" * 50)
    print("📊 检查汇总")
    print("=" * 50)

    total_skills = len(format_results)
    all_passed = (
        format_passed == total_skills and
        code_passed == total_skills and
        test_passed == total_skills
    )

    print(f"Skills 总数: {total_skills}")
    print(f"格式验证通过: {format_passed}")
    print(f"代码验证通过: {code_passed}")
    print(f"功能测试通过: {test_passed}")
    print(f"\n{'✅ 全部检查通过!' if all_passed else '❌ 存在问题，请修复后重试'}")

    # 列出有问题的 Skills
    if not all_passed:
        print("\n问题 Skills:")
        for fr in format_results:
            cr = next((c for c in code_results if c["skill_name"] == fr["skill_name"]), None)
            tr = next((t for t in test_results if t["skill_name"] == fr["skill_name"]), None)

            issues = []
            if not fr["passed"]:
                issues.append("格式")
            if cr and not cr["passed"]:
                issues.append("代码")
            if tr and not tr["passed"]:
                issues.append("测试")

            if issues:
                print(f"  ❌ {fr['skill_name']}: {', '.join(issues)}问题")

    return 0 if all_passed else 1


def main():
    parser = argparse.ArgumentParser(
        description="Claude Code Skill 管理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python skill_cli.py validate                    # 验证所有 Skills
  python skill_cli.py validate ./my-skill-cskill  # 验证单个 Skill
  python skill_cli.py test                        # 测试所有 Skills
  python skill_cli.py generate spec.json          # 从规格生成 Skill
  python skill_cli.py check-all                   # 全面检查
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # validate 命令
    validate_parser = subparsers.add_parser("validate", help="验证 Skill 格式和代码")
    validate_parser.add_argument("path", nargs="?", help="Skill 目录路径（可选）")

    # test 命令
    test_parser = subparsers.add_parser("test", help="运行 Skill 测试")
    test_parser.add_argument("path", nargs="?", help="Skill 目录路径（可选）")

    # generate 命令
    generate_parser = subparsers.add_parser("generate", help="从规格文件生成 Skill")
    generate_parser.add_argument("spec_file", help="规格 JSON 文件路径")
    generate_parser.add_argument("-o", "--output", help="输出目录")

    # check-all 命令
    check_parser = subparsers.add_parser("check-all", help="全面检查所有 Skills")

    args = parser.parse_args()

    if args.command == "validate":
        return cmd_validate(args)
    elif args.command == "test":
        return cmd_test(args)
    elif args.command == "generate":
        return cmd_generate(args)
    elif args.command == "check-all":
        return cmd_check_all(args)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
