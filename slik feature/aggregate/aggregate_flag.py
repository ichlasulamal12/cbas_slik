"""
==============================================================================
Project : CBAS SLIK Feature Engineering
File    : aggregate_flag.py
Author  : Ichlasul Amal
Version : 2.0.0
==============================================================================

Flag Aggregate

Aggregate seluruh flag level fasilitas menjadi level debitur.

"""

import polars as pl

from config import DEBTOR_KEY
from config import FLAG_COLUMNS

from utils.logger import get_logger

logger = get_logger(__name__)


# =============================================================================
# FLAG COLUMN
# =============================================================================

def get_flag_columns(df):

    return [

        c

        for c in FLAG_COLUMNS

        if c in df.columns

    ]


# =============================================================================
# BUILD
# =============================================================================

def build_aggregation(
    df: pl.DataFrame,
):

    expressions = []

    flag_columns = get_flag_columns(df)

    logger.info(

        "Flag Column : %s",

        len(flag_columns),

    )

    for column in flag_columns:

        expressions.extend(

            [

                # minimal satu fasilitas memiliki flag

                pl.col(column)

                .max()

                .alias(column),

                # jumlah fasilitas yang memiliki flag

                pl.col(column)

                .sum()

                .alias(f"{column}_count"),

            ]

        )

    return expressions


# =============================================================================
# CREATE
# =============================================================================

def create_flag_aggregate(
    df: pl.DataFrame,
) -> pl.DataFrame:

    logger.info(

        "Aggregate Flag Feature"

    )

    expressions = build_aggregation(df)

    result = (

        df

        .group_by(

            DEBTOR_KEY

        )

        .agg(

            expressions

        )

        .sort(

            DEBTOR_KEY

        )

    )

    logger.info(

        "Flag Aggregate : %s rows x %s columns",

        result.height,

        result.width,

    )

    return result
