"""
==============================================================================
Project : CBAS SLIK Preprocessing
File    : utils/date_utils.py
Author  : Ichlasul Amal
Version : 2.0.0
==============================================================================

Date Utilities
"""

from datetime import date
from datetime import datetime

from dateutil.relativedelta import relativedelta

from config import (
    PROCESS_START_PERIOD,
    PROCESS_END_PERIOD,
    DEVELOPMENT_END_PERIOD,
    OOT_START_PERIOD,
)


# =============================================================================
# PERIOD
# =============================================================================

def period_to_date(
    period: str,
) -> date:
    """
    Convert YYYYMM to date.
    """

    return datetime.strptime(

        period,

        "%Y%m",

    ).date()


def date_to_period(
    value: date,
) -> str:
    """
    Convert date to YYYYMM.
    """

    return value.strftime(

        "%Y%m"

    )


# =============================================================================
# PROCESS PERIOD
# =============================================================================

def process_periods(
) -> list[str]:
    """
    Processing periods.
    """

    periods = []

    current = period_to_date(

        PROCESS_START_PERIOD,

    )

    end = period_to_date(

        PROCESS_END_PERIOD,

    )

    while current <= end:

        periods.append(

            date_to_period(
                current
            )

        )

        current += relativedelta(

            months=1,

        )

    return periods


# =============================================================================
# DEVELOPMENT
# =============================================================================

def development_end_date(
) -> date:
    """
    Development end date.
    """

    return period_to_date(

        DEVELOPMENT_END_PERIOD,

    )


# =============================================================================
# OOT
# =============================================================================

def oot_start_date(
) -> date:
    """
    OOT start date.
    """

    return period_to_date(

        OOT_START_PERIOD,

    )


# =============================================================================
# SNAPSHOT
# =============================================================================

def snapshot_date(
    period: str,
) -> date:
    """
    Snapshot period to date.
    """

    return period_to_date(

        period,

    )
