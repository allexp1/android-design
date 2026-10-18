#!/usr/bin/env bash
# Compiles the skill's Kotlin snippets against pinned library versions.
# Needs the Android SDK and network access to Maven once.
#
#   bash scripts/compile_snippets.sh           # Material 3 1.5.0-beta01 and 1.4.0
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

JBR="/Applications/Android Studio.app/Contents/jbr/Contents/Home"
[[ -z "${JAVA_HOME:-}" && -d "$JBR" ]] && export JAVA_HOME="$JBR"
export ANDROID_HOME="${ANDROID_HOME:-$HOME/Library/Android/sdk}"

for m3 in 1.5.0-beta01 1.4.0; do
  python3 scripts/extract_snippets.py --m3 "$m3"
  (cd fixtures/compose && gradle -q --console=plain -Pm3="$m3" compileDebugKotlin)
  echo "compile_snippets: Material 3 $m3 ok"
done
