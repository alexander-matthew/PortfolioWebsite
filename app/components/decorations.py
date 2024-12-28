from dash import html

def create_corner_decorations():
    return html.Div([
        html.Div(className='corner-decoration corner-tl'),
        html.Div(className='corner-decoration corner-tr'),
        html.Div(className='corner-decoration corner-bl'),
        html.Div(className='corner-decoration corner-br'),
    ])