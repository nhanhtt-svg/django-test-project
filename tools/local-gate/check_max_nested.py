# import ast
# import sys


# def check_nested_levels(node, current_depth=0, max_depth=20, violations=None) -> list[dict]:
#     """Đếm mức độ lồng nhau."""
#     if violations is None:
#         violations = []

#     if isinstance(node, (ast.If, ast.For, ast.While)):
#         current_depth += 1

#         if current_depth > max_depth:
#             violations.append({"line": node.lineno, "depth": current_depth, "max": max_depth})

#     for child in ast.iter_child_nodes(node):
#         check_nested_levels(child, current_depth, max_depth, violations)

#     return violations


# def check_file(filepath, max_depth=20) -> list[dict]:
#     """Check một file Python."""
#     try:
#         with open(filepath, "r", encoding="utf-8") as f:
#             code = f.read()

#         tree = ast.parse(code)
#         violations = check_nested_levels(tree, max_depth=max_depth)

#         return violations

#     except Exception:
#         return []


# def main():
#     if len(sys.argv) < 2:
#         sys.exit(0)

#     all_violations = []
#     max_depth = 20

#     for arg in sys.argv[1:]:
#         if arg.startswith("--max-depth="):
#             try:
#                 max_depth = int(arg.split("=")[1])
#             except ValueError:
#                 pass

#     files_to_check = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

#     for filepath in files_to_check:
#         if "Test_commit_local.py" in filepath or "test_" in filepath:
#             continue

#         violations = check_file(filepath, max_depth)

#         for violation in violations:
#             all_violations.append(
#                 f"{filepath}:{violation['line']}: "
#                 f"Có {violation['depth']} mức lồng (tối đa {violation['max']})"
#             )

#     if all_violations:
#         print("\n" + "=" * 60)
#         print("VIOLATION: QUÁ NHIỀU MỨC LỒNG NHAU")
#         print("=" * 60)
#         for v in all_violations:
#             print(f"  ❌ {v}")
#         print("=" * 60)
#         sys.exit(1)



# if __name__ == "__main__":
#     main()
