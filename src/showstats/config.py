import os

# --- API credentials (from environment) ---
SETLIST_FM_API_KEY = os.environ.get("SETLIST_FM_API_KEY", "")
SETLIST_FM_HEADERS = {"Accept": "application/json", "x-api-key": SETLIST_FM_API_KEY}

# --- AWS ---
S3_BUCKET = os.environ.get("SHOWSTATS_S3_BUCKET", "showstats1")
S3_ARTIST_PARQUET_PREFIX = f"s3://{S3_BUCKET}"

# --- Artist config ---
ARTIST_SLUGS = ["grateful-dead", "phish", "billy-strings", "goose", "wsp"]

ARTIST_ID_MAPPING = {
    5: "Widespread Panic",
    4: "Phish",
    259: "Goose",
    202: "Billy Strings",
    9: "Grateful Dead",
}

# Setlist.fm Music Brainz IDs
ARTIST_MBID_MAPPING = {
    "Billy Strings": "640db492-34c4-47df-be14-96e2cd4b9fe4",
    "Goose": "b925a474-d245-4217-bc13-2e153d82bebb",
    "Grateful Dead": "6faa7ca7-0d99-4a5e-bfa6-1fd5037520c6",
    "Widespread Panic": "3797a6d0-7700-44bf-96fb-f44386bc9ab2",
    "Phish": "e01646f2-2a04-450d-8bf2-0d993082e058",
}

# Maps artist display name -> S3 dropdown key
ARTIST_S3_KEY_MAPPING = {
    "Phish": "phish",
    "Widespread Panic": "wsp",
    "Goose": "goose",
    "Grateful Dead": "dead",
    "Billy Strings": "billy",
}

# Song title keywords to filter out (not real songs)
SETLIST_FILTER_KEYWORDS = [
    "BANTER",
    "TUNING",
    "INTRO",
    "GREETING",
    "GREET",
    "GREETS",
    "THANKENCORE",
    "OUTRO",
    "HAPPY BIRTHDAY",
    "PA RECORDING",
    "HOUSE PA",
    "THANKS",
    "CROWD",
]

# Output columns written to S3
WRITE_COLS = [
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