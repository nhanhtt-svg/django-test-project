#!/bin/bash
set -euo pipefail

# Lấy staged files (đã git add)
changed_files=$(git diff --cached --name-only --diff-filter=ACM)

if [ -z "$changed_files" ]; then
  echo "No Python files staged, skipping tests."
  exit 0
fi

# Flags cho từng app (dễ mở rộng cho app C, D...)
declare -A run_tests
run_tests["appA"]=false
run_tests["appB"]=false
run_tests["appC"]=false  # Thêm nếu cần

# Kiểm tra thay đổi ở source hoặc test của app
while IFS= read -r file; do
  if [[ $file == appA/* ]] || [[ $file == tests/appA/* || $file == appA/tests/* ]]; then
    run_tests["appA"]=true
  fi
  if [[ $file == appB/* ]] || [[ $file == tests/appB/* || $file == appB/tests/* ]]; then
    run_tests["appB"]=true
  fi
  if [[ $file == appC/* ]] || [[ $file == tests/appC/* || $file == appC/tests/* ]]; then
    run_tests["appC"]=true
  fi
done <<< "$changed_files"

# Chạy test nếu app bị ảnh hưởng
any_failed=false

for app in "${!run_tests[@]}"; do
  if ${run_tests[$app]}; then
    test_dir="tests/unit/$app"  # Chỉnh theo cấu trúc thực tế của bạn (ví dụ tests/appA/unit, appA/tests/unit, v.v.)
    if [ -d "$test_dir" ]; then
      echo "🧪 Running unit tests for $app ($test_dir)..."
      python3 -m pytest "$test_dir" -m 'not slow' -q --tb=short || any_failed=true
    else
      echo "⚠️ No test dir for $app at $test_dir, skipping."
    fi
  fi
done

if $any_failed; then
  echo "❌ Some tests failed! Commit aborted."
  exit 1
fi

echo "✅ Relevant tests passed!"
exit 0