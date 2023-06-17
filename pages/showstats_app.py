#######################################
#               Imports               #
#######################################

import sys

import awswrangler as wr
import dash
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import Input, Output, State, callback, dcc, html
from dash_bootstrap_templates import load_figure_template

import helper_functions as hf

sys.path.insert(0, "/Users/brandonmurphy/projects/show_stats/ShowStats/")

#######################################
#            Initialize App           #
#######################################
dash.register_page(__name__, path="/", name="ShowStats")

#######################################
#            Read in data             #
#######################################
shows = wr.s3.read_parquet("s3://showstats1/showstats_update_new.parquet")
shows = shows.reset_index(drop=True)

#######################################
#            Read in Template         #
#######################################

load_figure_template("slate")


#########################################
#            Read in Drop Downs         #
#########################################

phish_options = hf.get_s3_object("phish")
panic_options = hf.get_s3_object("wsp")
goose_options = hf.get_s3_object("goose")
gd_options = hf.get_s3_object("dead")
billy_options = hf.get_s3_object("billy")


# Header Components
h1 = html.H1("Show Stats", style={"backgroundColor": "#99999A"})
h3_ = html.H3("Select Artist(s)", style={"paddingRight": "30px"})

#######################################
#           Dropdown Options          #
#######################################
nav_dropdown = dbc.DropdownMenu(
    label="Menu",
    children=[
        dbc.DropdownMenuItem("Item 1"),
        dbc.DropdownMenuItem("Item 2"),
        dbc.DropdownMenuItem("Item 3"),
    ],
)

phish_dropdown = dcc.Dropdown(
    id="phish_drop",
    options=phish_options,
    value=[],
    multi=True,
    searchable=True,
    style={"color": "black"},
    persistence=True,
)

panic_dropdown = dcc.Dropdown(
    id="panic_drop",
    options=panic_options,
    value=[],
    multi=True,
    searchable=True,
    style={"color": "black"},
    persistence=True,
)

goose_dropdown = dcc.Dropdown(
    id="goose_drop",
    options=goose_options,
    value=[],
    multi=True,
    searchable=True,
    style={"color": "black"},
    persistence=True,
)

billy_dropdown = dcc.Dropdown(
    id="billy_drop",
    options=billy_options,
    value=[],
    multi=True,
    searchable=True,
    style={"color": "black"},
    persistence=True,
)

