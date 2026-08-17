import os

import polars as pl

from dotenv import load_dotenv

load_dotenv()
OISOL_HOME_PATH = os.getenv('OISOL_HOME_PATH')

POLARS_TYPES_FROM_STRING = {
    'String': pl.String,
    'Boolean': pl.Boolean,
    'Integer': pl.Int64,
    'Float': pl.Float64,
}
