# Source and build

`biomod_brief.md` is the single authored source for everything in `wetlab/`.
The markdown files one level up and the Word document are both generated from
it. **Edit this file, not the generated ones.**

## Rebuild

From this directory:

```sh
python split_brief.py biomod_brief.md ..   # regenerate the markdown set
python build.py                            # build the Word document
```

`build.py` finds pandoc itself, so nothing needs to be on PATH.

## What build.py does that a raw pandoc call does not

- **Starts each `## Stage N` on a fresh page**, so a stage never straddles a
  page turn while someone is pipetting from it. The breaks are injected at
  build time, which keeps the markdown clean on GitHub - there are no raw
  OpenXML blocks in the source to trip over.
- **Forces A4 with 2 cm margins**, via `patch_a4.py`. Pandoc emits a bare
  `<w:sectPr>` with no `<w:pgSz>` at all, and Word defaults that to US Letter.
- **Never writes over the source.** An earlier hand-run sequence patched the
  wrong file and reported success, so several builds shipped as Letter before
  anyone noticed. That is why this is one command now rather than three.

## Why split_brief.py derives its own boundaries

It locates sections by their `# ` headings rather than by line number, so
inserting or reordering a section in the source does not silently shift the
split. If a heading is renamed the script exits with an error naming it, and
it warns about any heading that no output file claims. Add new sections to the
`GROUPS` table.

## Note on pandoc at Imperial

On Kirill's laptop pandoc is not on PATH; it ships inside RStudio at
`C:/Program Files/RStudio/resources/app/bin/quarto/bin/tools/pandoc.exe`.