dead_dropdown = dcc.Dropdown(
    id="dead_drop",
    options=gd_options,
    value=[],
    multi=True,
    searchable=True,
    style={"color": "black"},
    persistence=True,
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

layout = dbc.Container(
    [
        h3_,
        dbc.Row(
            [
                dbc.Col(accordion),
            ],
            class_name="my-4",
        ),
        dbc.Row([button], class_name="my-4"),
        html.H2("Show Count Over The Years"),
        dbc.Row([line_plot], class_name="my-4"),
        html.H2("Unique Songs Seen By Artist"),
        dbc.Row([unique_graph], class_name="my-4"),
        html.H2("What Are The Longest Jams You've Seen?"),
        dbc.Row([longest_jams_bar], class_name="my-4"),
        html.H2("What Songs Have You Seen Played Most?"),
        dbc.Row([song_count], class_name="my-4"),
        html.H2("Locations of Shows You've Been To"),
        dbc.Row([map_shows], class_name="my-4"),
    ],
)

#######################################
#              Callbacks              #
#######################################


@callback(
    Output("line_chart", "figure"),
    [Input("submit_button", "n_clicks")],
    [
        State("phish_drop", "value"),
        State("panic_drop", "value"),
        State("goose_drop", "value"),
        State("billy_drop", "value"),
        State("dead_drop", "value"),
    ],
    prevent_initial_call=False,
)
def update_show_counts(
    n_clicks, phish_uuids, wsp_uuids, goose_uuids, billy_uuids, dead_uuids
):
    data = hf.filter_dataset(
        shows, phish_uuids, wsp_uuids, goose_uuids, billy_uuids, dead_uuids
    )
    shows_by_year = (
        data.groupby(["year_prod", "artist_prod"])["uuid"]
        .nunique()
        .reset_index()
        .sort_values(by=["year_prod", "artist_prod"])
    )
    year_order = shows_by_year["year_prod"].sort_values(ascending=True).unique()
    category_order = {
        "year_prod": year_order,
        "artist_prod": ["Goose", "Phish", "Widespread Panic"],
    }
    line_chart = px.line(
        data_frame=shows_by_year,
        x="year_prod",
        y="uuid",
        color="artist_prod",
        color_discrete_map=hf.color_dict,
        markers=True,
        category_orders=category_order,
        labels={"year_prod": "Year", "uuid": "Show Count", "artist_prod": "Artist"},
    )

    line_chart.update_layout(legend_orientation="h", xaxis_title=None)

    return line_chart


@callback(
    Output("unique_", "figure"),
    [Input("submit_button", "n_clicks")],
    [
        State("phish_drop", "value"),
        State("panic_drop", "value"),
        State("goose_drop", "value"),
        State("billy_drop", "value"),
        State("dead_drop", "value"),
    ],
    prevent_initial_call=False,
)
def update_unique_songs(
    n_clicks, phish_uuids, wsp_uuids, goose_uuids, billy_uuids, dead_uuids
):
    my_shows = hf.filter_dataset(
        shows, phish_uuids, wsp_uuids, goose_uuids, billy_uuids, dead_uuids
    )
    unique_songs = (
        my_shows.dropna(subset=["song.name"])
        .groupby(["artist_prod"])["song.name"]
        .nunique()
        .reset_index()
        .copy()
    )

    unique_bar = px.bar(
        data_frame=unique_songs,
        x="artist_prod",
        y="song.name",
        color="artist_prod",
        color_discrete_map=hf.color_dict,
        category_orders=hf.category_orders,
        text="song.name",
        labels={"artist_prod": "Artist", "song.name": "Unique Songs Seen"},
    )
    unique_bar.update_traces(textposition="outside")
    unique_bar.update_layout(showlegend=False, xaxis_title=None)

    return unique_bar


@callback(
    Output("concert_map", "figure"),
    [Input("submit_button", "n_clicks")],
    [
        State("phish_drop", "value"),
        State("panic_drop", "value"),
        State("goose_drop", "value"),
        State("billy_drop", "value"),
        State("dead_drop", "value"),
    ],
    prevent_initial_call=False,
)
def update_scatter_mapbox(
    n_clicks, phish_uuids, wsp_uuids, goose_uuids, billy_uuids, dead_uuids
):
    my_shows = hf.filter_dataset(
        shows, phish_uuids, wsp_uuids, goose_uuids, billy_uuids, dead_uuids
    )
    map_data = my_shows.reset_index(drop=True).copy()
    map_data = hf.convert_seconds_to_hms(map_data, "avg_duration")
    map_data = (
        map_data[~map_data["latitude"].isna()]
        .reset_index(drop=True)
        .drop_duplicates(subset=["uuid", "latitude", "longitude"])
        .copy()
    )

    show_map = px.scatter_mapbox(
        data_frame=map_data,
        lat="latitude",
        lon="longitude",
        hover_name="artist_prod",
        hover_data=["venue_name", "venue_location", "display_date", "duration_hms"],
        color="artist_prod",
        color_discrete_map={
            "Phish": "#00205B",
            "Widespread Panic": "#00843D",
            "Goose": "#A6E4DE",
            "Grateful Dead": "#A8DDA8",
            "Billy Strings": "#779ecb",
        },
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
            "artist_prod": "Artist",
            "date_prod": "Date",
            "duration_hms": "Show Time",
        },
    )
    show_map.update_traces(marker={"size": 12})
    show_map.update_layout(
        mapbox_style="carto-positron",  # open-street-map
        mapbox=dict(
            center=dict(lat=39.18, lon=-96.60),
        ),
        legend_orientation="h",
    )

    return show_map


@callback(
    Output("songs_bar", "figure"),
    [Input("submit_button", "n_clicks")],
    [
        State("phish_drop", "value"),
        State("panic_drop", "value"),
        State("goose_drop", "value"),
        State("billy_drop", "value"),
        State("dead_drop", "value"),
    ],
    prevent_initial_call=False,
)
def update_top_songs(
    n_clicks, phish_uuids, wsp_uuids, goose_uuids, billy_uuids, dead_uuids
):
    my_shows = hf.filter_dataset(
        shows, phish_uuids, wsp_uuids, goose_uuids, billy_uuids, dead_uuids
    )
    song_counts = (
        my_shows.groupby(["artist_prod", "song.name"])["date_prod"]
        .count()
        .reset_index()
        .sort_values(["date_prod", "artist_prod", "song.name"], ascending=False)
        .rename(columns={"date_prod": "times_heard"})
        .head(15)
        .copy()
    )

    top_songs = px.bar(
        data_frame=song_counts,
        x="times_heard",
        y="song.name",
        color="artist_prod",
        color_discrete_map=hf.color_dict,
        category_orders=hf.category_orders,
        text="times_heard",
        labels={"song.name": "", "times_heard": "", "artist_prod": "Artist"},
    )
    top_songs.update_layout(
        yaxis={"categoryorder": "total ascending"},
        legend_orientation="h",
        font={"size": 12},
    )

    top_songs.update_traces(textposition="outside")

    return top_songs


@callback(
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
    prevent_initial_call=False,
)
def update_longest_jams(
    n_clicks, phish_uuids, wsp_uuids, goose_uuids, billy_uuids, dead_uuids
):
    my_shows = hf.filter_dataset(
        shows, phish_uuids, wsp_uuids, goose_uuids, billy_uuids, dead_uuids
    )
    longest_jams = (
        my_shows.sort_values("duration", ascending=False)
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
