"""
This module contains the Callbacks that modifies and determines the
behavior of the sidebar component.
"""

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from components.dashboard import dashboard_body
from components.sensors import sensors_body
from components.dynamic_analysis import dynamic_analysis_body
from components.structural_analysis import tabs, register_callbacks_structural_analysis
from components.risk_management import risk_management_body
from components.goal_seek import goalseek_body
from components.actives import actives_body
from components.trends import trends_body
from components.mines_location import mines_body
from components.event_alerts import alerts_layout
 

## Relationship between each element of the sidebar and the href that
## each one goes to for the structural inforamtion pages.
struct_information_pages = {
	'Dashboard' : 'dashboard',
	'Sensors Status': 'sensors',
	'Structural Information' : 'structural-information',
	'Risk Management' : 'risk-mngmt',
	'Event Alert': 'event-alert'
}

## Relationship between each element of the sidebar and the href that
## each one goes to for the data analytics pages.
data_analytics_pages = {
	#'Dynamic Response Analysis' : 'dynamic-res-an',
	'Goal' : 'goal',
	'Trends' : 'trends',
	'Comparison': 'comparison'
}

## Relationship between each element of the sidebar and the href that
## each one goes to for the settings pages.
settings_pages = {
	#'Dynamic Response Analysis' : 'dynamic-res-an',
	'Settings' : 'settings',
	'Report' : 'report'
}

all_pages = {**struct_information_pages,**data_analytics_pages,**settings_pages}
number_of_pages = len(all_pages)

## Controls the interactions that the final user can have with the sidebar and
## the response that each of this should have.
def register_callbacks(app):
	register_callbacks_structural_analysis(app)
	
	@app.callback(
		[Output(f"{page}-link", "active") for page in all_pages.values()],
		[Input("url", "pathname")],
	)
	def toggle_active_links(pathname):
		"""
		Function that uses the current pathname to set the active state of the
		corresponding nav link to true, allowing users to tell see page they are on.
		
		Parameters
		----------
		pathname -> url : pathname
			pathname of the url page
		
		Returns
		-------
		Returns the links for each page that was defined in the all_pages variable.
		"""
		print(pathname)
		if pathname == "/":
			# Treat page 1 as the homepage / index
			return [True] + [False]*(number_of_pages-1)
		return [pathname == f"/{page}" for page in all_pages.values()]


	@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
	def render_page_content(pathname):
		"""
		Function that uses the current pathname to render the page content of the 
		selected value in the sidebar list of values
		
		Parameters
		----------
		pathname -> url : pathname
			pathname of the url page
		
		Returns
		-------
		Returns the corresponding objects and data that are needed in the current page.
		"""
		if pathname in ["/", "/mines"]:
			return mines_body(app)
		if pathname in "/dashboard":
			return dashboard_body(app)
		elif pathname == "/sensors":
			return sensors_body(app)
		elif pathname == "/structural-information":
			return tabs
		elif pathname == "/risk-mngmt":
			return risk_management_body(app)
		#elif pathname == "/dynamic-res-an":
			#return dynamic_analysis_body(app)
		elif pathname == "/trends":
			return trends_body(app)
		elif pathname == "/event-alert":
			return alerts_layout
		elif pathname == "/goal":
			return goalseek_body(app)
		elif pathname == "/comparison":
			return html.Div(id = 'comparison-container')
			# return dbc.Jumbotron(
			# 	[
			# 		html.H1("404: Was found", className="text-danger"),
			# 		html.Hr(),
			# 		html.P(f"The pathname {pathname} was not recognised..."),
			# 	]
			# )
		elif pathname == "/actives":
			return actives_body(app)
		elif pathname == "/settings":
			return dbc.Jumbotron(
				[
					html.H1("404: Not found", className="text-danger"),
					html.Hr(),
					html.P(f"The pathname {pathname} was not recognised..."),
				]
			)
		elif pathname == "/report":
			return dbc.Jumbotron(
				[
					html.H1("404: Not found", className="text-danger"),
					html.Hr(),
					html.P(f"The pathname {pathname} was not recognised..."),
				]
			)
		# If the user tries to reach a different page, return a 404 message
		#return dbc.Jumbotron(
		#	[
		#		html.H1("404: Not found", className="text-danger"),
		#		html.Hr(),
		#		html.P(f"The pathname {pathname} was not recognised..."),
		#	]
		#)


	@app.callback(
		Output("sidebar", "className"),
		[Input("sidebar-toggle", "n_clicks")],
		[State("sidebar", "className")],
	)
	def toggle_classname(n, classname):
		if n and classname == "":
			return "collapsed"
		return ""


	@app.callback(
		[Output("collapse", "is_open"),
		Output("da-collapse", "is_open"),
		Output("s-collapse", "is_open")],
		[Input("navbar-toggle", "n_clicks")],
		[State("collapse", "is_open")],
	)
	def toggle_collapse(n, is_open):
		if n:
			return not is_open, not is_open, not is_open
		return is_open,is_open,is_open
