import datetime
import time
import warnings

import awswrangler as wr
import numpy as np
import pandas as pd
import requests

import helper_functions as hf

warnings.simplefilter(action="ignore", category=FutureWarning)

today_date = datetime.date.today().strftime("%Y-%m-%d")

slugs = [
    "grateful-dead",
    "phish",
    "billy-strings",
    "goose",
    "wsp",
]

headers = {
    "Accept": "application/json",
    "x-api-key": "Obo7MA1IRsf4nb4mSpOYuei5L6viXmLzYd8E",
}

artist_id_mapping = {
    5: "Widespread Panic",
    4: "Phish",
    259: "Goose",
    202: "Billy Strings",
    9: "Grateful Dead",
}

write_cols = [
    "uuid",
    "display_date",
    "year.year",
    "artist",
    "title",
    "duration",
    "avg_duration",
    "latitude",
    "longitude",
    "venue_location",
    "venue_name",
    "eventDate",
    "artist.name",
    "song.name",
    "date_prod",
    "year_prod",
    "artist_prod",
]


def get_show_dates(slug_list: list[str]):
    show_dates = []
    for slug in slug_list:
        print(slug)
        # Find the years that a band has been active (based on relisten.net reference)
        url = f"https://relistenapi.alecgorge.com/api/v2/artists/{slug}/years"
        response = requests.get(url)
        years = pd.json_normalize(response.json())
        active_years = years["year"].unique()

        # Find the dates of shows within each of the years returned from above
        for year in active_years:
            url_years = (
                f"https://relistenapi.alecgorge.com/api/v2/artists/{slug}/years/{year}"
            )
            response = requests.get(url_years)
            years = pd.json_normalize(response.json(), record_path=["shows"])
            show_dates.append(years)

    select_cols = [
        "artist_id",
        "venue_id",
        "tour_id",
        "uuid",
        "id",
        "date",
        "avg_rating",
        "avg_duration",
        "display_date",
        "venue.shows_at_venue",
        "venue.latitude",
        "venue.longitude",
        "venue.name",
        "venue.location",
        "venue.slug",
        "venue.past_names",
        "venue.id",
        "year.year",
    ]
    tour_dates = pd.concat(show_dates).drop_duplicates()
    tour_dates = tour_dates[select_cols]
    tour_dates["artist"] = tour_dates["artist_id"].map(artist_id_mapping)

    return tour_dates


def get_uuid_list(show_date_df: pd.DataFrame):
    uuid_list = show_date_df["uuid"].unique().tolist()
    return uuid_list


def get_new_uuids(old_df: str, new_uuids: list[str], append_mode=False):
    if append_mode:
        df = pd.read_parquet(path=old_df)
        old_uuids = set(df["uuid"])

    current_uuids = set(new_uuids)
    old_uuids = set()

    # Explanation: set A - set B is equal to the elements present in A but notB
    uuids_to_score = current_uuids - old_uuids

    return uuids_to_score


def get_show_songs(uuid_list=list[str]):
    setlist_tracks = []
    for show_uuid in uuid_list:
        # Make API call, and flatten dataframe
        url = f"https://relistenapi.alecgorge.com/api/v3/shows/{show_uuid}"
        response = requests.get(url)
        show_json = response.json()
        show_records = pd.json_normalize(
            data=show_json, record_path=["sources", "sets", "tracks"]
        )

        # Select Columns, only take 1st recording of a given show
        show_records["show_uuid"] = show_uuid
        select_cols = [
            "source_uuid",
            "show_uuid",
            "track_position",
            "duration",
            "title",
            "slug",
            "mp3_url",
        ]
        main_taper_id = show_records["source_uuid"].unique().tolist()[0]
        show = show_records[show_records["source_uuid"] == main_taper_id][select_cols]

        # Drop duplicates, push song titles to uppercase, filter out songs that arent actually songs
        show = show.drop_duplicates(subset=["title"])
        show["title"] = show["title"].str.upper()
        keywords = [
            "BANTER",
            "TUNING",
            "INTRO",
            "GREETING",
            "GREET",
            "GREETS",
            "THANK" "ENCORE",
            "OUTRO",
            "HAPPY BIRTHDAY",
            "PA RECORDING",
            "HOUSE PA",
            "THANKS",
        ]
        show = show[~show["title"].str.contains("|".join(keywords), regex=False)].copy()
        show = show[show["title"] != "CROWD"].copy()

        # Clean up song titles (remove special characters, remove file formats (.wav, .flac))
        show["title"] = show["title"].str.replace("^\d+\s+", "", regex=True)
        show["title"] = show["title"].str.replace(
            ".WAV|.FLAC|-|>|<|[|]", "", regex=True
        )
        setlist_tracks.append(show)

    setlist_final = pd.concat(setlist_tracks)

    return setlist_final


