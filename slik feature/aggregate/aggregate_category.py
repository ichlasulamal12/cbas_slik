"""
==============================================================================
Project : CBAS SLIK Feature Engineering
File    : aggregate_category.py
Author  : Ichlasul Amal
Version : 3.0.0
==============================================================================

Category Aggregate

Aggregate kategori level fasilitas menjadi level debitur.

Output:
- Jumlah kategori unik per debitur.

"""

import polars as pl

from config import DEBTOR_KEY

from utils.logger import get_logger

logger = get_logger(__name__)


# =============================================================================
# CATEGORY COLUMN
# =============================================================================

CATEGORY_COLUMNS = [

    "ljk",

    "jenisKredit",

    "jenisPenggunaan",

    "sektorEkonomi",

]


# =============================================================================
# GET AVAILABLE COLUMN
# =============================================================================

def get_category_columns(
    df: pl.DataFrame,
):

    return [

        column

        for column in CATEGORY_COLUMNS

        if column in df.columns

    ]


# =============================================================================
# BUILD
# =============================================================================

def build_aggregation(
    df: pl.DataFrame,
):

    expressions = []

    category_columns = get_category_columns(

        df

    )

    logger.info(

        "Category Column : %s",

        len(category_columns),

    )

    for column in category_columns:

        expressions.append(

            pl.col(column)

            .n_unique()

            .alias(f"nunique_{column}")

        )

    return expressions


# =============================================================================
# CREATE
# =============================================================================

def create_category_aggregate(
    df: pl.DataFrame,
) -> pl.DataFrame:

    logger.info(

        "Aggregate Category Feature"

    )

    expressions = build_aggregation(

        df

    )

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

        "Category Aggregate : %s rows x %s columns",

        result.height,

        result.width,

    )

    return result
