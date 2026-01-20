#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

code_paths=(
  "blux_quantum"
  "bq"
)

execution_primitives_regex='subprocess|os\.system|exec\(|spawn\(|child_process|bash -c|sh -c|powershell|cmd\.exe'
token_terms_regex='issue token|mint token|verify token|jwt|sign token|capability token'
guard_lite_responsibilities_regex='guard_(status|ps|net|perms|secrets|quarantine|report)|guard\.status|guard\.ps|guard\.net|guard\.perms|guard\.secrets|guard\.quarantine|guard\.report|lite_(info|activate)|lite\.info|lite\.activate|guard_plugin|lite_plugin'

scan_paths=()
for path in "${code_paths[@]}"; do
  if [[ -d "$path" ]]; then
    scan_paths+=("$path")
  fi
done

if [[ ${#scan_paths[@]} -gt 0 ]]; then
  if rg -n -e "$execution_primitives_regex" "${scan_paths[@]}" >/dev/null; then
    echo "Execution primitives detected in code paths:"
    rg -n -e "$execution_primitives_regex" "${scan_paths[@]}"
    exit 1
  fi

  if rg -n -i -e "$token_terms_regex" "${scan_paths[@]}" >/dev/null; then
    echo "Token issuance/verification terms detected in code paths:"
    rg -n -i -e "$token_terms_regex" "${scan_paths[@]}"
    exit 1
  fi

  if rg -n -i -e "$guard_lite_responsibilities_regex" "${scan_paths[@]}" >/dev/null; then
    echo "Guard/Lite responsibilities detected in code paths:"
    rg -n -i -e "$guard_lite_responsibilities_regex" "${scan_paths[@]}"
    exit 1
  fi
fi

enforcement_paths=()
for path in src lib cmd; do
  if [[ -d "$path" ]]; then
    enforcement_paths+=("$path")
  fi
done

if [[ ${#enforcement_paths[@]} -gt 0 ]]; then
  if rg -n -e "ALLOW|BLOCK|REQUIRE_CONFIRM" "${enforcement_paths[@]}" >/dev/null; then
    echo "Enforcement terms detected in /src /lib /cmd implementation paths:"
    rg -n -e "ALLOW|BLOCK|REQUIRE_CONFIRM" "${enforcement_paths[@]}"
    exit 1
  fi
fi
