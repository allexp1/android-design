#!/usr/bin/env python3
"""Checks the claim ledger (ledger/claims.tsv) against the skill's text.

  python3 scripts/check_ledger.py

Rules (PLAN-FINAL.md §5):
  - every VERIFIED / RESOLVED-BY-SOURCE / CONFLICT row's value appears in each
    file listed in its `files` column;
  - in those files, a CONFLICT row's value has the word "conflict" within
    400 characters of it;
  - an UNVERIFIED row's value appears in no file of the skill.
Exits 1 and lists every failure; prints a one-line summary otherwise.
"""
import csv
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL = ROOT / "android-design"
LEDGER = ROOT / "ledger" / "claims.tsv"
STATUSES = {"VERIFIED", "RESOLVED-BY-SOURCE", "CONFLICT", "UNVERIFIED"}
NEAR = 400


def skill_file(name):
    name = name.strip()
    if name == "SKILL.md":
        return SKILL / "SKILL.md"
    return SKILL / "references" / name


def all_skill_text():
    return {p: p.read_text(encoding="utf-8") for p in SKILL.rglob("*.md")}


def main():
    errors = []
    texts = all_skill_text()
    with LEDGER.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    ids = set()
    for row in rows:
        rid, value, status = row["id"], row["value"].strip(), row["status"].strip()
        if rid in ids:
            errors.append(f"{rid}: duplicate id")
        ids.add(rid)
        if status not in STATUSES:
            errors.append(f"{rid}: unknown status {status!r}")
            continue
        if not value:
            errors.append(f"{rid}: empty value")
            continue
        files = [x for x in row["files"].replace("|", "").split(";") if x.strip()]
        if status == "UNVERIFIED":
            for path, text in texts.items():
                if value in text:
                    errors.append(f"{rid}: UNVERIFIED value {value!r} appears in {path.relative_to(ROOT)}")
            continue
        if not files:
            errors.append(f"{rid}: no files listed")
        for name in files:
            path = skill_file(name)
            if path not in texts:
                errors.append(f"{rid}: listed file {name.strip()} does not exist")
                continue
            text = texts[path]
            at = text.find(value)
            if at < 0:
                errors.append(f"{rid}: value {value!r} not found in {name.strip()}")
                continue
            if status == "CONFLICT":
                ok = False
                while at >= 0:
                    window = text[max(0, at - NEAR): at + len(value) + NEAR].lower()
                    if "conflict" in window:
                        ok = True
                        break
                    at = text.find(value, at + 1)
                if not ok:
                    errors.append(f"{rid}: CONFLICT value {value!r} in {name.strip()} is not marked as a conflict")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        print(f"check_ledger: {len(errors)} problem(s) in {len(rows)} rows", file=sys.stderr)
        return 1
    print(f"check_ledger: {len(rows)} rows ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
