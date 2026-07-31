"""
==============================================================================
Project : CBAS SLIK Feature Engineering
File    : utilization.py
Author  : Ichlasul Amal
Version : 2.0.0
==============================================================================

Utilization Feature Engineering

Feature Level :
Facility

"""

import polars as pl

from feature_engine.feature_helper import (
    has_columns,
    log_feature,
)


# =============================================================================
# CONFIGURATION
# =============================================================================

UTILIZATION_THRESHOLDS = [

    (0.00, "flag_utilized"),

    (0.50, "flag_util50"),

    (0.70, "flag_util70"),

    (0.80, "flag_util80"),

    (0.90, "flag_util90"),

    (1.00, "flag_util100"),

    (1.10, "flag_util110"),

]


# =============================================================================
# UTILIZATION FLAG
# =============================================================================

def create_utilization_flag(
    df: pl.DataFrame,
) -> pl.DataFrame:

    if not has_columns(
        df,
        [
            "utilization",
        ],
    ):
        return df

    expressions = []

    for threshold, feature in UTILIZATION_THRESHOLDS:

        if threshold == 0:

            expr = (

                pl.col("utilization") > 0

            )

        else:

            expr = (

                pl.col("utilization") >= threshold

            )

        expressions.append(

            expr

            .cast(pl.Int8)

            .alias(feature)

        )

    return df.with_columns(

        expressions

    )


# =============================================================================
# UTILIZATION BUCKET
# =============================================================================

def create_utilization_bucket(
    df: pl.DataFrame,
) -> pl.DataFrame:

    if not has_columns(
        df,
        [
            "utilization",
        ],
    ):
        return df

    return df.with_columns(

        pl.when(

            pl.col("utilization") <= 0

        )

        .then(

            pl.lit("0%")

        )

        .when(

            pl.col("utilization") < 0.50

        )

        .then(

            pl.lit("0-50%")

        )

        .when(

            pl.col("utilization") < 0.70

        )

        .then(

            pl.lit("50-70%")

        )

        .when(

            pl.col("utilization") < 0.80

        )

        .then(

            pl.lit("70-80%")

        )

        .when(

            pl.col("utilization") < 0.90

        )

        .then(

            pl.lit("80-90%")

        )

        .when(

            pl.col("utilization") <= 1.00

        )

        .then(

            pl.lit("90-100%")

        )

        .otherwise(

            pl.lit(">100%")

        )

        .alias("utilization_bucket")

    )


# =============================================================================
# UTILIZATION QUALITY
# =============================================================================

def create_utilization_quality(
    df: pl.DataFrame,
) -> pl.DataFrame:

    if not has_columns(
        df,
        [
            "utilization",
        ],
    ):
        return df

    return df.with_columns(

        [

            (

                pl.col("utilization") < 0

            )

            .cast(pl.Int8)

            .alias("flag_negative_utilization"),

            (

                pl.col("utilization") > 1

            )

            .cast(pl.Int8)

            .alias("flag_over_utilization"),

            (

                pl.col("utilization") == 0

            )

            .cast(pl.Int8)

            .alias("flag_zero_utilization"),

        ]

    )


# =============================================================================
# MAIN
# =============================================================================

def create_utilization_feature(
    df: pl.DataFrame,
) -> pl.DataFrame:

    before = df.width

    functions = [

        create_utilization_flag,

        create_utilization_bucket,

        create_utilization_quality,

    ]

    for function in functions:

        df = function(df)

    log_feature(

        "Utilization Feature",

        before,

        df.width,

    )

    return df
