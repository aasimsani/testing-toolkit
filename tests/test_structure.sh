#!/usr/bin/env bash
# Run with: bash tests/test_structure.sh
# These are invariants of how the plugin's text is organised. Every file that a
# skill or a reference tells Claude to read must exist, and every skill that a
# file names must ship.
set -uo pipefail

P="$(cd "$(dirname "$0")/.." && pwd)/plugins/testing-toolkit"
fail=0
check() { if eval "$2"; then echo "ok   - $1"; else echo "FAIL - $1"; fail=1; fi; }

skills="$(find "$P/skills" -name SKILL.md 2>/dev/null)"
check "the plugin ships at least one skill" '[ -n "$skills" ]'

# A skill loads under the name in its frontmatter, so that name must match the
# directory that other files use to refer to it.
misnamed="$(for f in $skills; do d="$(basename "$(dirname "$f")")"
  grep -qx "name: $d" "$f" || printf '%s ' "$d"; done)"
check "every skill's name matches its directory${misnamed:+ (mismatch: $misnamed)}" '[ -z "$misnamed" ]'

# Paths written as ${CLAUDE_PLUGIN_ROOT}/... in any markdown file of the plugin.
missing="$(grep -rhoE --include='*.md' '\$\{CLAUDE_PLUGIN_ROOT\}/[A-Za-z0-9_./-]+' "$P" 2>/dev/null |
  sed 's|\${CLAUDE_PLUGIN_ROOT}/||; s|[.]$||' | sort -u |
  while read -r rel; do [ -e "$P/$rel" ] || printf '%s ' "$rel"; done)"
check "every \${CLAUDE_PLUGIN_ROOT} path exists${missing:+ (missing: $missing)}" '[ -z "$missing" ]'

# Skill names written in backticks, such as `test-unit`. The router sends work
# to these names, so each one must be a skill that ships.
unknown="$(grep -rhoE --include='*.md' '`(test-[a-z-]+|chaos-experiment|release-safety|testing)`' "$P/skills" "$P/references" 2>/dev/null |
  tr -d '`' | sort -u | while read -r s; do [ -f "$P/skills/$s/SKILL.md" ] || printf '%s ' "$s"; done)"
check "every skill a file names exists${unknown:+ (unknown: $unknown)}" '[ -z "$unknown" ]'

exit $fail
