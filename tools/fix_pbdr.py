import re, sys, zipfile, shutil, os
src = sys.argv[1]
tmp = src + ".tmp"
zin = zipfile.ZipFile(src)
zout = zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED)
order = ["top", "left", "bottom", "right", "between", "bar"]
def reorder(m):
    inner = m.group(1)
    parts = re.findall(r"<w:(\w+) [^>]*/>", inner)
    elems = {name: re.search(r"<w:%s [^>]*/>" % name, inner).group(0) for name in parts}
    return "<w:pBdr>" + "".join(elems[n] for n in order if n in elems) + "</w:pBdr>"
for item in zin.infolist():
    data = zin.read(item.filename)
    if item.filename == "word/document.xml":
        s = data.decode("utf8")
        s, n = re.subn(r"<w:pBdr>(.*?)</w:pBdr>", reorder, s, flags=re.S)
        print("reordered pBdr blocks:", n)
        data = s.encode("utf8")
    zout.writestr(item, data)
zout.close(); zin.close()
shutil.move(tmp, src)
