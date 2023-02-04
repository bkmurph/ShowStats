#######################################
#               Imports               #
#######################################

import dash
import dash_bootstrap_components as dbc
import helper_functions as hf
import pandas as pd
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output, State

#######################################
#            Read in data             #
#######################################
my_shows = pd.read_parquet(
    path="/Users/brandonmurphy/projects/show_stats/ShowStats/data/showstats.parquet"
)

my_shows = my_shows.reset_index(drop=True)

#######################################
#            Initialize App           #
#######################################
app = dash.Dash(
    external_stylesheets=[dbc.themes.SKETCHY],
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,",
        }
    ],
)

# Header Components
h1 = html.H1("Show Stats", style={"backgroundColor": "#99999A"})
h3_ = html.H3("Select Artist(s)", style={"paddingRight": "30px"})
# h3_2 = html.H3("Select Start and End Dates")


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
button = html.Button(
    id="submit_button",
    n_clicks=0,
    children="Submit",
    style={"fontSize": 24, "marginLeft": "30px"},
)


##############################################
# What is my (measurable) show count by year #
##############################################

line_plot = dcc.Graph(id="line_chart", className="h-100")

#######################################
# What Songs Have I Seen the Most?    #
#######################################

song_count = dcc.Graph(
    id="songs_bar",  # style={"display": "inline-block", "width": "85%"}
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
longest_jams_bar = dbc.Table(id="test_table")

##########################
# Map Out Show Locations #
##########################

map_shows = dcc.Graph(
    id="concert_map",
)


count_card = dbc.Card(
    [
        dbc.CardHeader(html.H2("Show Count Over The Years")),
        dbc.CardBody(html.Div([line_plot])),
    ]
)

unique_card = dbc.Card(
    [
        dbc.CardHeader(html.H2("Unique Songs Seen By Artist")),
        dbc.CardBody(html.Div([unique_graph])),
    ],
    # style={"height": "80vh", "width": "80vw"},
)

longest_jams_card = dbc.Card(
    [
        dbc.CardHeader(html.H2("What are the longest jams you've seen?")),
        dbc.CardBody(html.Div([longest_jams_bar])),
    ]
)
top_songs_card = dbc.Card(
    [
        dbc.CardHeader(html.H2("What songs have you seen played most?")),
        dbc.CardBody(html.Div([song_count])),
    ]
)

map_shows_card = dbc.Card(
    [
        dbc.CardHeader(html.H2("Locations of Shows You've Been To")),
        dbc.CardBody(html.Div([map_shows])),
    ]
)

accordion = html.Div(
    dbc.Accordion(
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
)


#######################################
# Combine All Components Defined Above #
#######################################

app.layout = html.Div(
    [
        html.Div(
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            html.A(
                                # href="https://relisten.net/",
                                children=[
                                    html.Img(
                                        src="/assets/fauget.png", height=175, width=499
                                    )
                                ],
                            )
                        ),
                        width={"size": 4},
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
                        width={"size": 1, "offset": 5},
                    ),
                    dbc.Col(
                        html.A(
                            href="https://relisten.net/",
                            children=[
                                html.Img(src="assets/relisten.png", height=90, width=90)
                            ],
                        ),
                        width={"size": 1},
                    ),
                    dbc.Col(
                        html.Div(
                            html.Img(src="/assets/coffee.png", height=90, width=90)
                        ),
                        width={"size": 1},
                    ),
                ],
                align="center",
                style={"backgroundColor": "#333F42"},
                className="g-0",
            )
        ),
        html.Div(html.Br()),
        dbc.Row(
            [
                dbc.Col(h3_, width={"size": 4, "offset": 1}),
            ]
        ),
        dbc.Row([dbc.Col(accordion, width={"size": 9, "offset": 1}), dbc.Col(button)]),
        html.Div(html.Br()),
        dbc.Row(
            [
                dbc.Col(count_card, width={"size": 6, "offset": 0}),
                dbc.Col(unique_card, width={"size": 6, "offset": 0}),
            ],
            className="g-0",
        ),
        html.Div(html.Br()),
        dbc.Row(dbc.Col(longest_jams_card, width={"size": 10, "offset": 1})),
        html.Div(html.Br()),
        dbc.Row(dbc.Col(top_songs_card, width={"size": 10, "offset": 1})),
        html.Div(html.Br()),
        dbc.Row(dbc.Col(map_shows_card, width={"size": 10, "offset": 1})),
    ]
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
    unique_bar.update_layout(showlegend=False)
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
    map_data = map_data[~map_data["venue.latitude"].isna()].reset_index().copy()

    show_map = px.scatter_mapbox(
        data_frame=map_data,
        lat="venue.latitude",
        lon="venue.longitude",
        hover_name="artist",
        hover_data=["venue.name", "venue.location", "display_date", "duration_hms"],
        color="artist",
        color_discrete_map=hf.color_dict,
        category_orders=hf.category_orders,
        zoom=3,
        height=450,
        opacity=0.6,
        size_max=90,
        labels={
            "venue.name": "Venue",
            "venue.location": "Location",
            "venue.latitude": "Latitude",
            "venue.longitude": "Longitude",
            "artist": "Artist",
            "display_date": "Date",
            "duration_hms": "Show Time",
        },
    )
    show_map.update_traces(marker={"size": 12})
    show_map.update_layout(mapbox_style="open-street-map")  # carto-darkmatter
    # show_map.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0})

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
    top_songs.update_layout(yaxis={"categoryorder": "total ascending"})
    top_songs.update_traces(textposition="outside")
    # top_songs.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 10})

    return top_songs


@app.callback(
    Output("test_table", "children"),
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
        .assign(city=my_shows["venue.location"].str.split(pat=",", n=1).str[0])
        .head(20)
    )
    longest_jams["title_year_city"] = (
        longest_jams["title"]
        + " - "
        + longest_jams["city"]
        + ", "
        + longest_jams["year.year"]
    )
    longest_jams = longest_jams[
        [
            "artist",
            "venue.location",
            "title",
            "duration_hms",
            "display_date",
            "track_position",
        ]
    ]
    table = dbc.Table.from_dataframe(
        longest_jams, hover=True, color="dark", size="lg", bordered=True
    )

    return table


#######################################
#           Run this thing            #
#######################################

if __name__ == "__main__":
    app.run_server()
