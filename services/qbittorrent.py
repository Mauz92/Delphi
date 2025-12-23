import requests
from config import QBITTORRENT_URL, QBITTORRENT_USER, QBITTORRENT_PASS

def login(session):
    r = session.post(f"{QBITTORRENT_URL}/api/v2/auth/login",
                     data={"username": QBITTORRENT_USER, "password": QBITTORRENT_PASS})
    return r.ok

def get_active_torrents():
    with requests.Session() as s:
        if not login(s):
            return []
        try:
            r = s.get(f"{QBITTORRENT_URL}/api/v2/torrents/info?filter=active")
            r.raise_for_status()
            return r.json()
        except Exception as e:
            print(f"qBittorrent error: {e}")
            return []
