#!/usr/bin/env python3
"""Copies every ```kotlin block in the skill into the compile fixture.

  python3 scripts/extract_snippets.py [--m3 1.4.0]

Writes fixtures/compose/src/main/kotlin/snippets/*.kt, one file per block,
each in its own package with a shared import header. A block whose first
comment names "Compose Material 3 1.5" is skipped when --m3 is a 1.4 version.
Then compile with:  bash scripts/compile_snippets.sh
"""
import pathlib
import re
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL = ROOT / "android-design"
OUT = ROOT / "fixtures" / "compose" / "src" / "main" / "kotlin" / "snippets"
BLOCK = re.compile(r"```kotlin\n(.*?)```", re.S)
HEADER = """\
@file:Suppress("unused", "UNUSED_PARAMETER")
package snippets.{pkg}

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.flow.*

"""


def main():
    m3 = sys.argv[sys.argv.index("--m3") + 1] if "--m3" in sys.argv else "1.5.0-beta01"
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    written = skipped = 0
    for path in sorted(SKILL.rglob("*.md")):
        for n, code in enumerate(BLOCK.findall(path.read_text(encoding="utf-8")), 1):
            if m3.startswith("1.4") and "Compose Material 3 1.5" in code.split("\n", 1)[0]:
                skipped += 1
                continue
            pkg = re.sub(r"\W", "_", path.stem) + f"_{n}"
            (OUT / f"{pkg}.kt").write_text(HEADER.format(pkg=pkg) + code, encoding="utf-8")
            written += 1
    print(f"extract_snippets: {written} snippet(s) for Material 3 {m3}, {skipped} skipped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
