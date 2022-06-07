"""
This module contains all the logic for the sidebar component.
"""

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

## Relationship between each element of the sidebar and the href that
## each one goes to for the structural inforamtion pages.
struct_information_pages = {
    'Dashboard': 'dashboard',
    'Sensors Status': 'sensors',
    'Structural Information': 'structural-information',
    'Risk Management': 'risk-mngmt',
}

## Relationship between each element of the sidebar and the href that
## each one goes to for the data analytics pages.
data_analytics_pages = {
    # 'Dynamic Response Analysis' : 'dynamic-res-an',
    'Event Alert': 'event-alert',
    'Goal': 'goal',
    'Trends': 'trends',
    'Comparison': 'comparison'
}

## Relationship between each element of the sidebar and the href that
## each one goes to for the settings pages.
settings_pages = {
    'Settings': 'settings',
    'Report': 'report'
}

## Variable that is going to have all the dash components to render the 
## header of the sidebar
sidebar_header = dbc.Row(
    [
        dbc.Col(html.H3("Structure Information", className="display-5")),
        dbc.Col(
            [
                html.Button(
                    # use the Bootstrap navbar-toggler classes to style
                    html.Span(className="navbar-toggler-icon"),
                    className="navbar-toggler",
                    # the navbar-toggler classes don't set color
                    style={
                        "color": "rgba(0,0,0,.1)",
                        "border-color": "rgba(0,0,0,.1)",
                    },
                    id="navbar-toggle",
                ),
                html.Button(
                    # use the Bootstrap navbar-toggler classes to style
                    html.Span(className="navbar-toggler-icon"),
                    className="navbar-toggler",
                    # the navbar-toggler classes don't set color
                    style={
                        "color": "rgba(0,0,0,.1)",
                        "border-color": "rgba(0,0,0,.1)",
                    },
                    id="sidebar-toggle",
                ),
            ],
            # the column containing the toggle will be only as wide as the
            # toggle, resulting in the toggle being right aligned
            width="auto",
            # vertically align the toggle in the center
            align="center",
        ),
    ],
    align="center"
)


## Fucntion with the dash components to create a line separator.
def create_separator_bar(id_name):
    """
	Function that create a line separator using the dash components, each
	separator has its own id.

	Parameters
	----------
	id_name : str value
		string with the name that is going to be assigned as id to the 
		line separator when it is call.

	Returns
	-------
	Returns the dash components to create the line separator with a specific id.
	"""
    separator_bar = html.Div(
        [
            html.Hr(),
        ],
        id=id_name,
    )
    return separator_bar


## Variable that is going to have all the dash components that are going to control
## the behaviour of the sidebar, when it is collapse no text is going to be shown and 
## when it is clicked then all the possible routes for the structural section in web plataform
## are displayed.
structural_analysis_section = dbc.Collapse(
    dbc.Nav(
        [
            dbc.NavLink(
                html.Span([html.I(className="fas fas fa-chart-bar ml-2"), "Dashboard"]),
                href=f"/{struct_information_pages['Dashboard']}",
                id=f"{struct_information_pages['Dashboard']}-link"),
            dbc.NavLink(
                html.Span([html.I(className="fas fas fa-wifi ml-2"), "Sensors Status"]),
                href=f"/{struct_information_pages['Sensors Status']}",
                id=f"{struct_information_pages['Sensors Status']}-link"),
            dbc.NavLink(
                html.Span([html.I(className="fas fa-toolbox ml-2"), "Structural Information"]),
                href=f"/{struct_information_pages['Structural Information']}",
                id=f"{struct_information_pages['Structural Information']}-link"),
            dbc.NavLink(
                html.Span([html.I(className="fas fa-cogs ml-2"), "Risk Management"]),
                href=f"/{struct_information_pages['Risk Management']}",
                id=f"{struct_information_pages['Risk Management']}-link"),
        ],
        vertical=True,
        pills=True,
    ),
    id="collapse",
)

## Variable that is going to have all the dash components that are going to control
## the behaviour of the sidebar, when it is collapse no text is going to be shown and 
## when it is clicked then all the possible routes for the analytics section in web plataform
## are displayed.
data_analytics_section = dbc.Collapse(
    dbc.Nav(
        [
            dbc.NavLink(
                html.Span([html.I(className="fas fa-exclamation-triangle ml-2"), "Event Alert"]),
                href=f"/{data_analytics_pages['Event Alert']}",
                id=f"{data_analytics_pages['Event Alert']}-link"),
            dbc.NavLink(
                html.Span([html.I(className="fas fa-award ml-2"), "Goal"]),
                href=f"/{data_analytics_pages['Goal']}",
                id=f"{data_analytics_pages['Goal']}-link"),
            dbc.NavLink(
                html.Span([html.I(className="fas fa-chart-line ml-2"), "Trends"]),
                href=f"/{data_analytics_pages['Trends']}",
                id=f"{data_analytics_pages['Trends']}-link"),
            dbc.NavLink(
                html.Span([html.I(className="fas fa-not-equal ml-2"), "Comparison"]),
                href=f"/{data_analytics_pages['Comparison']}",
                id=f"{data_analytics_pages['Comparison']}-link"),
        ],
        vertical=True,
        pills=True,
    ),
    id="da-collapse",
)

## Variable that is going to have all the dash components that are going to control
## the behaviour of the sidebar, when it is collapse no text is going to be shown and 
## when it is clicked then all the possible routes for the analytics section in web plataform
## are displayed.
settings_section = dbc.Collapse(
    dbc.Nav(
        [
            dbc.NavLink(
                html.Span([html.I(className="fas fa-tools ml-2"), "Settings"]),
                href=f"/{settings_pages['Settings']}",
                id=f"{settings_pages['Settings']}-link"),
            dbc.NavLink(
                html.Span([html.I(className="fas fa-book ml-2"), "Report"]),
                href=f"/{settings_pages['Report']}",
                id=f"{settings_pages['Report']}-link"),
        ],
        vertical=True,
        pills=True,
    ),
    id="s-collapse",
)

## Variable that has all the components of the sidebar in the order that they are 
## going to be rendered in the web page.
sidebar = html.Div(
    [

        sidebar_header,
        # we wrap the horizontal rule and short blurb in a div that can be
        # hidden on a small screen
        create_separator_bar('blurb'),
        # use the Collapse component to animate hiding / revealing links

        structural_analysis_section,

        create_separator_bar('blurb-2'),

        dbc.Row(
            [dbc.Col(html.H3("Data Analytics", className="display-5"))]
        ),

        create_separator_bar('blurb-3'),

        data_analytics_section,

        create_separator_bar('blurb-4'),

        dbc.Row(
            [dbc.Col(html.H3("Settings", className="display-5"))]
        ),

        create_separator_bar('blurb-5'),

        settings_section,

        create_separator_bar('blurb-6'),

        dbc.Row(
            dbc.Col([
                html.Button('Click',
                            id='run',
                            ),
                html.Button('Add',
                            id='addRun',
                            ),
                # width='auto',
            ]),
            justify='around'
        ),
		create_separator_bar('blurb-7'),

    ],
    id="sidebar",
    className="collapsed",
    style={'box-shadow': '4px 4px 4px #e3e3e3'}
)
