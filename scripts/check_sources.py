#!/usr/bin/env python3
"""Checks the URLs the skill cites.

  python3 scripts/check_sources.py            # offline checks only
  python3 scripts/check_sources.py --online   # also fetch every URL

Offline: every URL is on an allowed host, and none is listed as moved or
archived in .living/sources.md. Online: GET each URL (following redirects)
and report it OK, MOVED (ended on a different path) or UNKNOWN (no answer,
an error status, or a page without content). UNKNOWN is never "verified";
the online pass only reports and does not fail the build.
"""
import pathlib
import re
import sys
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL = ROOT / "android-design"
SOURCES = SKILL / ".living" / "sources.md"
URL = re.compile(r"https?://[^\s)>`'\"|]+")
ALLOWED = (
    "developer.android.com", "android-developers.googleblog.com", "m3.material.io",
    "design.google", "github.com", "www.figma.com", "material-foundation.github.io",
    "support.google.com", "developers.google.com", "blog.google", "raw.githubusercontent.com",
)


def cited_urls():
    urls = {}
    for path in sorted(SKILL.rglob("*.md")):
        if path.parent.name == ".living":
            continue
        for url in URL.findall(path.read_text(encoding="utf-8")):
            urls.setdefault(url.rstrip(".,;:"), path.relative_to(ROOT))
    return urls


def moved_urls():
    text = SOURCES.read_text(encoding="utf-8")
    section = text.split("## MOVED", 1)[1] if "## MOVED" in text else ""
    return {u.rstrip(".,;:") for u in URL.findall(section)}


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "android-design-skill-check"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = resp.read(200_000)
            final = resp.geturl()
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        return "UNKNOWN", str(exc)
    if len(body) < 500:
        return "UNKNOWN", "page has no content"
    strip = lambda u: u.split("#")[0].split("?")[0].rstrip("/")
    if strip(final) != strip(url):
        return "MOVED", final
    return "OK", ""


def main():
    online = "--online" in sys.argv
    urls = cited_urls()
    moved = moved_urls()
    errors = []
    for url, where in urls.items():
        host = url.split("/")[2]
        if host not in ALLOWED:
            errors.append(f"{where}: {url} is not on an allowed host")
        if url in moved:
            errors.append(f"{where}: {url} is listed as moved or archived in .living/sources.md")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        print(f"check_sources: {len(errors)} problem(s)", file=sys.stderr)
        return 1
    print(f"check_sources: {len(urls)} URLs on allowed hosts, none moved")
    if online:
        counts = {}
        for url in sorted(urls):
            status, detail = fetch(url)
            counts[status] = counts.get(status, 0) + 1
            if status != "OK":
                print(f"  {status:7} {url} {detail}")
        print("  online: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
