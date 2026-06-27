import requests

from config import API_BASE_URL


def get_claims():

    response = requests.get(
        f"{API_BASE_URL}/claims"
    )

    response.raise_for_status()

    return response.json()


def get_claim_review(
    claim_id: str
):

    response = requests.get(
        f"{API_BASE_URL}/claims/{claim_id}/review"
    )

    response.raise_for_status()

    return response.json()


def upload_claim(file):

    files = {
        "file": (
            file.name,
            file,
            file.type
        )
    }

    response = requests.post(
        f"{API_BASE_URL}/claims/upload",
        files=files
    )

    response.raise_for_status()

    return response.json()


def submit_decision(
    claim_id,
    decision,
    comments
):

    payload = {
        "decision": decision,
        "comments": comments
    }

    response = requests.post(
        f"{API_BASE_URL}/claims/{claim_id}/decision",
        json=payload
    )

    response.raise_for_status()

    return response.json()

def extract_claim(claim_id):

    response = requests.post(
        f"{BASE_URL}/claims/{claim_id}/extract"
    )

    response.raise_for_status()

    return response.json()


def start_ai_review(claim_id):

    response = requests.post(
        f"{BASE_URL}/claims/{claim_id}/review"
    )

    response.raise_for_status()

    return response.json()