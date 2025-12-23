import requests
from config import JELLYFIN_URL, JELLYFIN_API_KEY, JELLYFIN_USER

def get_recent_jellyfin_items(limit=10):
    """
    Fetches recently added movies or episodes from Jellyfin.
    """
    url = f"{JELLYFIN_URL}/Users/{JELLYFIN_USER}/Items/Latest?Limit={limit}&IncludeItemTypes=Movie,Episode"
    headers = {"X-MediaBrowser-Token": JELLYFIN_API_KEY}
    try:
        r = requests.get(url, headers=headers, timeout=5)
        r.raise_for_status()
        items = r.json()
        # For each item, set a 'title' and 'image' for template
        for item in items:
            # Jellyfin thumbnail URL
            item["imageUrl"] = f"{JELLYFIN_URL}/Items/{item['Id']}/Images/Primary?api_key={JELLYFIN_API_KEY}"
        return items
    except Exception as e:
        print(f"Jellyfin error: {e}")
        return []

def get_jellyfin_item(item_id):
    """Fetch detailed information for one Jellyfin item."""
    url = f"{JELLYFIN_URL}/Users/{JELLYFIN_USER}/Items/{item_id}"
    headers = {"X-MediaBrowser-Token": JELLYFIN_API_KEY}
    try:
        r = requests.get(url, headers=headers, timeout=5)
        r.raise_for_status()
        item = r.json()

        # Build image URLs
        item["imageUrl"] = f"{JELLYFIN_URL}/Items/{item['Id']}/Images/Primary?api_key={JELLYFIN_API_KEY}"
        item["backdropUrl"] = None
        if "BackdropImageTags" in item and len(item["BackdropImageTags"]) > 0:
            tag = item["BackdropImageTags"][0]
            item["backdropUrl"] = f"{JELLYFIN_URL}/UserItems/{item['Id']}/Images/Backdrop/{tag}?api_key={JELLYFIN_API_KEY}"
        return item
    except Exception as e:
        print(f"Jellyfin item error: {e}")
        return None
