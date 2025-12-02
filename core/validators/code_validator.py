"""
Code Validator - 代码验证器
验证 Python 代码语法和导入正确性
"""

import os
import sys
import ast
import importlib.util
from typing import Dict, List, Tuple, Set, Optional


class CodeValidator:
    """代码验证器"""

    def __init__(self, skill_path: str):
        self.skill_path = skill_path
        self.skill_name = os.path.basename(skill_path)
        self.scripts_path = os.path.join(skill_path, "scripts")
        self.errors = []
        self.warnings = []

    def validate_all(self) -> Tuple[bool, List[str], List[str]]:
        """
        执行所有代码验证

        Returns:
            (是否通过, 错误列表, 警告列表)
        """
        self.errors = []
        self.warnings = []

        if not os.path.isdir(self.scripts_path):
            self.errors.append("scripts 目录不存在")
            return False, self.errors, self.warnings

        # 1. 验证所有 Python 文件语法
        self._validate_syntax()

        # 2. 验证 __init__.py 导入一致性
        self._validate_imports_consistency()

        # 3. 验证函数签名一致性
        self._validate_function_signatures()

        # 4. 尝试实际导入测试
        self._validate_actual_imports()

        return len(self.errors) == 0, self.errors, self.warnings

    def _validate_syntax(self):
        """验证 Python 语法"""
        for filename in os.listdir(self.scripts_path):
            if filename.endswith('.py'):
                filepath = os.path.join(self.scripts_path, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        source = f.read()
                    ast.parse(source)
                except SyntaxError as e:
                    self.errors.append(f"{filename} 语法错误: 行 {e.lineno}: {e.msg}")
                except Exception as e:
                    self.errors.append(f"{filename} 解析错误: {e}")

    def _validate_imports_consistency(self):
        """验证 __init__.py 导入一致性"""
        init_path = os.path.join(self.scripts_path, "__init__.py")

        if not os.path.isfile(init_path):
            return

        with open(init_path, 'r', encoding='utf-8') as f:
            init_content = f.read()

        try:
            init_tree = ast.parse(init_content)
        except SyntaxError:
            return  # 语法错误已在上一步检查

        # 收集所有从子模块导入的函数
        imported_items = {}  # {module: [func1, func2, ...]}

        for node in ast.walk(init_tree):
            if isinstance(node, ast.ImportFrom):
                if node.module and node.module.startswith('.'):
                    # 相对导入
                    module_name = node.module[1:]  # 去掉开头的点
                else:
                    module_name = node.module or ""

                # 处理 from .module import ...
                if module_name:
                    if module_name not in imported_items:
                        imported_items[module_name] = []
                    for alias in node.names:
                        imported_items[module_name].append(alias.name)

        # 检查每个被导入的函数是否真实存在
        for module_name, functions in imported_items.items():
            module_file = os.path.join(self.scripts_path, f"{module_name}.py")

            if not os.path.isfile(module_file):
                self.errors.append(f"__init__.py 导入了不存在的模块: {module_name}")
                continue

            # 解析模块文件
            with open(module_file, 'r', encoding='utf-8') as f:
                module_content = f.read()

            try:
                module_tree = ast.parse(module_content)
            except SyntaxError:
                continue

            # 收集模块中定义的所有函数和类
            defined_names = set()
            for node in ast.walk(module_tree):
                if isinstance(node, ast.FunctionDef):
                    defined_names.add(node.name)
                elif isinstance(node, ast.ClassDef):
                    defined_names.add(node.name)
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            defined_names.add(target.id)

            # 检查导入的函数是否存在
            for func in functions:
                if func not in defined_names:
                    self.errors.append(
                        f"__init__.py 从 {module_name} 导入了不存在的: {func}"
                    )

    def _validate_function_signatures(self):
        """验证函数签名一致性（检查常见错误）"""
        for filename in os.listdir(self.scripts_path):
            if filename.endswith('.py') and filename != '__init__.py':
                filepath = os.path.join(self.scripts_path, filename)

                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                try:
                    tree = ast.parse(content)
                except SyntaxError:
                    continue

                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        self._check_function(node, filename)

    def _check_function(self, func_node: ast.FunctionDef, filename: str):
        """检查单个函数"""
        func_name = func_node.name

        # 检查返回类型注解
        if func_node.returns is None and not func_name.startswith('_'):
            self.warnings.append(
                f"{filename}:{func_name}() 建议添加返回类型注解"
            )

        # 检查函数体是否为空
        body = func_node.body
        if len(body) == 1 and isinstance(body[0], ast.Pass):
            self.warnings.append(
                f"{filename}:{func_name}() 函数体为空"
            )

        # 检查是否有文档字符串
        if not (body and isinstance(body[0], ast.Expr) and
                isinstance(body[0].value, (ast.Str, ast.Constant))):
            if not func_name.startswith('_'):
                self.warnings.append(
                    f"{filename}:{func_name}() 缺少文档字符串"
                )

    def _validate_actual_imports(self):
        """尝试实际导入模块"""
        # 先清理所有可能存在的 scripts 模块缓存
        modules_to_remove = [k for k in sys.modules.keys()
                            if k == 'scripts' or k.startswith('scripts.')]
        for mod in modules_to_remove:
            del sys.modules[mod]

        # 保存原始 sys.path
        original_path = sys.path.copy()

        # 设置新的 sys.path，只包含当前 skill 路径
        sys.path = [self.skill_path] + [p for p in original_path
                                         if not p.endswith('-cskill')]

        init_path = os.path.join(self.scripts_path, "__init__.py")

        if not os.path.isfile(init_path):
            sys.path = original_path
            return

        try:
            # 使用唯一的模块名避免冲突
            unique_module_name = f"scripts_{self.skill_name.replace('-', '_')}"

            # 使用 importlib 动态导入
            spec = importlib.util.spec_from_file_location(
                "scripts",
                init_path,
                submodule_search_locations=[self.scripts_path]
            )

            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules['scripts'] = module

                # 尝试加载
                spec.loader.exec_module(module)

        except ImportError as e:
            self.errors.append(f"模块导入失败: {e}")
        except Exception as e:
            self.errors.append(f"模块加载错误: {e}")
        finally:
            # 彻底清理所有 scripts 相关模块
            modules_to_remove = [k for k in sys.modules.keys()
                                if k == 'scripts' or k.startswith('scripts.')]
            for mod in modules_to_remove:
                del sys.modules[mod]

            # 恢复原始 sys.path
            sys.path = original_path


def validate_code(skill_path: str) -> Dict:
    """
    验证 Skill 代码

    Args:
        skill_path: Skill 目录路径

    Returns:
        验证结果
    """
    validator = CodeValidator(skill_path)
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


def validate_all_code(base_path: str) -> List[Dict]:
    """
    验证目录下所有 Skill 的代码

    Args:
        base_path: 基础目录路径

    Returns:
        所有验证结果
    """
    results = []

    for item in os.listdir(base_path):
        item_path = os.path.join(base_path, item)
        if os.path.isdir(item_path) and item.endswith('-cskill'):
            result = validate_code(item_path)
            results.append(result)

    return results


if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    print(f"代码验证: {path}\n")

    results = validate_all_code(path)

    total_errors = 0
    total_warnings = 0

    for result in results:
        status = "✅" if result["passed"] else "❌"
        print(f"{status} {result['skill_name']}")

        for error in result["errors"]:
            print(f"   ❌ {error}")
            total_errors += 1

        for warning in result["warnings"][:5]:  # 只显示前5个警告
            print(f"   ⚠️  {warning}")
            total_warnings += 1

        if len(result["warnings"]) > 5:
            print(f"   ... 还有 {len(result['warnings']) - 5} 个警告")

        print()

    print("=" * 50)
    print(f"总计: {len(results)} 个 Skill, {total_errors} 个错误, {total_warnings}+ 个警告")
