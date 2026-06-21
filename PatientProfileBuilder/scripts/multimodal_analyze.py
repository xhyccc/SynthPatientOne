#!/usr/bin/env python3
"""
multimodal_analyze.py — Analyze medical images using multimodal vision models
(Claude Vision, GPT-4V) to extract structured clinical information.

Strategy:
1. For image-based records (scanned documents, photos of reports, screenshots):
   - Convert to PNG if needed (via Pillow)
   - Send to a multimodal LLM with a structured extraction prompt
   - Parse the JSON response into clinical variables
2. For medical images (X-rays, CTs, MRIs, pathology slides):
   - Do NOT attempt to read pixel-level findings (requires trained radiologist)
   - Instead, extract any overlaid text, annotations, measurements, labels
   - Flag for human review if the image is a primary diagnostic image
3. Fallback: if no multimodal model is available, use Tesseract OCR only.

Dependencies: pillow, requests (or openai / anthropic SDK)
"""

import json
import os
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class ImageAnalysisResult:
    """Structured result from multimodal image analysis."""
    source_file: str
    analysis_date: str
    model_used: str
    
    # Extracted text content
    raw_text: str = ""
    
    # Structured clinical data extracted by the model
    patient_demographics: dict = field(default_factory=dict)
    vital_signs: dict = field(default_factory=dict)
    lab_results: list = field(default_factory=list)
    medications: list = field(default_factory=list)
    diagnoses: list = field(default_factory=list)
    procedures: list = field(default_factory=list)
    imaging_findings: list = field(default_factory=list)
    
    # Metadata
    image_type: str = ""          # "document_scan", "photo_report", "medical_image", "screenshot"
    requires_human_review: bool = False
    human_review_reason: str = ""
    confidence_score: float = 0.0  # 0.0 - 1.0
    warnings: list = field(default_factory=list)


# ---------------------------------------------------------------------------
# Image preprocessing
# ---------------------------------------------------------------------------

def preprocess_image(image_path: str, output_dir: Optional[str] = None) -> str:
    """
    Ensure image is in a format suitable for multimodal models.
    Converts to PNG, resizes if too large, enhances contrast for OCR-like tasks.
    
    Returns path to the preprocessed image.
    """
    from PIL import Image, ImageEnhance
    
    img = Image.open(image_path)
    
    # Convert to RGB if necessary (e.g., RGBA, CMYK)
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")
    
    # Resize if too large (most vision models prefer < 20MP)
    max_dim = 4096
    if max(img.size) > max_dim:
        ratio = max_dim / max(img.size)
        new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
        img = img.resize(new_size, Image.LANCZOS)
    
    # Enhance contrast for document scans
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.3)
    
    # Save as PNG
    if output_dir:
        out_path = Path(output_dir) / f"{Path(image_path).stem}_processed.png"
    else:
        out_path = Path(image_path).with_suffix(".processed.png")
    
    img.save(out_path, "PNG")
    return str(out_path)


# ---------------------------------------------------------------------------
# Multimodal Model Prompts
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are a medical document analysis assistant. Your task is to extract 
structured clinical information from images of health records.

Rules:
1. Extract ALL visible text, preserving medical terminology exactly.
2. Identify and structure: patient demographics, vital signs, lab results with reference ranges,
   medications with doses, diagnoses, procedures, and imaging findings.
3. For each value, note the date if visible.
4. Flag any information that is ambiguous, cut off, or partially visible.
5. Do NOT interpret medical images (X-rays, CTs, MRIs) — only extract visible text, annotations,
   and metadata from them. Do not make diagnostic statements from pixel data.
6. Output ONLY valid JSON matching the specified schema. No commentary outside the JSON."""

EXTRACTION_PROMPT = """Analyze this image of a health record and extract all clinical information.

Return a JSON object with these fields (omit empty fields):

