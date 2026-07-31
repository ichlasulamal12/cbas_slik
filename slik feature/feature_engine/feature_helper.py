"""
==============================================================================
Project : CBAS SLIK Feature Engineering
File    : feature_helper.py
Author  : Ichlasul Amal
Version : 2.0.0
==============================================================================

Feature Helper

Helper untuk memastikan seluruh feature engineering menghasilkan
schema yang konsisten meskipun source column tidak tersedia.

"""

import polars as pl


# =============================================================================
# CHECK COLUMN
# =============================================================================

def has_columns(
    df: pl.DataFrame,
    columns: list[str],
) -> bool:
    """
    True jika seluruh kolom tersedia.
    """

    return all(

        column in df.columns

        for column in columns

    )


# =============================================================================
# ADD NULL COLUMN
# =============================================================================

def add_null_column(
    df: pl.DataFrame,
    column: str,
    dtype=pl.Float64,
) -> pl.DataFrame:
    """
    Menambahkan satu kolom NULL apabila belum ada.
    """

    if column in df.columns:

        return df

    return df.with_columns(

        pl.lit(None)

        .cast(dtype)

        .alias(column)

    )


# =============================================================================
# ADD NULL COLUMNS
# =============================================================================

def add_null_columns(
    df: pl.DataFrame,
    columns: list[str],
    dtype=pl.Float64,
) -> pl.DataFrame:
    """
    Menambahkan beberapa kolom NULL apabila belum ada.
    """

    expressions = []

    for column in columns:

        if column not in df.columns:

            expressions.append(

                pl.lit(None)

                .cast(dtype)

                .alias(column)

            )

    if expressions:

        df = df.with_columns(

            expressions

        )

    return df


# =============================================================================
# ENSURE NUMERIC FEATURE
# =============================================================================

def ensure_numeric_feature(
    df: pl.DataFrame,
    source_columns: list[str],
    output_columns: list[str],
    dtype=pl.Float64,
) -> pl.DataFrame:
    """
    Jika source column tidak lengkap maka output feature tetap dibuat
    dengan nilai NULL.
    """

    if not has_columns(

        df,

        source_columns,

    ):

        return add_null_columns(

            df,

            output_columns,

            dtype,

        )

    return df


# =============================================================================
# ENSURE INTEGER FEATURE
# =============================================================================

def ensure_integer_feature(
    df: pl.DataFrame,
    source_columns: list[str],
    output_columns: list[str],
) -> pl.DataFrame:

    return ensure_numeric_feature(

        df,

        source_columns,

        output_columns,

        pl.Int32,

    )


# =============================================================================
# ENSURE FLAG FEATURE
# =============================================================================

def ensure_flag_feature(
    df: pl.DataFrame,
    source_columns: list[str],
    output_columns: list[str],
) -> pl.DataFrame:

    return ensure_numeric_feature(

        df,

        source_columns,

        output_columns,

        pl.Int8,

    )


# =============================================================================
# ENSURE STRING FEATURE
# =============================================================================

def ensure_string_feature(
    df: pl.DataFrame,
    source_columns: list[str],
    output_columns: list[str],
) -> pl.DataFrame:

    if not has_columns(

        df,

        source_columns,

    ):

        return add_null_columns(

            df,

            output_columns,

            pl.Utf8,

        )

    return df


# =============================================================================
# ENSURE DATE FEATURE
# =============================================================================

def ensure_date_feature(
    df: pl.DataFrame,
    source_columns: list[str],
    output_columns: list[str],
) -> pl.DataFrame:

    if not has_columns(

        df,

        source_columns,

    ):

        return add_null_columns(

            df,

            output_columns,

            pl.Date,

        )

    return df

from utils.logger import get_logger

logger = get_logger(__name__)


# =============================================================================
# SAFE RATIO
# =============================================================================

def safe_ratio(

    numerator: str,

    denominator: str,

):

    return (

        pl.when(

            (pl.col(denominator).is_not_null())

            &

            (pl.col(denominator) != 0)

        )

        .then(

            pl.col(numerator)

            /

            pl.col(denominator)

        )

        .otherwise(None)

    )


# =============================================================================
# FEATURE LOGGER
# =============================================================================

def log_feature(

    feature_name: str,

    before: int,

    after: int,

):

    logger.info(

        "%s : +%s column(s)",

        feature_name,

        after - before,

    )

# =============================================================================
# HISTORY WINDOW
# =============================================================================

def get_window_columns(

    columns: list[str],

    window: int,

) -> list[str]:

    """
    Mengambil sejumlah kolom history sesuai window.

    Contoh:
    columns = [
        "tahunBulan01Kol",
        "tahunBulan02Kol",
        ...
        "tahunBulan24Kol"
    ]

    window = 6

    return:
        tahunBulan01Kol
        ...
        tahunBulan06Kol
    """

    return columns[:window]
