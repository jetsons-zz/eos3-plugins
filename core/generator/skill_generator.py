"""
Skill Generator - 一键生成器
生成100%格式正确的 Claude Code Skill
"""

import os
import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Any

# 导入模板
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from templates.skill_template import (
    SKILL_MD_TEMPLATE,
    MARKETPLACE_JSON_TEMPLATE,
    INIT_PY_TEMPLATE,
    MODULE_PY_TEMPLATE,
    FUNCTION_TEMPLATE,
    README_MD_TEMPLATE,
    LICENSE_TEMPLATE,
    TEST_MODULE_TEMPLATE
)

from validators.format_validator import validate_skill
from validators.code_validator import validate_code


class SkillSpec:
    """Skill 规格定义"""

    def __init__(
        self,
        name: str,
        display_name: str,
        description: str,
        tagline: str = "",
        domain: str = "General",
        skill_type: str = "Utility",
        version: str = "1.0.0",
        author: str = "Agent-Skill-Creator",
        owner_name: str = "FrancyJGLisboa",
        owner_email: str = "contact@example.com",
        owner_url: str = "https://github.com/FrancyJGLisboa",
        repository: str = "https://github.com/FrancyJGLisboa/agent-skill-creator",
        keywords: List[str] = None,
        modules: List[Dict] = None
    ):
        # 验证并规范化名称
        self.name = self._normalize_name(name)
        self.display_name = display_name
        self.description = description
        self.tagline = tagline or description[:50]
        self.domain = domain
        self.skill_type = skill_type
        self.version = version
        self.author = author
        self.owner_name = owner_name
        self.owner_email = owner_email
        self.owner_url = owner_url
        self.repository = repository
        self.keywords = keywords or []
        self.modules = modules or []

    def _normalize_name(self, name: str) -> str:
        """规范化名称：只允许小写字母、数字、连字符"""
        # 转小写
        name = name.lower()
        # 替换空格和下划线为连字符
        name = re.sub(r'[\s_]+', '-', name)
        # 移除不允许的字符
        name = re.sub(r'[^a-z0-9-]', '', name)
        # 移除连续的连字符
        name = re.sub(r'-+', '-', name)
        # 移除首尾连字符
        name = name.strip('-')
        # 限制长度
        if len(name) > 60:  # 留4个字符给 -cskill
            name = name[:60]
        return name

    @property
    def full_name(self) -> str:
        """完整名称（带后缀）"""
        return f"{self.name}-cskill"


class ModuleSpec:
    """模块规格定义"""

    def __init__(
        self,
        name: str,
        description: str,
        tagline: str = "",
        functions: List[Dict] = None,
        constants: Dict = None
    ):
        self.name = name
        self.description = description
        self.tagline = tagline
        self.functions = functions or []
        self.constants = constants or {}


class FunctionSpec:
    """函数规格定义"""

    def __init__(
        self,
        name: str,
        description: str,
        params: List[Dict] = None,
        return_type: str = "Dict",
        return_description: str = "结果字典",
        body_template: str = None
    ):
        self.name = name
        self.description = description
        self.params = params or []
        self.return_type = return_type
        self.return_description = return_description
        self.body_template = body_template