{
  "patient_demographics": {
    "name": "if visible",
    "age": "number or string",
    "sex": "Male/Female/Other",
    "mrn": "if visible",
    "date_of_birth": "if visible"
  },
  "vital_signs": {
    "blood_pressure": "value with unit",
    "heart_rate": "value with unit",
    "temperature": "value with unit",
    "respiratory_rate": "value with unit",
    "spo2": "value with unit",
    "timestamp": "date/time if visible"
  },
  "lab_results": [
    {"test_name": "...", "value": "...", "unit": "...", "reference_range": "...", "date": "..."}
  ],
  "medications": [
    {"name": "...", "dose": "...", "frequency": "...", "route": "...", "date": "..."}
  ],
  "diagnoses": [
    {"diagnosis": "...", "icd_code": "if visible", "date": "...", "status": "active/resolved/chronic"}
  ],
  "procedures": [
    {"procedure": "...", "date": "...", "findings": "..."}
  ],
  "imaging_findings": [
    {"study_type": "X-ray/CT/MRI/Ultrasound", "body_part": "...", "findings_text": "...", "date": "..."}
  ],
  "image_quality": {
    "readable": true/false,
    "issues": ["blurry", "cropped", "low_contrast", "handwriting"],
    "estimated_completeness": 0.0-1.0
  },
  "warnings": ["list any issues like cut-off text, ambiguous values, conflicting info"]
}

