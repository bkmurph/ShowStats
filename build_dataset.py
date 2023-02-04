import warnings

import pandas as pd
import requests

warnings.simplefilter(action="ignore", category=FutureWarning)

slugs = [
    "grateful-dead",
    "phish",
    "billy-strings",
    "goose",
    "wsp",
]

artist_id_mapping = {
    5: "Widespread Panic",
    4: "Phish",
    259: "Goose",
    202: "Billy Strings",
    9: "Grateful Dead",
}


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


def get_new_uuids(old_df: str, new_uuids: list[str]):

    df = pd.read_parquet(path=old_df)
    old_uuids = set(df["uuid"])

    current_uuids = set(new_uuids)

    # Explanation: set A - set B is equal to the elements present in A but notB
    uuids_to_score = current_uuids - old_uuids

    return uuids_to_score


# Need to handle:
# Songs that get sandwiched
# Mispelled song titles
# Stuff like "jam", or "tuning"
# Missing venue information


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
            "JAM",
            "BANTER",
            "TUNING",
            "INTRO",
            "GREETING",
        ]
        show = show[~show["title"].str.contains("|".join(keywords))]

        # Clean up song titles (remove special characters, remove file formats (.wav, .flac))
        show["title"] = show["title"].str.replace("^\d+\s+", "", regex=True)
        show["title"] = show["title"].str.replace(
            ".WAV|.FLAC|-|>|<|[|]", "", regex=True
        )
        setlist_tracks.append(show)

    setlist_final = pd.concat(setlist_tracks)

    return setlist_final


def combine_and_save_dataset(old_show_file: str):
    print("reading old data")
    old_showstats = pd.read_parquet(path=old_show_file)

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

    print("joining new_show_dates to ")
    final_df = new_show_dates.merge(
        all_tracks, left_on="uuid", right_on="show_uuid", how="left"
    )

    write_df = pd.concat([old_showstats, final_df], axis=0)

    write_df.to_parquet(
        path="/Users/brandonmurphy/projects/show_stats/ShowStats/data/showstats.parquet"
    )


if __name__ == "__main__":
    combine_and_save_dataset(
        old_show_file="/Users/brandonmurphy/projects/show_stats/ShowStats/data/wsp_phish_goose_test_df.parquet"
    )