class SkillGenerator:
    """Skill 生成器"""

    def __init__(self, output_base_path: str):
        self.output_base_path = output_base_path

    def generate(self, spec: SkillSpec, validate: bool = True) -> Dict:
        """
        生成 Skill

        Args:
            spec: Skill 规格
            validate: 是否在生成后验证

        Returns:
            生成结果
        """
        skill_path = os.path.join(self.output_base_path, spec.full_name)

        # 创建目录结构
        self._create_directories(skill_path)

        # 生成文件
        self._generate_skill_md(skill_path, spec)
        self._generate_marketplace_json(skill_path, spec)
        self._generate_init_py(skill_path, spec)
        self._generate_modules(skill_path, spec)
        self._generate_readme(skill_path, spec)
        self._generate_license(skill_path, spec)
        self._generate_tests(skill_path, spec)

        result = {
            "status": "success",
            "skill_path": skill_path,
            "skill_name": spec.full_name,
            "files_created": self._count_files(skill_path)
        }

        # 验证
        if validate:
            format_result = validate_skill(skill_path)
            code_result = validate_code(skill_path)

            result["validation"] = {
                "format": format_result,
                "code": code_result,
                "passed": format_result["passed"] and code_result["passed"]
            }

            if not result["validation"]["passed"]:
                result["status"] = "warning"
                result["message"] = "生成完成但验证有问题"

        return result

    def _create_directories(self, skill_path: str):
        """创建目录结构"""
        dirs = [
            skill_path,
            os.path.join(skill_path, "scripts"),
            os.path.join(skill_path, ".claude-plugin"),
            os.path.join(skill_path, "tests")
        ]

        for dir_path in dirs:
            os.makedirs(dir_path, exist_ok=True)

    def _generate_skill_md(self, skill_path: str, spec: SkillSpec):
        """生成 SKILL.md"""
        # 构建模块树
        module_tree = ""
        for module in spec.modules:
            module_tree += f"│   ├── {module['name']}.py\n"

        # 构建特性列表
        features = ""
        for i, module in enumerate(spec.modules, 1):
            features += f"### {i}. {module['description']}\n"
            for func in module.get('functions', []):
                features += f"- {func['description']}\n"
            features += "\n"

        # 构建使用示例
        usage_examples = "\n".join([
            f'"{example}"'
            for module in spec.modules
            for example in module.get('examples', [])
        ][:5])

        content = SKILL_MD_TEMPLATE.format(
            skill_name=spec.full_name,
            display_name=spec.display_name,
            description=spec.description,
            version=spec.version,
            author=spec.author,
            skill_type=spec.skill_type,
            domain=spec.domain,
            overview=spec.tagline,
            features=features or "（功能描述）",
            usage_examples=usage_examples or '（使用示例）',
            module_tree=module_tree,
            dependencies="无外部依赖，纯Python实现"
        )

        with open(os.path.join(skill_path, "SKILL.md"), 'w', encoding='utf-8') as f:
            f.write(content)

    def _generate_marketplace_json(self, skill_path: str, spec: SkillSpec):
        """生成 marketplace.json"""
        content = MARKETPLACE_JSON_TEMPLATE.format(
            skill_name=spec.full_name,
            version=spec.version,
            description=spec.description,
            author=spec.author,
            owner_name=spec.owner_name,
            owner_email=spec.owner_email,
            owner_url=spec.owner_url,
            repository=spec.repository,
            keywords_json=json.dumps(spec.keywords, ensure_ascii=False),
            plugin_name=spec.name,
            plugin_description=spec.description
        )

        plugin_dir = os.path.join(skill_path, ".claude-plugin")
        with open(os.path.join(plugin_dir, "marketplace.json"), 'w', encoding='utf-8') as f:
            f.write(content)

    def _generate_init_py(self, skill_path: str, spec: SkillSpec):
        """生成 __init__.py"""
        imports = []
        exports = []

        for module in spec.modules:
            module_name = module['name']
            func_names = [f['name'] for f in module.get('functions', [])]

            if func_names:
                imports.append(f"from .{module_name} import (")
                for fn in func_names:
                    imports.append(f"    {fn},")
                imports.append(")")
                imports.append("")

                for fn in func_names:
                    exports.append(f"    '{fn}',")

        content = INIT_PY_TEMPLATE.format(
            display_name=spec.display_name,
            tagline=spec.tagline,
            imports="\n".join(imports),
            exports="\n".join(exports),
            version=spec.version
        )

        with open(os.path.join(skill_path, "scripts", "__init__.py"), 'w', encoding='utf-8') as f:
            f.write(content)

    def _generate_modules(self, skill_path: str, spec: SkillSpec):
        """生成模块文件"""
        for module in spec.modules:
            self._generate_module(skill_path, module, spec)

    def _generate_module(self, skill_path: str, module: Dict, spec: SkillSpec):
        """生成单个模块文件"""
        module_name = module['name']
        module_desc = module.get('description', '')
        module_tagline = module.get('tagline', '')

        # 生成常量
        constants = module.get('constants', {})
        constants_code = ""
        for const_name, const_value in constants.items():
            if isinstance(const_value, str):
                constants_code += f'{const_name} = "{const_value}"\n'
            elif isinstance(const_value, (dict, list)):
                constants_code += f'{const_name} = {json.dumps(const_value, ensure_ascii=False, indent=4)}\n'
            else:
                constants_code += f'{const_name} = {const_value}\n'

        # 生成函数
        functions_code = ""
        for func in module.get('functions', []):
            functions_code += self._generate_function(func)

        content = MODULE_PY_TEMPLATE.format(
            module_name=module_name,
            module_description=module_desc,
            module_tagline=module_tagline,
            module_constants=constants_code,
            module_functions=functions_code
        )

        with open(os.path.join(skill_path, "scripts", f"{module_name}.py"), 'w', encoding='utf-8') as f:
            f.write(content)

    def _generate_function(self, func: Dict) -> str:
        """生成函数代码"""
        func_name = func['name']
        func_desc = func.get('description', '')
        params = func.get('params', [])
        return_type = func.get('return_type', 'Dict')
        return_desc = func.get('return_description', '结果')

        # 构建参数字符串
        params_str = ", ".join([
            f"{p['name']}: {p.get('type', 'str')}" +
            (f" = {repr(p['default'])}" if 'default' in p else "")
            for p in params
        ])

        # 构建参数文档
        args_doc = "\n".join([
            f"        {p['name']}: {p.get('description', '')}"
            for p in params
        ]) or "        无"

        # 构建函数体
        body = func.get('body', '')
        if not body:
            # 生成默认函数体
            body = self._generate_default_body(func_name, params, return_type)

        # 确保函数体有正确缩进
        body_lines = body.split('\n')
        indented_body = '\n'.join(['    ' + line if line.strip() else line for line in body_lines])

        return FUNCTION_TEMPLATE.format(
            func_name=func_name,
            params=params_str,
            return_type=return_type,
            func_description=func_desc,
            args_doc=args_doc,
            return_description=return_desc,
            func_body=indented_body
        )

    def _generate_default_body(self, func_name: str, params: List[Dict], return_type: str) -> str:
        """生成默认函数体"""
        if return_type == "Dict":
            return '''return {
    "status": "success",
    "message": "操作完成"
}'''
        elif return_type == "List":
            return "return []"
        elif return_type == "str":
            return 'return ""'
        elif return_type == "bool":
            return "return True"
        elif return_type == "int":
            return "return 0"
        elif return_type == "float":
            return "return 0.0"
        else:
            return "pass"

    def _generate_readme(self, skill_path: str, spec: SkillSpec):
        """生成 README.md"""
        features_list = "\n".join([
            f"- {module['description']}"
            for module in spec.modules
        ])

        usage_examples = "\n".join([
            example
            for module in spec.modules
            for example in module.get('examples', [])
        ][:5])

        content = README_MD_TEMPLATE.format(
            display_name=spec.display_name,
            tagline=spec.tagline,
            features_list=features_list or "- （功能列表）",
            usage_examples=usage_examples or "（使用示例）",
            marketplace_url="https://github.com/FrancyJGLisboa/agent-skill-creator",
            skill_name=spec.full_name,
            marketplace_name="agent-skill-creator"
        )

        with open(os.path.join(skill_path, "README.md"), 'w', encoding='utf-8') as f:
            f.write(content)

    def _generate_license(self, skill_path: str, spec: SkillSpec):
        """生成 LICENSE"""
        content = LICENSE_TEMPLATE.format(
            year=datetime.now().year,
            author=spec.author
        )

        with open(os.path.join(skill_path, "LICENSE"), 'w', encoding='utf-8') as f:
            f.write(content)

    def _generate_tests(self, skill_path: str, spec: SkillSpec):
        """生成测试文件"""
        # 收集所有导入
        imports = []
        test_functions = []
        test_calls = []

        for module in spec.modules:
            for func in module.get('functions', []):
                imports.append(func['name'])

                # 生成测试函数
                test_func = f'''
def test_{func['name']}():
    """测试 {func['name']}"""
    try:
        result = {func['name']}()
        print(f"✅ {func['name']}() 返回: {{type(result).__name__}}")
        return True
    except Exception as e:
        print(f"❌ {func['name']}() 错误: {{e}}")
        return False
'''
                test_functions.append(test_func)
                test_calls.append(f'    results.append(("{func["name"]}", test_{func["name"]}()))')

        content = TEST_MODULE_TEMPLATE.format(
            module_name=spec.display_name,
            imports=", ".join(imports),
            test_functions="\n".join(test_functions),
            test_calls="\n".join(test_calls)
        )

        with open(os.path.join(skill_path, "tests", "test_skill.py"), 'w', encoding='utf-8') as f:
            f.write(content)

    def _count_files(self, path: str) -> int:
        """计算生成的文件数量"""
        count = 0
        for root, dirs, files in os.walk(path):
            count += len(files)
        return count


