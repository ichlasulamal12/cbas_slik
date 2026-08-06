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

def aggregate_files(
    period: str,
    segment: str,
) -> list[Path]:
    """
    Find all aggregate files for
    one snapshot period and segment.

    Supported format:

    Prefix_YYYYMM_Segment.parquet

    Prefix_YYYYMM_1_Segment.parquet
    Prefix_YYYYMM_2_Segment.parquet
    Prefix_YYYYMM_3_Segment.parquet
    """

    # -------------------------------------------------------------------------
    # SINGLE FILE
    # -------------------------------------------------------------------------

    single_file = (

        AGGREGATE_DIR

        /

        f"{AGGREGATE_PREFIX}_{period}_{segment}"

        f"{PARQUET_EXTENSION}"

    )

    # -------------------------------------------------------------------------
    # MULTI PART FILE
    # -------------------------------------------------------------------------

    multipart_pattern = (

        f"{AGGREGATE_PREFIX}_{period}_*_{segment}"

        f"{PARQUET_EXTENSION}"

    )

    multipart_files = list(

        AGGREGATE_DIR.glob(

            multipart_pattern,

        )

    )

    # -------------------------------------------------------------------------
    # RESULT
    # -------------------------------------------------------------------------

    files = []

    if single_file.exists():

        files.append(

            single_file,

        )

    files.extend(

        multipart_files,

    )

    # -------------------------------------------------------------------------
    # REMOVE DUPLICATE
    # -------------------------------------------------------------------------

    files = list(

        dict.fromkeys(

            files

        )

    )

    # -------------------------------------------------------------------------
    # SORT
    # -------------------------------------------------------------------------

    files = sorted(

        files,

        key=lambda file: file.name,

    )

    return files


def load_aggregate(
    period: str,
    segment: str,
) -> pl.DataFrame:
    """
    Load all aggregate files for
    one snapshot period and segment.
    """

    files = aggregate_files(

        period,

        segment,

    )

    # -------------------------------------------------------------------------
    # VALIDATION
    # -------------------------------------------------------------------------

    if len(files) == 0:

        raise FileNotFoundError(

            f"No aggregate file found for "
            f"period={period}, "
            f"segment={segment}"

        )

    # -------------------------------------------------------------------------
    # INFORMATION
    # -------------------------------------------------------------------------

    print(

        f"  {segment:<12} : "

        f"{len(files):,} file(s)"

    )

    for file in files:

        print(

            f"    - {file.name}"

        )

    # -------------------------------------------------------------------------
    # LOAD
    # -------------------------------------------------------------------------

    datasets = [

        pl.read_parquet(

            file,

        )

        for file in files

    ]

    # -------------------------------------------------------------------------
    # SINGLE FILE
    # -------------------------------------------------------------------------

    if len(datasets) == 1:

        return datasets[0]

    # -------------------------------------------------------------------------
    # MULTIPLE FILE
    # -------------------------------------------------------------------------

    return pl.concat(

        datasets,

        how="diagonal_relaxed",

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
