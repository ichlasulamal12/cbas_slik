"""
==============================================================================
Project : CBAS SLIK Feature Engineering
File    : aggregate_history.py
Author  : Ichlasul Amal
Version : 2.0.0
==============================================================================

History Aggregate

Aggregate seluruh history feature dari level fasilitas
menjadi level debitur.

"""

import polars as pl

from config import DEBTOR_KEY

from utils.logger import get_logger

logger = get_logger(__name__)


# =============================================================================
# HISTORY COLUMN
# =============================================================================

def get_history_columns(
    df: pl.DataFrame,
):

    return sorted(

        [

            column

            for column in df.columns

            if column.startswith("hist")

        ]

    )


# =============================================================================
# BUILD
# =============================================================================

def build_aggregation(
    df: pl.DataFrame,
):

    expressions = []

    history_columns = get_history_columns(df)

    logger.info(

        "History Column : %s",

        len(history_columns),

    )

    for column in history_columns:

        expressions.extend(

            [

                pl.col(column)
                .mean()
                .alias(f"{column}_mean"),

                pl.col(column)
                .max()
                .alias(f"{column}_max"),

                pl.col(column)
                .min()
                .alias(f"{column}_min"),

                pl.col(column)
                .std()
                .alias(f"{column}_std"),

                pl.col(column)
                .sum()
                .alias(f"{column}_sum"),

            ]

        )

    return expressions


# =============================================================================
# CREATE
# =============================================================================

def create_history_aggregate(
    df: pl.DataFrame,
) -> pl.DataFrame:

    logger.info(

        "Aggregate History Feature"

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

        "History Aggregate : %s rows x %s columns",

        result.height,

        result.width,

    )

    return result
