"""
OCR_Agent.py
------------
Agent 1: Reads the claim document (image file) and pulls text out of it
using AWS Textract.

Kept intentionally simple:
- Only handles single-page image files (.png / .jpg) using Textract's
  detect_document_text API (no forms/tables, no PDF splitting).
- Just pulls out a claim number and an amount using basic text search,
  nothing fancy.
"""

import json
import os
import re
import time
from pathlib import Path

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from openai import OpenAI

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)


DEFAULT_SAMPLE_IMAGE = "sample_claims/SampleInsuranceClaim.jpg"


def _parse_llm_json(text: str) -> dict:
    """Extract JSON from an LLM response, even if it is wrapped in markdown fences."""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                return {}
        return {}


def _extract_lines_from_blocks(blocks: list) -> str:
    lines = [block.get("Text", "") for block in blocks if block.get("BlockType") == "LINE"]
    return "\n".join(lines)


def _clean_value(value) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        cleaned = value.strip().strip("\"'")
        return cleaned or None
    return str(value).strip() or None


def _extract_claim_number(text: str) -> str | None:
    text_norm = re.sub(r"\s+", " ", text)

    patterns = [
        r"(?:^|\n)\s*(?:a\)\s*)?policy\s*no\.?\s*[:\-]?\s*(?:\n|\s)*([A-Za-z0-9][A-Za-z0-9/_-]{3,})",
        r"(?:^|\n)\s*policy\s*no\.?\s*[:\-]?\s*([A-Za-z0-9][A-Za-z0-9/_-]{3,})",
        r"(?:^|\n)\s*policy\s*number\s*[:\-]?\s*([A-Za-z0-9][A-Za-z0-9/_-]{3,})",
        r"(?:^|\n)\s*claim\s*(?:no|number|id|reference)\s*[:\-]?\s*([A-Za-z0-9][A-Za-z0-9/_-]{3,})",
        r"(?:^|\n)\s*case\s*(?:no|number)\s*[:\-]?\s*([A-Za-z0-9][A-Za-z0-9/_-]{3,})",
        r"(?:^|\n)\s*file\s*(?:no|number)\s*[:\-]?\s*([A-Za-z0-9][A-Za-z0-9/_-]{3,})",
    ]

    for pattern in patterns:
        match = re.search(pattern, text_norm, re.IGNORECASE | re.MULTILINE)
        if match:
            return _clean_value(match.group(1))

    # Fallback for same-line label/value pairs that still look like identifiers.
    for line in text.splitlines():
        lowered = line.lower()
        if re.search(r"\b(?:policy|claim|case|file)\s*(?:no|number|id|reference)\b", lowered):
            match = re.search(r"([A-Za-z0-9][A-Za-z0-9/_-]{3,})", line)
            if match:
                candidate = match.group(1)
                if candidate.lower() not in {"enter", "the", "policy", "number", "claim", "case", "file", "id", "reference"}:
                    return _clean_value(candidate)

    return None


def _extract_claim_amount(text: str) -> str | None:
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    # Strongest patterns: explicit labels with nearby numeric values.
    label_patterns = [
        r"\b(?:total|amount|claimed amount|total amount|amount paid|payment amount|sum insured|treatment expenses|hospitalization expenses|pre[- ]hospitalization expenses|post[- ]hospitalization expenses)\b",
        r"\b(?:paid|payments|payment)\b",
    ]

    for i, line in enumerate(lines):
        lowered = line.lower()
        if any(re.search(pattern, lowered) for pattern in label_patterns):
            for j in range(i + 1, min(i + 6, len(lines))):
                # Prefer explicit currency symbols first.
                value_match = re.search(r"(?:[$₹Rs\.]\s*)?([\d,]+(?:\.\d{1,2})?)", lines[j])
                if value_match:
                    candidate = value_match.group(1).replace(",", "")
                    # Avoid matching dates or short IDs.
                    if len(candidate) >= 3 and int(float(candidate)) >= 100:
                        return _clean_value(candidate)

    # Fall back to explicit currency values anywhere in the document when they
    # appear to be the main payment amount.
    for line in lines:
        lowered = line.lower()
        if re.search(r"(?:\$|rs\.|₹)\s*[\d,]+", lowered) or re.search(r"\b(?:total|amount paid|paid to|amount)\b", lowered):
            match = re.search(r"(?:[$₹Rs\.]\s*)?([\d,]{2,}(?:\.\d{1,2})?)", line)
            if match:
                candidate = match.group(1).replace(",", "")
                if int(float(candidate)) >= 1000:
                    return _clean_value(candidate)

    # Final fallback: look for a large standalone number near a total section.
    for i, line in enumerate(lines):
        lowered = line.lower()
        if re.search(r"\b(?:total|amount|payment|paid|claim|hospitalization|pre|post)\b", lowered):
            for j in range(i + 1, min(i + 7, len(lines))):
                value_match = re.search(r"([\d,]{3,}(?:\.\d{1,2})?)", lines[j])
                if value_match:
                    candidate = value_match.group(1).replace(",", "")
                    if int(float(candidate)) >= 1000:
                        return _clean_value(candidate)

    return None


