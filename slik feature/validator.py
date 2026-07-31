"""
==============================================================================
Project : CBAS SLIK Feature Engineering
File    : validator.py
Author  : Ichlasul Amal
Version : 1.0.0
==============================================================================

Data Validation Module

"""

import polars as pl

from config import (
    REQUIRED_COLUMNS,
    NUMERIC_COLUMNS,
    DATE_COLUMNS,
    STRING_COLUMNS,
    KOL_COLUMNS,
    HT_COLUMNS,
    PERIOD_COLUMNS,
)

from utils.logger import get_logger

logger = get_logger(__name__)


# =============================================================================
# REQUIRED COLUMN
# =============================================================================

def validate_required_columns(df: pl.DataFrame):

    logger.info("Validate required columns")

    missing = [

        c

        for c in REQUIRED_COLUMNS

        if c not in df.columns

    ]

    if missing:

        raise ValueError(

            f"Missing required columns : {missing}"

        )


# =============================================================================
# KEY
# =============================================================================

def validate_key(df: pl.DataFrame, keys: list):

    logger.info("Validate key")

    missing = [

        c

        for c in keys

        if c not in df.columns

    ]

    if missing:

        raise ValueError(

            f"Missing key columns : {missing}"

        )


# =============================================================================
# EMPTY DATA
# =============================================================================

def validate_empty(df: pl.DataFrame) -> bool:

    if df.height == 0:

        logger.warning("Dataset is empty.")

        return False

    return True


# =============================================================================
# DUPLICATE KEY
# =============================================================================

def validate_duplicate_key(
    df: pl.DataFrame,
    keys: list,
):

    logger.info("Validate duplicate key")

    duplicate = (

        df

        .group_by(keys)

        .len()

        .filter(

            pl.col("len") > 1

        )

    )

    if duplicate.height > 0:

        logger.warning(

            "%s duplicate key(s) found.",

            duplicate.height,

        )


# =============================================================================
# NULL KEY
# =============================================================================

def validate_null_key(
    df: pl.DataFrame,
    keys: list,
):

    logger.info("Validate null key")

    for key in keys:

        if key not in df.columns:

            continue

        total = (

            df

            .filter(

                pl.col(key).is_null()

            )

            .height

        )

        if total > 0:

            logger.warning(

                "%s has %s null values.",

                key,

                total,

            )

            # =============================================================================
# NUMERIC
# =============================================================================

def validate_numeric(
    df: pl.DataFrame,
) -> pl.DataFrame:

    logger.info("Validate numeric columns")

    expressions = []

    numeric_columns = [

        *NUMERIC_COLUMNS,

        *KOL_COLUMNS,

        *HT_COLUMNS,

    ]

    for column in numeric_columns:

        if column not in df.columns:

            continue

        expressions.append(

            pl.col(column)

            .cast(

                pl.Float64,

                strict=False,

            )

            .alias(column)

        )

    if expressions:

        df = df.with_columns(

            expressions

        )

    return df


# =============================================================================
# DATE
# =============================================================================

# =============================================================================
# DATE
# =============================================================================

def validate_date(
    df: pl.DataFrame,
) -> pl.DataFrame:

    logger.info("Validate date columns")

    expressions = []

    for column in DATE_COLUMNS:

        if column not in df.columns:

            continue

        dtype = df.schema[column]

        # -------------------------------------------------------------
        # Already Date
        # -------------------------------------------------------------

        if dtype == pl.Date:

            continue

        # -------------------------------------------------------------
        # Datetime -> Date
        # -------------------------------------------------------------

        if dtype == pl.Datetime:

            expressions.append(

                pl.col(column)

                .dt.date()

                .alias(column)

            )

            continue

        # -------------------------------------------------------------
        # String
        # -------------------------------------------------------------

        expressions.append(

            pl.col(column)

            .str.strptime(

                pl.Datetime,

                format="%Y-%m-%d %H:%M:%S%.f",

                strict=False,

            )

            .dt.date()

            .alias(column)

        )

    if expressions:

        df = df.with_columns(

            expressions

        )

    return df


# =============================================================================
# STRING
# =============================================================================

def validate_string(
    df: pl.DataFrame,
) -> pl.DataFrame:

    logger.info("Validate string columns")

    expressions = []

    for column in STRING_COLUMNS:

        if column not in df.columns:

            continue

        expressions.append(

            pl.col(column)

            .cast(

                pl.Utf8,

                strict=False,

            )

            .str.strip_chars()

            .alias(column)

        )

    if expressions:

        df = df.with_columns(

            expressions

        )

    return df


# =============================================================================
# HISTORY
# =============================================================================

