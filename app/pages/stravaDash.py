from dash import Dash, html, dcc, Input, Output
from datetime import datetime
import dash_bootstrap_components as dbc  # We'll use this for the grid system
from flask import redirect, request
from app.tools.stravaAPI import Strava
import pandas as pd
import plotly.express as px


def create_layout():
    return dbc.Container([
        html.H1("Strava Dashboard", className='mb-4'),
        html.Div([
            html.A(
                "Connect with Strava",
                href="/strava-auth",
                className="btn btn-primary mb-4"
            ),
            html.Div(id='profile-container'),
            html.Div(id='distance-plot'),
            html.Div(id='auth-status'),
            dcc.Location(id='url', refresh=False),
            dcc.Store(id='auth-store'),
        ])
    ], fluid=True)


# aggregation of stats
def create_profile_card(athlete, stats):
    return dbc.Container([
        dbc.Card([
            # Header with gradient background
            dbc.CardHeader(
                dbc.Row([
                    dbc.Col(
                        html.Img(
                            src=athlete.get('profile'),
                            className='rounded-circle',
                            style={'width': '100px', 'height': '100px', 'border': '3px solid white'}
                        ),
                        width={"size": 2},
                    ),
                    dbc.Col([
                        html.H2(f"{athlete.get('firstname', '')} {athlete.get('lastname', '')}",
                                className='text-white mb-0'),
                        html.P(f"{athlete.get('city', 'N/A')}, {athlete.get('country', 'N/A')}",
                               className='text-white-50'),
                    ])
                ]),
                style={
                    'background': 'linear-gradient(90deg, #fc4c02 0%, #f7631b 100%)',
                    'padding': '20px'
                }
            ),

            # Stats Grid
            dbc.CardBody([
                html.H4("Recent Activity (Last 4 Weeks)", className='mb-4'),
                dbc.Row([
                    dbc.Col(create_stat_card(
                        "Total Runs",
                        stats.get('recent_run_totals', {}).get('count', 0),
                        "fas fa-running"
                    ), width=3),
                    dbc.Col(create_stat_card(
                        "Distance",
                        f"{stats.get('recent_run_totals', {}).get('distance', 0) * 0.000621371:.1f} km",
                        "fas fa-road"
                    ), width=3),
                    dbc.Col(create_stat_card(
                        "Elevation",
                        f"{stats.get('recent_run_totals', {}).get('elevation_gain', 0):.0f} m",
                        "fas fa-mountain"
                    ), width=3),
                    dbc.Col(create_stat_card(
                        "Time",
                        f"{stats.get('recent_run_totals', {}).get('moving_time', 0) // 3600:.0f} hrs",
                        "fas fa-clock"
                    ), width=3),
                ], className='mb-4'),

                #YTD
                html.H4("Year-To-Date Stats", className='mb-4'),
                dbc.Row([
                    dbc.Col(create_stat_card(
                        "Total Activities",
                        stats.get('ytd_run_totals', {}).get('count', 0),
                        "fas fa-trophy"
                    ), width=3),
                    dbc.Col(create_stat_card(
                        "Total Distance",
                        f"{stats.get('ytd_run_totals', {}).get('distance', 0) / 1000:.0f} km",
                        "fas fa-globe"
                    ), width=3),
                    dbc.Col(create_stat_card(
                        "Total Elevation",
                        f"{stats.get('ytd_run_totals', {}).get('elevation_gain', 0):.0f} m",
                        "fas fa-mountain"
                    ), width=3),
                    dbc.Col(create_stat_card(
                        "Total Time",
                        f"{stats.get('ytd_run_totals', {}).get('moving_time', 0) // 3600:.0f} hrs",
                        "fas fa-hourglass"
                    ), width=3),
                ])
            ])
        ], className='shadow')
    ], fluid=True, className='py-4')


# single stat
def create_stat_card(label, value, icon):
    return dbc.Card([
        dbc.CardBody([
            html.I(className=f"{icon} fa-2x mb-2 text-primary"),
            html.P(label, className='text-muted text-center mb-1'),
            html.H4(str(value), className='text-center mb-0')
        ], className='text-center')
    ], className='bg-light h-100')


def init_app():
    app = Dash(__name__,
               external_stylesheets=[
                   dbc.themes.BOOTSTRAP,
                   'https://use.fontawesome.com/releases/v5.15.4/css/all.css'
               ])
    strava = Strava()

    app.layout = create_layout()

    @app.server.route('/strava-auth')
    def strava_auth():
        auth_url = strava.get_authorization_url()
        return app.server.redirect(auth_url)

    @app.callback(
        Output('profile-container', 'children'),
        Output('distance-plot', 'children'),
        Output('auth-store', 'data'),
        Input('url', 'search')
    )
    def handle_oauth_callback(search):
        if search and 'code=' in search:
            code = search.split('code=')[1].split('&')[0]
            tokens = strava.exchange_token(code)

            if tokens:
                athlete = strava.get_athlete(tokens['access_token'])

                if athlete:
                    # Fetch athlete stats
                    stats = strava.get_athlete_stats(
                        tokens['access_token'],
                        athlete['id']
                    )

                    # Fetch activities and create plot
                    activities = strava.get_all_activities(tokens['access_token'])
                    distance_plot = create_distance_plot(activities, 'Run')

                    return create_profile_card(athlete, stats), distance_plot, tokens

        return None, None

    return app


def create_distance_plot(activities, activity_type=None):
    # create timeseries
    df = pd.DataFrame(activities)
    df = df.loc[df['type'] == activity_type] if activity_type else df

    df['date'] = pd.to_datetime(df['start_date']).dt.date
    df['distance'] = df['distance'] / 1000

    ts = df.groupby('date')['distance'].sum()
    cumulative = ts.cumsum()

    fig = px.line(
        x=cumulative.index,
        y=cumulative.values,
        title=f'Distance Over Time - {activity_type}',
        labels={'x': 'Date', 'y': 'Kilometers'}
    )

    fig.update_traces(line_color='#fc4c02')  # Strava orange
    fig.update_layout(
        template='plotly_white',
        hovermode='x unified'
    )

    return dcc.Graph(figure=fig)


if __name__ == '__main__':
    app = init_app()
    app.run(debug=True, port=8050)
