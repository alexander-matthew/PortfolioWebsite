from dash import html, dcc, callback, Input, Output, State, callback_context
from dash_iconify import DashIconify
from app.tools.StravaAPI import Strava
import pandas as pd
import plotly.express as px
from typing import Dict

strava_api = Strava()


def create_stat_card(label, value, icon):
    return html.Div([
        DashIconify(
            icon=icon,
            width=24,
            className="stat-icon"
        ),
        html.Div([
            html.P(label, className='stat-label'),
            html.H4(str(value), className='stat-value')
        ], className='stat-info')
    ], className='stat-card')


def create_login_button():
    return html.Div([
        html.Div([
            html.H2('Connect with Strava',
                    className='section-title mb-4'),
            html.P(
                "Connect your Strava account to view your running statistics and activities.",
                className="text-secondary mb-4"
            ),
            html.A(
                html.Button([
                    DashIconify(
                        icon="mdi:run",
                        width=24,
                        className="mr-2 inline-block"
                    ),
                    "Connect with Strava"
                ],
                    className='modern-button'),
                href='/strava-auth',
                className='no-underline'
            )
        ],
            className='modern-card text-center py-8')
    ])


def create_profile_card(athlete, stats):
    return html.Div([
        html.Div([
            # Profile Header
            html.Div([
                html.Img(
                    src=athlete.get('profile'),
                    className='profile-image'
                ),
                html.Div([
                    html.H3(f"{athlete.get('firstname', '')} {athlete.get('lastname', '')}",
                            className='athlete-name'),
                    html.P(f"{athlete.get('city', 'N/A')}, {athlete.get('country', 'N/A')}",
                           className='athlete-location')
                ], className='profile-info')
            ], className='profile-header'),

            # Stats Grid
            html.Div([
                create_stat_card(
                    "Total Runs",
                    stats.get('recent_run_totals', {}).get('count', 0),
                    "mdi:run"
                ),
                create_stat_card(
                    "Distance",
                    f"{stats.get('recent_run_totals', {}).get('distance', 0) * 0.000621371:.1f} km",
                    "mdi:map-marker-distance"
                ),
                create_stat_card(
                    "Elevation",
                    f"{stats.get('recent_run_totals', {}).get('elevation_gain', 0):.0f} m",
                    "mdi:mountain"
                ),
                create_stat_card(
                    "Time",
                    f"{stats.get('recent_run_totals', {}).get('moving_time', 0) // 3600:.0f} hrs",
                    "mdi:clock-outline"
                )
            ], className='stats-grid')
        ], className='profile-card')
    ])


def create_distance_plot(activities, activity_type=None):
    if not activities:
        return html.Div("No activities found", className='no-data')

    df = pd.DataFrame(activities)
    df = df.loc[df['type'] == activity_type] if activity_type else df

    df['date'] = pd.to_datetime(df['start_date']).dt.date
    df['distance'] = df['distance'] / 1000  # Convert to kilometers

    ts = df.groupby('date')['distance'].sum()
    cumulative = ts.cumsum()

    fig = px.line(
        x=cumulative.index,
        y=cumulative.values,
        title='Distance Progress',
        labels={'x': 'Date', 'y': 'Kilometers'}
    )

    fig.update_traces(line_color='#fc4c02')  # Strava orange
    fig.update_layout(
        template='plotly_white',
        hovermode='x unified',
        margin=dict(l=40, r=40, t=40, b=40),
        title_x=0.5,
        title_font_size=16,
        paper_bgcolor='#1e293b',
        plot_bgcolor='#1e293b',
        font=dict(color='#ffffff')
    )

    return dcc.Graph(figure=fig, className='modern-graph')


def create_activity_map(activity_data: Dict):
    if not activity_data:
        return html.Div("No recent activity data available", className='no-data')

    activity = activity_data['activity']
    streams = activity_data['streams']

    if 'latlng' not in streams:
        return html.Div("No GPS data available for this activity", className='no-data')

    latlng = streams['latlng']['data']
    lat, lon = zip(*latlng)

    df = pd.DataFrame({
        'lat': lat,
        'lon': lon
    })

    fig = px.line_mapbox(
        df,
        lat='lat',
        lon='lon',
        center={'lat': sum(lat) / len(lat), 'lon': sum(lon) / len(lon)},
        zoom=11,
        height=400
    )

    fig.update_traces(line=dict(color="#fc4c02", width=4))
    fig.update_layout(
        mapbox_style="dark",
        margin=dict(l=0, r=0, t=40, b=0),
        showlegend=False,
        title=dict(
            text=f"Latest Activity: {activity['name']}",
            x=0.5,
            font=dict(color='#ffffff'),
            font_size=16
        ),
        paper_bgcolor='#1e293b'
    )

    return dcc.Graph(figure=fig, className='modern-graph')


def create_strava_page():
    return html.Div([
        html.Div([
            # Header
            html.Div([
                html.Div([
                    DashIconify(
                        icon="mdi:run",
                        width=32,
                        className="section-icon"
                    ),
                    html.H2('Your Running Journey: Activity Analysis', className='section-title')
                ], className='header-left'),

                # Time Range Selector
                html.Div([
                    dcc.Dropdown(
                        id='strava-time-range',
                        options=[
                            {'label': 'Last 4 Weeks', 'value': 'recent'},
                            {'label': 'Year to Date', 'value': 'ytd'},
                            {'label': 'All Time', 'value': 'all'}
                        ],
                        value='recent',
                        className='time-range-selector'
                    )
                ], className='dropdown-container')
            ], className='modern-card mb-6'),

            html.Div(id='strava-auth-container', className='mb-6'),
            html.Div(id='strava-profile-container', className='mb-6'),
            html.Div(id='strava-viz-container', className='modern-card'),

            # Hidden elements for auth
            dcc.Store(id='strava-auth-store'),
            dcc.Location(id='strava-url', refresh=False)
        ], className='content-container')
    ], className='modern-page')


def register_strava_callbacks(app):
    # Strava auth endpoint
    @app.server.route('/strava-auth')
    def strava_auth():
        auth_url = strava_api.get_authorization_url()
        return app.server.redirect(auth_url)

    # Handle OAuth callback
    @callback(
        [Output('strava-auth-store', 'data'),
         Output('strava-url', 'search')],
        [Input('strava-url', 'search')],
        [State('strava-auth-store', 'data')]
    )
    def handle_oauth_callback(search, current_auth):
        if search and 'code=' in search:
            code = search.split('code=')[1].split('&')[0]
            token_info = strava_api.exchange_token(code)
            return token_info, ''
        return current_auth or None, search or ''

    # Update dashboard based on auth state and time range
    @callback(
        [Output('strava-auth-container', 'children'),
         Output('strava-profile-container', 'children'),
         Output('strava-viz-container', 'children')],
        [Input('strava-auth-store', 'data'),
         Input('strava-time-range', 'value')]
    )
    def update_dashboard(auth_data, time_range):
        if not auth_data:
            return create_login_button(), None, None

        strava_api.access_token = auth_data.get('access_token')
        athlete = strava_api.get_athlete()

        if athlete:
            stats = strava_api.get_athlete_stats(athlete['id'])
            activities = strava_api.get_all_activities()
            map_data = strava_api.get_latest_activity_map()

            visualizations = html.Div([
                create_distance_plot(activities, 'Run'),
                create_activity_map(map_data)
            ])

            return None, create_profile_card(athlete, stats), visualizations

        return create_login_button(), None, None