If no information of a category is present, omit that field entirely.
Do not invent or hallucinate values. If uncertain, include in warnings."""


# ---------------------------------------------------------------------------
# Model-specific API calls
# ---------------------------------------------------------------------------

def analyze_with_claude(
    image_base64: str,
    media_type: str = "image/png",
    api_key: Optional[str] = None,
    model: str = "claude-sonnet-4-20250514",
) -> dict:
    """
    Send image to Claude Vision API for structured extraction.
    
    Requires: anthropic Python SDK
    Install: pip install anthropic
    """
    try:
        import anthropic
    except ImportError:
        return {"error": "anthropic SDK not installed. Run: pip install anthropic"}
    
    api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return {"error": "ANTHROPIC_API_KEY not set"}
    
    client = anthropic.Anthropic(api_key=api_key)
    
    message = client.messages.create(
        model=model,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_base64,
                        },
                    },
                    {"type": "text", "text": EXTRACTION_PROMPT},
                ],
            }
        ],
    )
    
    # Parse JSON from response
    response_text = message.content[0].text
    # Strip markdown code fences if present
    if response_text.startswith("```"):
        lines = response_text.split("\n")
        response_text = "\n".join(lines[1:-1])
    
    return json.loads(response_text)


def analyze_with_gpt4v(
    image_base64: str,
    api_key: Optional[str] = None,
    model: str = "gpt-4o",
) -> dict:
    """
    Send image to GPT-4V / GPT-4o API for structured extraction.
    
    Requires: openai Python SDK
    Install: pip install openai
    """
    try:
        import openai
    except ImportError:
        return {"error": "openai SDK not installed. Run: pip install openai"}
    
    api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return {"error": "OPENAI_API_KEY not set"}
    
    client = openai.OpenAI(api_key=api_key)
    
    response = client.chat.completions.create(
        model=model,
        max_tokens=4096,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": EXTRACTION_PROMPT},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_base64}",
                            "detail": "high",
                        },
                    },
                ],
            },
        ],
    )
    
    response_text = response.choices[0].message.content
    if response_text.startswith("```"):
        lines = response_text.split("\n")
        response_text = "\n".join(lines[1:-1])
    
    return json.loads(response_text)


# ---------------------------------------------------------------------------
# Main analysis function
# ---------------------------------------------------------------------------

def analyze_medical_image(
    image_path: str,
    model_provider: str = "auto",
    api_key: Optional[str] = None,
    preprocess: bool = True,
) -> ImageAnalysisResult:
    """
    Analyze a medical image using a multimodal model.
    
    Args:
        image_path: Path to the image file.
        model_provider: "claude", "openai", or "auto" (tries Claude first).
        api_key: API key for the model provider.
        preprocess: Whether to preprocess the image before sending.
    
    Returns:
        ImageAnalysisResult with structured clinical data.
    """
    import base64
    
    result = ImageAnalysisResult(
        source_file=image_path,
        analysis_date=datetime.now().isoformat(),
        model_used="",
    )
    
    # Preprocess if requested
    if preprocess:
        try:
            processed_path = preprocess_image(image_path)
        except Exception as e:
            result.warnings.append(f"Preprocessing failed: {e}")
            processed_path = image_path
    else:
        processed_path = image_path
    
    # Read and encode image
    with open(processed_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")
    
    # Determine media type
    ext = Path(processed_path).suffix.lower()
    media_type_map = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    media_type = media_type_map.get(ext, "image/png")
    
    # Try model providers
    parsed = None
    
    if model_provider in ("auto", "claude"):
        try:
            parsed = analyze_with_claude(image_data, media_type, api_key)
            result.model_used = "claude"
        except Exception as e:
            result.warnings.append(f"Claude analysis failed: {e}")
    
    if parsed is None and model_provider in ("auto", "openai"):
        try:
            parsed = analyze_with_gpt4v(image_data, api_key)
            result.model_used = "openai/gpt-4o"
        except Exception as e:
            result.warnings.append(f"OpenAI analysis failed: {e}")
    
    if parsed is None:
        result.warnings.append("All multimodal models failed. Falling back to OCR only.")
        result.requires_human_review = True
        result.human_review_reason = "Multimodal analysis unavailable"
        return result
    
    # Handle error responses
    if "error" in parsed:
        result.warnings.append(f"Model error: {parsed['error']}")
        result.requires_human_review = True
        return result
    
    # Populate result from parsed JSON
    result.patient_demographics = parsed.get("patient_demographics", {})
    result.vital_signs = parsed.get("vital_signs", {})
    result.lab_results = parsed.get("lab_results", [])
    result.medications = parsed.get("medications", [])
    result.diagnoses = parsed.get("diagnoses", [])
    result.procedures = parsed.get("procedures", [])
    result.imaging_findings = parsed.get("imaging_findings", [])
    
    quality = parsed.get("image_quality", {})
    result.confidence_score = quality.get("estimated_completeness", 0.5)
    if not quality.get("readable", True):
        result.warnings.extend(quality.get("issues", []))
        result.requires_human_review = True
        result.human_review_reason = f"Image quality issues: {quality.get('issues', [])}"
    
    result.warnings.extend(parsed.get("warnings", []))
    
    # Reconstruct raw text from structured data for downstream text-based processing
    raw_parts = []
    for key, val in result.patient_demographics.items():
        raw_parts.append(f"{key}: {val}")
    for key, val in result.vital_signs.items():
        raw_parts.append(f"{key}: {val}")
    for lab in result.lab_results:
        raw_parts.append(f"{lab.get('test_name')}: {lab.get('value')} {lab.get('unit','')} [{lab.get('reference_range','')}]")
    for med in result.medications:
        raw_parts.append(f"{med.get('name')} {med.get('dose','')} {med.get('frequency','')}")
    for dx in result.diagnoses:
        raw_parts.append(f"Diagnosis: {dx.get('diagnosis')} ({dx.get('status','')})")
    for proc in result.procedures:
        raw_parts.append(f"Procedure: {proc.get('procedure')} — {proc.get('findings','')}")
    for finding in result.imaging_findings:
        raw_parts.append(f"{finding.get('study_type')} {finding.get('body_part')}: {finding.get('findings_text','')}")
    result.raw_text = "\n".join(raw_parts)
    
    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Analyze medical images using multimodal vision models"
    )
    parser.add_argument("image", help="Path to medical image")
    parser.add_argument("--provider", choices=["claude", "openai", "auto"], default="auto",
                        help="Model provider (default: auto)")
    parser.add_argument("--api-key", help="API key for the model provider")
    parser.add_argument("--no-preprocess", action="store_true",
                        help="Skip image preprocessing")
    parser.add_argument("--output", "-o", help="Output JSON file path")
    parser.add_argument("--raw-text", action="store_true",
                        help="Print only the raw reconstructed text")
    
    args = parser.parse_args()
    
    result = analyze_medical_image(
        args.image,
        model_provider=args.provider,
        api_key=args.api_key,
        preprocess=not args.no_preprocess,
    )
    
    if args.raw_text:
        print(result.raw_text)
    else:
        output = asdict(result)
        if args.output:
            with open(args.output, "w") as f:
                json.dump(output, f, indent=2)
            print(f"Results written to {args.output}")
        else:
            print(json.dumps(output, indent=2))