def get_setlist_fm(mbid=list[str], headers=dict()):
    base_url = f"https://api.setlist.fm/rest/1.0/artist/{mbid}/setlists?"
    request = requests.get(base_url, headers=headers)
    find_num_pages = pd.json_normalize(request.json())
    find_num_pages["num_pages"] = np.ceil(
        find_num_pages["total"] / find_num_pages["itemsPerPage"]
    )
    num_pages = np.int64(find_num_pages.iloc[:, 5][0])

    setlist_info = []

    for i in range(1, num_pages + 1):
        url = f"https://api.setlist.fm/rest/1.0/artist/{mbid}/setlists?p={i}"
        page = requests.get(url, headers=headers)
        time.sleep(3)
        df = pd.json_normalize(page.json(), record_path=["setlist"])
        select_cols = [
            "eventDate",
            "artist.name",
            "venue.name",
            "venue.city.name",
            "venue.city.state",
            "venue.city.coords.lat",
            "venue.city.coords.long",
            "venue.city.country.name",
        ]

        df = df[select_cols]
        df["eventDate"] = pd.to_datetime(
            df["eventDate"], yearfirst=True, format="%d-%m-%Y"
        ).astype("str")
        setlist_info.append(df)

        print(df["eventDate"])

    df_out = pd.concat(setlist_info)
    df_out = df_out.rename(columns={"venue.name": "venue_sfm"})
    df_out = df_out.drop_duplicates(subset=["eventDate"]).copy()

    return df_out


def flatten_nested_json_df(df):
    df = df.reset_index()
    s = (df.applymap(type) == list).all()
    list_columns = s[s].index.tolist()

    s = (df.applymap(type) == dict).all()
    dict_columns = s[s].index.tolist()

    while len(list_columns) > 0 or len(dict_columns) > 0:
        new_columns = []

        for col in dict_columns:
            horiz_exploded = pd.json_normalize(df[col]).add_prefix(f"{col}.")
            horiz_exploded.index = df.index
            df = pd.concat([df, horiz_exploded], axis=1).drop(columns=[col])
            new_columns.extend(horiz_exploded.columns)

        for col in list_columns:
            df = df.drop(columns=[col]).join(df[col].explode().to_frame())
            df = df.reset_index(drop=True)
            new_columns.append(col)

        s = (df[new_columns].applymap(type) == list).all()
        list_columns = s[s].index.tolist()

        s = (df[new_columns].applymap(type) == dict).all()
        dict_columns = s[s].index.tolist()

    return df


def get_sfm_setlists(mbid: str, headers=dict()):
    # Download Setlist Data from the setlist.fm site

    base_url = f"https://api.setlist.fm/rest/1.0/artist/{mbid}/setlists?"
    request = requests.get(base_url, headers=headers)
    find_num_pages = pd.json_normalize(request.json())
    find_num_pages["num_pages"] = np.ceil(
        find_num_pages["total"] / find_num_pages["itemsPerPage"]
    )
    num_pages = np.int64(find_num_pages.iloc[:, 5][0])

    setlist_data = []

    for i in range(1, num_pages):
        url = f"https://api.setlist.fm/rest/1.0/artist/{mbid}/setlists?p={i}"
        page = requests.get(url, headers=headers)
        time.sleep(3)
        df = pd.json_normalize(page.json(), record_path=["setlist"])
        df["eventDate"] = pd.to_datetime(
            df["eventDate"], yearfirst=True, format="%d-%m-%Y"
        ).astype("str")
        setlist_data.append(df)

    sfm_pages = pd.concat(setlist_data)
    sfm_pages["bool"] = sfm_pages["sets.set"].astype(bool)
    sfm_pages = sfm_pages[sfm_pages["bool"]].reset_index(drop=True).copy()

    setlist_return = []
    select_cols = ["eventDate", "artist.name", "song.name"]
    for i in range(0, len(sfm_pages)):
        artist = sfm_pages.loc[i, "artist.name"]
        date = sfm_pages.loc[i, "eventDate"]
        sets = pd.json_normalize(sfm_pages["sets.set"].iloc[i])
        fix_json = flatten_nested_json_df(sets)
        fix_json["artist.name"] = artist
        fix_json["eventDate"] = date
        fix_json = (
            fix_json[select_cols].dropna(subset=["song.name"]).reset_index(drop=False)
        )
        fix_json["index"] = fix_json["index"] + 1

        setlist_return.append(fix_json)

    return_df = pd.concat(setlist_return)
    return_df["song.name"] = return_df["song.name"].str.upper()
    return_df["year_sfm"] = return_df["eventDate"].str.slice(0, 4)

    return return_df


