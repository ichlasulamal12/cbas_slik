"""
==============================================================================
Project : CBAS SLIK Feature Engineering
File    : tenor.py
Author  : Ichlasul Amal
Version : 2.0.0
==============================================================================

Tenor Feature Engineering

Feature Level :
Facility

"""

import polars as pl

from feature_engine.feature_helper import (
    has_columns,
    log_feature,
)


# =============================================================================
# TENOR UTILIZATION
# =============================================================================

def create_tenor_utilization(
    df: pl.DataFrame,
) -> pl.DataFrame:

    required = [

        "credit_age_days",

        "original_tenor_days",

    ]

    if not has_columns(df, required):

        return df

    return df.with_columns(

        pl.when(

            pl.col("original_tenor_days") > 0

        )

        .then(

            pl.col("credit_age_days")

            /

            pl.col("original_tenor_days")

        )

        .otherwise(None)

        .alias("tenor_utilization")

    )


# =============================================================================
# NEW CREDIT FLAG
# =============================================================================

def create_new_credit_flag(
    df: pl.DataFrame,
) -> pl.DataFrame:

    if not has_columns(

        df,

        [

            "credit_age_days",

        ],

    ):

        return df

    return df.with_columns(

        [

            (

                pl.col("credit_age_days")

                <= 180

            )

            .cast(pl.Int8)

            .alias("flag_new_credit_6m"),

            (

                pl.col("credit_age_days")

                <= 365

            )

            .cast(pl.Int8)

            .alias("flag_new_credit_12m"),

        ]

    )


# =============================================================================
# MATURITY FLAG
# =============================================================================

def create_maturity_flag(
    df: pl.DataFrame,
) -> pl.DataFrame:

    if not has_columns(

        df,

        [

            "remaining_tenor_days",

        ],

    ):

        return df

    return df.with_columns(

        [

            (

                pl.col("remaining_tenor_days")

                <= 180

            )

            .cast(pl.Int8)

            .alias("flag_maturity_6m"),

            (

                pl.col("remaining_tenor_days")

                <= 365

            )

            .cast(pl.Int8)

            .alias("flag_maturity_12m"),

            (

                pl.col("remaining_tenor_days")

                <= 0

            )

            .cast(pl.Int8)

            .alias("flag_matured"),

        ]

    )


# =============================================================================
# TENOR BUCKET
# =============================================================================

def create_tenor_bucket(
    df: pl.DataFrame,
) -> pl.DataFrame:

    if not has_columns(

        df,

        [

            "remaining_tenor_days",

        ],

    ):

        return df

    return df.with_columns(

        pl.when(

            pl.col("remaining_tenor_days") <= 180

        )

        .then(

            pl.lit("<=6M")

        )

        .when(

            pl.col("remaining_tenor_days") <= 365

        )

        .then(

            pl.lit("6-12M")

        )

        .when(

            pl.col("remaining_tenor_days") <= 730

        )

        .then(

            pl.lit("1-2Y")

        )

        .when(

            pl.col("remaining_tenor_days") <= 1825

        )

        .then(

            pl.lit("2-5Y")

        )

        .otherwise(

            pl.lit(">5Y")

        )

        .alias("tenor_bucket")

    )


# =============================================================================
# TENOR QUALITY
# =============================================================================

def create_tenor_quality(
    df: pl.DataFrame,
) -> pl.DataFrame:

    required = [

        "credit_age_days",

        "remaining_tenor_days",

    ]

    if not has_columns(df, required):

        return df

    return df.with_columns(

        [

            (

                pl.col("credit_age_days")

                >

                pl.col("remaining_tenor_days")

            )

            .cast(pl.Int8)

            .alias("flag_credit_age_gt_remaining"),

            (

                pl.col("remaining_tenor_days")

                <

                0

            )

            .cast(pl.Int8)

            .alias("flag_negative_remaining"),

        ]

    )


# =============================================================================
# MAIN
# =============================================================================

def create_tenor_feature(
    df: pl.DataFrame,
) -> pl.DataFrame:

    before = df.width

    functions = [

        create_tenor_utilization,

        create_new_credit_flag,

        create_maturity_flag,

        create_tenor_bucket,

        create_tenor_quality,

    ]

    for function in functions:

        df = function(df)

    log_feature(

        "Tenor Feature",

        before,

        df.width,

    )

    return df
