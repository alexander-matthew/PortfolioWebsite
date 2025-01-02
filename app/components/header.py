
# app/components/header.py
from dash import html
import dash_bootstrap_components as dbc


def create_header():
    return dbc.Row([
        dbc.Col([
            html.H1('PERSONAL DATABASE', className='mb-4 typewriter'),
            html.Div([
                html.Span('SYSTEM STATUS: ', className='text-muted'),
                html.Span('ONLINE', className='status-text blink')
            ]),
        ])
    ], className='mb-4')