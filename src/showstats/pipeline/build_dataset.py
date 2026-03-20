import datetime
import time
import warnings

import awswrangler as wr
import numpy as np
import pandas as pd
import requests

from showstats import utils as hf
from showstats.config import (
    ARTIST_ID_MAPPING,
    ARTIST_MBID_MAPPING,
    ARTIST_S3_KEY_MAPPING,
    ARTIST_SLUGS,
    S3_ARTIST_PARQUET_PREFIX,
    SETLIST_FILTER_KEYWORDS,
    SETLIST_FM_HEADERS,
    WRITE_COLS,
)

warnings.simplefilter(action="ignore", category=FutureWarning)

today_date = datetime.date.today().strftime("%Y-%m-%d")


def get_show_dates(slug_list: list[str]):
    show_dates = []
    for slug in slug_list:
        print(slug)
        url = f"https://api.relisten.net/api/v2/artists/{slug}/years"
        response = requests.get(url)
        years = pd.json_normalize(response.json())
        active_years = years["year"].unique()

        for year in active_years:
            url_years = f"https://api.relisten.net/api/v2/artists/{slug}/years/{year}"
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
    tour_dates["artist"] = tour_dates["artist_id"].map(ARTIST_ID_MAPPING)

    return tour_dates


def get_new_uuids(old_df: str, new_uuids: list[str], append_mode=False):
    old_uuids = set()
    if append_mode:
        df = pd.read_parquet(path=old_df)
        old_uuids = set(df["uuid"])

    return set(new_uuids) - old_uuids


def get_show_songs(uuid_list: list[str]):
    setlist_tracks = []
    keyword_pattern = "|".join(SETLIST_FILTER_KEYWORDS)

    for show_uuid in uuid_list:
        url = f"https://api.relisten.net/api/v3/shows/{show_uuid}"
        response = requests.get(url)
        show_records = pd.json_normalize(data=response.json(), record_path=["sources", "sets", "tracks"])

        show_records["show_uuid"] = show_uuid
        select_cols = ["source_uuid", "show_uuid", "track_position", "duration", "title", "slug", "mp3_url"]

        main_taper_id = show_records["source_uuid"].unique().tolist()[0]
        show = show_records[show_records["source_uuid"] == main_taper_id][select_cols]

        show = show.drop_duplicates(subset=["title"])
        show["title"] = show["title"].str.upper()
        show = show[~show["title"].str.contains(keyword_pattern, regex=True)].copy()

        show["title"] = show["title"].str.replace(r"^\d+\s+", "", regex=True)
        show["title"] = show["title"].str.replace(r"\.WAV|\.FLAC|-|>|<|\[|\]", "", regex=True)
        setlist_tracks.append(show)
        time.sleep(0.25)

    return pd.concat(setlist_tracks)


def _get_sfm_page_count(mbid: str, headers: dict) -> int:
    url = f"https://api.setlist.fm/rest/1.0/artist/{mbid}/setlists?"
    response = requests.get(url, headers=headers)
    data = pd.json_normalize(response.json())
    data["num_pages"] = np.ceil(data["total"] / data["itemsPerPage"])
    return int(data["num_pages"].iloc[0])


def get_setlist_fm(mbid: str, headers: dict):
    num_pages = _get_sfm_page_count(mbid, headers)
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

    setlist_info = []
    for i in range(1, num_pages + 1):
        url = f"https://api.setlist.fm/rest/1.0/artist/{mbid}/setlists?p={i}"
        page = requests.get(url, headers=headers)
        time.sleep(3)
        df = pd.json_normalize(page.json(), record_path=["setlist"])
        df = df[select_cols]
        df["eventDate"] = pd.to_datetime(df["eventDate"], yearfirst=True, format="%d-%m-%Y").astype("str")
        setlist_info.append(df)

    df_out = pd.concat(setlist_info)
    df_out = df_out.rename(columns={"venue.name": "venue_sfm"})
    df_out = df_out.drop_duplicates(subset=["eventDate"]).copy()

    return df_out


def flatten_nested_json_df(df):
    df = df.reset_index()
    s = df.map(lambda x: isinstance(x, list)).all()
    list_columns = s[s].index.tolist()

    s = df.map(lambda x: isinstance(x, dict)).all()
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

        s = df[new_columns].map(lambda x: isinstance(x, list)).all()
        list_columns = s[s].index.tolist()

        s = df[new_columns].map(lambda x: isinstance(x, dict)).all()
        dict_columns = s[s].index.tolist()

    return df


