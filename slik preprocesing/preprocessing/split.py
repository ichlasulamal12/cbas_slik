"""
==============================================================================
Project : CBAS SLIK Preprocessing
File    : preprocessing/split.py
Author  : Ichlasul Amal
Version : 2.0.0
==============================================================================

Dataset Split
"""

import polars as pl

from config import (
    IDLIMIT_COLUMN,
    DATE_COLUMN,
    SNAPSHOT_DATE_COLUMN,
)

from utils.date_utils import (
    development_end_date,
    oot_start_date,
)


# =============================================================================
# SNAPSHOT SELECTION
# =============================================================================

def select_snapshot(
    df: pl.DataFrame,
) -> pl.DataFrame:
    """
    Select the latest available snapshot
    before or equal to application date.
    """

    if df.height == 0:

        return df

    return (

        df

        .filter(

            pl.col(SNAPSHOT_DATE_COLUMN)

            <=

            pl.col(DATE_COLUMN)

        )

        .sort(

            [

                IDLIMIT_COLUMN,

                SNAPSHOT_DATE_COLUMN,

            ],

            descending=[

                False,

                True,

            ],

        )

        .unique(

            subset=[IDLIMIT_COLUMN],

            keep="first",

        )

    )


# =============================================================================
# DEVELOPMENT
# =============================================================================

def development_dataset(
    df: pl.DataFrame,
) -> pl.DataFrame:
    """
    Development dataset.
    """

    return df.filter(

        pl.col(DATE_COLUMN)

        <=

        development_end_date()

    )


# =============================================================================
# OOT
# =============================================================================

def oot_dataset(
    df: pl.DataFrame,
) -> pl.DataFrame:
    """
    Out-of-Time dataset.
    """

    return df.filter(

        pl.col(DATE_COLUMN)

        >=

        oot_start_date()

    )


# =============================================================================
# PROCESS
# =============================================================================

def split_dataset(
    df: pl.DataFrame,
) -> tuple[
    pl.DataFrame,
    pl.DataFrame,
]:
    """
    Complete split process.
    """

    df = select_snapshot(
        df,
    )

    development = development_dataset(
        df,
    )

    oot = oot_dataset(
        df,
    )

    return (

        development,

        oot,

    )
