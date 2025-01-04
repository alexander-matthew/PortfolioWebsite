import pandas as pd
from app.tools.Spotify import SpotifyAPI
from dash import Dash, html, dcc, callback, Output, Input, State
import plotly.express as px

app = Dash(__name__)

spotify_api = SpotifyAPI()

# Simple CSS for a clean look
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                background-color: #0f172a;
                color: white;
                font-family: system-ui, -apple-system, sans-serif;
                margin: 0;
                padding: 20px;
            }
            .container {
                max-width: 1400px;
                margin: 0 auto;
                padding: 0 20px;
            }
            .track-grid {
                display: grid;
                grid-template-columns: repeat(5, 1fr);
                gap: 20px;
                padding: 20px 0;
            }
            .track-card {
                background: #1e293b;
                border-radius: 8px;
                overflow: hidden;
                transition: transform 0.2s;
                position: relative;
            }
            .track-card:hover {
                transform: translateY(-5px);
            }
            .track-info {
                padding: 15px;
            }
            .track-name {
                margin: 0;
                font-size: 16px;
                font-weight: 600;
            }
            .artist-name {
                margin: 5px 0 0 0;
                font-size: 14px;
                color: #94a3b8;
            }
            .rank-badge {
                position: absolute;
                top: 10px;
                left: 10px;
                background: rgba(0, 0, 0, 0.75);
                color: white;
                border-radius: 50%;
                width: 30px;
                height: 30px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                font-size: 14px;
            }
            .time-range-selector {
                background: #1e293b;
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 20px;
                width: 200px;
            }
            .Select-control {
                background-color: #334155 !important;
                border-color: #475569 !important;
            }
            .Select-value-label {
                color: white !important;
            }
            .Select-menu-outer {
                background-color: #334155 !important;
                border-color: #475569 !important;
                width: 200px;
            }
            .Select-option {
                background-color: #334155 !important;
                color: white !important;
            }
            .Select-option:hover {
                background-color: #475569 !important;
            }
            .Select-placeholder {
                color: #94a3b8 !important;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# App layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
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
    ], className='container'),
    dcc.Store(id='auth-store')
])


def create_login_button():
    return html.Div([
        html.Div([
            html.H2('Begin Your Journey', className='card-title'),
            html.A(
                html.Button('Connect with Spotify', className='login-button'),
                href='/spotify-auth'
            )
        ], className='card')
    ])


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


@app.server.route('/spotify-auth')
def spotify_auth():
    auth_url = spotify_api.get_auth_url()
    return app.server.redirect(auth_url)


@app.callback(
    [Output('auth-store', 'data'),
     Output('url', 'search')],
    [Input('url', 'search')],
    [State('auth-store', 'data')]
)
def handle_oauth_callback(search, current_auth):
    if search and 'code=' in search:
        code = search.split('code=')[1].split('&')[0]
        token_info = spotify_api.get_token(code)
        return token_info, ''
    return current_auth or None, search or ''



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