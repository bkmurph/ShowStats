import dash
import dash_bootstrap_components as dbc
from dash import html

app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.SLATE],
)

sidebar = dbc.Nav(
    [
        dbc.NavLink(
            [
                html.Div(page["name"]),  # className="ms-2"
            ],
            href=page["path"],
            active="exact",
        )
        for page in dash.page_registry.values()
    ],
    vertical=True,
    pills=True,
    className="my-4",
)

app.layout = dbc.Container(
    [
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        html.A(
                            children=[
                                html.Img(
                                    src="/assets/shell_transparent.png",
                                    height=220,
                                    width=350,
                                )
                            ],
                        ),
                    ),
                    className="text-center",
                ),
                dbc.Col([sidebar]),
            ]
        ),
        html.Hr(),
        dbc.Row([dash.page_container]),
    ],
)


if __name__ == "__main__":
    app.run(debug=False)
