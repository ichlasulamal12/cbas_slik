"""
==============================================================================
Project : CBAS SLIK Feature Engineering
File    : helper.py
Author  : Ichlasul Amal
Version : 1.0.0
==============================================================================

General Helper Functions

"""

from pathlib import Path
from datetime import datetime

import polars as pl


# =============================================================================
# DIRECTORY
# =============================================================================

def create_directory(path):

    path = Path(path)

    path.mkdir(

        parents=True,

        exist_ok=True,

    )

    return path


# =============================================================================
# FILE EXISTS
# =============================================================================

def file_exists(path):

    return Path(path).exists()


# =============================================================================
# TIMESTAMP
# =============================================================================

def current_timestamp():

    return datetime.now().strftime(

        "%Y-%m-%d %H:%M:%S"

    )


# =============================================================================
# DATE
# =============================================================================

def current_date():

    return datetime.now().strftime(

        "%Y-%m-%d"

    )


# =============================================================================
# MONTH
# =============================================================================

def current_month():

    return datetime.now().strftime(

        "%Y%m"

    )


# =============================================================================
# SAFE DIVISION
# =============================================================================

def safe_divide(numerator, denominator):

    return (

        pl.when(

            denominator.is_not_null()

            &

            (denominator != 0)

        )

        .then(

            numerator / denominator

        )

        .otherwise(None)

    )


# =============================================================================
# SAFE LOG
# =============================================================================

def safe_log(column):

    return (

        pl.when(

            column > 0

        )

        .then(

            column.log()

        )

        .otherwise(None)

    )


# =============================================================================
# SAFE SQRT
# =============================================================================

def safe_sqrt(column):

    return (

        pl.when(

            column >= 0

        )

        .then(

            column.sqrt()

        )

        .otherwise(None)

    )


# =============================================================================
# CLIP
# =============================================================================

def clip(column, lower=None, upper=None):

    expr = column

    if lower is not None:

        expr = pl.when(

            expr < lower

        ).then(

            lower

        ).otherwise(

            expr

        )

    if upper is not None:

        expr = pl.when(

            expr > upper

        ).then(

            upper

        ).otherwise(

            expr

        )

    return expr


# =============================================================================
# CHECK COLUMN
# =============================================================================

def has_columns(df, columns):

    return all(

        col in df.columns

        for col in columns

    )


# =============================================================================
# GET EXISTING COLUMNS
# =============================================================================

def existing_columns(df, columns):

    return [

        col

        for col in columns

        if col in df.columns

    ]


# =============================================================================
# MISSING COLUMNS
# =============================================================================

def missing_columns(df, columns):

    return [

        col

        for col in columns

        if col not in df.columns

    ]


# =============================================================================
# MEMORY
# =============================================================================

def dataframe_size(df):

    return round(

        df.estimated_size("mb"),

        2,

    )


# =============================================================================
# DATAFRAME INFO
# =============================================================================

def dataframe_info(df):

    return {

        "rows": df.height,

        "columns": df.width,

        "memory_mb": dataframe_size(df),

    }


# =============================================================================
# PRINT HEADER
# =============================================================================

def print_header(title):

    print("=" * 80)

    print(title)

    print("=" * 80)


# =============================================================================
# PRINT STEP
# =============================================================================

def print_step(title):

    print(f">>> {title}")


# =============================================================================
# PRINT FINISH
# =============================================================================

def print_finish(title):

    print(f"Finished : {title}")
