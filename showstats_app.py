#######################################
#               Imports               #
#######################################

import dash
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import helper_functions as hf
import pandas as pd
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash_bootstrap_templates import load_figure_template

#######################################
#            Read in data             #
#######################################
my_shows = pd.read_parquet(
    path="/Users/brandonmurphy/projects/show_stats/ShowStats/data/showstats_update.parquet"
)

my_shows = my_shows.reset_index(drop=True)


#######################################
#            Read in Template         #
#######################################

load_figure_template("slate")

#######################################
#            Initialize App           #
#######################################
app = dash.Dash(external_stylesheets=[dbc.themes.SLATE])

# Header Components
h1 = html.H1("Show Stats", style={"backgroundColor": "#99999A"})
h3_ = html.H3("Select Artist(s)", style={"paddingRight": "30px"})

#######################################
#           Dropdown Options          #
#######################################
unique_shows = (
    my_shows.drop_duplicates(subset=["uuid"])
    .sort_values("date", ascending=False)
    .reset_index()
)

phish_options = hf.create_show_list(unique_shows, "Phish")
panic_options = hf.create_show_list(unique_shows, "Widespread Panic")
goose_options = hf.create_show_list(unique_shows, "Goose")
gd_options = hf.create_show_list(unique_shows, "Grateful Dead")
billy_options = hf.create_show_list(unique_shows, "Billy Strings")

phish_dropdown = dcc.Dropdown(
    id="phish_drop",
    options=phish_options,
    value=hf.phish_starter_uuids,
    multi=True,
    searchable=True,
    style={"color": "black"},
)

panic_dropdown = dcc.Dropdown(
    id="panic_drop",
    options=panic_options,
    value=hf.panic_starter_uuids,
    multi=True,
    searchable=True,
    style={"color": "black"},
)

goose_dropdown = dcc.Dropdown(
    id="goose_drop",
    options=goose_options,
    value=hf.goose_starter_uuids,
    multi=True,
    searchable=True,
    style={"color": "black"},
)

billy_dropdown = dcc.Dropdown(
    id="billy_drop",
    options=billy_options,
    value=[],
    multi=True,
    searchable=True,
    style={"color": "black"},
)

dead_dropdown = dcc.Dropdown(
    id="dead_drop",
    options=gd_options,
    value=[],
    multi=True,
    searchable=True,
    style={"color": "black"},
)

#######################################
#           Submit Button             #
#######################################

button = dbc.Button(
    id="submit_button",
    n_clicks=0,
    children="Submit",
)


##############################################
# What is my (measurable) show count by year #
##############################################

line_plot = dcc.Graph(
    id="line_chart",
)

#######################################
# What Songs Have I Seen the Most?    #
#######################################

song_count = dcc.Graph(
    id="songs_bar",
)

###############################
# Number of Unique Songs Seen #
###############################

unique_graph = dcc.Graph(id="unique_")

########################################
# What are the longest jams I've seen? #
########################################
# longest_jams_bar = dcc.Graph(
#     id="jams_bar",
# )
longest_jams_bar = dag.AgGrid(
    id="test_table",
    className="ag-theme-alpine-dark",
    # columnSize="sizeToFit"
)

##########################
# Map Out Show Locations #
##########################

map_shows = dcc.Graph(
    id="concert_map",
)


# count_card = dbc.Card(
#     [
#         dbc.CardHeader(html.H2("Show Count Over The Years")),
#         dbc.CardBody(html.Div([line_plot])),
#     ]
# )

# unique_card = dbc.Card(
#     [
#         dbc.CardHeader(html.H2("Unique Songs Seen By Artist")),
#         dbc.CardBody(html.Div([unique_graph])),
#     ],
#     # style={"height": "80vh", "width": "80vw"},
# )

# longest_jams_card = dbc.Card(
#     [
#         dbc.CardHeader(html.H2("What Are The Longest Jams You've Seen?")),
#         dbc.CardBody(html.Div([longest_jams_bar])),
#     ]
# )
# top_songs_card = dbc.Card(
#     [
#         dbc.CardHeader(html.H2("What songs have you seen played most?")),
#         dbc.CardBody(html.Div([song_count])),
#     ]
# )

# map_shows_card = dbc.Card(
#     [
#         dbc.CardHeader(html.H2("Locations of Shows You've Been To")),
#         dbc.CardBody(html.Div([map_shows])),
#     ]
# )

accordion = dbc.Accordion(
    [
        dbc.AccordionItem([billy_dropdown], title="Billy Strings"),
        dbc.AccordionItem(
            [goose_dropdown],
            title="Goose",
        ),
        dbc.AccordionItem([dead_dropdown], title="Grateful Dead"),
        dbc.AccordionItem(
            [phish_dropdown],
            title="Phish",
        ),
        dbc.AccordionItem(
            [panic_dropdown],
            title="Widespread Panic",
        ),
    ],
)

