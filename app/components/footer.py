# app/components/footer.py
from dash import html
from dash_iconify import DashIconify


def create_footer():
    return html.Div([

        # Credits section
        html.Div([
            'Created by Alexander Matthew in Python + Plotly Dash with the help of my intern (Claude AI). ',
            'Hosted using Heroku. ',
           ],
            className='footer-credits'),

        # Socials
        html.Div([
            html.A([
                DashIconify(icon="mdi:github", width=24)
            ], href="https://github.com/alexander-matthew", target="_blank", className='social-link'),

            html.A([
                DashIconify(icon="mdi:linkedin", width=24)
            ], href="https://www.linkedin.com/in/alex-matthew1/", target="_blank", className='social-link'),
        ], className='footer-social')

    ]
    , className='footer')
