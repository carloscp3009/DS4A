# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, Input, Output, State
import dash_bootstrap_components as dbc
from components.navbar import navbar
from components.central_container import central_container
from components.footer import footer
import dash_auth

# ------------------------------------------------------------------------------

app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])
app.title = "Dashboard | Agrosavia"
app._favicon = "favicon.png"

USERNAME_PASSWORD_PAIRS = {
    'agrosavia': 'team50',
    'correlationone': 'team50',
    'ds4a': 'team50'
}
auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)

# ------------------------------------------------------------------------------
# App layout
# ------------------------------------------------------------------------------
app.layout = dbc.Container(
    children=[
        navbar,
        central_container,
        footer,
    ],
    id="main-container",
)


# ------------------------------------------------------------------------------
# Callbacks
# ------------------------------------------------------------------------------
# Add callback for toggling the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# ------------------------------------------------------------------------------
# Run the Dash app
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0')
