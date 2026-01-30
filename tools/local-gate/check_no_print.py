# #!/usr/bin/env python3
# """
# Custom hook: Check for print() statements in production code.
# """

# import ast
# import os
# import re
# import sys
# from typing import Any, List

# import yaml


# class NoPrintChecker:
#     """Check for print() statements in production code."""

#     def __init__(self, config_path: str = "tools/local-gate/rules.yaml"):
#         self.config_path = config_path
#         self.config = self._load_config()

#     def _load_config(self) -> dict[str, Any]:
#         """Load configuration from YAML file."""
#         try:
#             with open(self.config_path, "r", encoding="utf-8") as f:
#                 return yaml.safe_load(f) or {}
#         except FileNotFoundError:
#             print(f"⚠️ Config file not found: {self.config_path}")
#             return {}
#         except yaml.YAMLError as e:
#             print(f"❌ Error loading config: {e}")
#             return {}

#     def _is_allowed_file(self, filepath: str) -> bool:
#         """Check if file is allowed to have print()."""
#         ignore_patterns = self.config.get("ignore", [])
#         for pattern in ignore_patterns:
#             if pattern and re.match(pattern, filepath):
#                 return True

#         allow_patterns = self.config.get("no_print", {}).get("allow_in", [])
#         for pattern in allow_patterns:
#             if pattern and re.match(pattern, filepath):
#                 return True

#         return False

#     def check_file(self, filepath: str) -> List[str]:
#         """Check a single Python file for print() statements."""
#         if not filepath.endswith(".py"):
#             return []

#         if self._is_allowed_file(filepath):
#             return []

#         violations = []

#         try:
#             with open(filepath, "r", encoding="utf-8") as f:
#                 content = f.read()

#             tree = ast.parse(content, filename=filepath)

#             for node in ast.walk(tree):
#                 if isinstance(node, ast.Call):
#                     if isinstance(node.func, ast.Name):
#                         if node.func.id == "print":
#                             message = self.config.get("no_print", {}).get(
#                                 "message", "print() is not allowed in production code"
#                             )
#                             violations.append(f"{filepath}:{node.lineno}: {message}")

#         except SyntaxError as e:
#             violations.append(f"{filepath}: Syntax error: {e}")
#         except Exception as e:
#             violations.append(f"{filepath}: Error: {e}")

#         return violations

#     def run(self, files: List[str]) -> bool:
#         """Run checker on multiple files."""
#         all_violations = []

#         for filepath in files:
#             if os.path.exists(filepath):
#                 violations = self.check_file(filepath)
#                 if violations:
#                     all_violations.extend(violations)

#         if all_violations:
#             print("\n" + "=" * 60)
#             print("PRINT() STATEMENT VIOLATIONS:")
#             print("=" * 60)
#             for violation in all_violations:
#                 print(f"  {violation}")
#             print("=" * 60)
#             return False
#         else:
#             return True


# def main():
#     """Main entry point."""
#     import argparse

#     parser = argparse.ArgumentParser(description="Check for print() statements")
#     parser.add_argument(
#         "--config", default="tools/local-gate/rules.yaml", help="Path to config file"
#     )
#     parser.add_argument("files", nargs="+", help="Python files to check")

#     args = parser.parse_args()

#     checker = NoPrintChecker(args.config)
#     success = checker.run(args.files)

#     sys.exit(0 if success else 1)


# if __name__ == "__main__":
#     main()
