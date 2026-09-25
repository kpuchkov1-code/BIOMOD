"""Build the Word version of the project brief.

One command instead of the three-step pandoc/patch/move dance, which is easy
to get subtly wrong - an earlier hand-run sequence patched the wrong file and
shipped several builds as US Letter.

    python build.py

Does three things the raw pandoc call does not:

  1. Starts each `## Stage N` on a fresh page, so a stage never straddles a
     page turn while someone is pipetting from it.
  2. Forces A4 with 2 cm margins (pandoc emits no page size at all, which
     Word renders as US Letter).
  3. Writes the result next to the split markdown, never over the source.
"""
import pathlib
import re
import shutil
import subprocess
import sys

import patch_a4

HERE = pathlib.Path(__file__).resolve().parent
SOURCE = HERE / "biomod_brief.md"
OUTPUT = HERE.parent / "BIOMOD_2026_Project_Brief.docx"

# pandoc is not on PATH on the Imperial laptop; it ships inside RStudio.
PANDOC_CANDIDATES = [
    "pandoc",
    r"C:/Program Files/RStudio/resources/app/bin/quarto/bin/tools/pandoc.exe",
]

PAGE_BREAK = '\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n\n'
STAGE_HEADING = re.compile(r"^## Stage \d", re.M)


def find_pandoc():
    for candidate in PANDOC_CANDIDATES:
        try:
            subprocess.run([candidate, "--version"], capture_output=True,
                           check=True)
            return candidate
        except (OSError, subprocess.CalledProcessError):
            continue
    sys.exit("pandoc not found; tried: " + ", ".join(PANDOC_CANDIDATES))


def with_page_breaks(text):
    """Put a page break before every stage heading except the first."""
    parts = STAGE_HEADING.split(text)
    if len(parts) < 2:
        return text
    # split() drops the matched text, so rebuild from the match positions.
    out = []
    last = 0
    for n, m in enumerate(STAGE_HEADING.finditer(text)):
        out.append(text[last:m.start()])
        if n > 0:
            out.append(PAGE_BREAK)
        last = m.start()
    out.append(text[last:])
    return "".join(out)


def main():
    pandoc = find_pandoc()
    staged = HERE / "_build_input.md"
    tmp_docx = HERE / "_build.docx"
    try:
        staged.write_text(
            with_page_breaks(SOURCE.read_text(encoding="utf-8")),
            encoding="utf-8")
        subprocess.run(
            [pandoc, str(staged), "-o", str(tmp_docx),
             "--toc", "--toc-depth=2", "--standalone"],
            check=True)
        patch_a4.patch(str(tmp_docx))
        shutil.move(str(tmp_docx), str(OUTPUT))
        print("built {} ({:,} bytes)".format(OUTPUT.name,
                                             OUTPUT.stat().st_size))
    finally:
        for f in (staged, tmp_docx):
            if f.exists():
                f.unlink()


if __name__ == "__main__":
    main()
