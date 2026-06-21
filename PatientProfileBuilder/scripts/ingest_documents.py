"""
ingest_documents.py — Convert health records in any format to normalized markdown text.

Uses markitdown as the primary converter (PDF, Word, Excel, PowerPoint, images, HTML, etc.),
with fallback extractors for edge cases.

Usage:
    python ingest_documents.py <input_file_or_dir> [--output OUTPUT_DIR] [--ocr]

Dependencies:
    pip install markitdown pdfplumber PyMuPDF python-docx pillow pytesseract
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Optional imports — not all are required if markitdown handles the format
# ---------------------------------------------------------------------------

try:
    from markitdown import MarkItDown
    HAS_MARKITDOWN = True
except ImportError:
    HAS_MARKITDOWN = False
    print("[WARN] markitdown not installed. Install with: pip install markitdown")

try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False

try:
    import fitz  # PyMuPDF
    HAS_PYMUPDF = True
except ImportError:
    HAS_PYMUPDF = False

try:
    from docx import Document
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False

try:
    from PIL import Image
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False

try:
    import pytesseract
    HAS_TESSERACT = True
except ImportError:
    HAS_TESSERACT = False

# ---------------------------------------------------------------------------
# File-type detection
# ---------------------------------------------------------------------------

TEXT_EXTENSIONS = {".txt", ".md", ".csv", ".json", ".xml", ".html", ".htm"}

MARKITDOWN_EXTENSIONS = {
    ".pdf", ".docx", ".pptx", ".xlsx", ".xls",
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif",
    ".mp3", ".wav", ".m4a", ".ogg",
    ".epub", ".rtf", ".odt",
    ".zip",
}

def detect_format(filepath: str) -> str:
    """Return the format kind of a file."""
    ext = Path(filepath).suffix.lower()
    if ext in TEXT_EXTENSIONS:
        return "text"
    if ext in MARKITDOWN_EXTENSIONS:
        return "markitdown"
    if ext in (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif"):
        return "image"
    return "unknown"


# ---------------------------------------------------------------------------
# Converters
# ---------------------------------------------------------------------------

def convert_with_markitdown(filepath: str) -> str:
    """Use Microsoft markitdown to convert a file to markdown."""
    if not HAS_MARKITDOWN:
        raise RuntimeError("markitdown is not installed. Run: pip install markitdown")
    md = MarkItDown()
    result = md.convert(filepath)
    return result.text_content


def convert_text(filepath: str) -> str:
    """Read a plain-text file directly."""
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def convert_pdf_fallback_pdfplumber(filepath: str) -> str:
    """Fallback PDF extraction using pdfplumber (per-page text)."""
    if not HAS_PDFPLUMBER:
        raise RuntimeError("pdfplumber is not installed. Run: pip install pdfplumber")
    pages = []
    with pdfplumber.open(filepath) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            if text:
                pages.append(f"## Page {i}\n\n{text}")
    return "\n\n".join(pages)


def convert_pdf_fallback_pymupdf(filepath: str) -> str:
    """Fallback PDF extraction using PyMuPDF (fitz)."""
    if not HAS_PYMUPDF:
        raise RuntimeError("PyMuPDF is not installed. Run: pip install PyMuPDF")
    doc = fitz.open(filepath)
    pages = []
    for i, page in enumerate(doc, 1):
        text = page.get_text()
        if text:
            pages.append(f"## Page {i}\n\n{text}")
    doc.close()
    return "\n\n".join(pages)


def convert_docx_fallback(filepath: str) -> str:
    """Fallback Word extraction using python-docx."""
    if not HAS_DOCX:
        raise RuntimeError("python-docx is not installed. Run: pip install python-docx")
    doc = Document(filepath)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n\n".join(paragraphs)


def ocr_image(filepath: str, lang: str = "eng") -> str:
    """OCR an image file with Tesseract. Returns extracted text."""
    if not HAS_PILLOW:
        raise RuntimeError("Pillow is not installed. Run: pip install Pillow")
    if not HAS_TESSERACT:
        raise RuntimeError("pytesseract is not installed. Run: pip install pytesseract")
    img = Image.open(filepath)
    text = pytesseract.image_to_string(img, lang=lang)
    return text


# ---------------------------------------------------------------------------
# Main ingestion pipeline
# ---------------------------------------------------------------------------

def ingest_file(
    filepath: str,
    use_ocr: bool = False,
    ocr_lang: str = "eng",
) -> dict:
    """
    Ingest a single file and return:
        {
            "file": str,
            "format": str,
            "method": str,
            "text": str,
            "pages_or_lines": int,
            "error": str | None
        }
    """
    result = {
        "file": filepath,
        "format": detect_format(filepath),
        "method": "",
        "text": "",
        "pages_or_lines": 0,
        "error": None,
    }
    fmt = result["format"]

    try:
        if fmt == "text":
            result["method"] = "direct_read"
            result["text"] = convert_text(filepath)
            result["pages_or_lines"] = result["text"].count("\n") + 1

        elif fmt == "markitdown" and HAS_MARKITDOWN:
            result["method"] = "markitdown"
            result["text"] = convert_with_markitdown(filepath)
            result["pages_or_lines"] = result["text"].count("\n") + 1

        elif fmt == "image" and use_ocr and HAS_TESSERACT:
            result["method"] = "tesseract_ocr"
            result["text"] = ocr_image(filepath, ocr_lang)
            result["pages_or_lines"] = result["text"].count("\n") + 1

        elif fmt == "image" and HAS_MARKITDOWN:
            # markitdown can also handle images (via vision model if configured)
            result["method"] = "markitdown"
            result["text"] = convert_with_markitdown(filepath)
            result["pages_or_lines"] = result["text"].count("\n") + 1

        else:
            # Fallback chain
            ext = Path(filepath).suffix.lower()
            if ext == ".pdf":
                if HAS_PDFPLUMBER:
                    result["method"] = "pdfplumber_fallback"
                    result["text"] = convert_pdf_fallback_pdfplumber(filepath)
                elif HAS_PYMUPDF:
                    result["method"] = "pymupdf_fallback"
                    result["text"] = convert_pdf_fallback_pymupdf(filepath)
                else:
                    raise RuntimeError("No PDF reader available. Install pdfplumber or PyMuPDF.")
            elif ext == ".docx" and HAS_DOCX:
                result["method"] = "python-docx_fallback"
                result["text"] = convert_docx_fallback(filepath)
            else:
                raise RuntimeError(f"No converter available for {ext}. Install markitdown for broad format support.")

            result["pages_or_lines"] = result["text"].count("\n") + 1

    except Exception as e:
        result["error"] = str(e)

    return result


def ingest_directory(
    directory: str,
    use_ocr: bool = False,
    ocr_lang: str = "eng",
    output_dir: Optional[str] = None,
) -> list[dict]:
    """Ingest all supported files in a directory. Optionally write per-file .md outputs."""
    results = []
    path = Path(directory)

    if path.is_file():
        results.append(ingest_file(str(path), use_ocr, ocr_lang))
        return results

    for f in sorted(path.rglob("*")):
        if f.is_file() and not f.name.startswith("."):
            fmt = detect_format(str(f))
            if fmt != "unknown":
                results.append(ingest_file(str(f), use_ocr, ocr_lang))

    return results


def merge_results(results: list[dict]) -> str:
    """Merge all ingestion results into one chronological markdown narrative."""
    parts = []
    parts.append(f"# Combined Patient Health Records\n")
    parts.append(f"**Generated:** {datetime.now().isoformat()}\n")
    parts.append(f"**Files Processed:** {len(results)}\n\n---\n\n")

    for i, r in enumerate(results, 1):
        lang = detect_text_languages(r.get("text", ""))
        lang_note = _lang_note(lang)
        parts.append(f"## Document {i}: {Path(r['file']).name}\n\n")
        parts.append(f"- **Source:** `{r['file']}`\n")
        parts.append(f"- **Format:** {r['format']}\n")
        parts.append(f"- **Method:** {r['method']}\n")
        parts.append(f"- **Languages:** {', '.join(lang)}\n")
        if r.get("error"):
            parts.append(f"- **Error:** {r['error']}\n")
        if lang_note:
            parts.append(lang_note)
        parts.append(f"\n{r['text']}\n\n---\n\n")

    return "".join(parts)


# ---------------------------------------------------------------------------
# Language detection (for multilingual record flagging)
# ---------------------------------------------------------------------------

def detect_text_languages(text: str, sample_size: int = 2000) -> list[str]:
    """
    Quick heuristic language detection based on Unicode ranges.
    Returns list of detected language families.
    """
    sample = text[:sample_size]
    detected = set()

    # CJK Unified Ideographs (Chinese, Japanese, Korean)
    cjk_count = sum(1 for c in sample if '\u4e00' <= c <= '\u9fff')
    if cjk_count > 5:
        detected.add("zh/ja/ko (CJK)")

    # Japanese-specific: Hiragana + Katakana
    hiragana = sum(1 for c in sample if '\u3040' <= c <= '\u309f')
    katakana = sum(1 for c in sample if '\u30a0' <= c <= '\u30ff')
    if hiragana + katakana > 3:
        detected.add("ja (Hiragana/Katakana)")

    # Korean Hangul
    hangul = sum(1 for c in sample if '\uac00' <= c <= '\ud7af')
    if hangul > 5:
        detected.add("ko (Hangul)")

    # Latin with diacritics (French, German, Spanish, etc.)
    latin_ext = sum(1 for c in sample if '\u00c0' <= c <= '\u024f')
    if latin_ext > 5:
        detected.add("fr/de/es/etc. (Latin-ext)")

    # Cyrillic (Russian, etc.)
    cyrillic = sum(1 for c in sample if '\u0400' <= c <= '\u04ff')
    if cyrillic > 5:
        detected.add("ru (Cyrillic)")

    # Arabic
    arabic = sum(1 for c in sample if '\u0600' <= c <= '\u06ff')
    if arabic > 5:
        detected.add("ar (Arabic)")

    # If only ASCII, it's English-dominant
    ascii_count = sum(1 for c in sample if ord(c) < 128 and c.isalpha())
    if ascii_count > len(sample) * 0.5 and not detected:
        detected.add("en (English-dominant)")

    return sorted(detected) if detected else ["en (English-dominant)"]


def _lang_note(languages: list[str]) -> str:
    """Generate a language note for the merged output."""
    non_en = [l for l in languages if "en" not in l]
    if non_en:
        return (f"\n> 🌐 **Non-English content detected:** {', '.join(languages)}\n"
                f"> ⚠️ Translate to English during Phase 2 audit. "
                f"Log all translations to logs/translation.txt.\n")
    return ""


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Convert health records to normalized markdown text."
    )
    parser.add_argument("input", help="Input file or directory")
    parser.add_argument("--output", "-o", help="Output directory for per-file .md and combined .md", default=None)
    parser.add_argument("--ocr", action="store_true", help="Apply OCR to image files")
    parser.add_argument("--ocr-lang", default="eng", help="OCR language (default: eng)")
    parser.add_argument("--json", action="store_true", help="Also output results as JSON")
    args = parser.parse_args()

    results = ingest_directory(args.input, args.ocr, args.ocr_lang)

    if args.output:
        os.makedirs(args.output, exist_ok=True)
        # Write per-file markdown
        for r in results:
            if r.get("text") and not r.get("error"):
                out_name = Path(r["file"]).stem + ".md"
                out_path = os.path.join(args.output, out_name)
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(r["text"])
        # Write combined
        combined = merge_results(results)
        combined_path = os.path.join(args.output, "combined_records.md")
        with open(combined_path, "w", encoding="utf-8") as f:
            f.write(combined)
        print(f"Output written to {args.output}/")

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        success = sum(1 for r in results if not r.get("error"))
        failed = sum(1 for r in results if r.get("error"))
        print(f"Ingested {len(results)} files: {success} OK, {failed} failed")
        if failed:
            for r in results:
                if r.get("error"):
                    print(f"  FAIL: {r['file']} — {r['error']}")

    # Always print the combined output to stdout if no --output
    if not args.output:
        print("\n" + merge_results(results))


if __name__ == "__main__":
    main()
