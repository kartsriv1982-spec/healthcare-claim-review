"""
Recommendation.py
------------------
Agent 3: Looks at the validation result and gives a final recommendation.
If an OpenAI API key is available, it uses the model to produce a more
natural explanation. Otherwise it falls back to the original rule-based logic.
"""

import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def _fallback_recommendation(is_valid: bool, validation_reasons: list | None = None) -> dict:
    if is_valid:
        return {
            "recommendation": "APPROVE",
            "reasoning": "Claim passed all validation checks.",
        }

    return {
        "recommendation": "REJECT",
        "reasoning": (
            "Claim failed validation checks. "
            f"Reasons: {'; '.join(validation_reasons or [])}"
        ),
    }


def get_recommendation(
    is_valid: bool,
    claim_number: str | None = None,
    claim_amount: str | None = None,
    validation_reasons: list | None = None,
    ocr_text: str | None = None,
) -> dict:
    # Safe default behavior if the API key is unavailable.
    if not os.getenv("OPENAI_API_KEY"):
        return _fallback_recommendation(is_valid, validation_reasons)

    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        prompt = f"""
You are an insurance claims assistant.
Based on the claim data below, decide whether to APPROVE or REJECT the claim.
Return ONLY valid JSON with keys: recommendation and reasoning.

Claim number: {claim_number or 'Unknown'}
Claim amount: {claim_amount or 'Unknown'}
Validation status: {'valid' if is_valid else 'invalid'}
Validation reasons: {validation_reasons or []}
OCR text:
{ocr_text or 'No OCR text available'}
"""

        response = client.chat.completions.create(
            model=model,
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a careful insurance claims assistant. "
                        "Always return JSON with recommendation and reasoning."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        content = response.choices[0].message.content
        if not content:
            raise ValueError("OpenAI returned an empty response.")

        parsed = json.loads(content)
        recommendation = str(parsed.get("recommendation", "")).upper()
        reasoning = str(parsed.get("reasoning", "No reasoning provided.")).strip()

        if recommendation not in {"APPROVE", "REJECT"}:
            raise ValueError(f"Invalid recommendation: {recommendation}")

        return {
            "recommendation": recommendation,
            "reasoning": reasoning,
        }
    except Exception:
        # If the API call fails for any reason, fall back to the deterministic logic.
        return _fallback_recommendation(is_valid, validation_reasons)


# ---- LangGraph node ----
def recommendation_agent_node(state: dict) -> dict:
    print("Running Recommendation Agent...")
    result = get_recommendation(
        state.get("is_valid"),
        state.get("claim_number"),
        state.get("claim_amount"),
        state.get("validation_reasons"),
        state.get("ocr_text"),
    )

    state["recommendation"] = result["recommendation"]
    state["reasoning"] = result["reasoning"]
    return state


if __name__ == "__main__":
    # Quick manual test
    print(get_recommendation(True, "CLM-001", "45000", [], "Sample OCR text"))
    print(get_recommendation(False, "CLM-002", "999999", ["Claim amount is too high."], "Sample OCR text"))
