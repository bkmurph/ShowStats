import json
import warnings

import boto3
import pandas as pd

from showstats.config import ARTIST_ID_MAPPING, ARTIST_SLUGS, S3_BUCKET, SETLIST_FM_HEADERS, WRITE_COLS

warnings.simplefilter(action="ignore", category=FutureWarning)

s3 = boto3.client("s3")


def json_to_s3(json_file, artist: str):
    s3.put_object(Body=json.dumps(json_file), Bucket=S3_BUCKET, Key=f"{artist}_uuids.json")


def get_s3_object(artist: str):
    content_object = s3.get_object(Bucket=S3_BUCKET, Key=artist + "_uuids.json")["Body"].read().decode("utf-8")
    return json.loads(content_object)


def convert_seconds_to_hms(df, column):
    df["duration_hms"] = df[column].astype("datetime64[s]").dt.strftime("%H:%M:%S")
    return df


def filter_dataset(df, phish_uuids, wsp_uuids, goose_uuids, billy_uuids, dead_uuids):
    uuids = phish_uuids + wsp_uuids + goose_uuids + billy_uuids + dead_uuids
    return df[df["uuid"].isin(uuids)].copy()


def create_show_list(df: pd.DataFrame, artist_name: str):
    show_list = []
    df_new = df[(df["artist"] == artist_name) | (df["artist.name"] == artist_name)].reset_index(drop=True).copy()

    for i in range(len(df_new)):
        date = df_new.loc[i, "date_prod"]
        location = df_new.loc[i, "venue_location"]
        uuid = df_new.loc[i, "uuid"]
        show_list.append({"label": f"{date} / {location}", "value": uuid})
    return show_list


color_dict = {
    "Phish": "#00205B",
    "Widespread Panic": "#00843D",
    "Goose": "#E1F6F4",
    "Grateful Dead": "#A8DDA8",
    "Billy Strings": "#779ecb",
}

category_orders = {"artist": ["Billy Strings", "Goose", "Grateful Dead", "Phish", "Widespread Panic"]}

# Re-exported for modules that import these from utils
headers = SETLIST_FM_HEADERS
slugs = ARTIST_SLUGS
artist_id_mapping = ARTIST_ID_MAPPING
write_cols = WRITE_COLS