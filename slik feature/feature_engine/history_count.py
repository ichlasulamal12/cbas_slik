"""
==============================================================================
Project : CBAS SLIK Feature Engineering
File    : history_count.py
Author  : Ichlasul Amal
Version : 3.0.0
==============================================================================

History Count Feature Engineering

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
# CONFIGURATION
# =============================================================================

WINDOWS = [

    6,

    12,

    24,

]

KOL_CONFIG = [

    ("kol_ge2", lambda c: pl.col(c) >= 2),

    ("kol_ge3", lambda c: pl.col(c) >= 3),

    ("kol5", lambda c: pl.col(c) == 5),

]

DPD_CONFIG = [

    ("dpd30", lambda c: pl.col(c) >= 30),

    ("dpd90", lambda c: pl.col(c) >= 90),

]


# =============================================================================
# GENERIC
# =============================================================================

def create_history_count(
    df: pl.DataFrame,
    columns: list[str],
    config: list,
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

    expressions = []

    for name, condition in config:

        expressions.append(

            pl.sum_horizontal(

                [

                    condition(column)

                    .cast(pl.Int8)

                    for column in cols

                ]

            )

            .alias(

                f"hist{window}_{name}_count"

            )

        )

    return df.with_columns(

        expressions

    )


# =============================================================================
# KOL
# =============================================================================

def create_kol_count(
    df: pl.DataFrame,
):

    for window in WINDOWS:

        df = create_history_count(

            df,

            KOL_COLUMNS,

            KOL_CONFIG,

            window,

        )

    return df


# =============================================================================
# DPD
# =============================================================================

def create_dpd_count(
    df: pl.DataFrame,
):

    for window in WINDOWS:

        df = create_history_count(

            df,

            HT_COLUMNS,

            DPD_CONFIG,

            window,

        )

    return df


# =============================================================================
# MAIN
# =============================================================================

def create_history_count_feature(
    df: pl.DataFrame,
):

    before = df.width

    df = create_kol_count(

        df

    )

    df = create_dpd_count(

        df

    )

    log_feature(

        "History Count Feature",

        before,

        df.width,

    )

    return df
