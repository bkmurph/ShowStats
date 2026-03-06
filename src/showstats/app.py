import dash
import dash_bootstrap_components as dbc
from dash import Dash, html

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.SLATE],
    suppress_callback_exceptions=True,
)

app.index_string = """<!DOCTYPE html>
<html>
    <head>
        <!-- Google tag (gtag.js) -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-96VFHDJ12B"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());

          gtag('config', 'G-96VFHDJ12B');
        </script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""


server = app.server

sidebar = dbc.Nav(
    [
        dbc.NavLink(
            [
                html.Div(page["name"]),
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
                                    src="https://showstats1.s3.amazonaws.com/assets/shell_transparent.PNG",
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
        html.Hr(),
        html.H2("External Links:"),
        dbc.Row(
            [
                dbc.Col(
                    html.A(
                        href="https://github.com/bkmurph/ShowStats",
                        children=[
                            html.Img(
                                src="https://showstats1.s3.amazonaws.com/assets/pngegg.png",
                                alt="Link to my GitHub",
                                height=90,
                                width=90,
                            )
                        ],
                    ),
                    className="text-center",
                ),
                dbc.Col(
                    html.A(
                        href="https://relisten.net/",
                        children=[
                            html.Img(
                                src="https://showstats1.s3.amazonaws.com/assets/relisten.png",
                                alt="Data source for much of this site",
                                height=90,
                                width=90,
                            )
                        ],
                    ),
                    className="text-center",
                ),
                dbc.Col(
                    html.A(
                        href="https://www.buymeacoffee.com/bkmurphy5k",
                        children=[
                            html.Img(
                                src="https://showstats1.s3.amazonaws.com/assets/coffee.png",
                                height=90,
                                width=90,
                            )
                        ],
                    ),
                    className="text-center",
                ),
            ],
            className="my-4",
            justify="center",
        ),
    ],
)


if __name__ == "__main__":
    app.run(debug=False)