#######################################
# Combine All Components Defined Above #
#######################################

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        html.A(
                            children=[
                                html.Img(
                                    src="/assets/shell_transparent.png",
                                    height=180,
                                    width=300,
                                )
                            ],
                        ),
                    ),
                    md=8,
                    lg=10
                    # width={"size": 4},
                ),
                dbc.Col(
                    html.A(
                        href="https://github.com/bkmurph/ShowStats",
                        children=[
                            html.Img(
                                src="assets/pngegg.png",
                                alt="Link to my GitHub",
                                height=90,
                                width=90,
                            )
                        ],
                    ),
                    md=4,
                    lg=1
                    # width={"size": 1, "offset": 5},
                ),
                # dbc.Col(
                #     html.A(
                #         href="https://relisten.net/",
                #         children=[
                #             html.Img(src="assets/relisten.png", height=90, width=90)
                #         ],
                #     ),
                #     #  width={"size": 1},
                # ),
                dbc.Col(
                    html.Div(html.Img(src="/assets/coffee.png", height=90, width=90)),
                    md=4,
                    lg=1
                    #  width={"size": 1},
                ),
            ],
            class_name="my-4",
            justify="center",
        ),
        h3_,
        dbc.Row(
            [
                dbc.Col(accordion, md=6, lg=10),
                dbc.Col(button),
            ],
            class_name="my-4",
        ),
        html.H2("Show Count Over The Years"),
        dbc.Row([line_plot], class_name="my-4"),
        html.H2("Unique Songs Seen By Artist"),
        dbc.Row([unique_graph], class_name="my-4"),
        html.H2("What Are The Longest Jams You've Seen?"),
        dbc.Row([longest_jams_bar], class_name="my-4"),
        # html.Div([longest_jams_bar]),
        html.H2("What Songs Have You Seen Played Most?"),
        dbc.Row([song_count], class_name="my-4"),
        html.H2("Locations of Shows You've Been To"),
        dbc.Row([map_shows], class_name="my-4"),
    ],
)

#######################################
#              Callbacks              #
#######################################


@app.callback(
    Output("line_chart", "figure"),
    [Input("submit_button", "n_clicks")],
    [
        State("phish_drop", "value"),
        State("panic_drop", "value"),
        State("goose_drop", "value"),
        State("billy_drop", "value"),
        State("dead_drop", "value"),
    ],
)
def update_show_counts(
    n_clicks, phish_uuids, wsp_uuids, goose_uuids, billy_uuids, dead_uuids
):
    uuids = phish_uuids + wsp_uuids + goose_uuids + billy_uuids + dead_uuids
    shows_by_year = (
        my_shows[my_shows["uuid"].isin(uuids)]
        .groupby(["year.year", "artist"])["uuid"]
        .nunique()
        .reset_index()
        .sort_values(by=["year.year", "artist"])
    )
    year_order = shows_by_year["year.year"].sort_values(ascending=True).unique()
    category_order = {
        "year.year": year_order,
        "artist": ["Goose", "Phish", "Widespread Panic"],
    }
    line_chart = px.line(
        data_frame=shows_by_year,
        x="year.year",
        y="uuid",
        color="artist",
        color_discrete_map=hf.color_dict,
        markers=True,
        category_orders=category_order,
        labels={"year.year": "Year", "uuid": "Show Count", "artist": "Artist"},
    )

    line_chart.update_layout(legend_orientation="h", xaxis_title=None)

    return line_chart


@app.callback(
    Output("unique_", "figure"),
    [Input("submit_button", "n_clicks")],
    [
        State("phish_drop", "value"),
        State("panic_drop", "value"),
        State("goose_drop", "value"),
        State("billy_drop", "value"),
        State("dead_drop", "value"),
    ],
)
def update_unique_songs(
    n_clicks, phish_uuids, wsp_uuids, goose_uuids, billy_uuids, dead_uuids
):
    uuids = phish_uuids + wsp_uuids + goose_uuids + billy_uuids + dead_uuids
    unique_songs = (
        my_shows[my_shows["uuid"].isin(uuids)]
        .groupby(["artist"])["title"]
        .nunique()
        .reset_index()
        .copy()
    )

    unique_bar = px.bar(
        data_frame=unique_songs,
        x="artist",
        y="title",
        color="artist",
        color_discrete_map=hf.color_dict,
        category_orders=hf.category_orders,
        text="title",
        labels={"artist": "Artist", "title": "Unique Songs Seen"},
    )
    unique_bar.update_traces(textposition="outside")
    unique_bar.update_layout(showlegend=False, xaxis_title=None)
    return unique_bar


