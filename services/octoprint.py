import requests
from config import OCTOPRINT_URL, OCTOPRINT_API_KEY


def get_current_job():
    url = f"{OCTOPRINT_URL}/api/job"
    headers = {"X-Api-Key": OCTOPRINT_API_KEY}

    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        jobs = r.json()
        return jobs

    except Exception as e:
        print(f"Octoprint error: {e}")