def run_ocr(document_path: str) -> dict:
    """Takes an image or multi-page PDF and returns OCR text plus fields."""

    if not os.path.isfile(document_path):
        raise FileNotFoundError(
            f"Claim file not found: {document_path}. "
            "Please provide a valid path to an image or PDF file."
        )

    textract = boto3.client(
        "textract",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    path = Path(document_path)
    suffix = path.suffix.lower()

    try:
        if suffix in {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif"}:
            with open(document_path, "rb") as f:
                image_bytes = f.read()
            response = textract.detect_document_text(Document={"Bytes": image_bytes})
            blocks = response.get("Blocks", [])
            full_text = _extract_lines_from_blocks(blocks)
        elif suffix == ".pdf":
            bucket = os.getenv("AWS_S3_BUCKET")
            if not bucket:
                raise RuntimeError(
                    "PDF OCR requires AWS_S3_BUCKET to be set so Textract can process the file."
                )

            s3 = boto3.client(
                "s3",
                region_name=os.getenv("AWS_REGION", "us-east-1"),
            )
            s3_key = f"claims/{path.name}"
            s3.upload_file(document_path, bucket, s3_key)

            job = textract.start_document_text_detection(
                DocumentLocation={
                    "S3Object": {
                        "Bucket": bucket,
                        "Name": s3_key,
                    }
                }
            )
            job_id = job["JobId"]

            while True:
                job_response = textract.get_document_text_detection(JobId=job_id)
                status = job_response.get("JobStatus")
                if status in {"SUCCEEDED", "PARTIAL_SUCCESS", "FAILED"}:
                    break
                time.sleep(2)

            if status != "SUCCEEDED" and status != "PARTIAL_SUCCESS":
                raise RuntimeError(
                    f"Textract PDF job failed with status: {status}"
                )

            blocks = []
            next_token = None
            while True:
                params = {"JobId": job_id}
                if next_token:
                    params["NextToken"] = next_token
                page_response = textract.get_document_text_detection(**params)
                blocks.extend(page_response.get("Blocks", []))
                next_token = page_response.get("NextToken")
                if not next_token:
                    break

            full_text = _extract_lines_from_blocks(blocks)
        else:
            raise ValueError(
                f"Unsupported file type: {suffix}. Supported types are .png, .jpg, .jpeg, .bmp, .tiff, .pdf"
            )
    except (ClientError, RuntimeError, ValueError) as e:
        error_message = str(e)
        if hasattr(e, "response"):
            error = e.response.get("Error", {})
            code = error.get("Code", "Unknown")
            message = error.get("Message", str(e))
            error_message = f"Textract request failed ({code}): {message}"
        return {
            "ocr_text": "",
            "claim_number": None,
            "claim_amount": None,
            "ocr_error": error_message,
        }

    # Try to extract fields using the LLM first, then fall back to regex.
    claim_number = None
    claim_amount = None

    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        try:
            print("Calling OpenAI LLM for OCR extraction...")
            client = OpenAI(api_key=api_key)
            model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            response = client.chat.completions.create(
                model=model,
                temperature=0,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You extract insurance claim fields from OCR text. "
                            "Return valid JSON only with keys 'claim_number' and 'claim_amount'."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            "Extract the policy number and claim amount from this text. "
                            "If a value is not found, use null.\n\n"
                            f"OCR TEXT:\n{full_text}"
                        ),
                    },
                ],
            )
            content = response.choices[0].message.content or "{}"
            print("LLM response content:", content)
            parsed = _parse_llm_json(content)
            claim_number = parsed.get("claim_number")
            claim_amount = parsed.get("claim_amount")
            print(f"LLM extracted claim_number={claim_number}, claim_amount={claim_amount}")
        except Exception as e:
            print(f"LLM extraction failed: {type(e).__name__}: {e}")
            claim_number = None
            claim_amount = None
    else:
        print("OPENAI_API_KEY is not set, skipping LLM extraction.")

    if claim_number is None:
        claim_number = _extract_claim_number(full_text)

    if claim_amount is None or (isinstance(claim_amount, str) and not claim_amount.strip()):
        claim_amount = _extract_claim_amount(full_text)

    if isinstance(claim_amount, str):
        claim_amount = claim_amount.replace(",", "").strip()

    if claim_amount == "":
        claim_amount = None

    return {
        "ocr_text": full_text,
        "claim_number": claim_number,
        "claim_amount": claim_amount,
        "ocr_error": None,
    }


# ---- LangGraph node ----
def ocr_agent_node(state: dict) -> dict:
    print("Running OCR Agent...")
    result = run_ocr(state["document_path"])

    state["ocr_text"] = result.get("ocr_text", "")
    state["claim_number"] = result.get("claim_number")
    state["claim_amount"] = result.get("claim_amount")
    state["ocr_error"] = result.get("ocr_error")
    return state


if __name__ == "__main__":
    # Quick manual test: python Agents/OCR_Agent.py sample_claims/SampleInsuranceClaim.jpg
    import sys

    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SAMPLE_IMAGE

    try:
        result = run_ocr(path)
        print(result)
    except Exception as e:
        print(f"Error: {e}")
