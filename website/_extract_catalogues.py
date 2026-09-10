from pathlib import Path
import fitz

downloads = Path(r"C:\Users\gardo\Downloads")
files = [
    "HOME CENTER - COIMBATORE.pdf",
    "Athangudi Series .pdf",
    "GC COIMBATORE.pdf",
    "12x18-wall tiles.pdf",
    "GC TILES COIMBATORE LLP.pdf",
    "LEVERPOOL 15.pdf",
    "(20)SONEX - 600x1200 EARTH COLLECTION(MATT).pdf",
    "HOME CENTRE COIMBATORE MOROCAN COLLECTION_R.pdf",
]
out = Path(r"C:\Users\gardo\Vicky\website\catalogue_extract")
out.mkdir(parents=True, exist_ok=True)

for name in files:
    fp = downloads / name
    if not fp.exists():
        print("MISS", name)
        continue
    doc = fitz.open(fp)
    text_chunks = []
    for i, page in enumerate(doc):
        t = page.get_text("text") or ""
        if t.strip():
            text_chunks.append(f"--- PAGE {i+1} ---\n{t.strip()}")
    stem = "".join(c if c.isalnum() or c in "-_" else "_" for c in fp.stem)[:50]
    (out / f"{stem}.txt").write_text("\n\n".join(text_chunks)[:150000], encoding="utf-8")
    preview_dir = out / stem
    preview_dir.mkdir(exist_ok=True)
    nprev = min(8, len(doc))
    for i in range(nprev):
        pix = doc[i].get_pixmap(matrix=fitz.Matrix(1.15, 1.15), alpha=False)
        pix.save(str(preview_dir / f"page_{i+1:02d}.jpg"))
    print(f"{name}: pages={len(doc)} text={sum(len(x) for x in text_chunks)} prev={nprev}")
print("DONE")
