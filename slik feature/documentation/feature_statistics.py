"""
==============================================================================
Project : CBAS SLIK Feature Engineering
File    : feature_statistics.py
Author  : Ichlasul Amal
Version : 2.0.0
==============================================================================

Feature Statistics

Generate descriptive statistics untuk setiap feature.

"""

import polars as pl


# =============================================================================
# NUMERIC TYPE
# =============================================================================

NUMERIC_TYPES = {

    pl.Int8,
    pl.Int16,
    pl.Int32,
    pl.Int64,

    pl.UInt8,
    pl.UInt16,
    pl.UInt32,
    pl.UInt64,

    pl.Float32,
    pl.Float64,

}


# =============================================================================
# NUMERIC
# =============================================================================

def is_numeric(
    dtype,
) -> bool:

    return dtype in NUMERIC_TYPES


# =============================================================================
# BASIC STATISTICS
# =============================================================================

def create_statistics(
    df: pl.DataFrame,
    column: str,
) -> dict:

    series = df[column]

    dtype = df.schema[column]

    missing_count = series.null_count()

    row_count = df.height

    result = {

        "feature_name": column,

        "data_type": str(dtype),

        "row_count": row_count,

        "missing_count": missing_count,

        "missing_ratio": (

            missing_count / row_count

            if row_count > 0

            else 0.0

        ),

        "unique_count": series.n_unique(),

    }

    if is_numeric(dtype):

        result.update(

            {

                "mean": series.mean(),

                "std": series.std(),

                "min": series.min(),

                "q1": series.quantile(0.25),

                "median": series.median(),

                "q3": series.quantile(0.75),

                "max": series.max(),

                "range": (

                    series.max() - series.min()

                    if (

                        series.max() is not None

                        and

                        series.min() is not None

                    )

                    else None

                ),

                "variance": series.var(),

                "sum": series.sum(),

            }

        )

    else:

        result.update(

            {

                "mean": None,

                "std": None,

                "min": None,

                "q1": None,

                "median": None,

                "q3": None,

                "max": None,

                "range": None,

                "variance": None,

                "sum": None,

            }

        )

    return result


# =============================================================================
# CREATE FEATURE STATISTICS
# =============================================================================

def create_feature_statistics(
    df: pl.DataFrame,
) -> pl.DataFrame:

    rows = []

    for column in df.columns:

        rows.append(

            create_statistics(

                df,

                column,

            )

        )

    return (

        pl.DataFrame(rows)

        .sort(

            "feature_name"

        )

    )
