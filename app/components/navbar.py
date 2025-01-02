from dash import html
import dash_bootstrap_components as dbc


def create_navbar():
    return dbc.NavbarSimple(
        children=[
            # Games Dropdown
            dbc.NavItem(
                dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem("Poker", href="/games/poker"),
                        dbc.DropdownMenuItem("Chess", href="/games/chess"),
                    ],
                    nav=True,
                    label="Games",
                    toggle_style={
                        "color": "var(--primary-color)",
                    }
                )
            ),

            # Projects Dropdown
            dbc.NavItem(
                dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem("Project 1", href="/projects/1"),
                        dbc.DropdownMenuItem("Project 2", href="/projects/2"),
                        dbc.DropdownMenuItem("Project 3", href="/projects/3"),
                    ],
                    nav=True,
                    label="Projects",
                    toggle_style={
                        "color": "var(--primary-color)",
                    }
                )
            ),

            # About Link
            dbc.NavItem(
                dbc.NavLink("About", href="/about", style={"color": "var(--primary-color)"})
            ),
        ],
        brand="ACM",
        brand_href="/",
        color="black",
        dark=True,
        className="navbar-custom",
        style={
            "border": "2px solid var(--primary-color)",
            "background-color": "var(--panel-bg)",
            "font-family": "'Share Tech Mono', monospace",
        }
    )