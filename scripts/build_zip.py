"""Build an installable skin zip: dist/skin.estuary.yblod-<version>.zip."""

from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ADDON_ID = "skin.estuary.yblod"
EXCLUDE_TOP = {".git", ".github", "dist", "scripts", "tools", ".gitignore"}


def version() -> str:
    match = re.search(r'<addon[^>]*\sversion="([^"]+)"', (ROOT / "addon.xml").read_text())
    if not match:
        sys.exit("version not found in addon.xml")
    return match.group(1)


def main() -> None:
    out = ROOT / "dist" / f"{ADDON_ID}-{version()}.zip"
    out.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(ROOT.rglob("*")):
            rel = path.relative_to(ROOT)
            if path.is_dir() or rel.parts[0] in EXCLUDE_TOP or path.name == ".DS_Store":
                continue
            zf.write(path, f"{ADDON_ID}/{rel.as_posix()}")
    print(out)


if __name__ == "__main__":
    main()
