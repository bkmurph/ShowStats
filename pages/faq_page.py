import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State

# import show_stats.ShowStats.helper_functions as hf

dash.register_page(__name__, name="FAQs")

layout = html.Div([dcc.Markdown("# This will be the FAQ Page")])
