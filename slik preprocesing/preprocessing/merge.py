"""
==============================================================================
Project : CBAS SLIK Preprocessing
File    : preprocessing/merge.py
Author  : Ichlasul Amal
Version : 2.0.0
==============================================================================

Merge Dataset
"""

from datetime import datetime

import polars as pl

from config import (
    COMPANY_SEGMENT,
    INDIVIDUAL_SEGMENT,
    COMPANY_AGGREGATE_KEY,
    INDIVIDUAL_AGGREGATE_KEY,
    COMPANY_APPLICATION_KEY,
    INDIVIDUAL_APPLICATION_KEY,
    SEGMENT_COLUMN,
    SNAPSHOT_COLUMN,
    SNAPSHOT_DATE_COLUMN,
)


# =============================================================================
# SNAPSHOT
# =============================================================================

def snapshot_date(
    period: str,
):
    """
    Convert YYYYMM
    into date.
    """

    return datetime.strptime(

        period,

        "%Y%m",

    ).date()


# =============================================================================
# COMPANY
# =============================================================================

def merge_company(
    aggregate: pl.DataFrame,
    application: pl.DataFrame,
    period: str,
) -> pl.DataFrame:
    """
    Merge company dataset.
    """

    if aggregate.height == 0:

        return pl.DataFrame()

    result = aggregate.join(

        application,

        left_on=COMPANY_AGGREGATE_KEY,

        right_on=COMPANY_APPLICATION_KEY,

        how="inner",

    )

    result = result.with_columns(

        [

            pl.lit(

                COMPANY_SEGMENT,

            )

            .alias(

                SEGMENT_COLUMN,

            ),

            pl.lit(

                period,

            )

            .alias(

                SNAPSHOT_COLUMN,

            ),

            pl.lit(

                snapshot_date(

                    period,

                )

            )

            .alias(

                SNAPSHOT_DATE_COLUMN,

            ),

        ]

    )

    return result


# =============================================================================
# INDIVIDUAL
# =============================================================================

def merge_individual(
    aggregate: pl.DataFrame,
    application: pl.DataFrame,
    period: str,
) -> pl.DataFrame:
    """
    Merge individual dataset.
    """

    if aggregate.height == 0:

        return pl.DataFrame()

    result = aggregate.join(

        application,

        left_on=INDIVIDUAL_AGGREGATE_KEY,

        right_on=INDIVIDUAL_APPLICATION_KEY,

        how="inner",

    )

    result = result.with_columns(

        [

            pl.lit(

                INDIVIDUAL_SEGMENT,

            )

            .alias(

                SEGMENT_COLUMN,

            ),

            pl.lit(

                period,

            )

            .alias(

                SNAPSHOT_COLUMN,

            ),

            pl.lit(

                snapshot_date(

                    period,

                )

            )

            .alias(

                SNAPSHOT_DATE_COLUMN,

            ),

        ]

    )

    return result


# =============================================================================
# PERIOD
# =============================================================================

def merge_period(
    period: str,
    company_aggregate: pl.DataFrame,
    individual_aggregate: pl.DataFrame,
    company_application: pl.DataFrame,
    individual_application: pl.DataFrame,
) -> pl.DataFrame:
    """
    Merge one snapshot period.
    """

    datasets = []

    company = merge_company(

        company_aggregate,

        company_application,

        period,

    )

    if company.height > 0:

        datasets.append(

            company,

        )

    individual = merge_individual(

        individual_aggregate,

        individual_application,

        period,

    )

    if individual.height > 0:

        datasets.append(

            individual,

        )

    if len(datasets) == 0:

        return pl.DataFrame()

    return pl.concat(

        datasets,

        how="diagonal_relaxed",

    )


# =============================================================================
# COMBINE
# =============================================================================

def combine_periods(
    periods: list[pl.DataFrame],
) -> pl.DataFrame:
    """
    Combine all periods.
    """

    periods = [

        df

        for df in periods

        if df.height > 0

    ]

    if len(periods) == 0:

        return pl.DataFrame()

    return pl.concat(

        periods,

        how="diagonal_relaxed",

    )
