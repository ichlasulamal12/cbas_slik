"""
==============================================================================
Project : CBAS SLIK Feature Engineering
File    : interest.py
Author  : Ichlasul Amal
Version : 2.0.0
==============================================================================

Interest Feature Engineering

Feature Level :
Facility

"""

import polars as pl

from feature_engine.feature_helper import (
    has_columns,
    log_feature,
)


# =============================================================================
# INTEREST RATE
# =============================================================================

def create_interest_rate(
    df: pl.DataFrame,
) -> pl.DataFrame:

    if not has_columns(
        df,
        [
            "sukuBunga",
        ],
    ):
        return df

    return df.with_columns(

        pl.col("sukuBunga")

        .cast(pl.Float64)

        .alias("interest_rate")

    )


# =============================================================================
# INTEREST FLAG
# =============================================================================

def create_interest_flag(
    df: pl.DataFrame,
) -> pl.DataFrame:

    if not has_columns(
        df,
        [
            "interest_rate",
        ],
    ):
        return df

    return df.with_columns(

        [

            (

                pl.col("interest_rate") >= 10

            )

            .cast(pl.Int8)

            .alias("flag_interest_10"),

            (

                pl.col("interest_rate") >= 15

            )

            .cast(pl.Int8)

            .alias("flag_interest_15"),

            (

                pl.col("interest_rate") >= 20

            )

            .cast(pl.Int8)

            .alias("flag_interest_20"),

            (

                pl.col("interest_rate") < 5

            )

            .cast(pl.Int8)

            .alias("flag_interest_low"),

        ]

    )


# =============================================================================
# INTEREST TYPE
# =============================================================================

def create_interest_type(
    df: pl.DataFrame,
) -> pl.DataFrame:

    if not has_columns(
        df,
        [
            "jenisSukuBunga",
        ],
    ):
        return df

    interest_type = (

        pl.col("jenisSukuBunga")

        .cast(
            pl.Utf8,
            strict=False,
        )

        .str.strip_chars()

    )

    return df.with_columns(

        [

            (

                interest_type

                ==

                "1"

            )

            .cast(pl.Int8)

            .alias("flag_fixed_rate"),

            (

                interest_type

                ==

                "2"

            )

            .cast(pl.Int8)

            .alias("flag_floating_rate"),

        ]

    )


# =============================================================================
# INTEREST BUCKET
# =============================================================================

def create_interest_bucket(
    df: pl.DataFrame,
) -> pl.DataFrame:

    if not has_columns(
        df,
        [
            "interest_rate",
        ],
    ):
        return df

    return df.with_columns(

        pl.when(

            pl.col("interest_rate") < 5

        )

        .then(

            pl.lit("<5")

        )

        .when(

            pl.col("interest_rate") < 10

        )

        .then(

            pl.lit("5-10")

        )

        .when(

            pl.col("interest_rate") < 15

        )

        .then(

            pl.lit("10-15")

        )

        .when(

            pl.col("interest_rate") < 20

        )

        .then(

            pl.lit("15-20")

        )

        .otherwise(

            pl.lit(">=20")

        )

        .alias("interest_bucket")

    )


# =============================================================================
# INTEREST QUALITY
# =============================================================================

def create_interest_quality(
    df: pl.DataFrame,
) -> pl.DataFrame:

    if not has_columns(
        df,
        [
            "interest_rate",
        ],
    ):
        return df

    return df.with_columns(

        [

            (

                pl.col("interest_rate") == 0

            )

            .cast(pl.Int8)

            .alias("flag_zero_interest"),

            (

                pl.col("interest_rate") < 0

            )

            .cast(pl.Int8)

            .alias("flag_negative_interest"),

        ]

    )


# =============================================================================
# MAIN
# =============================================================================

def create_interest_feature(
    df: pl.DataFrame,
) -> pl.DataFrame:

    before = df.width

    functions = [

        create_interest_rate,

        create_interest_flag,

        create_interest_type,

        create_interest_bucket,

        create_interest_quality,

    ]

    for function in functions:

        df = function(df)

    log_feature(

        "Interest Feature",

        before,

        df.width,

    )

    return df
