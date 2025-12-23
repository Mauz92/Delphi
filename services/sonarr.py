import requests
from config import SONARR_URL, SONARR_API_KEY

def get_recent_series(limit=10):
    url = f"{SONARR_URL}/api/v3/series"
    headers = {"X-Api-Key": SONARR_API_KEY}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        movies = sorted(response.json(), key=lambda m: m.get("added"), reverse=True)
        return movies[:limit]
    except Exception as e:
        print(f"Radarr error: {e}")
        return []

def get_diskspace():
    url = f"{SONARR_URL}/api/v3/diskspace"
    headers = {"X-Api-Key": SONARR_API_KEY}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        def bytes_to_gb(b):
            return round(b/(1024**3), 2)
        disks = [] 
        for disk in response.json():
            free_gb = bytes_to_gb(disk["freeSpace"])
            total_gb = bytes_to_gb(disk["totalSpace"])
            disks.append({'path':disk["path"], 'freeSpace':free_gb, 'totalSpace':total_gb})
        return disks
    except Exception as e:
        print(f"Radarr error: {e}")
        return []
