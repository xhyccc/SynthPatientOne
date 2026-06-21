#!/usr/bin/env python3
"""
ocr_images.py — Handle image-heavy health records.

Strategy for image-based documents:
1. For scanned PDFs: render each page as PNG via PyMuPDF (fitz) or pdf2image
2. For standalone images (JPG, PNG, TIFF): convert/pass-through to PNG
3. OCR via Tesseract (pytesseract) for text extraction
4. For handwriting or complex medical images (X-rays, scans, photos):
   defer to multimodal_analyze.py for vision-model analysis
5. Embed extracted text back into the normalized markdown stream

Usage:
    python ocr_images.py <input_path> [--output-dir <dir>] [--lang <lang>] [--multimodal]
"""

from __future__ import annotations

import argparse
import base64
import io
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ensure_png(image_path: Path) -> Path:
    """Convert any image to PNG if it isn't already; return path to PNG."""
    if image_path.suffix.lower() == ".png":
        return image_path
    try:
        from PIL import Image
        img = Image.open(image_path)
        png_path = image_path.with_suffix(".png")
        img.save(png_path, "PNG")
        return png_path
    except ImportError:
        print("[ocr_images] WARNING: Pillow not available, cannot convert to PNG", file=sys.stderr)
        return image_path


def _render_pdf_to_images(pdf_path: Path, dpi: int = 200) -> List[Path]:
    """Render each page of a PDF to a PNG image. Returns list of image paths."""
    images: List[Path] = []
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(str(pdf_path))
        out_dir = Path(tempfile.mkdtemp(prefix="pdf_pages_"))
        for i, page in enumerate(doc):
            pix = page.get_pixmap(dpi=dpi)
            img_path = out_dir / f"page_{i + 1:04d}.png"
            pix.save(str(img_path))
            images.append(img_path)
        doc.close()
        return images
    except ImportError:
        pass

    # Fallback: pdf2image + poppler
    try:
        from pdf2image import convert_from_path
        out_dir = Path(tempfile.mkdtemp(prefix="pdf_pages_"))
        pil_images = convert_from_path(str(pdf_path), dpi=dpi)
        for i, pil_img in enumerate(pil_images):
            img_path = out_dir / f"page_{i + 1:04d}.png"
            pil_img.save(str(img_path), "PNG")
            images.append(img_path)
        return images
    except ImportError:
        pass

    # Fallback: pypdfium2
    try:
        import pypdfium2 as pdfium
        out_dir = Path(tempfile.mkdtemp(prefix="pdf_pages_"))
        pdf = pdfium.PdfDocument(str(pdf_path))
        n_pages = len(pdf)
        for i in range(n_pages):
            page = pdf[i]
            bitmap = page.render(scale=dpi / 72.0)
            pil_image = bitmap.to_pil()
            img_path = out_dir / f"page_{i + 1:04d}.png"
            pil_image.save(str(img_path), "PNG")
            images.append(img_path)
        return images
    except ImportError:
        pass

    raise RuntimeError(
        "No PDF-to-image backend available. "
        "Install PyMuPDF, pdf2image, or pypdfium2."
    )


# ---------------------------------------------------------------------------
# OCR
# ---------------------------------------------------------------------------

def _ocr_image(image_path: Path, lang: str = "eng") -> str:
    """Run Tesseract OCR on a single image and return extracted text."""
    try:
        import pytesseract
        from PIL import Image
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang=lang)
        return text.strip()
    except ImportError:
        print("[ocr_images] WARNING: pytesseract not installed", file=sys.stderr)
        return f"[OCR not available for: {image_path.name}]"
    except Exception as exc:
        return f"[OCR error on {image_path.name}: {exc}]"


# ---------------------------------------------------------------------------
# Multimodal analysis stub
# ---------------------------------------------------------------------------

