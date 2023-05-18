import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

# import show_stats.ShowStats.helper_functions as hf

dash.register_page(__name__, name="About the Site")

layout = html.Div([dcc.Markdown("# This will be the About the Site Page")])
