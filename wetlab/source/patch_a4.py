"""Force A4 page size + 2 cm margins into a pandoc-generated .docx.

Pandoc emits a bare <w:sectPr> with no <w:pgSz>, which Word renders as US Letter.
Takes the target path as argv[1] so it cannot silently patch the wrong file.
"""
import re
import shutil
import sys
import zipfile

PGSZ = (
    '<w:pgSz w:w="11906" w:h="16838"/>'
    '<w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134"'
    ' w:header="709" w:footer="709" w:gutter="0"/>'
)


def patch(path):
    tmp = path + ".tmp"
    patched = False
    with zipfile.ZipFile(path, "r") as zin, \
            zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/document.xml":
                x = data.decode("utf-8")
                if "<w:pgSz" in x:
                    print("pgSz already present in {}, left alone".format(path))
                else:
                    x2 = re.sub(r"<w:sectPr\b([^>]*)>",
                                r"<w:sectPr\1>" + PGSZ, x, count=1)
                    if x2 == x:  # self-closing <w:sectPr/>
                        x2 = re.sub(r"<w:sectPr\b([^>]*)/>",
                                    r"<w:sectPr\1>" + PGSZ + "</w:sectPr>",
                                    x, count=1)
                    patched = x2 != x
                    data = x2.encode("utf-8")
            zout.writestr(item, data)
    shutil.move(tmp, path)
    return patched


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: patch_a4.py <file.docx>")
    target = sys.argv[1]
    print("A4 page size patched into {}: {}".format(target, patch(target)))
