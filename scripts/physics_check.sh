#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

forbidden_regex='ethic|morality|discern|posture|illusion|therapy|safety policy|harm'

for file in $(git ls-files); do
  case "$file" in
    LICENSE*|scripts/physics_check.sh) continue ;;
  esac
  if rg -n -i -e "$forbidden_regex" "$file" >/dev/null; then
    echo "Forbidden content detected in $file"
    rg -n -i -e "$forbidden_regex" "$file"
    exit 1
  fi
done

for file in $(git ls-files); do
  case "$file" in
    scripts/physics_check.sh) continue ;;
  esac
  hits="$(rg -n -e 'subprocess\\.run\\(|os\\.system\\(' "$file" || true)"
  if [[ -n "$hits" ]]; then
    if echo "$hits" | rg -v 'blux-guard|blux-lite|blux-reg' >/dev/null; then
      echo "Direct tool execution detected in $file"
      echo "$hits"
      exit 1
    fi
  fi
done

expected_phase0_hash="8e13b0236fdfb573ba6db9c6f5de6ed3d154b0f6885f1d30d3294fbc2aa13657"
actual_phase0_hash="$(python - <<'PY'
import hashlib
from pathlib import Path

path = Path("blux_quantum/envelope.py")
print(hashlib.sha256(path.read_bytes()).hexdigest())
PY
)"
if [[ "$actual_phase0_hash" != "$expected_phase0_hash" ]]; then
  echo "Phase 0 contract schema mismatch in blux_quantum/envelope.py"
  echo "expected=$expected_phase0_hash"
  echo "actual=$actual_phase0_hash"
  exit 1
fi
