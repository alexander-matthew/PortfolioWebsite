import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlencode
import pandas as pd
import base64


class SpotifyAPI:

    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
        self.access_token = None

    def get_auth_url(self):
        scope = "user-read-recently-played user-top-read"
        auth_params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': self.redirect_uri,
            'scope': scope
        }

        return f"https://accounts.spotify.com/authorize?{urlencode(auth_params)}"

    def get_token(self, code):
        """Exchange authorization code for access token"""
        token_url = 'https://accounts.spotify.com/api/token'

        auth_header = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()

        headers = {
            'Authorization': f'Basic {auth_header}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri
        }

        try:
            response = requests.post(token_url, headers=headers, data=data)
            print(f"Token exchange response status: {response.status_code}")
            print(f"Token exchange response: {response.text}")

            if response.status_code != 200:
                print(f"Error in token exchange. Status: {response.status_code}")
                print(f"Response: {response.text}")
                return None

            token_info = response.json()
            self.access_token = token_info.get('access_token')
            return token_info
        except Exception as e:
            print(f"Exception during token exchange: {str(e)}")
            return None

    def get_user_profile(self):
        if not self.access_token:
            return None

        endpoint = "https://api.spotify.com/v1/me"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        response = requests.get(endpoint, headers=headers)

        return response.json() if response.ok else None

    def get_top_tracks(self, time_range='medium_term',limit=10):
        if not self.access_token:
            return None

        endpoint = "https://api.spotify.com/v1/me/top/tracks"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        params = {
            "limit": limit,
            "time_range": time_range  # short_term (4 weeks), medium_term (6 months), long_term (years)
        }

        response = requests.get(endpoint, headers=headers, params=params)

        if response.status_code != 200:
            return None

        data = response.json()
        tracks = []
        for item in data['items']:
            track_info = {
                'track_name': item['name'],
                'artist': item['artists'][0]['name'],
                'album': item['album']['name'],
                'album_image': item['album']['images'][0]['url'] if item['album']['images'] else None,
                'popularity': item['popularity'],
                'duration_ms': item['duration_ms']
            }
            tracks.append(track_info)

        return pd.DataFrame(tracks)
