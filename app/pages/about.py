from datetime import datetime

from dash import html
import dash_bootstrap_components as dbc
from app.components.header import create_header
from app.components.footer import create_footer
from app.components.decorations import create_corner_decorations
from app.components.welcome_sequence import create_welcome_sequence, register_welcome_callbacks
from app.components.clock import create_clock

def create_header():
    return dbc.Row([
        dbc.Col([
            create_welcome_sequence(),
            html.Div([
                html.Span('SYSTEM STATUS: ', className='text-muted'),
                html.Span('ONLINE', className='status-text blink')
            ]),
            create_clock(),
        ])
    ], className='mb-4')


def create_profile_panel():
    return dbc.Col([
        html.Div([
            html.H2('CREW PROFILE', className='heading'),
            html.Div([
                html.Span('NAME: ', className='text-muted'),
                html.Span('[Your Name]', className='status-text')
            ], className='mb-2'),
            html.Div([
                html.Span('ROLE: ', className='text-muted'),
                html.Span('[Your Role]', className='status-text')
            ], className='mb-2'),
            html.Div([
                html.Span('STATUS: ', className='text-muted'),
                html.Span('ACTIVE', className='status-text')
            ]),
        ], className='panel')
    ], width=6)

def create_skills_panel():
    skills = ['Python', 'Dash', 'Data Analysis', 'Machine Learning']
    return dbc.Col([
        html.Div([
            html.H2('TECHNICAL PROFICIENCIES', className='heading'),
            html.Div([
                html.Div([
                    html.Span(className='skill-dot'),
                    html.Span(skill)
                ], className='mb-2') for skill in skills
            ])
        ], className='panel')
    ], width=6)

def create_mission_panel():
    return dbc.Row([
        dbc.Col([
            html.Div([
                html.H2('MISSION STATEMENT', className='heading'),
                html.P('''
                    [Your professional summary and mission statement here. 
                    Describe your journey, passions, and what drives you in your field.]
                ''', style={'color': 'var(--primary-color)'})
            ], className='panel')
        ])
    ], className='mt-4')

def create_about_layout():
    return html.Div([
        html.Div([
            create_header(),
            dbc.Row([
                create_profile_panel(),
                create_skills_panel()
            ]),
            create_mission_panel(),
            create_footer(),
            create_corner_decorations()
        ], className='nostromo-border')
    ])
