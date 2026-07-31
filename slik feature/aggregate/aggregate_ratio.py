"""
==============================================================================
Project : CBAS SLIK Feature Engineering
File    : aggregate_ratio.py
Author  : Ichlasul Amal
Version : 2.0.0
==============================================================================

Ratio Aggregate

Aggregate seluruh ratio feature dari level fasilitas
menjadi level debitur.

"""

import polars as pl

from config import DEBTOR_KEY

from utils.logger import get_logger

logger = get_logger(__name__)


# =============================================================================
# RATIO COLUMN
# =============================================================================

def get_ratio_columns(
    df: pl.DataFrame,
):

    return sorted(

        [

            column

            for column in df.columns

            if column.startswith("ratio_")

        ]

    )


# =============================================================================
# BUILD
# =============================================================================

def build_aggregation(
    df: pl.DataFrame,
):

    expressions = []

    ratio_columns = get_ratio_columns(df)

    logger.info(

        "Ratio Column : %s",

        len(ratio_columns),

    )

    for column in ratio_columns:

        expressions.extend(

            [

                pl.col(column)
                .mean()
                .alias(f"mean_{column}"),

                pl.col(column)
                .max()
                .alias(f"max_{column}"),

                pl.col(column)
                .min()
                .alias(f"min_{column}"),

                pl.col(column)
                .median()
                .alias(f"median_{column}"),

                pl.col(column)
                .std()
                .alias(f"std_{column}"),

            ]

        )

    return expressions


# =============================================================================
# CREATE
# =============================================================================

def create_ratio_aggregate(
    df: pl.DataFrame,
) -> pl.DataFrame:

    logger.info(

        "Aggregate Ratio Feature"

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

        "Ratio Aggregate : %s rows x %s columns",

        result.height,

        result.width,

    )

    return result
