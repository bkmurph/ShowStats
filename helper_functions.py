import datetime
import json
import warnings

import numpy as np
import pandas as pd
import requests

warnings.simplefilter(action="ignore", category=FutureWarning)


def convert_seconds_to_hms(df, column):
    df["duration_hms"] = df[column].astype("datetime64[s]").dt.strftime("%H:%M:%S")
    return df


def create_show_list(df: pd.DataFrame, artist_name: str):
    show_list = []
    df_new = df[df["artist"] == artist_name].reset_index(drop=True).copy()

    for i in range(len(df_new)):
        venue = df_new.loc[i, "venue.name"]
        date = df_new.loc[i, "display_date"]
        location = df_new.loc[i, "venue.location"]
        uuid = df_new.loc[i, "uuid"]

        show_list.append({"label": f"{date} / {location} / {venue}", "value": uuid})
    return show_list


color_dict = {
    "Phish": "#00205B",
    "Widespread Panic": "#00843D",
    "Goose": "#ED7766",
    "Grateful Dead": "#45BCE5",
    "Billy Strings": "#00C39C",
}

category_orders = {
    "artist": ["Billy Strings", "Goose", "Grateful Dead", "Phish", "Widespread Panic"]
}

panic_starter_uuids = [
    "1ef462cc-7647-878f-78b0-4a7f635b5c52",
    "8caf7ca3-21e9-d1e6-4ad3-760a2565e2b3",
    "f7f33882-abc8-314f-5cad-33811c74525e",
    "ff62abb3-8327-93df-5db5-d02a682b375b",
    "715e7c96-0def-9781-9bae-0b1a53510b62",
    "d599090e-1d55-8e9a-8557-113bc3fd3353",
    "8a890c21-2732-cbbe-a596-8d8958485e27",
    "cd37e7c4-1c5a-b17f-30ea-515189dd876e",
    "5cee6580-4d79-8cdd-1f0a-30b7fcca66aa",
    "fb84061b-5564-3f6a-b6f5-ee0ffeecbb55",
    "0be926ad-7264-faa4-b9d4-807d2532f495",
]

phish_starter_uuids = [
    "11005e2a-46b7-288a-d0fb-5281e6730f51",
    "e588f4ea-be66-3924-419e-3085fff17a4e",
    "72507b40-4b02-fc82-109a-b919566976f4",
    "4a5d66c7-1c9b-6eda-e198-1bd3f4cdcfd6",
    "13367854-2d61-402d-4e35-ac76af4042cd",
    "b8b481fd-bc0d-f9ac-7202-5e4185a163ec",
    "df8da48f-7c7c-0273-ea9d-9b7bc877c6d1",
    "821f67a4-2a5c-85e5-6fdd-4503b6cf7bbc",
]

goose_starter_uuids = [
    "41a9fa41-de1c-dc50-1a78-73350ad1766b",
    "0484ba95-27d1-314e-4ab6-9923ca3105a3",
    "b8a97c8d-8850-6f9b-6b6a-792b067c8c10",
    "2acafa23-1821-e5dd-f2b8-a680c73a92db",
]
