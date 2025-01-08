from dash import html, dcc, callback, Input, Output, State
from dash_iconify import DashIconify
from app.tools.Spotify import SpotifyAPI

spotify_api = SpotifyAPI()


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
                html.P(track['artist'], className='track-artist')
            ], className='track-info')
        ], className='track-card')
        for idx, track in enumerate(tracks)
    ], className='track-grid')


def create_login_button():
    return html.Div([
        html.Div([
            html.H2('Connect with Spotify', className='card-title'),
            html.A(
                html.Button([
                    DashIconify(icon="mdi:spotify", className="mr-2"),
                    "Connect Spotify"
                ], className='connect-button'),
                href='/spotify-auth'
            )
        ], className='modern-card')
    ])


def register_spotify_callbacks(app):
    # Spotify auth endpoint
    @app.server.route('/spotify-auth')
    def spotify_auth():
        auth_url = spotify_api.get_auth_url()
        return app.server.redirect(auth_url)

    # Handle OAuth callback
    @callback(
        [Output('spotify-auth-store', 'data'),
         Output('spotify-url', 'search')],
        [Input('spotify-url', 'search')],
        [State('spotify-auth-store', 'data')]
    )
    def handle_oauth_callback(search, current_auth):
        if search and 'code=' in search:
            code = search.split('code=')[1].split('&')[0]
            token_info = spotify_api.get_token(code)
            return token_info, ''
        return current_auth or None, search or ''

    # Update tracks based on time range
    @callback(
        Output('spotify-tracks-container', 'children'),
        [Input('spotify-time-range', 'value'),
         Input('spotify-auth-store', 'data')]
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

    # Update auth container
    @callback(
        Output('spotify-auth-container', 'children'),
        Input('spotify-auth-store', 'data')
    )
    def update_auth_container(auth_data):
        if not auth_data:
            return create_login_button()
        return None


def create_spotify_page():
    return html.Div([
        # Main container
        html.Div([
            # Header
            html.Div([
                html.Div([
                    DashIconify(icon="mdi:spotify", className="section-icon"),
                    html.H2('My Music Taste', className='section-title')
                ], className='section-header'),

                # Time Range Selector
                dcc.Dropdown(
                    id='spotify-time-range',  # Updated ID
                    options=[
                        {'label': 'Last 4 Weeks', 'value': 'short_term'},
                        {'label': 'Last 6 Months', 'value': 'medium_term'},
                        {'label': 'Last 1 Year', 'value': 'long_term'}
                    ],
                    value='medium_term',
                    className='time-range-selector'
                )
            ], className='modern-card'),

            # Login container
            html.Div(id='spotify-auth-container', className='modern-card'),  # Updated ID

            # Tracks container
            html.Div(id='spotify-tracks-container'),  # Updated ID

            # Hidden elements for auth
            dcc.Store(id='spotify-auth-store'),  # Updated ID
            dcc.Location(id='spotify-url', refresh=False)  # Updated ID
        ], className='content-container')
    ], className='modern-page')