from dash import html, dcc
from datetime import datetime
from dash.dependencies import Input, Output

def create_clock():
    """Create the clock component with interval trigger."""
    return html.Div([
        html.Div([
            html.Span('TIME: ', className='text-muted'),
            html.Div([
                html.Span(id='clock-display', className='clock-digit'),
            ], className='clock-container'),
        ], className='clock-wrapper'),
        # Interval component that triggers update every second
        dcc.Interval(
            id='clock-interval',
            interval=1000,  # in milliseconds
            n_intervals=0
        )
    ])

def register_clock_callbacks(app):
    """Register the clock update callback."""
    @app.callback(
        Output('clock-display', 'children'),
        Input('clock-interval', 'n_intervals')
    )
    def update_clock(n):
        return datetime.now().strftime('%H:%M:%S')
