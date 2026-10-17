"""Lint the skin: catches what Kodi only shows as a broken screen.

    python3 tools/lint_skin.py          # exit status 1 on any problem (CI runs it)

- every XML file parses;
- no window has two controls with one id: Kodi links navigation by id, so a
  duplicate stops up/down at that row (stock Estuary's own duplicates are
  listed in KNOWN_DUPLICATES);
- every $LOCALIZE[n] in the skin's range (31000-31999) has a string in
  strings.po, and every string the skin's own add-ons use ($ADDON[id n]) when
  that add-on's repository is checked out next to this one;
- every $VAR[...], $EXP[...] and include a file uses is defined;
- the generated files match their generators (tools/gen_*.py).
"""

from __future__ import annotations

import re
import subprocess
import sys
import xml.dom.minidom
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
XML = ROOT / "xml"
STRINGS = ROOT / "language" / "resource.language.en_gb" / "strings.po"
# Stock Estuary windows with duplicate ids (labels shown one at a time); not ours.
KNOWN_DUPLICATES = {"DialogMusicInfo.xml": {"130"}, "VideoFullScreen.xml": {"1"}}
SKIN_STRINGS = range(31000, 32000)
# Add-ons whose strings the skin uses, and where their repositories usually are.
ADDON_REPOS = {
    "service.webostv": "kodi-webos-control",
    "service.denonavr": "kodi-denon-control",
    "service.sonos": "kodi-sonos-control",
}
GENERATORS = ("gen_lgtv.py", "gen_denon.py", "gen_sonos.py", "gen_osd_panels.py", "gen_pointer.py")


def string_ids(po: Path) -> set[int]:
    return {int(n) for n in re.findall(r'^msgctxt "#(\d+)"', po.read_text(), re.M)}


def check_parse(files: list[Path]) -> list[str]:
    problems = []
    for f in files:
        try:
            xml.dom.minidom.parse(str(f))
        except Exception as err:  # noqa: BLE001 - any parse error is the finding
            problems.append(f"{f.name}: not well-formed XML ({err})")
    return problems


def check_duplicate_ids(files: list[Path]) -> list[str]:
    problems = []
    for f in files:
        text = f.read_text()
        if "<window" not in text:
            continue
        counts = Counter(re.findall(r'<control type="\w+" id="(\d+)"', text))
        extra = {i for i, n in counts.items() if n > 1} - KNOWN_DUPLICATES.get(f.name, set())
        if extra:
            problems.append(f"{f.name}: duplicate control ids {sorted(extra, key=int)}")
    return problems


def check_strings(files: list[Path]) -> list[str]:
    problems = []
    skin = string_ids(STRINGS)
    addons = {}
    for addon, repo in ADDON_REPOS.items():
        po = ROOT.parent / repo / "resources" / "language" / "resource.language.en_gb" / "strings.po"
        if po.is_file():
            addons[addon] = string_ids(po)
    for f in files:
        text = f.read_text()
        for n in sorted({int(n) for n in re.findall(r"\$LOCALIZE\[(\d+)\]", text)}):
            if n in SKIN_STRINGS and n not in skin:
                problems.append(f"{f.name}: $LOCALIZE[{n}] has no string in strings.po")
        for addon, n in sorted(set(re.findall(r"\$ADDON\[([\w.]+) (\d+)\]", text))):
            if addon in addons and int(n) not in addons[addon]:
                problems.append(f"{f.name}: $ADDON[{addon} {n}] has no string in {addon}")
    return problems


def check_references(files: list[Path]) -> list[str]:
    texts = {f: f.read_text() for f in files}
    everything = "\n".join(texts.values())
    variables = set(re.findall(r'<variable name="([^"]+)"', everything))
    expressions = set(re.findall(r'<expression name="([^"]+)"', everything))
    includes = set(re.findall(r'<include name="([^"]+)"', everything))
    problems = []
    for f, text in texts.items():
        for name in sorted(set(re.findall(r"\$VAR\[([^\],\]]+)", text)) - variables):
            problems.append(f"{f.name}: $VAR[{name}] is not defined")
        for name in sorted(set(re.findall(r"\$EXP\[([^\]]+)\]", text)) - expressions):
            problems.append(f"{f.name}: $EXP[{name}] is not defined")
        used = set(re.findall(r"<include>([^<$]+)</include>", text))
        used |= set(re.findall(r'<include content="([^"$]+)"', text))
        for name in sorted(used - includes):
            problems.append(f"{f.name}: include {name} is not defined")
    return problems


def check_generated() -> list[str]:
    """Run each generator; report the files it changed (left as generated)."""
    before = {f: f.read_bytes() for f in XML.glob("*.xml")}
    problems = []
    for gen in GENERATORS:
        result = subprocess.run([sys.executable, str(ROOT / "tools" / gen)], cwd=ROOT, capture_output=True, text=True)
        if result.returncode:
            problems.append(f"tools/{gen} failed: {(result.stderr or result.stdout).strip()}")
    for f in sorted(XML.glob("*.xml")):
        if before.get(f) != f.read_bytes():
            problems.append(f"{f.name}: was out of date with its generator (now regenerated: review and commit)")
    return problems


def main() -> int:
    files = sorted(XML.glob("*.xml"))
    problems = check_parse(files)
    if not problems:
        problems += check_duplicate_ids(files) + check_strings(files) + check_references(files)
    if "--no-generated" not in sys.argv:
        problems += check_generated()
    for problem in problems:
        print(problem)
    print(f"{len(problems)} problem(s)" if problems else "skin lint: ok")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
