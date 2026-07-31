"""
==============================================================================
Project : CBAS SLIK Feature Engineering
File    : history_statistics.py
Author  : Ichlasul Amal
Version : 3.0.0
==============================================================================

History Statistics Feature Engineering

Feature Level :
Facility

"""

import polars as pl

from config import (
    KOL_COLUMNS,
    HT_COLUMNS,
)

from feature_engine.feature_helper import (
    get_window_columns,
    has_columns,
    log_feature,
)

# =============================================================================
# CONFIG
# =============================================================================

WINDOWS = [

    6,

    12,

    24,

]

# =============================================================================
# GENERIC
# =============================================================================

def create_history_statistics(
    df: pl.DataFrame,
    columns: list[str],
    prefix: str,
    window: int,
):

    cols = get_window_columns(

        columns,

        window,

    )

    if not has_columns(

        df,

        cols,

    ):

        return df

    return df.with_columns(

        [

            pl.max_horizontal(cols)

            .alias(

                f"hist{window}_{prefix}_max"

            ),

            pl.mean_horizontal(cols)

            .alias(

                f"hist{window}_{prefix}_mean"

            ),

        ]

    )


# =============================================================================
# KOL
# =============================================================================

def create_kol_statistics(
    df: pl.DataFrame,
):

    for window in WINDOWS:

        df = create_history_statistics(

            df,

            KOL_COLUMNS,

            "kol",

            window,

        )

    return df


# =============================================================================
# HT
# =============================================================================

def create_ht_statistics(
    df: pl.DataFrame,
):

    for window in WINDOWS:

        df = create_history_statistics(

            df,

            HT_COLUMNS,

            "ht",

            window,

        )

    return df


# =============================================================================
# MAIN
# =============================================================================

def create_history_statistics_feature(
    df: pl.DataFrame,
):

    before = df.width

    df = create_kol_statistics(

        df

    )

    df = create_ht_statistics(

        df

    )

    log_feature(

        "History Statistics Feature",

        before,

        df.width,

    )

    return df
