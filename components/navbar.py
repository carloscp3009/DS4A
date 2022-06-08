""" NavBar

This module contains the navbar definition used across all page. All changes must be done here. 
To change something dynamically, please create a navbar_callbacks.py file. 

"""
from pathlib import Path
import base64
import dash_bootstrap_components as dbc
from dash import html, dcc

image_filename = Path.cwd() / 'assets' / 'LOGO.png'  # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())
navbar = dbc.Navbar(
    [
        dbc.Row(
            [
                dbc.Col(html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                                 height='30px'),
                        className='ml-4'),
                dbc.Col(dbc.NavbarBrand(id='Navbar',
                                        children='DS4A',
                                        href='/dashboard'),
                        className='navbar-brand'
                        ),
            ],
            align='center',
            # no_gutters=True,
            justify='end'
        ),
        dbc.Collapse(
            dbc.Row([html.A(id='redirect',
                            children=[dbc.Col(html.H1(id='mineheader',
                                                      children="Data Exploration",
                                                      )
                                              )],
                            href='/dashboard'
                            )
                     ],
                    # no_gutters=True,
                    className="ml-auto flex-nowrap mt-3 mt-md-0",
                    align="center",
                    ),
            navbar=True
        ),
    ],
    id='navbar',
    style={
        'height': '4rem',
    },
    dark='True',
    color='#333333'
)
