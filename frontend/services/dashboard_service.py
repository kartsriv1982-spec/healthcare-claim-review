import requests

from config import API_BASE_URL

def get_dashboard_metrics():

    response = requests.get(
        f"{API_BASE_URL}/dashboard/metrics"
    )

    response.raise_for_status()

    return response.json()