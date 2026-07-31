"""
==============================================================================
Project : CBAS SLIK Feature Engineering
File    : aggregate_basic.py
Author  : Ichlasul Amal
Version : 2.0.0
==============================================================================

Basic Aggregate

Output :
One row per debtor

"""

import polars as pl

from config import DEBTOR_KEY

from utils.logger import get_logger

logger = get_logger(__name__)


# =============================================================================
# BASIC COLUMNS
# =============================================================================

FIRST_COLUMNS = [

    "ktp",

    "npwp",

    "namaDebitur",

]

# =============================================================================
# BUILD AGGREGATION
# =============================================================================

def build_aggregation(
    df: pl.DataFrame,
):

    expressions = []

    # -------------------------------------------------------------------------
    # Facility Count
    # -------------------------------------------------------------------------

    expressions.append(

        pl.len()

        .alias("facility_count")

    )

    # -------------------------------------------------------------------------
    # First Value
    # -------------------------------------------------------------------------

    for column in FIRST_COLUMNS:

        if column not in df.columns:

            continue

        expressions.append(

            pl.col(column)

            .first()

            .alias(column)

        )

    return expressions


# =============================================================================
# CREATE BASIC AGGREGATE
# =============================================================================

def create_basic_aggregate(
    df: pl.DataFrame,
) -> pl.DataFrame:

    logger.info(

        "Aggregate Basic Feature"

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

        "Basic Aggregate : %s rows x %s columns",

        result.height,

        result.width,

    )

    return result
