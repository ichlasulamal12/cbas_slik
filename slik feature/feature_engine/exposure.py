"""
==============================================================================
Project : CBAS SLIK Feature Engineering
File    : exposure.py
Author  : Ichlasul Amal
Version : 2.0.0
==============================================================================

Exposure Feature Engineering

Feature Level :
Facility

"""

import polars as pl

from feature_engine.feature_helper import (
    has_columns,
    log_feature,
)


# =============================================================================
# UTILIZATION
# =============================================================================

def create_initial_utilization(
    df: pl.DataFrame,
) -> pl.DataFrame:

    required = [

        "bakiDebet",

        "plafonAwal",

    ]

    if not has_columns(df, required):

        return df

    return df.with_columns(

        pl.when(

            pl.col("plafonAwal") > 0

        )

        .then(

            pl.col("bakiDebet")

            /

            pl.col("plafonAwal")

        )

        .otherwise(None)

        .alias("initial_utilization")

    )


# =============================================================================
# UNUSED LIMIT
# =============================================================================

def create_unused_limit(
    df: pl.DataFrame,
) -> pl.DataFrame:

    required = [

        "plafon",

        "bakiDebet",

    ]

    if not has_columns(df, required):

        return df

    return df.with_columns(

        [

            (

                pl.col("plafon")

                -

                pl.col("bakiDebet")

            )

            .alias("unused_limit"),

            pl.when(

                pl.col("plafon") > 0

            )

            .then(

                (

                    pl.col("plafon")

                    -

                    pl.col("bakiDebet")

                )

                /

                pl.col("plafon")

            )

            .otherwise(None)

            .alias("unused_ratio"),

        ]

    )


# =============================================================================
# PLAFOND CHANGE
# =============================================================================

def create_plafond_change(
    df: pl.DataFrame,
) -> pl.DataFrame:

    required = [

        "plafon",

        "plafonAwal",

    ]

    if not has_columns(df, required):

        return df

    return df.with_columns(

        (

            pl.col("plafon")

            -

            pl.col("plafonAwal")

        )

        .alias("plafond_change")

    )


# =============================================================================
# OVERLIMIT
# =============================================================================

def create_overlimit_feature(
    df: pl.DataFrame,
) -> pl.DataFrame:

    required = [

        "bakiDebet",

        "plafon",

    ]

    if not has_columns(df, required):

        return df

    return df.with_columns(

        [

            (

                pl.col("bakiDebet")

                >

                pl.col("plafon")

            )

            .cast(pl.Int8)

            .alias("flag_overlimit"),

            (

                pl.col("bakiDebet")

                -

                pl.col("plafon")

            )

            .clip(lower_bound=0)

            .alias("overlimit_amount"),

        ]

    )


# =============================================================================
# AVAILABLE LIMIT
# =============================================================================

def create_available_limit(
    df: pl.DataFrame,
) -> pl.DataFrame:

    required = [

        "plafon",

        "bakiDebet",

    ]

    if not has_columns(df, required):

        return df

    return df.with_columns(

        (

            pl.col("plafon")

            -

            pl.col("bakiDebet")

        )

        .clip(lower_bound=0)

        .alias("available_limit")

    )


# =============================================================================
# ZERO OS
# =============================================================================

def create_zero_os_flag(
    df: pl.DataFrame,
) -> pl.DataFrame:

    if not has_columns(df, ["bakiDebet"]):

        return df

    return df.with_columns(

        (

            pl.col("bakiDebet")

            ==

            0

        )

        .cast(pl.Int8)

        .alias("flag_zero_os")

    )


# =============================================================================
# FULL DRAWDOWN
# =============================================================================

def create_full_drawdown_flag(
    df: pl.DataFrame,
) -> pl.DataFrame:

    required = [

        "bakiDebet",

        "plafon",

    ]

    if not has_columns(df, required):

        return df

    return df.with_columns(

        (

            pl.col("bakiDebet")

            >=

            pl.col("plafon")

        )

        .cast(pl.Int8)

        .alias("flag_full_drawdown")

    )


# =============================================================================
# MAIN
# =============================================================================

def create_exposure_feature(
    df: pl.DataFrame,
) -> pl.DataFrame:

    before = df.width

    functions = [

        create_initial_utilization,

        create_unused_limit,

        create_plafond_change,

        create_overlimit_feature,

        create_available_limit,

        create_zero_os_flag,

        create_full_drawdown_flag,

    ]

    for function in functions:

        df = function(df)

    log_feature(

        "Exposure Feature",

        before,

        df.width,

    )

    return df
