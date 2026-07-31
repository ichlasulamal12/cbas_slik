"""
==============================================================================
Project : CBAS SLIK Preprocessing
File    : loader.py
Author  : Ichlasul Amal
Version : 2.0.0
==============================================================================

Data Loader
"""

from pathlib import Path

import polars as pl

from config import (
    APPLICATION_COLUMNS,
    COMPANY_APPLICATION_FILE,
    INDIVIDUAL_APPLICATION_FILE,
    FEATURE_LIST_FILE,
    FEATURE_NAME_COLUMN,
    FEATURE_USE_COLUMN,
    FEATURE_USE_VALUE,
    AGGREGATE_DIR,
    AGGREGATE_PREFIX,
    PARQUET_EXTENSION,
)


# =============================================================================
# VALIDATION
# =============================================================================

def validate_file(
    file: Path,
) -> None:
    """
    Validate file existence.
    """

    if not file.exists():

        raise FileNotFoundError(

            f"File not found:\n{file}"

        )


# =============================================================================
# APPLICATION
# =============================================================================

def load_application(
    file: Path,
) -> pl.DataFrame:
    """
    Load application dataset.
    """

    validate_file(file)

    df = pl.read_excel(
        file,
    )

    columns = [

        column

        for column in APPLICATION_COLUMNS

        if column in df.columns

    ]

    return df.select(
        columns
    )


def load_company_application(
) -> pl.DataFrame:
    """
    Load company application.
    """

    return load_application(

        COMPANY_APPLICATION_FILE,

    )


def load_individual_application(
) -> pl.DataFrame:
    """
    Load individual application.
    """

    return load_application(

        INDIVIDUAL_APPLICATION_FILE,

    )


def load_application_dataset(
) -> tuple[
    pl.DataFrame,
    pl.DataFrame,
]:
    """
    Load application dataset.
    """

    return (

        load_company_application(),

        load_individual_application(),

    )


# =============================================================================
# AGGREGATE
# =============================================================================

def aggregate_file(
    period: str,
    segment: str,
) -> Path:
    """
    Aggregate file path.
    """

    return (

        AGGREGATE_DIR

        /

        f"{AGGREGATE_PREFIX}_{period}_{segment}"

        f"{PARQUET_EXTENSION}"

    )


def load_aggregate(
    period: str,
    segment: str,
) -> pl.DataFrame:
    """
    Load aggregate dataset.
    """

    file = aggregate_file(

        period,

        segment,

    )

    validate_file(file)

    return pl.read_parquet(

        file,

    )


# =============================================================================
# FEATURE LIST
# =============================================================================

def load_feature_list(
) -> list[str]:
    """
    Load active feature list.
    """

    validate_file(

        FEATURE_LIST_FILE,

    )

    df = pl.read_excel(

        FEATURE_LIST_FILE,

    )

    if FEATURE_USE_COLUMN in df.columns:

        df = df.filter(

            pl.col(

                FEATURE_USE_COLUMN

            )

            ==

            FEATURE_USE_VALUE

        )

    return (

        df

        .get_column(

            FEATURE_NAME_COLUMN,

        )

        .drop_nulls()

        .cast(pl.String)

        .to_list()

    )


# =============================================================================
# CHECK FEATURE
# =============================================================================

def available_feature(
    df: pl.DataFrame,
    feature_list: list[str],
) -> list[str]:
    """
    Keep available features only.
    """

    columns = set(
        df.columns
    )

    return [

        feature

        for feature in feature_list

        if feature in columns

    ]
