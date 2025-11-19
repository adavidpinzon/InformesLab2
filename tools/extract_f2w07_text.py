from pathlib import Path
from pdfminer.high_level import extract_text
import sys


def main() -> int:
    pdf_path = Path('Taller_3') / 'F2W07.pdf'
    out_path = Path('Taller_3') / 'F2W07_extracted.txt'

    if not pdf_path.exists():
        sys.stderr.write(f'ERROR: PDF not found: {pdf_path}\n')
        return 1

    try:
        text = extract_text(str(pdf_path))
    except Exception as exc:
        sys.stderr.write(f'ERROR extracting text: {exc}\n')
        return 2

    try:
        out_path.write_text(text or '', encoding='utf-8')
    except Exception as exc:
        sys.stderr.write(f'ERROR writing output: {exc}\n')
        return 3

    print(f'Wrote {out_path} ({len(text or "")} chars)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
