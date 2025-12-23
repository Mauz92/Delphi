
## Docker compose

version: "3.9"
services:
  dashboard:
    image: ghcr.io/<username>/delphi:latest
    ports:
      - "5000:5000"
    environment:
      SONARR_URL: "http://192.168.x.x:8989"
      SONARR_API_KEY: "..."
      RADARR_URL: "http://192.168.x.x:7878"
      RADARR_API_KEY: "..."
      JELLYFIN_URL: "http://192.168.x.x:8096"
      JELLYFIN_API_KEY: "..."
      JELLYFIN_USER: "..."
    restart: unless-stopped
