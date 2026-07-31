"""
==============================================================================
Project : CBAS SLIK Feature Engineering
File    : processor.py
Author  : Ichlasul Amal
Version : 1.0.0
==============================================================================

Feature Engineering Orchestrator

"""

from utils.logger import get_logger

from feature_engine.basic import create_basic_feature
from feature_engine.facility import create_facility_feature
from feature_engine.exposure import create_exposure_feature
from feature_engine.utilization import create_utilization_feature
from feature_engine.delinquency import create_delinquency_feature
from feature_engine.restructuring import create_restructuring_feature
from feature_engine.tenor import create_tenor_feature
from feature_engine.interest import create_interest_feature

from feature_engine.history_statistics import (
    create_history_statistics_feature,
)

from feature_engine.history_count import (
    create_history_count_feature,
)

from feature_engine.history_transition import (
    create_history_transition_feature,
)

from feature_engine.history_streak import (
    create_history_streak_feature,
)

from feature_engine.ratio import create_ratio_feature

logger = get_logger(__name__)


# =============================================================================
# FEATURE ENGINEERING
# =============================================================================

def create_feature_engineering(df):

    logger.info("=" * 80)
    logger.info("START FEATURE ENGINEERING")
    logger.info("=" * 80)

    modules = [

        ("Basic", create_basic_feature),

        ("Facility", create_facility_feature),

        ("Exposure", create_exposure_feature),

        ("Utilization", create_utilization_feature),

        ("Delinquency", create_delinquency_feature),

        ("Restructuring", create_restructuring_feature),

        ("Tenor", create_tenor_feature),

        ("Interest", create_interest_feature),

        ("History Statistics", create_history_statistics_feature),

        ("History Count", create_history_count_feature),

        ("History Transition", create_history_transition_feature),

        ("History Streak", create_history_streak_feature),

        ("Ratio", create_ratio_feature),

    ]

    for module_name, function in modules:

        logger.info("Create %s Feature", module_name)

        before = df.width

        df = function(df)

        after = df.width

        logger.info(

            "%s Feature : +%s column(s)",

            module_name,

            after - before,

        )

    logger.info("-" * 80)

    logger.info(

        "Total Feature : %s",

        df.width,

    )

    logger.info("=" * 80)

    logger.info("FINISH FEATURE ENGINEERING")

    logger.info("=" * 80)

    return df
