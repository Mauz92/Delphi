from flask import Flask, render_template, jsonify, request
import requests
from services.radarr import get_recent_movies, get_diskspace
from services.sonarr import get_recent_series
from services.qbittorrent import get_active_torrents
from services.jellyfin import get_recent_jellyfin_items, get_jellyfin_item
from services.octoprint import get_current_job
from config import JELLYFIN_URL, OCTOPRINT_URL, RADARR_URL, SONARR_URL, QBITTORRENT_URL
from config import RADARR_API_KEY, SONARR_API_KEY
from datetime import datetime, timedelta, timezone
from pathlib import Path
import json

CONFIG_PATH = Path("config.json")
app = Flask(__name__)

@app.route("/")
def index():
    ### Radarr
    movies = get_recent_movies()
    diskspace = get_diskspace()

    ### Sonarr
    series = get_recent_series()
    ### QBittorrent
    torrents = get_active_torrents()

    ### Jellyfin
    jellyfin_items = get_recent_jellyfin_items()

    ### Octoprint
    octoprint_job = get_current_job()

    print(calendar_data())
    URLS = {
        "JELLYFIN_URL":JELLYFIN_URL, 
        "OCTOPRINT_URL":OCTOPRINT_URL, 
        "RADARR_URL":RADARR_URL,
        "SONARR_URL": SONARR_URL,
        "QBITTORRENT_URL":QBITTORRENT_URL,
    }
    return render_template("index.html",
                           **URLS,
                           movies=movies, 
                           series=series,
                           diskspace=diskspace, 
                           torrents=torrents, 
                           jellyfin_items=jellyfin_items, 
                           octoprint_job=octoprint_job)

@app.route("/api/torrents")
def api_torrents():
    torrents = get_active_torrents()
    return jsonify(torrents)

@app.route("/jellyfin/item/<item_id>")
def jellyfin_item(item_id):
    item = get_jellyfin_item(item_id)
    if not item:
        return "Item not found", 404
    return render_template("jellyfin_item.html", item=item, JELLYFIN_URL=JELLYFIN_URL)

@app.route("/api/calendar")
def calendar_data():
    now_utc = datetime.now(timezone.utc)
    start = now_utc.isoformat(timespec='seconds').replace('+00:00', 'Z')
    end = (now_utc + timedelta(days=180)).isoformat(timespec='seconds').replace('+00:00', 'Z')  # 180 days ahead
    events = []

    # Sonarr 
    try:
        sonarr_url = f"{SONARR_URL}/api/v3/calendar?start={start}&end={end}&apikey={SONARR_API_KEY}"
        r = requests.get(sonarr_url, timeout=5)
        sonarr_data = r.json()
        for ep in sonarr_data:
            title = f"{ep['title']} S{ep['seasonNumber']:02d}E{ep['episodeNumber']:02d}"
            events.append({
                "title": title,
                "start": ep["airDate"],
                "color": "#17a2b8",
                "source": "Sonarr"
            })
    except Exception as e:
        print(f"Sonarr calendar error: {e}")
    # Radarr
    try:
        radarr_url = f"{RADARR_URL}/api/v3/calendar?start={start}&end={end}"
        headers = {"X-Api-Key": RADARR_API_KEY}
        r = requests.get(radarr_url, headers=headers, timeout=5)
        radarr_data = r.json() 
        for movie in radarr_data:
            date = movie.get("inCinemas") or movie.get("digitalRelease") or movie.get("physicalRelease")
            if date:
                events.append({
                    "title": movie["title"],
                    "start": date,
                    "color": "#dc3545",
                    "source": "Radarr"
                })
    except Exception as e:
        print(f"Radarr calendar error: {e}")
    return jsonify(events)

def load_config():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    else: 
        with open(CONFIG_PATH, 'w') as f:
            json.dump({}, f, indent=2)
    return {}

def save_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

@app.route("/settings", methods=["GET", "POST"])
def settings():
    config = load_config()
    if request.method == "POST":
        app_name = request.form.get("app_name")
        print(app_name)
        url = request.form.get("url")
        api_key = request.form.get("api_key")
        username = request.form.get("username")
        password = request.form.get("password")

        # Dynamically update config
        config[app_name] = {}
        if url: config[app_name]["url"] = url
        if api_key: config[app_name]["api_key"] = api_key
        if username: config[app_name]["username"] = username
        if password: config[app_name]["password"] = password

        save_config(config)
        # return "Config updated successfully!"

    return render_template("settings.html", config=config)

@app.route("/settings/delete/<app_name>", methods=["POST"])
def delete_setting(app_name):
    config = load_config()
    if app_name in config:
        del config[app_name]
        save_config(config)
        return jsonify({"success": True})
    return jsonify({"success": False, "error": "Not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
