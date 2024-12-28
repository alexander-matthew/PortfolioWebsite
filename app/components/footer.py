# app/components/footer.py
from dash import html

def create_footer():
    return html.Div([
        html.Div('SYSTEM: OPERATIONAL'),
        html.Div('MEMORY: 98.2% AVAILABLE'),
        html.Div('Created by Alexander Matthew in Python + Plotly Dash with the help of my intern (Claude AI). Hosted using Heroku. Github repo: https://github.com/alexander-matthew/PortfolioWebsite')

    ], style={'position': 'absolute', 'bottom': '20px', 'right': '20px'})