def generate_skill_from_spec(spec_dict: Dict, output_path: str) -> Dict:
    """
    从规格字典生成 Skill

    Args:
        spec_dict: 规格字典
        output_path: 输出路径

    Returns:
        生成结果
    """
    spec = SkillSpec(
        name=spec_dict['name'],
        display_name=spec_dict.get('display_name', spec_dict['name']),
        description=spec_dict['description'],
        tagline=spec_dict.get('tagline', ''),
        domain=spec_dict.get('domain', 'General'),
        skill_type=spec_dict.get('skill_type', 'Utility'),
        version=spec_dict.get('version', '1.0.0'),
        author=spec_dict.get('author', 'Agent-Skill-Creator'),
        keywords=spec_dict.get('keywords', []),
        modules=spec_dict.get('modules', [])
    )

    generator = SkillGenerator(output_path)
    return generator.generate(spec)


# 示例用法
if __name__ == "__main__":
    # 示例：生成一个简单的 Skill
    example_spec = {
        "name": "example-skill",
        "display_name": "Example Skill",
        "description": "这是一个示例 Skill",
        "tagline": "示例 Skill 演示",
        "domain": "Demo",
        "skill_type": "Example",
        "keywords": ["example", "demo"],
        "modules": [
            {
                "name": "main_module",
                "description": "主模块",
                "tagline": "主要功能模块",
                "functions": [
                    {
                        "name": "hello_world",
                        "description": "打印 Hello World",
                        "params": [
                            {"name": "name", "type": "str", "default": "World", "description": "名称"}
                        ],
                        "return_type": "str",
                        "return_description": "问候语",
                        "body": 'return f"Hello, {name}!"'
                    },
                    {
                        "name": "get_info",
                        "description": "获取信息",
                        "params": [],
                        "return_type": "Dict",
                        "return_description": "信息字典"
                    }
                ],
                "examples": [
                    '"Say hello"',
                    '"Get info"'
                ]
            }
        ]
    }

    output_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    result = generate_skill_from_spec(example_spec, output_path)

    print(json.dumps(result, indent=2, ensure_ascii=False))
