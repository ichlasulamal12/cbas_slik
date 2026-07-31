"""
==============================================================================
Project : CBAS SLIK Feature Engineering
File    : facility.py
Author  : Ichlasul Amal
Version : 2.0.0
==============================================================================

Facility Feature Engineering

Feature Level :
Facility

"""

import polars as pl

from feature_engine.feature_helper import (
    has_columns,
    log_feature,
)


# =============================================================================
# FACILITY FLAG
# =============================================================================

def create_facility_flag(
    df: pl.DataFrame,
) -> pl.DataFrame:

    if not has_columns(
        df,
        [
            "noRekening",
        ],
    ):

        return df

    return df.with_columns(

        pl.lit(1)

        .cast(pl.Int8)

        .alias("facility_flag")

    )


# =============================================================================
# LJK FLAG
# =============================================================================

def create_ljk_flag(
    df: pl.DataFrame,
) -> pl.DataFrame:

    if not has_columns(
        df,
        [
            "ljk",
        ],
    ):

        return df

    return df.with_columns(

        pl.col("ljk")

        .is_not_null()

        .cast(pl.Int8)

        .alias("ljk_flag")

    )


# =============================================================================
# BRANCH FLAG
# =============================================================================

def create_branch_flag(
    df: pl.DataFrame,
) -> pl.DataFrame:

    if not has_columns(
        df,
        [
            "cabang",
        ],
    ):

        return df

    return df.with_columns(

        pl.col("cabang")

        .is_not_null()

        .cast(pl.Int8)

        .alias("branch_flag")

    )


# =============================================================================
# CREDIT TYPE FLAG
# =============================================================================

def create_credit_type_flag(
    df: pl.DataFrame,
) -> pl.DataFrame:

    if not has_columns(
        df,
        [
            "CreditType",
        ],
    ):

        return df

    return df.with_columns(

        pl.col("CreditType")

        .is_not_null()

        .cast(pl.Int8)

        .alias("credit_type_flag")

    )


# =============================================================================
# GOVERNMENT PROGRAM FLAG
# =============================================================================

def create_program_flag(
    df: pl.DataFrame,
) -> pl.DataFrame:

    if not has_columns(
        df,
        [
            "kreditProgramPemerintah",
        ],
    ):

        return df

    return df.with_columns(

        pl.col("kreditProgramPemerintah")

        .is_not_null()

        .cast(pl.Int8)

        .alias("program_flag")

    )


# =============================================================================
# PROJECT FLAG
# =============================================================================

def create_project_flag(
    df: pl.DataFrame,
) -> pl.DataFrame:

    if not has_columns(
        df,
        [
            "lokasiProyek",
        ],
    ):

        return df

    return df.with_columns(

        pl.col("lokasiProyek")

        .is_not_null()

        .cast(pl.Int8)

        .alias("project_flag")

    )


# =============================================================================
# FOREIGN CURRENCY FLAG
# =============================================================================

def create_foreign_currency_flag(
    df: pl.DataFrame,
) -> pl.DataFrame:

    if not has_columns(
        df,
        [
            "kodeValuta",
        ],
    ):

        return df

    return df.with_columns(

        (

            pl.col("kodeValuta")

            !=

            "IDR"

        )

        .fill_null(False)

        .cast(pl.Int8)

        .alias("foreign_currency_flag")

    )


# =============================================================================
# MAIN
# =============================================================================

def create_facility_feature(
    df: pl.DataFrame,
) -> pl.DataFrame:

    before = df.width

    functions = [

        create_facility_flag,

        create_ljk_flag,

        create_branch_flag,

        create_credit_type_flag,

        create_program_flag,

        create_project_flag,

        create_foreign_currency_flag,

    ]

    for function in functions:

        df = function(df)

    log_feature(

        "Facility Feature",

        before,

        df.width,

    )

    return df
