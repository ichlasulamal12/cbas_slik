"""
==============================================================================
Project : CBAS SLIK Preprocessing
File    : feature_engine/iv.py
Author  : Ichlasul Amal
Version : 2.0.0
==============================================================================

Information Value
"""

import polars as pl

from config import (
    IV_THRESHOLD,
    TARGET_COLUMN,
)


# =============================================================================
# BUILD IV TABLE
# =============================================================================

def build_iv_table(
    woe_model: dict,
) -> pl.DataFrame:
    """
    Build IV summary table.
    """

    rows = []

    for feature, model in woe_model.items():

        rows.append(

            {

                "Variable": feature,

                "IV": float(model.iv),

                "Bin": len(model.mapping),

            }

        )

    if len(rows) == 0:

        return pl.DataFrame()

    return (

        pl.DataFrame(rows)

        .sort(

            "IV",

            descending=True,

        )

    )


# =============================================================================
# FEATURE SELECTION
# =============================================================================

def select_feature(
    iv_table: pl.DataFrame,
    threshold: float = IV_THRESHOLD,
) -> list[str]:
    """
    Select feature using IV threshold.
    """

    if iv_table.height == 0:

        return []

    return (

        iv_table

        .filter(

            pl.col("IV") >= threshold

        )

        .get_column("Variable")

        .to_list()

    )

# =============================================================================
# INFORMATION
# =============================================================================

def information(
    iv_table: pl.DataFrame,
) -> dict:
    """
    IV information.
    """

    if iv_table.height == 0:

        return {

            "feature": 0,

            "selected": 0,

        }

    return {

        "feature": iv_table.height,

        "selected": (

            iv_table

            .filter(

                pl.col("IV")

                >=

                IV_THRESHOLD

            )

            .height

        ),

    }


# =============================================================================
# PRINT INFORMATION
# =============================================================================

def print_information(
    iv_table: pl.DataFrame,
) -> None:
    """
    Print IV summary.
    """

    info = information(

        iv_table,

    )

    print()

    print("=" * 80)

    print("IV SUMMARY")

    print("=" * 80)

    print(

        f"Feature      : "

        f"{info['feature']:,}"

    )

    print(

        f"Selected     : "

        f"{info['selected']:,}"

    )

    print(

        f"Threshold    : "

        f"{IV_THRESHOLD:.3f}"

    )

    print()
