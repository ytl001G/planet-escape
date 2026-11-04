"""대사집 md → pdf. 사용법: python md2pdf.py [파일.md ...]  (인자 없으면 md/*.md 전부 → pdf/)"""
import sys, subprocess, pathlib, markdown

PDF_DIR = pathlib.Path(__file__).parent / "pdf"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
# 파일명에 든 인물 이름 → 대표색 (원색, 파스텔)
COLORS = {"알렉스": ("#E53935", "#F8CCCC"), "비아": ("#FB8C00", "#FFE0BD"),
          "오펠리아": ("#FDD835", "#FFF3BD"), "노아": ("#43A047", "#D2EBD3"),
          "에바": ("#1E88E5", "#CCE2FA"), "릴리": ("#8E24AA", "#E6D3F0"),
          "시스템": ("#757575", "#E0E0E0"), "오메가": ("#546E7A", "#CFD8DC")}

CSS = """
@page { size: A4; margin: 18mm 16mm; }
body { font-family: 'Malgun Gothic', sans-serif; font-size: 10.5pt; line-height: 1.55; color: #222; }
h1 { border-bottom: 4px solid MAIN; padding-bottom: 4px; }
h2 { background: PASTEL; border-left: 6px solid MAIN; padding: 4px 10px; font-size: 12.5pt; margin-top: 22px; break-after: avoid; }
table { width: 100%; border-collapse: collapse; margin: 6px 0 12px; }
tr { break-inside: avoid; }
th { background: PASTEL; }
th, td { border: 1px solid #ccc; padding: 5px 8px; vertical-align: top; text-align: left; }
td:first-child, th:first-child { width: 3.6em; white-space: nowrap; text-align: center; color: #777; }
td em { color: #888; }  /* 전체본 지문 */
code { font-family: inherit; font-size: 8.5pt; color: #666; background: #f1f1f1; padding: 0 4px; border-radius: 3px; }  /* [태그] */
table.whole td:nth-child(2), table.whole th:nth-child(2) { width: 6.5em; white-space: nowrap; }
"""

def convert(md_path: pathlib.Path):
    main, pastel = next((c for k, c in COLORS.items() if k in md_path.stem), ("#333", "#eee"))
    body = markdown.markdown(md_path.read_text(encoding="utf-8"), extensions=["tables"])
    if "<th>화자</th>" in body:  # 전체본: 화자 칸 폭 고정 + 화자 칸을 인물 대표색으로
        body = body.replace("<table>", '<table class="whole">')
        for name, (m, p) in COLORS.items():
            body = body.replace(f"<td>{name}</td>", f'<td style="background:{p};border-left:5px solid {m}">{name}</td>')
    css = CSS.replace("PASTEL", pastel).replace("MAIN", main)
    PDF_DIR.mkdir(exist_ok=True)
    html_path = PDF_DIR / (md_path.stem + ".html")
    html_path.write_text(f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{body}</body></html>", encoding="utf-8")
    pdf_path = PDF_DIR / (md_path.stem + ".pdf")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf_path}", html_path.resolve().as_uri()], check=True, capture_output=True)
    html_path.unlink()
    print("ok:", pdf_path.name)

if __name__ == "__main__":
    here = pathlib.Path(__file__).parent
    files = [pathlib.Path(a) for a in sys.argv[1:]] or sorted((here / "md").glob("*.md"))
    for f in files:
        convert(f)