def write_dropdown_choices(df: pd.DataFrame):
    unique_shows = (
        df.dropna(subset=["song.name"])
        .drop_duplicates(subset=["uuid"])
        .sort_values("date_prod", ascending=False)
        .reset_index(drop=True)
        .copy()
    )

    phish_options = hf.create_show_list(unique_shows, "Phish")
    hf.json_to_s3(phish_options, "phish")
    panic_options = hf.create_show_list(unique_shows, "Widespread Panic")
    hf.json_to_s3(panic_options, "wsp")
    goose_options = hf.create_show_list(unique_shows, "Goose")
    hf.json_to_s3(goose_options, "goose")
    gd_options = hf.create_show_list(unique_shows, "Grateful Dead")
    hf.json_to_s3(gd_options, "dead")
    billy_options = hf.create_show_list(unique_shows, "Billy Strings")
    hf.json_to_s3(billy_options, "billy")


def create_new_cols_write_df(df: pd.DataFrame):
    df["location_sfm"] = df["venue.city.name"] + ", " + df["venue.city.state"]
    df["venue_location"] = (
        df[["location_sfm", "venue.location"]].bfill(axis=1).iloc[:, 0]
    )
    df["date_prod"] = df[["display_date", "eventDate"]].bfill(axis=1).iloc[:, 0]
    df["venue_name"] = df[["venue_sfm", "venue.name"]].bfill(axis=1).iloc[:, 0]
    df["latitude"] = (
        df[["venue.latitude", "venue.city.coords.lat"]].bfill(axis=1).iloc[:, 0]
    )
    df["longitude"] = (
        df[["venue.longitude", "venue.city.coords.long"]].bfill(axis=1).iloc[:, 0]
    )

    df["year_prod"] = df["date_prod"].str.slice(0, 4)
    df["artist_prod"] = df[["artist", "artist.name"]].bfill(axis=1).iloc[:, 0]

    df["alt_uuid"] = df["artist.name"] + df["eventDate"] + df["venue_location"]
    df[["uuid", "alt_uuid"]] = df.groupby(["date_prod", "artist_prod"])[
        ["uuid", "alt_uuid"]
    ].transform(lambda x: x.ffill().bfill())

    df["uuid"] = df[["uuid", "alt_uuid"]].bfill(axis=1).iloc[:, 0].copy()
    df = df.drop(columns=["alt_uuid"]).copy()

    return df


