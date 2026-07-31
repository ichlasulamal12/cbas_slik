"""
==============================================================================
Project : CBAS SLIK Feature Engineering
File    : history_streak.py
Author  : Ichlasul Amal
Version : 2.0.0
==============================================================================

History Streak Feature Engineering

Feature Level :
Facility

"""

import polars as pl

from config import (
    KOL_COLUMNS,
    HT_COLUMNS,
    HISTORY_WINDOWS,
)

from feature_engine.feature_helper import (
    get_window_columns,
    has_columns,
    log_feature,
)

# =============================================================================
# CONFIGURATION
# =============================================================================

KOL_STREAK = [

    ("kol_ge2", lambda c: pl.col(c) >= 2),

    ("kol_ge3", lambda c: pl.col(c) >= 3),

    ("kol_ge4", lambda c: pl.col(c) >= 4),

    ("kol5", lambda c: pl.col(c) >= 5),

]

DPD_STREAK = [

    ("dpd", lambda c: pl.col(c) > 0),

    ("dpd30", lambda c: pl.col(c) >= 30),

    ("dpd60", lambda c: pl.col(c) >= 60),

    ("dpd90", lambda c: pl.col(c) >= 90),

    ("dpd120", lambda c: pl.col(c) >= 120),

    ("dpd180", lambda c: pl.col(c) >= 180),

]

# =============================================================================
# GENERIC
# =============================================================================

def create_history_streak(
    df: pl.DataFrame,
    columns: list,
    configs: list,
    window: int,
):

    cols = get_window_columns(
        columns,
        window,
    )

    if not has_columns(df, cols):

        return df

    expressions = []

    for feature, condition in configs:

        expr = pl.lit(0)

        # mulai dari bulan terbaru
        for column in reversed(cols):

            expr = (

                pl.when(condition(column))

                .then(expr + 1)

                .otherwise(0)

            )

        expressions.append(

            expr.alias(

                f"hist{window}_{feature}_streak"

            )

        )

    return df.with_columns(

        expressions

    )

# =============================================================================
# KOL
# =============================================================================

def create_kol_streak(
    df: pl.DataFrame,
):

    for window in HISTORY_WINDOWS:

        df = create_history_streak(

            df,

            KOL_COLUMNS,

            KOL_STREAK,

            window,

        )

    return df

# =============================================================================
# DPD
# =============================================================================

def create_dpd_streak(
    df: pl.DataFrame,
):

    for window in HISTORY_WINDOWS:

        df = create_history_streak(

            df,

            HT_COLUMNS,

            DPD_STREAK,

            window,

        )

    return df

# =============================================================================
# MAIN
# =============================================================================

def create_history_streak_feature(
    df: pl.DataFrame,
):

    before = df.width

    df = create_kol_streak(df)

    df = create_dpd_streak(df)

    log_feature(

        "History Streak Feature",

        before,

        df.width,

    )

    return df
