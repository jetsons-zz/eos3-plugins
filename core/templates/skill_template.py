"""
Skill Template - 标准化Skill模板
确保生成的Skill格式100%正确
"""

# ============================================================
# SKILL.md 模板
# ============================================================
SKILL_MD_TEMPLATE = '''---
name: {skill_name}
description: {description}
version: {version}
author: {author}
license: MIT
---

# {display_name}

**Version:** {version}
**Type:** {skill_type}
**Domain:** {domain}

## Overview

{overview}

## Core Features

{features}

## Usage Examples

```
{usage_examples}
```

## Architecture

```
{skill_name}/
├── scripts/
│   ├── __init__.py
{module_tree}
├── .claude-plugin/
│   └── marketplace.json
├── SKILL.md
├── README.md
└── LICENSE
```

## Dependencies

{dependencies}

## License

MIT License
'''

# ============================================================
# marketplace.json 模板
# ============================================================
MARKETPLACE_JSON_TEMPLATE = '''{
  "name": "{skill_name}",
  "version": "{version}",
  "description": "{description}",
  "author": "{author}",
  "owner": {
    "name": "{owner_name}",
    "email": "{owner_email}",
    "url": "{owner_url}"
  },
  "license": "MIT",
  "repository": "{repository}",
  "keywords": {keywords_json},
  "plugins": [{
    "name": "{plugin_name}",
    "description": "{plugin_description}",
    "source": "./",
    "skills": ["./"]
  }]
}
'''

# ============================================================
# __init__.py 模板
# ============================================================
INIT_PY_TEMPLATE = '''"""
{display_name}
{tagline}
"""

{imports}

__all__ = [
{exports}
]

__version__ = '{version}'
'''

# ============================================================
# 模块文件模板
# ============================================================
MODULE_PY_TEMPLATE = '''"""
{module_name} Module - {module_description}
{module_tagline}
"""

from datetime import datetime
from typing import Dict, List, Optional, Any

{module_constants}

{module_functions}
'''

# ============================================================
# 函数模板
# ============================================================
FUNCTION_TEMPLATE = '''
def {func_name}({params}) -> {return_type}:
    """
    {func_description}

    Args:
{args_doc}

    Returns:
        {return_description}
    """
{func_body}
'''

# ============================================================
# README.md 模板
# ============================================================
README_MD_TEMPLATE = '''# {display_name}

{tagline}

## Features

{features_list}

## Usage

```
{usage_examples}
```

## Installation

### As Plugin (Recommended)
```bash
/plugin marketplace add {marketplace_url}
/plugin install {skill_name}@{marketplace_name}
```

### As Skill
```bash
cp -r {skill_name} ~/.claude/skills/
```

## License

MIT License
'''

# ============================================================
# LICENSE 模板
# ============================================================
LICENSE_TEMPLATE = '''MIT License

Copyright (c) {year} {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

# ============================================================
# 测试文件模板
# ============================================================
TEST_MODULE_TEMPLATE = '''"""
Test {module_name} - 自动生成的测试
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts import {imports}


def test_imports():
    """测试模块导入"""
    print("✅ 模块导入成功")
    return True


{test_functions}


def run_all_tests():
    """运行所有测试"""
    results = []

    results.append(("导入测试", test_imports()))
{test_calls}

    # 汇总
    passed = sum(1 for _, r in results if r)
    total = len(results)

    print(f"\\n{'='*50}")
    print(f"测试结果: {passed}/{total} 通过")
    print(f"{'='*50}")

    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
'''
