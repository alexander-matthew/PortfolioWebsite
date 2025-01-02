from dash import Dash, html,dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Import all components and pages
from .pages.about import create_about_layout
from .components.navbar import create_navbar
from .components.footer import create_footer


def create_app():
    app = Dash(
        __name__,
        external_stylesheets=[dbc.themes.CYBORG],
        suppress_callback_exceptions=True
    )
    return app


def init_app():
    app = create_app()

    #outer corners
    app.layout = html.Div([
        dcc.Location(id='url', refresh=False),

        # Main container
        html.Div([
            create_navbar(),

            html.Div(id='welcome-sequence', className='welcome-container'),

            # Main content
            html.Div(
                id='page-content',
                className='flex-grow',
                style={
                    'min-height': 'calc(100vh - 200px)',
                    'padding': '20px 0'
                }
            ),

            create_footer(),
        ]),
    ])

    # Page routing callback
    @app.callback(
        Output('page-content', 'children'),
        Input('url', 'pathname')
    )
    def display_page(pathname):
        if pathname == '/' or pathname == '/about':
            return create_about_layout()
        elif pathname == '/games/poker':
            return html.Div("Poker Page")
        elif pathname == '/games/chess':
            return html.Div("Chess")
        elif pathname.startswith('/projects/'):
            return html.Div("Projects Page - Coming Soon")
        return create_about_layout()

    return app