"""
==============================================================================
Project : CBAS SLIK Feature Engineering
File    : basic.py
Author  : Ichlasul Amal
Version : 2.0.0
==============================================================================

Basic Feature Engineering

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
# UTILIZATION
# =============================================================================

def create_utilization(df: pl.DataFrame) -> pl.DataFrame:

    feature = "Utilization"

    if not has_columns(
        df,
        [
            "bakiDebet",
            "plafon",
        ],
    ):
        return df

    before = df.width

    df = df.with_columns(

        pl.when(pl.col("plafon") > 0)

        .then(

            pl.col("bakiDebet")

            /

            pl.col("plafon")

        )

        .otherwise(None)

        .alias("utilization")

    )

    log_feature(
        feature,
        before,
        df.width,
    )

    return df


# =============================================================================
# CREDIT AGE
# =============================================================================

def create_credit_age(df: pl.DataFrame) -> pl.DataFrame:

    feature = "Credit Age"

    if not has_columns(
        df,
        [
            "tanggalAwalKredit",
        ],
    ):
        return df

    before = df.width

    df = df.with_columns(

        (

            pl.lit(TODAY)

            -

            pl.col("tanggalAwalKredit")

        )

        .dt.total_days()

        .alias("umur_kredit")

    )

    log_feature(
        feature,
        before,
        df.width,
    )

    return df


# =============================================================================
# REMAINING TENOR
# =============================================================================

def create_remaining_tenor(df: pl.DataFrame) -> pl.DataFrame:

    feature = "Remaining Tenor"

    if not has_columns(
        df,
        [
            "tanggalJatuhTempo",
        ],
    ):
        return df

    before = df.width

    df = df.with_columns(

        (

            pl.col("tanggalJatuhTempo")

            -

            pl.lit(TODAY)

        )

        .dt.total_days()

        .alias("sisa_tenor")

    )

    log_feature(
        feature,
        before,
        df.width,
    )

    return df


# =============================================================================
# RESTRUCTURE FLAG
# =============================================================================

def create_restructure_flag(df: pl.DataFrame) -> pl.DataFrame:

    feature = "Restructure Flag"

    if not has_columns(
        df,
        [
            "frekuensiRestrukturisasi",
        ],
    ):
        return df

    before = df.width

    df = df.with_columns(

        (

            pl.col("frekuensiRestrukturisasi")

            .fill_null(0)

            >

            0

        )

        .cast(pl.Int8)

        .alias("flag_restruktur")

    )

    log_feature(
        feature,
        before,
        df.width,
    )

    return df


# =============================================================================
# DEFAULT FLAG
# =============================================================================

def create_default_flag(df: pl.DataFrame) -> pl.DataFrame:

    feature = "Default Flag"

    if not has_columns(
        df,
        [
            "kodeSebabMacet",
        ],
    ):
        return df

    before = df.width

    df = df.with_columns(

        pl.col("kodeSebabMacet")

        .is_not_null()

        .cast(pl.Int8)

        .alias("flag_macet")

    )

    log_feature(
        feature,
        before,
        df.width,
    )

    return df


# =============================================================================
# CURRENT KOL FLAG
# =============================================================================

def create_current_kol_flag(df: pl.DataFrame) -> pl.DataFrame:

    feature = "Current KOL Flag"

    if not has_columns(
        df,
        [
            "kolektibilitas",
        ],
    ):
        return df

    before = df.width

    df = df.with_columns(

        [

            (pl.col("kolektibilitas") >= 2)

            .cast(pl.Int8)

            .alias("flag_kol2"),

            (pl.col("kolektibilitas") >= 3)

            .cast(pl.Int8)

            .alias("flag_kol3"),

            (pl.col("kolektibilitas") >= 4)

            .cast(pl.Int8)

            .alias("flag_kol4"),

            (pl.col("kolektibilitas") >= 5)

            .cast(pl.Int8)

            .alias("flag_kol5"),

        ]

    )

    log_feature(
        feature,
        before,
        df.width,
    )

    return df


# =============================================================================
# CURRENT DPD FLAG
# =============================================================================

def create_current_dpd_flag(df: pl.DataFrame) -> pl.DataFrame:

    feature = "Current DPD Flag"

    if not has_columns(
        df,
        [
            "jumlahHariTunggakan",
        ],
    ):
        return df

    before = df.width

    df = df.with_columns(

        [

            (pl.col("jumlahHariTunggakan") > 0)

            .cast(pl.Int8)

            .alias("flag_dpd"),

            (pl.col("jumlahHariTunggakan") >= 30)

            .cast(pl.Int8)

            .alias("flag_dpd30"),

            (pl.col("jumlahHariTunggakan") >= 60)

            .cast(pl.Int8)

            .alias("flag_dpd60"),

            (pl.col("jumlahHariTunggakan") >= 90)

            .cast(pl.Int8)

            .alias("flag_dpd90"),

            (pl.col("jumlahHariTunggakan") >= 120)

            .cast(pl.Int8)

            .alias("flag_dpd120"),

        ]

    )

    log_feature(
        feature,
        before,
        df.width,
    )

    return df


# =============================================================================
# CREATE FEATURE
# =============================================================================

def create_basic_feature(df: pl.DataFrame) -> pl.DataFrame:

    create_functions = [

        create_utilization,

        create_credit_age,

        create_remaining_tenor,

        create_restructure_flag,

        create_default_flag,

        create_current_kol_flag,

        create_current_dpd_flag,

    ]

    for function in create_functions:

        df = function(df)

    return df
