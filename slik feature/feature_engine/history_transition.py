"""
==============================================================================
Project : CBAS SLIK Feature Engineering
File    : history_transition.py
Author  : Ichlasul Amal
Version : 3.0.0
==============================================================================

History Transition Feature Engineering

Feature Level :
Facility

"""

import polars as pl

from config import (
    KOL_COLUMNS,
    HISTORY_WINDOWS,
)

from feature_engine.feature_helper import (
    get_window_columns,
    has_columns,
    log_feature,
)

# =============================================================================
# CONFIGURATION
# =============================================================================

TRANSITIONS = [

    (
        "transition_worsen",
        lambda current, previous:
            pl.col(current) > pl.col(previous),
    ),

    (
        "transition_improve",
        lambda current, previous:
            pl.col(current) < pl.col(previous),
    ),

    (
        "transition_stable",
        lambda current, previous:
            pl.col(current) == pl.col(previous),
    ),

]

# =============================================================================
# GENERIC
# =============================================================================

def create_transition(
    df: pl.DataFrame,
    window: int,
):

    cols = get_window_columns(

        KOL_COLUMNS,

        window,

    )

    if not has_columns(

        df,

        cols,

    ):

        return df

    pairs = list(

        zip(

            cols[:-1],

            cols[1:],

        )

    )

    expressions = []

    for feature_name, rule in TRANSITIONS:

        expressions.append(

            pl.sum_horizontal(

                [

                    rule(

                        current,

                        previous,

                    )

                    .cast(pl.Int8)

                    for current, previous in pairs

                ]

            )

            .alias(

                f"hist{window}_{feature_name}"

            )

        )

    return df.with_columns(

        expressions

    )


# =============================================================================
# MAIN
# =============================================================================

def create_history_transition_feature(
    df: pl.DataFrame,
):

    before = df.width

    for window in HISTORY_WINDOWS:

        df = create_transition(

            df,

            window,

        )

    log_feature(

        "History Transition Feature",

        before,

        df.width,

    )

    return df
