"""
==============================================================================
Project : CBAS SLIK Feature Engineering
File    : aggregate_numeric.py
Author  : Ichlasul Amal
Version : 3.0.0
==============================================================================

Numeric Aggregate

Aggregate numeric feature level fasilitas menjadi level debitur.

"""

import polars as pl

from config import (
    DEBTOR_KEY,
    AGGREGATE_SUM_COLUMNS,
    AGGREGATE_MAX_COLUMNS,
)

from utils.logger import get_logger

logger = get_logger(__name__)


# =============================================================================
# BUILD
# =============================================================================

def build_aggregation(
    df: pl.DataFrame,
):

    expressions = []

    sum_columns = [

        column

        for column in AGGREGATE_SUM_COLUMNS

        if column in df.columns

    ]

    max_columns = [

        column

        for column in AGGREGATE_MAX_COLUMNS

        if column in df.columns

    ]

    logger.info(

        "Aggregate Sum Column : %s",

        len(sum_columns),

    )

    logger.info(

        "Aggregate Max Column : %s",

        len(max_columns),

    )

    for column in sum_columns:

        expressions.append(

            pl.col(column)

            .sum()

            .alias(f"sum_{column}")

        )

    for column in max_columns:

        expressions.append(

            pl.col(column)

            .max()

            .alias(f"max_{column}")

        )

    return expressions


# =============================================================================
# CREATE
# =============================================================================

def create_numeric_aggregate(
    df: pl.DataFrame,
) -> pl.DataFrame:

    logger.info(

        "Aggregate Numeric Feature"

    )

    result = (

        df

        .group_by(

            DEBTOR_KEY

        )

        .agg(

            build_aggregation(

                df

            )

        )

        .sort(

            DEBTOR_KEY

        )

    )

    logger.info(

        "Numeric Aggregate : %s rows x %s columns",

        result.height,

        result.width,

    )

    return result
