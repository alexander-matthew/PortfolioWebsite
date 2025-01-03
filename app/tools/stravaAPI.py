import os
from dotenv import load_dotenv
import requests
from urllib.parse import urlencode


# see strava documentation: https://developers.strava.com/docs/reference/#api-Streams
class Strava:
    def __init__(self):
        load_dotenv()
        self.base_url = "https://www.strava.com/api/v3"
        self.client_id = os.getenv("STRAVA_CLIENT_ID")
        self.client_secret = os.getenv("STRAVA_CLIENT_SECRET")
        self.refresh_token = os.getenv("STRAVA_REFRESH_TOKEN")
        self.access_token = os.getenv("STRAVA_ACCESS_TOKEN")
        self.athlete_id = os.getenv("STRAVA_ATHLETE_ID")
        self.redirect_uri = 'http://127.0.0.1:8050'

    #initiate authentication
    def get_authorization_url(self):
        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': self.redirect_uri,
            'approval_prompt': 'force',
            'scope': 'read,activity:read_all'
        }
        return f"https://www.strava.com/oauth/authorize?{urlencode(params)}"

    # confirm authentication
    def exchange_token(self, code):
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'grant_type': 'authorization_code'
        }

        response = requests.post('https://www.strava.com/oauth/token', data=payload)

        if response.ok:
            data = response.json()
            self.access_token = data['access_token']
            self.athlete_id = data['athlete']['id']
            return data
        return None

    # general user info
    def get_athlete(self, access_token):
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(f'{self.base_url}/athlete', headers=headers)
        return response.json() if response.ok else None

    # summary stats about user
    def get_athlete_stats(self, access_token, athlete_id):
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(
            f'{self.base_url}/athletes/{athlete_id}/stats',
            headers=headers
        )
        return response.json() if response.ok else None

    def get_recent_activities(self, per_page=10):
        if not self.access_token:
            return None

        headers = {'Authorization': f'Bearer {self.access_token}'}
        params = {
            'per_page': per_page,
            'page': 1
        }
        response = requests.get(
            f"{self.base_url}/athlete/activities",
            headers=headers,
            params=params
        )
        return response.json() if response.ok else None
