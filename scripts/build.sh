#!/usr/bin/env bash
# Checks the skill and rebuilds what is derived from it. Run after any edit:
#
#   bash scripts/build.sh           # check, then rebuild the hash and the package
#   bash scripts/build.sh --check   # check only, write nothing
#
# --check is read-only and works on a clean checkout (dist/ is not required).
# Checks: the SKILL.md frontmatter (name, version, description length), that
# the version matches package.json and has a CHANGELOG.md entry, and that every
# reference file SKILL.md points at exists and every reference is routed, the
# size budgets, the claim ledger, the cited URLs and the style heuristics.
# Snippet compilation is separate (needs network): bash scripts/compile_snippets.sh
# Rebuilds: android-design/.living/ORIGINAL.sha256 and dist/android-design.skill, but only
# when they are out of date, so a second run leaves the working tree unchanged.

set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

CHECK_ONLY=0
[[ "${1:-}" == "--check" ]] && CHECK_ONLY=1

SKILL_MD="android-design/SKILL.md"
HASH_FILE="android-design/.living/ORIGINAL.sha256"
DIST="dist/android-design.skill"

fail() { echo "error: $*" >&2; exit 1; }

sha256_of() {
  if command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$1" | awk '{print $1}'
  else
    sha256sum "$1" | awk '{print $1}'
  fi
}

# True when the package exists and unpacks to exactly the skill folder.
dist_is_current() {
  [[ -f "$DIST" ]] || return 1
  local tmp rc=0
  tmp="$(mktemp -d)"
  unzip -q "$DIST" -d "$tmp" 2>/dev/null \
    && diff -r -x .DS_Store "$tmp/android-design" android-design >/dev/null 2>&1 \
    || rc=1
  rm -rf "$tmp"
  return $rc
}

[[ -f "$SKILL_MD" ]] || fail "$SKILL_MD not found"

# Frontmatter: the first block between --- lines must hold name, version, and
# a description of at most 1024 characters.
FRONT="$(awk '/^---[[:space:]]*$/ {n++; next} n==1 {print} n>=2 {exit}' "$SKILL_MD")"
NAME="$(printf '%s\n' "$FRONT" | awk -F': *' '/^name:/ {print $2; exit}')"
SKILL_VERSION="$(printf '%s\n' "$FRONT" | awk -F'"' '/^version:/ {print $2; exit}')"
DESC="$(printf '%s\n' "$FRONT" | sed -n 's/^description: //p')"
DESC_LEN="$(printf '%s' "$DESC" | wc -m | tr -d ' ')"

[[ "$NAME" == "android-design" ]] || fail "frontmatter name is '$NAME', expected android-design"
[[ -n "$SKILL_VERSION" ]] || fail "no quoted version in the SKILL.md frontmatter"
(( DESC_LEN > 0 )) || fail "no description in the SKILL.md frontmatter"
(( DESC_LEN <= 1024 )) || fail "description is $DESC_LEN characters; the limit is 1024"

PKG_VERSION="$(sed -n 's/^  "version": "\(.*\)",$/\1/p' package.json)"
[[ "$PKG_VERSION" == "$SKILL_VERSION" ]] \
  || fail "version mismatch: SKILL.md $SKILL_VERSION, package.json $PKG_VERSION"

grep -q "^## $SKILL_VERSION " CHANGELOG.md \
  || fail "CHANGELOG.md has no entry for $SKILL_VERSION"

# Every reference file that SKILL.md points at must exist.
for ref in $(grep -o 'references/[a-z-]*\.md' "$SKILL_MD" | sort -u); do
  [[ -f "android-design/$ref" ]] || fail "SKILL.md mentions $ref, which does not exist"
done

# Every reference file is routed from SKILL.md (by its file name).
for ref in android-design/references/*.md; do
  grep -q "$(basename "$ref")" "$SKILL_MD" || fail "$(basename "$ref") is not routed from SKILL.md"
done

# Size budgets (PLAN-FINAL.md §3): SKILL.md 12 KB, references 175 KB, .living 25 KB.
bytes() { cat "$@" | wc -c | tr -d ' '; }
(( $(bytes "$SKILL_MD") <= 12288 )) || fail "SKILL.md is over 12 KB"
(( $(bytes android-design/references/*.md) <= 179200 )) || fail "references are over 175 KB"
(( $(bytes android-design/.living/*.md) <= 25600 )) || fail ".living is over 25 KB"

python3 scripts/check_ledger.py || fail "claim ledger check failed"
python3 scripts/check_sources.py || fail "source check failed"
python3 scripts/check_style.py || fail "style check failed"

if (( CHECK_ONLY )); then
  [[ "$(cat "$HASH_FILE" 2>/dev/null)" == "$(sha256_of "$SKILL_MD")" ]] \
    || fail "$HASH_FILE is out of date; run 'bash scripts/build.sh'"
  echo "android-design $SKILL_VERSION: checks passed"
  exit 0
fi

HASH="$(sha256_of "$SKILL_MD")"
[[ "$(cat "$HASH_FILE" 2>/dev/null)" == "$HASH" ]] || echo "$HASH" > "$HASH_FILE"

if ! dist_is_current; then
  mkdir -p dist
  rm -f "$DIST"
  zip -q -r -X "$DIST" android-design -x '*.DS_Store' '*/__pycache__/*'
fi

echo "android-design $SKILL_VERSION"
echo "  description: $DESC_LEN / 1024 characters"
echo "  hash:        $(cat "$HASH_FILE")"
echo "  package:     $DIST ($(unzip -l "$DIST" | tail -1 | awk '{print $2}') entries)"