@app.callback(
    Output("concert_map", "figure"),
    [Input("submit_button", "n_clicks")],
    [
        State("phish_drop", "value"),
        State("panic_drop", "value"),
        State("goose_drop", "value"),
        State("billy_drop", "value"),
        State("dead_drop", "value"),
    ],
)
def update_scatter_mapbox(
    n_clicks, phish_uuids, wsp_uuids, goose_uuids, billy_uuids, dead_uuids
):
    uuids = phish_uuids + wsp_uuids + goose_uuids + billy_uuids + dead_uuids
    map_data = my_shows[my_shows["uuid"].isin(uuids)].reset_index().copy()
    map_data = hf.convert_seconds_to_hms(map_data, "avg_duration")
    map_data = map_data[~map_data["latitude"].isna()].reset_index().copy()

    show_map = px.scatter_mapbox(
        data_frame=map_data,
        lat="latitude",
        lon="longitude",
        hover_name="artist",
        hover_data=["venue_name", "venue_location", "display_date", "duration_hms"],
        color="artist",
        color_discrete_map=hf.color_dict,
        category_orders=hf.category_orders,
        zoom=2.9,
        height=450,
        opacity=0.6,
        size_max=90,
        labels={
            "venue_name": "Venue",
            "venue_location": "Location",
            "latitude": "Latitude",
            "longitude": "Longitude",
            "artist": "Artist",
            "display_date": "Date",
            "duration_hms": "Show Time",
        },
    )
    show_map.update_traces(marker={"size": 12})
    show_map.update_layout(
        mapbox_style="open-street-map",
        mapbox=dict(
            center=dict(lat=39.18, lon=-96.60),
        ),
        legend_orientation="h",
    )

    return show_map


@app.callback(
    Output("songs_bar", "figure"),
    [Input("submit_button", "n_clicks")],
    [
        State("phish_drop", "value"),
        State("panic_drop", "value"),
        State("goose_drop", "value"),
        State("billy_drop", "value"),
        State("dead_drop", "value"),
    ],
)
def update_top_songs(
    n_clicks, phish_uuids, wsp_uuids, goose_uuids, billy_uuids, dead_uuids
):
    uuids = phish_uuids + wsp_uuids + goose_uuids + billy_uuids + dead_uuids
    song_counts = (
        my_shows[my_shows["uuid"].isin(uuids)]
        .groupby(["artist", "title"])["slug"]
        .count()
        .reset_index()
        .sort_values("slug", ascending=False)
        .rename(columns={"slug": "times_heard"})
        .head(15)
        .copy()
    )

    top_songs = px.bar(
        data_frame=song_counts,
        x="times_heard",
        y="title",
        color="artist",
        color_discrete_map=hf.color_dict,
        category_orders=hf.category_orders,
        text="times_heard",
        labels={"title": "", "times_heard": "Number Times Seen", "artist": "Artist"},
    )
    top_songs.update_layout(
        yaxis={"categoryorder": "total ascending"},
        legend_orientation="h",
        font={"size": 12},
    )
    # top_songs.update_yaxes(tickangle=-30)

    top_songs.update_traces(textposition="outside")
    # top_songs.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 10})

    return top_songs


@app.callback(
    Output("test_table", "rowData"),
    Output("test_table", "columnDefs"),
    [Input("submit_button", "n_clicks")],
    [
        State("phish_drop", "value"),
        State("panic_drop", "value"),
        State("goose_drop", "value"),
        State("billy_drop", "value"),
        State("dead_drop", "value"),
    ],
)
def update_longest_jams(
    n_clicks, phish_uuids, wsp_uuids, goose_uuids, billy_uuids, dead_uuids
):
    uuids = phish_uuids + wsp_uuids + goose_uuids + billy_uuids + dead_uuids
    longest_jams = (
        my_shows[my_shows["uuid"].isin(uuids)]
        .sort_values("duration", ascending=False)
        .assign(
            duration_hms=my_shows["duration"]
            .astype("datetime64[s]")
            .dt.strftime("%M:%S")
        )
        .assign(minutes=round(my_shows["duration"] / 60, 2))
        .rename(
            columns={
                "artist": "Artist",
                "venue_location": "City",
                "title": "Song",
                "duration_hms": "Duration",
                "display_date": "Date",
                "venue_name": "Venue",
            }
        )
        .head(20)
    )

    longest_jams = longest_jams[
        [
            "Artist",
            "City",
            "Venue",
            "Song",
            "Duration",
            "Date",
        ]
    ]

    rowData = longest_jams.to_dict("records")
    columnDefs = [{"field": i, "id": i} for i in longest_jams.columns]

    return rowData, columnDefs


#######################################
#           Run this thing            #
#######################################

if __name__ == "__main__":
    app.run_server()
