"""
==============================================================================
Project : CBAS SLIK Feature Engineering
File    : ratio.py
Author  : Ichlasul Amal
Version : 2.0.0
==============================================================================

Ratio Feature Engineering

Feature Level :
Facility

"""

import polars as pl

from feature_engine.feature_helper import (

    has_columns,

    log_feature,

)

RATIO_CONFIG = [

    # -------------------------------------------------------------------------
    # EXPOSURE
    # -------------------------------------------------------------------------

    ("ratio_os_plafon",
     "bakiDebet",
     "plafon"),

    ("ratio_unused_plafon",
     "unused_limit",
     "plafon"),

    # -------------------------------------------------------------------------
    # DELINQUENCY
    # -------------------------------------------------------------------------

    ("ratio_overdue_os",
     "total_overdue",
     "bakiDebet"),

    ("ratio_overdue_plafon",
     "total_overdue",
     "plafon"),

    ("ratio_dpd_os",
     "jumlahHariTunggakan",
     "bakiDebet"),

    # -------------------------------------------------------------------------
    # TENOR
    # -------------------------------------------------------------------------

    ("ratio_credit_age",
     "credit_age_days",
     "original_tenor_days"),

    ("ratio_remaining_tenor",
     "remaining_tenor_days",
     "original_tenor_days"),

]

def create_ratio(

    df: pl.DataFrame,

):

    expressions = []

    for feature, numerator, denominator in RATIO_CONFIG:

        if not has_columns(

            df,

            [

                numerator,

                denominator,

            ],

        ):

            continue

        expressions.append(

            pl.when(

                pl.col(

                    denominator

                ) != 0

            )

            .then(

                pl.col(

                    numerator

                )

                /

                pl.col(

                    denominator

                )

            )

            .otherwise(

                None

            )

            .alias(

                feature

            )

        )

    return df.with_columns(

        expressions

    )

def create_ratio_feature(

    df: pl.DataFrame,

):

    before = df.width

    df = create_ratio(

        df

    )

    log_feature(

        "Ratio Feature",

        before,

        df.width,

    )

    return df