def combine_and_save_dataset(old_show_file: str, append_mode=False):
    if append_mode:
        print("reading old data")
        old_showstats = pd.read_parquet(path=old_show_file)
        old_showstats = old_showstats.drop(
            columns=[
                "eventDate",
                "artist.name",
                "venue.city.name",
                "venue.city.state",
                "venue.city.coords.lat",
                "venue.city.coords.long",
                "venue.city.country.name",
                "venue_sfm",
            ]
        )
    else:
        None

    print("finding all show dates")
    all_show_dates = get_show_dates(slug_list=slugs)

    print("getting uuid list")
    all_uuids = get_uuid_list(show_date_df=all_show_dates)

    print("finding new uuids to score")
    uuids_to_score = get_new_uuids(
        old_df=old_show_file,
        new_uuids=all_uuids,
    )

    print("finding tracklist associated with songs")
    all_tracks = get_show_songs(uuids_to_score)

    print("filtering all tracks df to only new songs")
    new_show_dates = all_show_dates[all_show_dates["uuid"].isin(uuids_to_score)]

    print("joining new_show_dates to all tracks")
    final_df = new_show_dates.merge(
        all_tracks, left_on="uuid", right_on="show_uuid", how="left"
    )

    final_df["index"] = final_df.groupby(["artist", "display_date"]).cumcount() + 1

    final_df.to_parquet(
        path="/Users/brandonmurphy/projects/show_stats/ShowStats/data/intermediate_relisten.parquet"
    )

    final_df = pd.read_parquet(
        "/Users/brandonmurphy/projects/show_stats/ShowStats/data/intermediate_relisten.parquet"
    )

    print("Generating SetlistFM indivdual show data")
    billy = get_setlist_fm(mbid="640db492-34c4-47df-be14-96e2cd4b9fe4", headers=headers)
    goose = get_setlist_fm(mbid="b925a474-d245-4217-bc13-2e153d82bebb", headers=headers)
    dead = get_setlist_fm(mbid="6faa7ca7-0d99-4a5e-bfa6-1fd5037520c6", headers=headers)
    wsp = get_setlist_fm(mbid="3797a6d0-7700-44bf-96fb-f44386bc9ab2", headers=headers)
    phish = get_setlist_fm(mbid="e01646f2-2a04-450d-8bf2-0d993082e058", headers=headers)

    setlist_fm = pd.concat([billy, goose, dead, wsp, phish], axis=0)
    setlist_fm.to_parquet(
        path="/Users/brandonmurphy/projects/show_stats/ShowStats/data/sfm_individual_shows.parquet"
    )

    setlist_fm = pd.read_parquet(
        "/Users/brandonmurphy/projects/show_stats/ShowStats/data/sfm_individual_shows.parquet"
    )

    print("Generating setlist fm song data")
    billy_sfm = get_sfm_setlists(
        mbid="640db492-34c4-47df-be14-96e2cd4b9fe4", headers=headers
    )
    goose_sfm = get_sfm_setlists(
        mbid="b925a474-d245-4217-bc13-2e153d82bebb", headers=headers
    )
    dead_sfm = get_sfm_setlists(
        mbid="6faa7ca7-0d99-4a5e-bfa6-1fd5037520c6", headers=headers
    )
    wsp_sfm = get_sfm_setlists(
        mbid="3797a6d0-7700-44bf-96fb-f44386bc9ab2", headers=headers
    )
    phish_sfm = get_sfm_setlists(
        mbid="e01646f2-2a04-450d-8bf2-0d993082e058", headers=headers
    )
    setlist_fm_songs = pd.concat([billy_sfm, goose_sfm, dead_sfm, wsp_sfm, phish_sfm])
    setlist_fm_songs.to_parquet(
        path="/Users/brandonmurphy/projects/show_stats/ShowStats/data/sfm_setlists.parquet"
    )

    setlist_fm_songs = pd.read_parquet(
        "/Users/brandonmurphy/projects/show_stats/ShowStats/data/sfm_setlists.parquet"
    )

    print("Merging setlist fm songs to setlist fm shows")
    sfm_final = setlist_fm.merge(
        setlist_fm_songs, how="left", on=["eventDate", "artist.name"]
    )

    if append_mode:
        final_df = pd.concat([old_showstats, final_df], axis=0)
    else:
        None

    print("Merging and preparing to write final df")
    write_df = final_df.merge(
        sfm_final,
        how="outer",
        left_on=["display_date", "artist", "index"],
        right_on=["eventDate", "artist.name", "index"],
    )

    write_df.to_parquet(
        "/Users/brandonmurphy/projects/show_stats/ShowStats/data/temp_delete.parquet"
    )

    print("Coalescing venue information")
    write_df = create_new_cols_write_df(write_df)

    write_df = write_df[write_df["date_prod"] < today_date].copy()

    write_dropdown_choices(write_df)

    wr.s3.to_parquet(
        write_df[write_cols], path="s3://showstats1/showstats_update_new.parquet"
    )

    print("Done!!!")


if __name__ == "__main__":
    combine_and_save_dataset(
        old_show_file="",
        append_mode=False,
    )
