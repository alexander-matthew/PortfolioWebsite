# app/components/welcome_sequence.py
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import requests
from dash import callback
import time


def create_welcome_sequence():
    return html.Div([
        # Hidden div for storing the current sequence state
        dcc.Store(id='sequence-state', data=0),

        # Welcome messages container
        html.Div([
            html.Div(id='welcome-text', className='welcome-text'),
            dcc.Interval(id='sequence-interval', interval=4000, max_intervals=3),  # 4 seconds per message
        ], className='welcome-container'),
    ])


def register_welcome_callbacks(app):
    @app.callback(
        [Output('welcome-text', 'children'),
         Output('welcome-text', 'className'),
         Output('sequence-state', 'data')],
        [Input('sequence-interval', 'n_intervals')],
        [State('sequence-state', 'data')]
    )
    def update_welcome_sequence(n_intervals, current_state):
        if n_intervals is None:
            # Initial state
            return "HELLO", "welcome-text typewriter", 0

        # Get visitor's location
        try:
            ip_info = requests.get('https://ipapi.co/json/').json()
            location = f"{ip_info.get('city', 'Unknown City')}, {ip_info.get('country_name', 'Unknown Country')}"
        except:
            location = "Unknown Location"

        sequences = [
            ("HELLO", "welcome-text typewriter"),
            ("WELCOME TO MY PAGE", "welcome-text typewriter"),
            (f"SIGNAL ORIGIN: {location}", "welcome-text typewriter")
        ]

        current_state = (current_state + 1) % len(sequences)
        return sequences[current_state][0], sequences[current_state][1], current_state