def _image_to_base64(image_path: Path) -> str:
    """Read image and return base64 data URI."""
    with open(image_path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    ext = image_path.suffix.lower().lstrip(".")
    if ext == "jpg":
        ext = "jpeg"
    return f"data:image/{ext};base64,{data}"


def _describe_image_for_mm(image_path: Path) -> str:
    """
    Produce a base64 payload + prompt suitable for a multimodal model.
    The actual model call is handled by the agent (multimodal_analyze.py).
    This returns a structured JSON string describing the image for downstream processing.
    """
    b64 = _image_to_base64(image_path)
    payload = {
        "image_path": str(image_path),
        "image_base64": b64,
        "prompt": (
            "You are a medical document analyst. Describe every clinically relevant detail in this image. "
            "Include: visible text, numbers, units, dates, measurements, anatomical structures, "
            "abnormalities, modality (if medical imaging), and any handwritten content. "
            "Be thorough and precise. If the image is a medical scan (X-ray, CT, MRI, ultrasound), "
            "describe the findings in structured clinical terms."
        ),
    }
    return json.dumps(payload, indent=2)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def process_image_file(
    file_path: Path,
    *,
    lang: str = "eng",
    use_multimodal: bool = False,
) -> Dict:
    """
    Process a single image file. Returns dict with extracted text and metadata.
    """
    result = {
        "file": str(file_path),
        "format": file_path.suffix.lower(),
        "ocr_text": "",
        "multimodal_payload": None,
    }

    png_path = _ensure_png(file_path)
    result["png_path"] = str(png_path)

    # OCR
    ocr_text = _ocr_image(png_path, lang=lang)
    result["ocr_text"] = ocr_text

    # Multimodal payload (for downstream vision-model analysis)
    if use_multimodal:
        result["multimodal_payload"] = _describe_image_for_mm(png_path)

    return result


def process_pdf_as_images(
    pdf_path: Path,
    *,
    lang: str = "eng",
    dpi: int = 200,
    use_multimodal: bool = False,
) -> Dict:
    """
    Render a PDF to images page-by-page, OCR each page, optionally prepare
    multimodal payloads.
    """
    result = {
        "file": str(pdf_path),
        "format": ".pdf (scanned)",
        "pages": [],
    }

    page_images = _render_pdf_to_images(pdf_path, dpi=dpi)

    for i, img_path in enumerate(page_images):
        page_result = {
            "page": i + 1,
            "image_path": str(img_path),
            "ocr_text": "",
        }

        ocr_text = _ocr_image(img_path, lang=lang)
        page_result["ocr_text"] = ocr_text

        if use_multimodal:
            page_result["multimodal_payload"] = json.loads(
                _describe_image_for_mm(img_path)
            )

        result["pages"].append(page_result)

    return result


def is_scanned_pdf(pdf_path: Path, sample_pages: int = 3) -> bool:
    """
    Heuristic: check first N pages for extractable text.
    If average char count < 50 per page, treat as scanned/image-based PDF.
    """
    try:
        import fitz
        doc = fitz.open(str(pdf_path))
        total_chars = 0
        pages_checked = min(sample_pages, len(doc))
        for i in range(pages_checked):
            total_chars += len(doc[i].get_text().strip())
        doc.close()
        avg = total_chars / max(pages_checked, 1)
        return avg < 50
    except ImportError:
        # Can't check — conservatively treat as scanned
        return True


def main():
    parser = argparse.ArgumentParser(
        description="OCR and image processing for health records"
    )
    parser.add_argument("input_path", help="Path to image or PDF file")
    parser.add_argument("--output-dir", default=".", help="Output directory")
    parser.add_argument("--lang", default="eng", help="Tesseract language code")
    parser.add_argument("--dpi", type=int, default=200, help="DPI for PDF rendering")
    parser.add_argument(
        "--multimodal",
        action="store_true",
        help="Prepare multimodal payloads for vision-model analysis",
    )
    parser.add_argument(
        "--json", action="store_true", help="Output as JSON instead of markdown"
    )
    args = parser.parse_args()

    input_path = Path(args.input_path)

    if not input_path.exists():
        print(f"ERROR: file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    suffix = input_path.suffix.lower()

    if suffix == ".pdf":
        if is_scanned_pdf(input_path):
            result = process_pdf_as_images(
                input_path,
                lang=args.lang,
                dpi=args.dpi,
                use_multimodal=args.multimodal,
            )
        else:
            print(
                f"[ocr_images] {input_path.name} appears to be a text-based PDF, "
                "use ingest_documents.py instead",
                file=sys.stderr,
            )
            sys.exit(0)
    elif suffix in {".png", ".jpg", ".jpeg", ".tiff", ".tif", ".bmp", ".gif"}:
        result = process_image_file(
            input_path,
            lang=args.lang,
            use_multimodal=args.multimodal,
        )
    else:
        print(f"[ocr_images] Unsupported format: {suffix}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        # Print as markdown
        print(f"## OCR Result: {input_path.name}\n")
        if "pages" in result:
            for page in result["pages"]:
                print(f"### Page {page['page']}\n")
                print(page["ocr_text"] or "*(No text extracted)*")
                print()
        else:
            print(result["ocr_text"] or "*(No text extracted)*")

        if args.multimodal:
            print("\n---\n")
            print("> ⚠️ This image contains content that requires multimodal analysis.")
            print("> Pass the multimodal_payload to a vision-capable model for full interpretation.\n")


if __name__ == "__main__":
    main()
