import dash_bootstrap_components as dbc

footer = dbc.Navbar(
    dbc.Col(
        "Developed by Team 50 - DS4A",
        className="text-end text-muted px-2",
    ),
    id="bottom-bar",
    color="dark", dark=True, fixed="bottom",
    # className="ms-2 mx-2",
)
