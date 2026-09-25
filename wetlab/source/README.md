# Source and build

`biomod_brief.md` is the single authored source for everything in `wetlab/`.
The markdown files one level up and the Word document are both generated from
it. **Edit this file, not the generated ones.**

## Rebuild

From this directory, with [pandoc](https://pandoc.org) on PATH:

```sh
# 1. regenerate the split markdown set
python split_brief.py biomod_brief.md ..

# 2. build the Word document
pandoc biomod_brief.md -o BIOMOD_2026_Project_Brief.docx --toc --toc-depth=2 --standalone
python patch_a4.py BIOMOD_2026_Project_Brief.docx
mv BIOMOD_2026_Project_Brief.docx ..
```

## Why patch_a4.py exists

Pandoc emits a bare `<w:sectPr>` with no `<w:pgSz>`, which Word renders as US
Letter. The script injects A4 dimensions and 2 cm margins. It takes the target
path as an argument - an earlier version had the filename hardcoded, silently
patched the wrong file and reported success, so a few builds went out as
Letter. If you change the build, keep the path explicit.

## Why split_brief.py derives its own boundaries

It locates sections by their `# ` headings rather than by line number, so
inserting or reordering a section in the source does not silently shift the
split. If a heading is renamed the script exits with an error naming it, and
it warns about any heading that no output file claims. Add new sections to the
`GROUPS` table.

## Note on pandoc at Imperial

On Kirill's laptop pandoc is not on PATH; it ships inside RStudio at
`C:/Program Files/RStudio/resources/app/bin/quarto/bin/tools/pandoc.exe`.