def get_sfm_setlists(mbid: str, headers: dict):
    num_pages = _get_sfm_page_count(mbid, headers)

    setlist_data = []
    for i in range(1, num_pages):
        url = f"https://api.setlist.fm/rest/1.0/artist/{mbid}/setlists?p={i}"
        page = requests.get(url, headers=headers)
        time.sleep(3)
        df = pd.json_normalize(page.json(), record_path=["setlist"])
        df["eventDate"] = pd.to_datetime(df["eventDate"], yearfirst=True, format="%d-%m-%Y").astype("str")
        setlist_data.append(df)

    sfm_pages = pd.concat(setlist_data)
    sfm_pages = sfm_pages[sfm_pages["sets.set"].astype(bool)].reset_index(drop=True).copy()

    select_cols = ["eventDate", "artist.name", "song.name"]
    setlist_return = []
    for _, row in sfm_pages.iterrows():
        sets = pd.json_normalize(row["sets.set"])
        fix_json = flatten_nested_json_df(sets)
        fix_json["artist.name"] = row["artist.name"]
        fix_json["eventDate"] = row["eventDate"]
        fix_json = fix_json[select_cols].dropna(subset=["song.name"]).reset_index(drop=False)
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

    for artist_name, s3_key in ARTIST_S3_KEY_MAPPING.items():
        options = hf.create_show_list(unique_shows, artist_name)
        hf.json_to_s3(options, s3_key)


def create_new_cols_write_df(df: pd.DataFrame):
    df["location_sfm"] = df["venue.city.name"] + ", " + df["venue.city.state"]
    df["venue_location"] = df[["location_sfm", "venue.location"]].bfill(axis=1).iloc[:, 0]
    df["date_prod"] = df[["display_date", "eventDate"]].bfill(axis=1).iloc[:, 0]
    df["venue_name"] = df[["venue_sfm", "venue.name"]].bfill(axis=1).iloc[:, 0]
    df["latitude"] = df[["venue.latitude", "venue.city.coords.lat"]].bfill(axis=1).iloc[:, 0]
    df["longitude"] = df[["venue.longitude", "venue.city.coords.long"]].bfill(axis=1).iloc[:, 0]

    df["year_prod"] = df["date_prod"].str.slice(0, 4)
    df["artist_prod"] = df[["artist", "artist.name"]].bfill(axis=1).iloc[:, 0]

    df["alt_uuid"] = df["artist.name"] + df["eventDate"] + df["venue_location"]
    df[["uuid", "alt_uuid"]] = df.groupby(["date_prod", "artist_prod"])[["uuid", "alt_uuid"]].transform(
        lambda x: x.ffill().bfill()
    )

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

    print("finding all show dates")
    all_show_dates = get_show_dates(slug_list=ARTIST_SLUGS)

    print("finding new uuids to score")
    uuids_to_score = get_new_uuids(old_df=old_show_file, new_uuids=all_show_dates["uuid"].unique().tolist())

    print("finding tracklist associated with songs")
    all_tracks = get_show_songs(uuids_to_score)

    print("joining new show dates to tracks")
    new_show_dates = all_show_dates[all_show_dates["uuid"].isin(uuids_to_score)]
    final_df = new_show_dates.merge(all_tracks, left_on="uuid", right_on="show_uuid", how="left")
    final_df["index"] = final_df.groupby(["artist", "display_date"]).cumcount() + 1

    print("Generating SetlistFM individual show data")
    setlist_fm = pd.concat(
        [get_setlist_fm(mbid=mbid, headers=SETLIST_FM_HEADERS) for mbid in ARTIST_MBID_MAPPING.values()]
    )

    print("Generating setlist fm song data")
    setlist_fm_songs = pd.concat(
        [get_sfm_setlists(mbid=mbid, headers=SETLIST_FM_HEADERS) for mbid in ARTIST_MBID_MAPPING.values()]
    )

    print("Merging setlist fm songs to setlist fm shows")
    sfm_final = setlist_fm.merge(setlist_fm_songs, how="left", on=["eventDate", "artist.name"])

    if append_mode:
        final_df = pd.concat([old_showstats, final_df], axis=0)

    print("Merging and preparing to write final df")
    write_df = final_df.merge(
        sfm_final,
        how="outer",
        left_on=["display_date", "artist", "index"],
        right_on=["eventDate", "artist.name", "index"],
    )

    print("Coalescing venue information")
    write_df = create_new_cols_write_df(write_df)
    write_df = write_df[write_df["date_prod"] < today_date].copy()

    write_dropdown_choices(write_df)

    for artist_name, s3_key in ARTIST_S3_KEY_MAPPING.items():
        artist_df = write_df[write_df["artist_prod"] == artist_name][WRITE_COLS].copy()
        wr.s3.to_parquet(artist_df, path=f"{S3_ARTIST_PARQUET_PREFIX}/{s3_key}.parquet")

    print("Done!!!")


if __name__ == "__main__":
    combine_and_save_dataset(
        old_show_file="",
        append_mode=False,
    )
