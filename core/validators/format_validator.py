"""
Format Validator - 格式验证器
验证 Claude Code Skill/Plugin 格式正确性
"""

import os
import json
import re
from typing import Dict, List, Tuple, Optional


class FormatValidator:
    """格式验证器"""

    def __init__(self, skill_path: str):
        self.skill_path = skill_path
        self.skill_name = os.path.basename(skill_path)
        self.errors = []
        self.warnings = []

    def validate_all(self) -> Tuple[bool, List[str], List[str]]:
        """
        执行所有格式验证

        Returns:
            (是否通过, 错误列表, 警告列表)
        """
        self.errors = []
        self.warnings = []

        # 1. 验证目录结构
        self._validate_directory_structure()

        # 2. 验证 SKILL.md
        self._validate_skill_md()

        # 3. 验证 marketplace.json
        self._validate_marketplace_json()

        # 4. 验证 __init__.py
        self._validate_init_py()

        # 5. 验证 README.md
        self._validate_readme()

        # 6. 验证 LICENSE
        self._validate_license()

        return len(self.errors) == 0, self.errors, self.warnings

    def _validate_directory_structure(self):
        """验证目录结构"""
        required_dirs = [
            "scripts",
            ".claude-plugin"
        ]

        required_files = [
            "SKILL.md",
            "scripts/__init__.py",
            ".claude-plugin/marketplace.json"
        ]

        for dir_name in required_dirs:
            dir_path = os.path.join(self.skill_path, dir_name)
            if not os.path.isdir(dir_path):
                self.errors.append(f"缺少必需目录: {dir_name}/")

        for file_name in required_files:
            file_path = os.path.join(self.skill_path, file_name)
            if not os.path.isfile(file_path):
                self.errors.append(f"缺少必需文件: {file_name}")

        # 可选文件检查
        optional_files = ["README.md", "LICENSE"]
        for file_name in optional_files:
            file_path = os.path.join(self.skill_path, file_name)
            if not os.path.isfile(file_path):
                self.warnings.append(f"建议添加文件: {file_name}")

    def _validate_skill_md(self):
        """验证 SKILL.md 格式"""
        skill_md_path = os.path.join(self.skill_path, "SKILL.md")

        if not os.path.isfile(skill_md_path):
            return

        with open(skill_md_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 验证 frontmatter
        frontmatter_pattern = r'^---\n(.*?)\n---'
        match = re.search(frontmatter_pattern, content, re.DOTALL)

        if not match:
            self.errors.append("SKILL.md 缺少 YAML frontmatter (---)")
            return

        frontmatter = match.group(1)

        # 必需字段
        required_fields = ['name', 'description']
        for field in required_fields:
            if f'{field}:' not in frontmatter:
                self.errors.append(f"SKILL.md frontmatter 缺少必需字段: {field}")

        # 验证 name 格式
        name_match = re.search(r'name:\s*(.+)', frontmatter)
        if name_match:
            name = name_match.group(1).strip()
            # 只允许小写字母、数字、连字符
            if not re.match(r'^[a-z0-9-]+$', name):
                self.errors.append(f"SKILL.md name 格式错误: 只允许小写字母、数字、连字符")
            if len(name) > 64:
                self.errors.append(f"SKILL.md name 超过64字符限制")

    def _validate_marketplace_json(self):
        """验证 marketplace.json 格式"""
        json_path = os.path.join(self.skill_path, ".claude-plugin", "marketplace.json")

        if not os.path.isfile(json_path):
            return

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            self.errors.append(f"marketplace.json JSON解析错误: {e}")
            return

        # 必需字段
        required_fields = ['name', 'version', 'description', 'plugins']
        for field in required_fields:
            if field not in data:
                self.errors.append(f"marketplace.json 缺少必需字段: {field}")

        # 验证 owner 格式 (必须是对象，不能是字符串)
        if 'owner' in data:
            if isinstance(data['owner'], str):
                self.errors.append("marketplace.json owner 必须是对象格式，不能是字符串")
            elif isinstance(data['owner'], dict):
                owner_fields = ['name']
                for field in owner_fields:
                    if field not in data['owner']:
                        self.warnings.append(f"marketplace.json owner 建议包含字段: {field}")

        # 验证 plugins 格式
        if 'plugins' in data:
            if not isinstance(data['plugins'], list):
                self.errors.append("marketplace.json plugins 必须是数组")
            elif len(data['plugins']) > 0:
                plugin = data['plugins'][0]
                plugin_required = ['name', 'description', 'source', 'skills']
                for field in plugin_required:
                    if field not in plugin:
                        self.errors.append(f"marketplace.json plugins[0] 缺少字段: {field}")

        # 验证版本格式
        if 'version' in data:
            version = data['version']
            if not re.match(r'^\d+\.\d+\.\d+$', version):
                self.warnings.append(f"marketplace.json version 建议使用 semver 格式 (如 1.0.0)")

    def _validate_init_py(self):
        """验证 __init__.py"""
        init_path = os.path.join(self.skill_path, "scripts", "__init__.py")

        if not os.path.isfile(init_path):
            return

        with open(init_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查是否有 __all__ 导出
        if '__all__' not in content:
            self.warnings.append("scripts/__init__.py 建议定义 __all__ 列表")

        # 检查导入语句
        if 'from .' not in content and 'import' not in content:
            self.warnings.append("scripts/__init__.py 没有导入任何模块")

    def _validate_readme(self):
        """验证 README.md"""
        readme_path = os.path.join(self.skill_path, "README.md")

        if not os.path.isfile(readme_path):
            return

        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查基本结构
        if len(content) < 100:
            self.warnings.append("README.md 内容过短，建议添加更多说明")

        if '# ' not in content:
            self.warnings.append("README.md 建议添加标题")

    def _validate_license(self):
        """验证 LICENSE"""
        license_path = os.path.join(self.skill_path, "LICENSE")

        if not os.path.isfile(license_path):
            return

        with open(license_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if len(content) < 100:
            self.warnings.append("LICENSE 内容过短，请确认许可证完整")


def validate_skill(skill_path: str) -> Dict:
    """
    验证 Skill 格式

    Args:
        skill_path: Skill 目录路径

    Returns:
        验证结果
    """
    validator = FormatValidator(skill_path)
    passed, errors, warnings = validator.validate_all()

    return {
        "skill_path": skill_path,
        "skill_name": validator.skill_name,
        "passed": passed,
        "errors": errors,
        "warnings": warnings,
        "error_count": len(errors),
        "warning_count": len(warnings)
    }


def validate_all_skills(base_path: str) -> List[Dict]:
    """
    验证目录下所有 Skill

    Args:
        base_path: 基础目录路径

    Returns:
        所有验证结果
    """
    results = []

    for item in os.listdir(base_path):
        item_path = os.path.join(base_path, item)
        if os.path.isdir(item_path) and item.endswith('-cskill'):
            result = validate_skill(item_path)
            results.append(result)

    return results


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    print(f"验证目录: {path}\n")

    results = validate_all_skills(path)

    total_errors = 0
    total_warnings = 0

    for result in results:
        status = "✅" if result["passed"] else "❌"
        print(f"{status} {result['skill_name']}")

        for error in result["errors"]:
            print(f"   ❌ {error}")
            total_errors += 1

        for warning in result["warnings"]:
            print(f"   ⚠️  {warning}")
            total_warnings += 1

        print()

    print("=" * 50)
    print(f"总计: {len(results)} 个 Skill, {total_errors} 个错误, {total_warnings} 个警告")
