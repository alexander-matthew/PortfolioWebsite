from dash import Dash, html,dcc
from dash.dependencies import Input, Output
from .pages.about import create_about_me_page
from .components.navbar import create_navbar
from .components.footer import create_footer
import dash_bootstrap_components as dbc
from .pages.SpotifyDemo import create_spotify_page
from .pages.stravaDash import create_strava_page
from .components.sphere_renderer import create_sphere_component

def create_app():
    app = Dash(
        __name__,
        external_stylesheets=[dbc.themes.CYBORG],
        suppress_callback_exceptions=True,
        assets_folder='assets',  # Tell Dash where to find your assets
        assets_url_path='/assets'  # URL path where assets will be served from
    )
    return app


def init_app():
    app = create_app()

    from .pages.SpotifyDemo import register_spotify_callbacks
    register_spotify_callbacks(app)

    #outer corners
    app.layout = html.Div([
        dcc.Location(id='url', refresh=False),

        # Main container
        html.Div([
            create_navbar(),

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
        base_path = pathname.rstrip('/').split('?')[0]

        if base_path == '/' or base_path == '/about':
            return create_about_me_page()
        elif base_path.startswith('/projects/spotify'):
            return create_spotify_page()
        elif base_path == '/projects/strava':
            return create_strava_page()
        elif base_path == '/games/poker':
            return html.Div("Poker Page")
        elif base_path == '/games/chess':
            return html.Div("Chess")
        elif base_path.startswith('/visualArt/sphere'):
            return create_sphere_component(app)
        elif base_path.startswith('/projects/'):
            return html.Div("Projects Page - Coming Soon")
        return create_about_me_page()

    return app