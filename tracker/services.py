import requests
from django.conf import settings

def get_igdb_token():
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": settings.IGDB_CLIENT_ID,
        "client_secret": settings.IGDB_CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data["access_token"]

def search_igdb_games(query):
    token = get_igdb_token()
    url = "https://api.igdb.com/v4/games"
    headers = {
        "Client-ID": settings.IGDB_CLIENT_ID,
        "Authorization": f"Bearer {token}"
    }
    data = f'search "{query}"; fields name,cover.url,first_release_date,summary; limit 10;'
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()
