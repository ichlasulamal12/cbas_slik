"""
==============================================================================
Project : CBAS SLIK Feature Engineering
File    : delinquency.py
Author  : Ichlasul Amal
Version : 2.0.0
==============================================================================

Current Delinquency Feature Engineering

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

DPD_THRESHOLDS = [

    (0, "flag_dpd"),

    (30, "flag_dpd30"),

    (60, "flag_dpd60"),

    (90, "flag_dpd90"),

    (120, "flag_dpd120"),

    (180, "flag_dpd180"),

]

KOL_THRESHOLDS = [

    (1, "flag_kol1"),

    (2, "flag_kol2"),

    (3, "flag_kol3"),

    (4, "flag_kol4"),

    (5, "flag_kol5"),

]


# =============================================================================
# CURRENT KOL FLAG
# =============================================================================

def create_kol_flag(
    df: pl.DataFrame,
) -> pl.DataFrame:

    if not has_columns(
        df,
        [
            "kolektibilitas",
        ],
    ):

        return df

    expressions = []

    for threshold, feature in KOL_THRESHOLDS:

        expressions.append(

            (

                pl.col("kolektibilitas")

                >=

                threshold

            )

            .cast(pl.Int8)

            .alias(feature)

        )

    return df.with_columns(

        expressions

    )


# =============================================================================
# CURRENT DPD FLAG
# =============================================================================

def create_dpd_flag(
    df: pl.DataFrame,
) -> pl.DataFrame:

    if not has_columns(
        df,
        [
            "jumlahHariTunggakan",
        ],
    ):

        return df

    expressions = []

    for threshold, feature in DPD_THRESHOLDS:

        operator = (

            pl.col("jumlahHariTunggakan") > threshold

            if threshold == 0

            else

            pl.col("jumlahHariTunggakan") >= threshold

        )

        expressions.append(

            operator

            .cast(pl.Int8)

            .alias(feature)

        )

    return df.with_columns(

        expressions

    )


# =============================================================================
# KOL BUCKET
# =============================================================================

def create_kol_bucket(
    df: pl.DataFrame,
) -> pl.DataFrame:

    if not has_columns(
        df,
        [
            "kolektibilitas",
        ],
    ):

        return df

    return df.with_columns(

        pl.when(

            pl.col("kolektibilitas") == 1

        )

        .then(

            pl.lit("KOL1")

        )

        .when(

            pl.col("kolektibilitas") == 2

        )

        .then(

            pl.lit("KOL2")

        )

        .when(

            pl.col("kolektibilitas") == 3

        )

        .then(

            pl.lit("KOL3")

        )

        .when(

            pl.col("kolektibilitas") == 4

        )

        .then(

            pl.lit("KOL4")

        )

        .when(

            pl.col("kolektibilitas") >= 5

        )

        .then(

            pl.lit("KOL5")

        )

        .otherwise(

            None

        )

        .alias("kol_bucket")

    )


# =============================================================================
# DPD BUCKET
# =============================================================================

def create_dpd_bucket(
    df: pl.DataFrame,
) -> pl.DataFrame:

    if not has_columns(
        df,
        [
            "jumlahHariTunggakan",
        ],
    ):

        return df

    return df.with_columns(

        pl.when(

            pl.col("jumlahHariTunggakan") == 0

        )

        .then(

            pl.lit("0")

        )

        .when(

            pl.col("jumlahHariTunggakan") < 30

        )

        .then(

            pl.lit("1-29")

        )

        .when(

            pl.col("jumlahHariTunggakan") < 60

        )

        .then(

            pl.lit("30-59")

        )

        .when(

            pl.col("jumlahHariTunggakan") < 90

        )

        .then(

            pl.lit("60-89")

        )

        .when(

            pl.col("jumlahHariTunggakan") < 120

        )

        .then(

            pl.lit("90-119")

        )

        .when(

            pl.col("jumlahHariTunggakan") < 180

        )

        .then(

            pl.lit("120-179")

        )

        .otherwise(

            pl.lit("180+")

        )

        .alias("dpd_bucket")

    )


# =============================================================================
# DELINQUENCY SEVERITY
# =============================================================================

def create_delinquency_severity(
    df: pl.DataFrame,
) -> pl.DataFrame:

    if not has_columns(
        df,
        [
            "kolektibilitas",
            "jumlahHariTunggakan",
        ],
    ):

        return df

    return df.with_columns(

        (

            pl.col("kolektibilitas")

            *

            pl.col("jumlahHariTunggakan")

        )

        .alias("delinquency_severity")

    )


# =============================================================================
# OVERDUE
# =============================================================================

def create_overdue_feature(
    df: pl.DataFrame,
) -> pl.DataFrame:

    required = [

        "tunggakanPokok",

        "tunggakanBunga",

        "denda",

        "bakiDebet",

    ]

    if not has_columns(
        df,
        required,
    ):

        return df

    return df.with_columns(

        [

            (

                pl.col("tunggakanPokok")

                +

                pl.col("tunggakanBunga")

                +

                pl.col("denda")

            )

            .alias("total_overdue"),

            (

                (

                    pl.col("tunggakanPokok")

                    +

                    pl.col("tunggakanBunga")

                    +

                    pl.col("denda")

                )

                /

                pl.col("bakiDebet")

            )

            .alias("overdue_ratio"),

            (

                (

                    pl.col("tunggakanPokok")

                    +

                    pl.col("tunggakanBunga")

                    +

                    pl.col("denda")

                )

                >

                0

            )

            .cast(pl.Int8)

            .alias("flag_overdue"),

        ]

    )


# =============================================================================
# MAIN
# =============================================================================

def create_delinquency_feature(
    df: pl.DataFrame,
) -> pl.DataFrame:

    before = df.width

    functions = [

        create_kol_flag,

        create_dpd_flag,

        create_kol_bucket,

        create_dpd_bucket,

        create_delinquency_severity,

        create_overdue_feature,

    ]

    for function in functions:

        df = function(df)

    log_feature(

        "Delinquency Feature",

        before,

        df.width,

    )

    return df
