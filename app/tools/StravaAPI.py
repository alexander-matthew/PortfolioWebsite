import os
from dotenv import load_dotenv
import requests
from urllib.parse import urlencode
from typing import Dict, List, Optional


# see strava documentation: https://developers.strava.com/docs/reference/#api-Streams
class Strava:
    def __init__(self):
        load_dotenv()
        self.base_url = "https://www.strava.com/api/v3"
        self.client_id     = os.getenv("STRAVA_CLIENT_ID")
        self.client_secret = os.getenv("STRAVA_CLIENT_SECRET")
        self.refresh_token = os.getenv("STRAVA_REFRESH_TOKEN")
        self.access_token  = os.getenv("STRAVA_ACCESS_TOKEN")
        self.athlete_id    = os.getenv("STRAVA_ATHLETE_ID")
        self.redirect_uri = 'http://127.0.0.1:8050'

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
    def get_athlete(self):
        response = requests.get(f'{self.base_url}/athlete',
                                headers={'Authorization': f'Bearer {self.access_token}'})
        return response.json() if response.ok else None

    # summary stats about user
    def get_athlete_stats(self,athlete_id):
        response = requests.get(
            f'{self.base_url}/athletes/{athlete_id}/stats',
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        return response.json() if response.ok else None

    def get_activities(self, **params):
        """
        Params:
        - before (int, optional): Epoch timestamp
        - after (int, optional): Epoch timestamp
        - page (int, optional): Page number (default: 1)
        - per_page (int, optional): # of items per page (default: 30) -- max 200
        """
        response = requests.get(
            f'{self.base_url}/athlete/activities',
            headers={'Authorization': f'Bearer {self.access_token}'},
            params=params
        )
        return response.json() if response.ok else None

    def get_all_activities(self, before=None, after=None):
        # handle pagination to get all
        results, page = [], 1
        while res := self.get_activities( before=before, after=after, page=page, per_page=100):
            if not res:
                break
            results.extend(res)
            if len(res) < 100:
                break
            page += 1
        return results

    def get_activity_streams(self, activity_id: int, stream_types: List[str]) -> Optional[Dict]:

        response = requests.get(
            f'{self.base_url}/activities/{activity_id}/streams',
            headers={'Authorization': f'Bearer {self.access_token}'},
            params={'keys': ','.join(stream_types), 'key_by_type': True}
        )
        return response.json() if response.status_code == 200 else None

    def get_latest_activity_map(self) -> Optional[Dict]:
        activities = self.get_activities(per_page=1)
        if not activities:
            return None

        activity = activities[0]
        streams = self.get_activity_streams(activity['id'],['latlng', 'altitude', 'time'])

        if not streams:
            return None

        return {
            'activity': activity,
            'streams': streams
        }