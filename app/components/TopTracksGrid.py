import pandas as pd
from app.tools.Spotify import SpotifyAPI
from dash import Dash, html, dcc, callback, Output, Input, State
import plotly.express as px

spotify_api = SpotifyAPI()

# App layout
html.Div([
    html.Div(id='auth-container'),
    html.Div([
        dcc.Dropdown(
            id='time-range-selector',
            options=[
                {'label': 'Last 4 Weeks', 'value': 'short_term'},
                {'label': 'Last 6 Months', 'value': 'medium_term'},
                {'label': 'Last 1 Year', 'value': 'long_term'}
            ],
            value='medium_term',
            className='time-range-selector'
        ),
        html.Div(id='top-tracks-container')
    ])
], className='container')


def create_top_artists(df):
    artist_counts = df['artist'].value_counts().head(10)
    return html.Div([
        html.H2('Top Artists'),
        dcc.Graph(
            figure=px.bar(
                x=artist_counts.index,
                y=artist_counts.values,
                title='Most Played Artists'
            )
        )
    ])

def create_track_grid(tracks):
    return html.Div([
        html.Div([
            html.Div(str(idx + 1), className='rank-badge'),
            html.Img(
                src=track['album_image'],
                style={
                    'width': '100%',
                    'height': 'auto',
                    'display': 'block'
                }
            ),
            html.Div([
                html.H3(track['track_name'], className='track-name'),
                html.P(track['artist'], className='artist-name')
            ], className='track-info')
        ], className='track-card')
        for idx, track in enumerate(tracks)
    ], className='track-grid')


@app.callback(
    Output('top-tracks-container', 'children'),
    [Input('time-range-selector', 'value'),
     Input('auth-store', 'data')]
)
def update_tracks(time_range, auth_data):
    if auth_data and auth_data.get('access_token'):
        spotify_api.access_token = auth_data.get('access_token')
        top_tracks = spotify_api.get_top_tracks(time_range=time_range)
        if top_tracks is not None:
            tracks_data = []
            for _, track in top_tracks.iterrows():
                track_info = {
                    'track_name': track['track_name'],
                    'artist': track['artist'],
                    'album_image': track['album_image']
                }
                tracks_data.append(track_info)
            return create_track_grid(tracks_data)
    return None


# Callback to show login button if not authenticated
@app.callback(
    Output('auth-container', 'children'),
    Input('auth-store', 'data')
)
def update_auth_container(auth_data):
    if not auth_data:
        return create_login_button()
    return None


if __name__ == '__main__':
    app.run_server(debug=True)