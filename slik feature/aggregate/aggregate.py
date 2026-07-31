"""
==============================================================================
Project : CBAS SLIK Feature Engineering
File    : aggregate.py
Author  : Ichlasul Amal
Version : 2.0.0
==============================================================================

Aggregate Orchestrator

Semua modul aggregate menerima Facility Dataset.

Output setiap modul harus berupa Debtor Dataset
(group_by(DEBTOR_KEY)).

"""

import polars as pl

from config import DEBTOR_KEY

from aggregate.aggregate_basic import create_basic_aggregate
from aggregate.aggregate_numeric import create_numeric_aggregate
from aggregate.aggregate_flag import create_flag_aggregate
from aggregate.aggregate_history import create_history_aggregate
from aggregate.aggregate_ratio import create_ratio_aggregate
from aggregate.aggregate_category import create_category_aggregate

from utils.logger import get_logger

logger = get_logger(__name__)


# =============================================================================
# MODULES
# =============================================================================

AGGREGATE_MODULES = [

    ("Basic", create_basic_aggregate),

    ("Numeric", create_numeric_aggregate),

    ("Category", create_category_aggregate),

    ("Flag", create_flag_aggregate),

    ("History", create_history_aggregate),

    ("Ratio", create_ratio_aggregate),

]


# =============================================================================
# AGGREGATE
# =============================================================================

def create_aggregate_feature(
    facility_df: pl.DataFrame,
) -> pl.DataFrame:

    logger.info("=" * 80)
    logger.info("START AGGREGATE FEATURE ENGINEERING")
    logger.info("=" * 80)

    result = None

    # -------------------------------------------------------------------------
    # RUN MODULE
    # -------------------------------------------------------------------------

    for module_name, function in AGGREGATE_MODULES:

        logger.info(

            "Create %s Aggregate",

            module_name,

        )

        agg_df = function(

            facility_df

        )

        logger.info(

            "%s Aggregate : %s rows x %s columns",

            module_name,

            agg_df.height,

            agg_df.width,

        )

        # ---------------------------------------------------------------------
        # FIRST DATASET
        # ---------------------------------------------------------------------

        if result is None:

            result = agg_df

            continue

        # ---------------------------------------------------------------------
        # DROP DUPLICATED KEY
        # ---------------------------------------------------------------------

        duplicate = [

            c

            for c in agg_df.columns

            if (

                c in result.columns

                and

                c not in DEBTOR_KEY

            )

        ]

        if duplicate:

            logger.warning(

                "%s duplicate column(s) removed from %s : %s",

                len(duplicate),

                module_name,

                duplicate,

            )

            agg_df = agg_df.drop(

                duplicate

            )

        # ---------------------------------------------------------------------
        # JOIN
        # ---------------------------------------------------------------------

        result = result.join(

            agg_df,

            on=DEBTOR_KEY,

            how="left",

        )

    logger.info("=" * 80)

    logger.info(

        "Aggregate Finished"

    )

    logger.info(

        "Rows    : %s",

        f"{result.height:,}",

    )

    logger.info(

        "Columns : %s",

        result.width,

    )

    logger.info("=" * 80)

    return result
