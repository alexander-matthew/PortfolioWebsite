from dash import html
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify

def create_navbar():
    return html.Div([
        # Main navbar container
        dbc.Navbar([
            # Left side - Brand and Status
            html.Div([
                dbc.NavbarBrand("AM", href="/", className="mr-4"),
                html.Div([
                    DashIconify(icon="octicon:dot-fill-24", className="status-icon"),
                    html.Span("Building something cool", className="status-text")
                ], className="d-none d-md-flex align-items-center current-status")
            ], className="d-flex align-items-center"),

            # Right side - Navigation
            dbc.Nav([

                # Games Dropdown
                dbc.NavItem(
                    dbc.DropdownMenu(
                        children=[
                            dbc.DropdownMenuItem([
                                DashIconify(icon="mdi:poker", className="me-2"),
                                "Poker"
                            ], href="/games/poker"),
                            dbc.DropdownMenuItem([
                                DashIconify(icon="mdi:chess", className="me-2"),
                                "Chess"
                            ], href="/games/chess"),
                        ],
                        nav=True,
                        label=[DashIconify(icon="mdi:gamepad", className="me-1"), "Play"],
                        toggle_style={"color": "var(--text-primary)"}
                    )
                ),

                # Projects Dropdown
                dbc.NavItem(
                    dbc.DropdownMenu(
                        children=[
                            dbc.DropdownMenuItem([
                                DashIconify(icon="mdi:run", className="me-2"),
                                "StravaViz"
                            ], href="/projects/strava"),
                            dbc.DropdownMenuItem([
                                DashIconify(icon="mdi:music", className="me-2"),
                                "Music Analysis"
                            ], href="/projects/spotify"),
                        ],
                        nav=True,
                        label=[DashIconify(icon="mdi:code-braces", className="me-1"), "Projects"],
                        toggle_style={"color": "var(--text-primary)"}
                    )
                ),

                # About Dropdown
                dbc.NavItem(
                    dbc.DropdownMenu(
                        children=[
                            dbc.DropdownMenuItem([
                                "Me"
                            ], href="/about/me"),
                            dbc.DropdownMenuItem([
                                "This Project"
                            ], href="/about/thisProject"),
                        ],
                        nav=True,
                        label=[DashIconify(icon="mdi:account", className="me-1"), "About"],
                        toggle_style={"color": "var(--text-primary)"}
                    )
                ),

            ], className="ms-auto", navbar=True)
        ],
        className="navbar-modern",
        color="transparent",
        dark=True,
        expand="lg"
        )
    ])