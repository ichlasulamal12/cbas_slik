"""
==============================================================================
Project : CBAS SLIK Feature Engineering
File    : feature_catalog.py
Author  : Ichlasul Amal
Version : 2.0.0
==============================================================================

Feature Catalog

Menggabungkan metadata feature dan statistik feature
menjadi satu catalog otomatis.

"""

import polars as pl

from documentation.feature_classifier import (
    classify_feature,
)

from documentation.feature_statistics import (
    create_feature_statistics,
)

from documentation.feature_formula import get_formula

# =============================================================================
# CREATE FEATURE CATALOG
# =============================================================================

def create_feature_catalog(
    df: pl.DataFrame,
) -> pl.DataFrame:

    statistics = create_feature_statistics(

        df

    )

    rows = []

    for row in statistics.iter_rows(

        named=True,

    ):

        feature_name = row["feature_name"]

        metadata = classify_feature(feature_name)

        rows.append(

            {

                "feature_name": feature_name,

                "display_name": feature_name.replace("_", " ").title(),

                "formula": get_formula(feature_name),

                **metadata,

                **row,

            }

        )

    catalog = (

        pl.DataFrame(

            rows,

        )

        .sort(

            [

                "module",

                "domain",

                "category",

                "feature_name",

            ]

        )

    )

    return catalog
