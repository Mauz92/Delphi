import requests
from config import RADARR_URL, RADARR_API_KEY

def get_recent_movies(limit=10):
    url = f"{RADARR_URL}/api/v3/movie"
    headers = {"X-Api-Key": RADARR_API_KEY}
    try:
        r = requests.get(url, headers=headers, timeout=5)
        r.raise_for_status()
        movies = sorted(r.json(), key=lambda m: m.get("added"), reverse=True)
        return movies[:limit]
    except Exception as e:
        print(f"Radarr error: {e}")
        return []

def get_diskspace():
    url = f"{RADARR_URL}/api/v3/diskspace"
    headers = {"X-Api-Key": RADARR_API_KEY}
    try:
        r = requests.get(url, headers=headers, timeout=5)
        r.raise_for_status()
        def bytes_to_gb(b):
            return round(b/(1024**3), 2)
        disks = [] 
        for disk in r.json():
            free_gb = bytes_to_gb(disk["freeSpace"])
            total_gb = bytes_to_gb(disk["totalSpace"])
            disks.append({'path':disk["path"], 'freeSpace':free_gb, 'totalSpace':total_gb})
        return disks
    except Exception as e:
        print(f"Radarr error: {e}")
        return []

def get_calendar():
    url = f"{RADARR_URL}/api/v3/calendar"
    headers = {"X-Api-Key": RADARR_API_KEY}
    try:
        r = requests.get(url, headers=headers, timeout=5)
        r.raise_for_status()
        calendar_feed = r.json()
        return calendar_feed
    except Exception as e:
        print(f"Radarr error: {e}")
        return []
