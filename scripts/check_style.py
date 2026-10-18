#!/usr/bin/env python3
"""Heuristic style checks for the skill's text (a heuristic, not a licence check).

  python3 scripts/check_style.py

Flags: long quoted runs (possible verbatim copying), attribution strings,
British spellings the house style avoids, first-person "I", and references
missing their "Applies to" opening or "Sources" section.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL = ROOT / "android-design"
CHECKS = [
    (re.compile(r"[\"“][^\"”\n]{160,}[\"”]"), "long quoted run; paraphrase instead"),
    (re.compile(r"co-authored-by|generated with|noreply@anthropic", re.I), "attribution string"),
    (re.compile(r"\b(colour|behaviour|centre|organis|optimis|favour)", re.I), "use US spelling"),
    (re.compile(r"(^|[\s(])I (think|believe|recommend)\b"), "first person"),
]


def main():
    problems = []
    for path in sorted(SKILL.rglob("*.md")):
        if path.parent.name == ".living":
            continue
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)
        for n, line in enumerate(text.splitlines(), 1):
            for rx, why in CHECKS:
                if rx.search(line):
                    problems.append(f"{rel}:{n}: {why}")
        if path.parent.name == "references" and path.name != "glossary.md":
            if "**Applies to:**" not in text[:600]:
                problems.append(f"{rel}: no 'Applies to' opening")
            if not re.search(r"^## (\d+\. )?Sources", text, re.M):
                problems.append(f"{rel}: no Sources section")
    if problems:
        print("\n".join(problems), file=sys.stderr)
        print(f"check_style: {len(problems)} problem(s)", file=sys.stderr)
        return 1
    print("check_style: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
