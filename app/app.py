from dash import Dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


def create_app():
    app = Dash(
        __name__,
        external_stylesheets=[dbc.themes.CYBORG],
        suppress_callback_exceptions=True
    )
    return app


def init_app():
    from app.pages.about import create_about_layout
    from app.components.welcome_sequence import register_welcome_callbacks
    from app.components.clock import register_clock_callbacks

    app = create_app()
    app.layout = create_about_layout()

    # Register callbacks
    register_welcome_callbacks(app)
    register_clock_callbacks(app)

    return app