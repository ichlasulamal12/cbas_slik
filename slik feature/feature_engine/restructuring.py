"""
==============================================================================
Project : CBAS SLIK Feature Engineering
File    : restructuring.py
Author  : Ichlasul Amal
Version : 2.0.0
==============================================================================

Restructuring Feature Engineering

Feature Level :
Facility

"""

from datetime import date

import polars as pl

from feature_engine.feature_helper import (
    has_columns,
    log_feature,
)

TODAY = date.today()


# =============================================================================
# RESTRUCTURE COUNT
# =============================================================================

def create_restructure_count(
    df: pl.DataFrame,
) -> pl.DataFrame:

    if not has_columns(
        df,
        [
            "frekuensiRestrukturisasi",
        ],
    ):
        return df

    return df.with_columns(

        pl.col("frekuensiRestrukturisasi")

        .fill_null(0)

        .cast(pl.Int32)

        .alias("restrukturisasi_count")

    )


# =============================================================================
# RESTRUCTURE FLAG
# =============================================================================

def create_restructure_flag(
    df: pl.DataFrame,
) -> pl.DataFrame:

    if not has_columns(
        df,
        [
            "restrukturisasi_count",
        ],
    ):
        return df

    return df.with_columns(

        [

            (

                pl.col("restrukturisasi_count")

                >= 2

            )

            .cast(pl.Int8)

            .alias("flag_multiple_restruktur"),

            (

                pl.col("restrukturisasi_count")

                >= 3

            )

            .cast(pl.Int8)

            .alias("flag_heavy_restruktur"),

        ]

    )


# =============================================================================
# RESTRUCTURE METHOD
# =============================================================================

def create_restructure_method(
    df: pl.DataFrame,
) -> pl.DataFrame:

    if not has_columns(
        df,
        [
            "kodeCaraRestrukturisasi",
        ],
    ):
        return df

    return df.with_columns(

        pl.col("kodeCaraRestrukturisasi")

        .is_not_null()

        .cast(pl.Int8)

        .alias("flag_restruktur_method")

    )


# =============================================================================
# DAYS SINCE RESTRUCTURE
# =============================================================================

def create_days_since_restructure(
    df: pl.DataFrame,
) -> pl.DataFrame:

    if not has_columns(
        df,
        [
            "tanggalRestrukturisasiAkhir",
        ],
    ):
        return df

    return df.with_columns(

        (

            pl.lit(TODAY)

            -

            pl.col("tanggalRestrukturisasiAkhir")

        )

        .dt.total_days()

        .alias("days_since_restruktur")

    )


# =============================================================================
# RECENCY FLAG
# =============================================================================

def create_restructure_recency(
    df: pl.DataFrame,
) -> pl.DataFrame:

    if not has_columns(
        df,
        [
            "days_since_restruktur",
        ],
    ):
        return df

    return df.with_columns(

        [

            (

                pl.col("days_since_restruktur")

                <= 180

            )

            .cast(pl.Int8)

            .alias("flag_restruktur_6m"),

            (

                pl.col("days_since_restruktur")

                <= 365

            )

            .cast(pl.Int8)

            .alias("flag_restruktur_12m"),

            (

                pl.col("days_since_restruktur")

                <= 730

            )

            .cast(pl.Int8)

            .alias("flag_restruktur_24m"),

        ]

    )


# =============================================================================
# RESTRUCTURE SCORE
# =============================================================================

def create_restructure_score(
    df: pl.DataFrame,
) -> pl.DataFrame:

    required = [

        "restrukturisasi_count",

        "flag_dpd90",

        "flag_kol3",

    ]

    if not has_columns(
        df,
        required,
    ):
        return df

    return df.with_columns(

        [

            (

                pl.col("restrukturisasi_count")

                +

                pl.col("flag_dpd90")

            )

            .alias("restruktur_dpd_score"),

            (

                pl.col("restrukturisasi_count")

                +

                pl.col("flag_kol3")

            )

            .alias("restruktur_kol_score"),

        ]

    )


# =============================================================================
# MAIN
# =============================================================================

def create_restructuring_feature(
    df: pl.DataFrame,
) -> pl.DataFrame:

    before = df.width

    functions = [

        create_restructure_count,

        create_restructure_flag,

        create_restructure_method,

        create_days_since_restructure,

        create_restructure_recency,

        create_restructure_score,

    ]

    for function in functions:

        df = function(df)

    log_feature(

        "Restructuring Feature",

        before,

        df.width,

    )

    return df
