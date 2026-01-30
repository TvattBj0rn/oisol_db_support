import pathlib

import polars as pl

OISOL_HOME_PATH = pathlib.Path('/') / 'oisol'

POLARS_TYPES_FROM_STRING = {
    'String': pl.String,
    'Boolean': pl.Boolean,
    'Integer': pl.Int64,
    'Float': pl.Float64,
}
