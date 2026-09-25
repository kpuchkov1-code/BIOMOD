"""Split the single-file project brief into the wetlab/ documentation set.

The brief is authored as one markdown file so pandoc can build one Word
document from it. The repo wants it as reviewable pieces.

Boundaries are derived from the top-level (`# `) headings rather than from
line numbers, so inserting or reordering a section does not silently shift
the split. Each output file is a named group of consecutive headings.
"""
import pathlib
import re
import sys

# output file -> (title, blurb, [top-level headings it contains, in order])
GROUPS = [
    ("01-project.md", "What the project is",
     "The circuit, the mechanism, and what the model predicts.",
     ["What we are building", "How the circuit works",
      "What the model predicts"]),
    ("02-deviations.md", "How we differ from Fujii",
     "Every deliberate departure from the 2013 paper, and what each one risks.",
     ["How our experiment differs", "Risks these changes create"]),
    ("03-reagents.md", "What goes in each well",
     "Every component, what it does, and the volume that delivers it.",
     ["What goes in each well"]),
    ("04-budget.md", "Reagent budget and well volume",
     "How many runs each reagent buys, why the nickase is the bottleneck, "
     "and whether to halve the well to 50 uL.",
     ["Reagent budget and the well volume decision"]),
    ("05-plate-layout.md", "Plate layout and controls",
     "Which well holds what, and why each control earns its place.",
     ["Plate layout and controls"]),
    ("06-labbook-crosscheck.md", "Cross-check against the lab book",
     "Audrey's bench numbers against this document: agreements, corrections, "
     "and what is still outstanding.",
     ["Cross-check against the lab book"]),
    ("PROTOCOL.md", "Bench protocol",
     "Sequential instructions: what to add, at what concentration, in what "
     "volume. This is the file to have open at the bench.",
     ["BENCH PROTOCOL", "Before the first run"]),
]

NAV = (
    "> Part of the [wet lab documentation set](README.md). "
    "The assembled Word version of all of these is "
    "`BIOMOD_2026_Project_Brief.docx`.\n"
)

HEADING = re.compile(r"^# (.+?)\s*$")


def index_headings(lines):
    """Map each top-level heading to the line range it owns (0-indexed)."""
    starts = [(i, m.group(1)) for i, line in enumerate(lines)
              for m in [HEADING.match(line)] if m]
    spans = {}
    for n, (i, title) in enumerate(starts):
        end = starts[n + 1][0] if n + 1 < len(starts) else len(lines)
        spans[title] = (i, end)
    return spans


def main(src_path, out_dir):
    lines = pathlib.Path(src_path).read_text(encoding="utf-8").splitlines()
    spans = index_headings(lines)
    out = pathlib.Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    claimed = set()
    for name, title, blurb, headings in GROUPS:
        chunks = []
        for h in headings:
            if h not in spans:
                sys.exit("heading not found in brief: {!r}".format(h))
            start, end = spans[h]
            chunks.append("\n".join(lines[start:end]).strip())
            claimed.add(h)
        body = "\n\n".join(chunks)
        text = "# {}\n\n*{}*\n\n{}\n\n---\n\n{}".format(name and title, blurb,
                                                        NAV, body)
        (out / name).write_text(text + "\n", encoding="utf-8")
        print("{:28s} {:5d} lines".format(name, len(body.splitlines())))

    missed = [h for h in spans if h not in claimed]
    if missed:
        print("\nWARNING: headings in the brief that no file claims:")
        for h in missed:
            print("  - {}".format(h))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: split_brief.py <brief.md> <out_dir>")
    main(sys.argv[1], sys.argv[2])
