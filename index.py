""" SHM Web Page

This module contains the driver of the webpage using Dash. Bootstrap theme and Awsome Font icons are loaded in order
to have the styles and icons. Responside tags for header are added and color palette is defined. 

This webapge is made with a sort of MVC pattern, where all the pages Callbacks are loaded here. 

NavBar and SideBar are separated entities of this application, as they are showed in all pages. Besides, by 
decision, SideBar is the responsable for rendering the views.  

All data is allocated in data folder and assest (Images and Stylesheets) are allocated in assets

"""

import dash
import dash_auth
import dash_bootstrap_components as dbc
from dash import html, dcc

# import dash_core_components as dcc
# import dash_html_components as html
# from flask_cors import CORS

# import components.sidebar_callbacks as sc
# import components.dashboard_callbacks as dashboard
# #import components.sensors_callbacks as sensors
# import components.dynamic_analysis_callbacks as dynamic_analysis
# import components.risk_management as risk_management
# import components.goal_seek as goal_seek
# import components.layout_modification_callbacks as layout_callbacks
from components.navbar import navbar
# from components.sidebar import sidebar
# from components.api import api
import json

FONT_AWESOME = "https://use.fontawesome.com/releases/v5.7.2/css/all.css"

USERNAME_PASSWORD_PAIRS = {
    'user1': 'test1'
    , 'user2': 'test2'
    , 'user3': 'test3'
}


app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP, FONT_AWESOME],
             
                # these meta_tags ensure content is scaled correctly on different devices
                # see: https://www.w3schools.com/css/css_rwd_viewport.asp for more
                title="DS4A",
                meta_tags=[
                    {
                        "name": "viewport",
                        "content": "width=device-width, initial-scale=1"
                    }
                ],
                )

auth = dash_auth.BasicAuth(
    app,
    USERNAME_PASSWORD_PAIRS
)

server = app.server
# CORS(server)

theme = {
    'dark': True,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E',
}

content = html.Div(id="page-content")
# app.layout = html.Div([dcc.Location(id="url"), navbar, sidebar, content])
app.layout = html.Div([dcc.Location(id="url"), navbar, content])



@server.route('/test')
def test():
    return json.dumps([{'message' : 'Running on index'}])

if __name__ == "__main__":
    app.run_server(port=8888, host="0.0.0.0", debug=True)
# if running locally put localhost:8888 on your browser to enter
