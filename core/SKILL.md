---
name: skill-generator-core
description: Zero-error Claude Code Skill generation system. Generates validated, production-ready skills with automatic format checking, code validation, and testing. Use when creating new Claude Code skills or plugins.
version: 1.0.0
author: Agent-Skill-Creator
license: MIT
---

# Skill Generator Core - 零错误生成系统

**Version:** 1.0.0
**Type:** Meta Skill (Skill生成器)
**Domain:** Development Tools

## Overview

为 Claude Code 提供零错误 Skill 生成能力，确保生成的 Skill 可以一次性成功安装为 Plugin。

## Core Features

### 1. 格式验证器 (Format Validator)
- 验证目录结构完整性
- 验证 SKILL.md frontmatter 格式
- 验证 marketplace.json Schema
- 验证 README.md 和 LICENSE

### 2. 代码验证器 (Code Validator)
- Python 语法检查
- 导入一致性验证
- 函数签名验证
- 实际导入测试

### 3. 一键生成器 (Skill Generator)
- 从规格字典生成完整 Skill
- 自动生成所有必需文件
- 内置模板确保格式正确
- 生成后自动验证

### 4. 测试运行器 (Test Runner)
- 模块导入测试
- 函数调用测试
- 集成测试
- 测试报告生成

## Usage

### CLI 命令

```bash
# 验证所有 Skills
python skill_cli.py validate

# 验证单个 Skill
python skill_cli.py validate ./my-skill-cskill

# 测试所有 Skills
python skill_cli.py test

# 从规格生成 Skill
python skill_cli.py generate spec.json

# 全面检查（验证 + 测试）
python skill_cli.py check-all
```

### 生成规格示例

```json
{
  "name": "my-skill",
  "display_name": "My Skill",
  "description": "这是我的 Skill",
  "domain": "Utility",
  "keywords": ["utility", "tool"],
  "modules": [
    {
      "name": "main_module",
      "description": "主模块",
      "functions": [
        {
          "name": "do_something",
          "description": "执行某操作",
          "params": [
            {"name": "input", "type": "str", "description": "输入"}
          ],
          "return_type": "Dict"
        }
      ]
    }
  ]
}
```

## Architecture

```
core/
├── templates/
│   └── skill_template.py      # 文件模板
├── validators/
│   ├── format_validator.py    # 格式验证
│   └── code_validator.py      # 代码验证
├── generator/
│   └── skill_generator.py     # 生成器
├── tests/
│   └── test_runner.py         # 测试运行
└── __init__.py
```

## Workflow

```
1. 定义规格 (JSON/Dict)
   ↓
2. 调用生成器
   ↓
3. 自动生成所有文件
   ↓
4. 格式验证 ✓
   ↓
5. 代码验证 ✓
   ↓
6. 功能测试 ✓
   ↓
7. 输出可直接安装的 Skill
```

## 质量保证

- ✅ marketplace.json Schema 100% 正确
- ✅ SKILL.md frontmatter 格式正确
- ✅ Python 语法无错误
- ✅ 导入导出一致
- ✅ 基础功能可用

## License

MIT License