def validate_history(
    df: pl.DataFrame,
):

    logger.info("Validate history columns")

    history = [

        *KOL_COLUMNS,

        *HT_COLUMNS,

        *PERIOD_COLUMNS,

    ]

    missing = [

        c

        for c in history

        if c not in df.columns

    ]

    if missing:

        logger.warning(

            "%s history column(s) missing.",

            len(missing),

        )

        logger.debug(

            "Missing history columns : %s",

            missing,

        )


# =============================================================================
# HISTORY COMPLETENESS
# =============================================================================

def validate_history_completeness(
    df: pl.DataFrame,
):

    logger.info("Validate history completeness")

    available_kol = [

        c

        for c in KOL_COLUMNS

        if c in df.columns

    ]

    available_ht = [

        c

        for c in HT_COLUMNS

        if c in df.columns

    ]

    logger.info(

        "KOL History : %s/%s",

        len(available_kol),

        len(KOL_COLUMNS),

    )

    logger.info(

        "DPD History : %s/%s",

        len(available_ht),

        len(HT_COLUMNS),

    )

    # =============================================================================
# KOL
# =============================================================================

def validate_kol(
    df: pl.DataFrame,
):

    logger.info("Validate KOL history")

    available = [

        c

        for c in KOL_COLUMNS

        if c in df.columns

    ]

    if not available:

        logger.warning(

            "No KOL history found."

        )

        return

    invalid = (

        df

        .select(

            [

                (

                    (

                        ~pl.col(c)

                        .is_in(

                            [1,2,3,4,5]

                        )

                    )

                    &

                    pl.col(c)

                    .is_not_null()

                )

                .sum()

                .alias(c)

                for c in available

            ]

        )

    )

    total = sum(

        invalid.row(0)

    )

    if total > 0:

        logger.warning(

            "%s invalid KOL value(s).",

            total,

        )


# =============================================================================
# DPD
# =============================================================================

def validate_dpd(
    df: pl.DataFrame,
):

    logger.info("Validate DPD history")

    available = [

        c

        for c in HT_COLUMNS

        if c in df.columns

    ]

    if not available:

        logger.warning(

            "No DPD history found."

        )

        return

    invalid = (

        df

        .select(

            [

                (

                    pl.col(c) < 0

                )

                .sum()

                .alias(c)

                for c in available

            ]

        )

    )

    total = sum(

        invalid.row(0)

    )

    if total > 0:

        logger.warning(

            "%s negative DPD value(s).",

            total,

        )


# =============================================================================
# DATA QUALITY
# =============================================================================

def validate_data_quality(
    df: pl.DataFrame,
):

    logger.info("Validate data quality")

    total_null = (

        df

        .null_count()

        .sum_horizontal()

        .item()

    )

    logger.info(

        "Total Null : %s",

        f"{total_null:,}",

    )

    logger.info(

        "Rows       : %s",

        f"{df.height:,}",

    )

    logger.info(

        "Columns    : %s",

        df.width,

    )


# =============================================================================
# VALIDATE DATA
# =============================================================================

def validate_data(

    df: pl.DataFrame,

    keys: list,

):

    logger.info("=" * 80)

    logger.info("VALIDATE DATA")

    logger.info("=" * 80)

    # -------------------------------------------------------------------------
    # EMPTY DATASET
    # -------------------------------------------------------------------------

    if not validate_empty(df):

        logger.warning(

            "Validation skipped because dataset is empty."

        )

        logger.info("=" * 80)

        return None

    # -------------------------------------------------------------------------
    # REQUIRED COLUMN
    # -------------------------------------------------------------------------

    validate_required_columns(

        df

    )

    # -------------------------------------------------------------------------
    # KEY
    # -------------------------------------------------------------------------

    validate_key(

        df,

        keys,

    )

    validate_duplicate_key(

        df,

        keys,

    )

    validate_null_key(

        df,

        keys,

    )

    # -------------------------------------------------------------------------
    # DATA TYPE
    # -------------------------------------------------------------------------

    df = validate_numeric(

        df

    )

    df = validate_date(

        df

    )

    df = validate_string(

        df

    )

    # -------------------------------------------------------------------------
    # HISTORY
    # -------------------------------------------------------------------------

    validate_history(

        df

    )

    validate_history_completeness(

        df

    )

    # -------------------------------------------------------------------------
    # HISTORY VALUE
    # -------------------------------------------------------------------------

    validate_kol(

        df

    )

    validate_dpd(

        df

    )

    # -------------------------------------------------------------------------
    # DATA QUALITY
    # -------------------------------------------------------------------------

    validate_data_quality(

        df

    )

    logger.info(

        "Validation completed."

    )

    logger.info("=" * 80)

    return df
