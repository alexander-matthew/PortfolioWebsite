# app/components/footer.py
from dash import html

def create_footer():
    return html.Div([
        html.Div('SYSTEM: OPERATIONAL'),
        html.Div('MEMORY: 98.2% AVAILABLE')
    ], style={'position': 'absolute', 'bottom': '20px', 'right': '20px'})
