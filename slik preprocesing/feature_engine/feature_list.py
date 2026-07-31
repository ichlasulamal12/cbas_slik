"""
==============================================================================
Project : CBAS SLIK Preprocessing
File    : feature_engine/feature_list.py
Author  : Ichlasul Amal
Version : 2.0.0
==============================================================================

Feature List Utilities
"""

import polars as pl


# =============================================================================
# AVAILABLE FEATURE
# =============================================================================

def available_feature(
    df: pl.DataFrame,
    feature_list: list[str],
) -> list[str]:
    """
    Keep only features that
    exist in dataset.
    """

    columns = set(
        df.columns
    )

    return [

        feature

        for feature in feature_list

        if feature in columns

    ]


# =============================================================================
# MISSING FEATURE
# =============================================================================

def missing_feature(
    df: pl.DataFrame,
    feature_list: list[str],
) -> list[str]:
    """
    Feature defined in metadata
    but not found in dataset.
    """

    columns = set(
        df.columns
    )

    return [

        feature

        for feature in feature_list

        if feature not in columns

    ]


# =============================================================================
# CONSTANT FEATURE
# =============================================================================

def constant_feature(
    df: pl.DataFrame,
    feature_list: list[str],
) -> list[str]:
    """
    Detect constant feature.
    """

    constant = []

    for feature in feature_list:

        if feature not in df.columns:

            continue

        if (

            df

            .get_column(feature)

            .drop_nulls()

            .n_unique()

            <= 1

        ):

            constant.append(
                feature
            )

    return constant


# =============================================================================
# VALID FEATURE
# =============================================================================

def valid_feature(
    df: pl.DataFrame,
    feature_list: list[str],
) -> list[str]:
    """
    Remove unavailable and
    constant feature.
    """

    available = available_feature(

        df,

        feature_list,

    )

    constant = set(

        constant_feature(

            df,

            available,

        )

    )

    return [

        feature

        for feature in available

        if feature not in constant

    ]


# =============================================================================
# SUMMARY
# =============================================================================

def feature_summary(
    df: pl.DataFrame,
    feature_list: list[str],
) -> None:
    """
    Print feature summary.
    """

    available = available_feature(

        df,

        feature_list,

    )

    missing = missing_feature(

        df,

        feature_list,

    )

    constant = constant_feature(

        df,

        available,

    )

    valid = valid_feature(

        df,

        feature_list,

    )

    print()

    print("=" * 80)

    print("FEATURE SUMMARY")

    print("=" * 80)

    print(

        f"Feature Metadata : {len(feature_list):,}"

    )

    print(

        f"Available        : {len(available):,}"

    )

    print(

        f"Missing          : {len(missing):,}"

    )

    print(

        f"Constant         : {len(constant):,}"

    )

    print(

        f"Valid            : {len(valid):,}"

    )

    print()
