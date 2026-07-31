"""
==============================================================================
Project : CBAS SLIK Preprocessing
File    : processor.py
Author  : Ichlasul Amal
Version : 2.0.0
==============================================================================

Processing Pipeline
"""

import polars as pl

from config import (
    COMPANY_SEGMENT,
    INDIVIDUAL_SEGMENT,
    MODEL_OUTPUT_DIR,
    MODEL_ID_COLUMNS,
)

from loader import (
    load_application_dataset,
    load_aggregate,
    load_feature_list,
)

from preprocessing.merge import (
    merge_period,
    combine_periods,
)

from preprocessing.split import (
    split_dataset,
)

from feature_engine.feature_list import (
    feature_summary,
    valid_feature,
)

from feature_engine.binning import (
    fit as fit_binning,
    save as save_binning,
    print_information as print_binning_information,
)

from feature_engine.woe import (
    fit as fit_woe,
    transform as transform_woe,
    save as save_woe,
    print_information as print_woe_information,
)

from feature_engine.iv import (
    build_iv_table,
    select_feature,
    print_information as print_iv_information,
)

from utils.date_utils import (
    process_periods,
)

# =============================================================================
# PROCESS
# =============================================================================

def process() -> dict:
    """
    Complete preprocessing pipeline.
    """

    # -------------------------------------------------------------------------
    # LOAD APPLICATION DATASET
    # -------------------------------------------------------------------------

    print()

    print("=" * 80)
    print("LOAD APPLICATION DATASET")
    print("=" * 80)

    (
        company_application,
        individual_application,
    ) = load_application_dataset()

    feature_list = load_feature_list()

    # -------------------------------------------------------------------------
    # MERGE ALL PERIOD
    # -------------------------------------------------------------------------

    print()

    print("=" * 80)
    print("MERGE DATASET")
    print("=" * 80)

    merged_periods = []

    for period in process_periods():

        print(

            f"Processing Aggregate "

            f"{period} ..."

        )

        # -------------------------------------------------------------
        # COMPANY
        # -------------------------------------------------------------

        try:

            company = load_aggregate(

                period,

                COMPANY_SEGMENT,

            )

        except FileNotFoundError:

            company = pl.DataFrame()

        # -------------------------------------------------------------
        # INDIVIDUAL
        # -------------------------------------------------------------

        try:

            individual = load_aggregate(

                period,

                INDIVIDUAL_SEGMENT,

            )

        except FileNotFoundError:

            individual = pl.DataFrame()

        # -------------------------------------------------------------
        # MERGE
        # -------------------------------------------------------------

        merged = merge_period(

            period=period,

            company_aggregate=company,

            individual_aggregate=individual,

            company_application=company_application,

            individual_application=individual_application,

        )

        if merged.height > 0:

            merged_periods.append(

                merged,

            )

    # -------------------------------------------------------------------------
    # VALIDATE
    # -------------------------------------------------------------------------

    if len(merged_periods) == 0:

        raise RuntimeError(

            "No merged dataset."

        )

    # -------------------------------------------------------------------------
    # COMBINE
    # -------------------------------------------------------------------------

    merged = combine_periods(

        merged_periods,

    )

    print()

    print(

        f"Total Observation : "

        f"{merged.height:,}"

    )

    print(

        f"Total Variable    : "

        f"{merged.width:,}"

    )

    # -------------------------------------------------------------------------
    # SPLIT DATASET
    # -------------------------------------------------------------------------

    print()

    print("=" * 80)
    print("SPLIT DATASET")
    print("=" * 80)

    development, oot = split_dataset(

        merged,

    )

    print()

    print(

        f"Development : "

        f"{development.height:,} rows"

    )

    print(

        f"OOT         : "

        f"{oot.height:,} rows"

    )

    # -------------------------------------------------------------------------
    # COPY RAW DATASET
    # -------------------------------------------------------------------------

    development_raw = development.clone()

    if oot.height > 0:

        oot_raw = oot.clone()

    else:

        oot_raw = pl.DataFrame()

    # -------------------------------------------------------------------------
    # FEATURE LIST
    # -------------------------------------------------------------------------

    print()

    print("=" * 80)
    print("FEATURE SELECTION")
    print("=" * 80)

    feature_summary(

        development,

        feature_list,

    )

    feature_list = valid_feature(

        development,

        feature_list,

    )

    print(

        f"Valid Feature : "

        f"{len(feature_list):,}"

    )

    # -------------------------------------------------------------------------
    # BINNING
    # -------------------------------------------------------------------------

    print()

    print("=" * 80)
    print("FIT BINNING")
    print("=" * 80)

    binning_model = fit_binning(

        development,

        feature_list,

    )

    print_binning_information(

        binning_model,

    )

    save_binning(

        binning_model,

        MODEL_OUTPUT_DIR,

    )

    # -------------------------------------------------------------------------
    # WOE
    # -------------------------------------------------------------------------

    print()

    print("=" * 80)
    print("FIT WOE")
    print("=" * 80)

    (
        woe_model,
        woe_table,
    ) = fit_woe(

        development,

        binning_model,

    )

    print_woe_information(

        woe_model,

    )

    save_woe(

        woe_model,

        MODEL_OUTPUT_DIR,

    )

    # -------------------------------------------------------------------------
    # TRANSFORM DEVELOPMENT
    # -------------------------------------------------------------------------

    print()

    print("=" * 80)
    print("TRANSFORM DEVELOPMENT")
    print("=" * 80)

    development_woe = transform_woe(

        development,

        binning_model,

        woe_model,

    )

    # -------------------------------------------------------------------------
    # TRANSFORM OOT
    # -------------------------------------------------------------------------

    if oot.height > 0:

        print()

        print("=" * 80)
        print("TRANSFORM OOT")
        print("=" * 80)

        oot_woe = transform_woe(

            oot,

            binning_model,

            woe_model,

        )

    else:

        oot_woe = pl.DataFrame()

    # -------------------------------------------------------------------------
    # INFORMATION VALUE
    # -------------------------------------------------------------------------

    print()

    print("=" * 80)
    print("INFORMATION VALUE")
    print("=" * 80)

    iv_table = build_iv_table(

        woe_model,

    )

    selected_feature = select_feature(

        iv_table,

    )

    print_iv_information(

        iv_table,

    )

    # -------------------------------------------------------------------------
    # FINAL COLUMN
    # -------------------------------------------------------------------------

    columns = MODEL_ID_COLUMNS + selected_feature

    # -------------------------------------------------------------------------
    # RAW DATASET
    # -------------------------------------------------------------------------

    development_raw = development_raw.select(

        [

            column

            for column in columns

            if column in development_raw.columns

        ]

    )

    if oot_raw.height > 0:

        oot_raw = oot_raw.select(

            [

                column

                for column in columns

                if column in oot_raw.columns

            ]

        )

    # -------------------------------------------------------------------------
    # WOE DATASET
    # -------------------------------------------------------------------------

    development_woe = development_woe.select(

        [

            column

            for column in columns

            if column in development_woe.columns

        ]

    )

    if oot_woe.height > 0:

        oot_woe = oot_woe.select(

            [

                column

                for column in columns

                if column in oot_woe.columns

            ]

        )

    # -------------------------------------------------------------------------
    # PROCESS COMPLETED
    # -------------------------------------------------------------------------

    print()

    print("=" * 80)
    print("PROCESS COMPLETED")
    print("=" * 80)

    print()

    print(

        f"Selected Feature : "

        f"{len(selected_feature):,}"

    )

    print(

        f"Development Row  : "

        f"{development_woe.height:,}"

    )

    print(

        f"OOT Row          : "

        f"{oot_woe.height:,}"

    )

    # -------------------------------------------------------------------------
    # RETURN
    # -------------------------------------------------------------------------

    return {

        "development_raw": development_raw,

        "development_woe": development_woe,

        "oot_raw": oot_raw,

        "oot_woe": oot_woe,

        "binning_model": binning_model,

        "woe_model": woe_model,

        "woe_table": woe_table,

        "iv_table": iv_table,

        "selected_feature": selected_feature,

    }
