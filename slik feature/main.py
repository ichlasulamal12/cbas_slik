"""
==============================================================================
Project : CBAS SLIK Feature Engineering
File    : main.py
Author  : Ichlasul Amal
Version : 1.0.0
==============================================================================

Main Pipeline

"""

from datetime import datetime
import time

import polars as pl

from config import (
    PROJECT_NAME,
    VERSION,
    FACILITY_OUTPUT_DIR,
    DEBTOR_OUTPUT_DIR,
    DOCUMENTATION_DIR,
)

from loader import load_all
from validator import validate_data
from processor import create_feature_engineering
from aggregate.aggregate import create_aggregate_feature
from documentation.documentation import create_documentation

from utils.helper import create_directory
from utils.logger import (
    setup_logger,
    get_logger,
)

logger = get_logger(__name__)


# =============================================================================
# MAIN
# =============================================================================

def main():

    # =========================================================================
    # INITIALIZE
    # =========================================================================

    setup_logger()

    start_time = time.time()

    logger.info("=" * 80)
    logger.info(PROJECT_NAME)
    logger.info("Version : %s", VERSION)
    logger.info("=" * 80)

    create_directory(FACILITY_OUTPUT_DIR)
    create_directory(DEBTOR_OUTPUT_DIR)
    create_directory(DOCUMENTATION_DIR)

    # =========================================================================
    # LOAD DATASET
    # =========================================================================

    datasets = load_all()

    debtor_results = []

    total_raw_rows = 0

    total_facility_rows = 0

    total_debtor_rows = 0

    # =========================================================================
    # PROCESS
    # =========================================================================

    for index, dataset in enumerate(datasets, start=1):

        logger.info("")
        logger.info("=" * 80)
        logger.info(
            "PROCESS FILE %s OF %s",
            index,
            len(datasets),
        )
        logger.info("=" * 80)

        filename = dataset["filename"]

        logger.info(
            "File : %s",
            filename,
        )

        raw_df = dataset["data"]

        keys = dataset["keys"]

        total_raw_rows += raw_df.height

        # ---------------------------------------------------------------------
        # VALIDATION
        # ---------------------------------------------------------------------

        validated_df = validate_data(

            raw_df,

            keys,

        )

        if validated_df is None:

            logger.warning(
                "Skip file because dataset is empty: %s",
                filename,
            )

            continue        

        # ---------------------------------------------------------------------
        # FEATURE ENGINEERING
        # ---------------------------------------------------------------------

        facility_df = create_feature_engineering(

            validated_df

        )

        total_facility_rows += facility_df.height

        # ---------------------------------------------------------------------
        # AGGREGATE
        # ---------------------------------------------------------------------

        debtor_df = create_aggregate_feature(

            facility_df

        )

        total_debtor_rows += debtor_df.height

        debtor_results.append(

            debtor_df

        )

        # ---------------------------------------------------------------------
        # SAVE FACILITY
        # ---------------------------------------------------------------------

        facility_path = (

            FACILITY_OUTPUT_DIR

            /

            dataset["facility_filename"]

        )

        facility_df.write_parquet(

            facility_path

        )

        logger.info(

            "Facility Saved : %s",

            facility_path.name,

        )

        # ---------------------------------------------------------------------
        # SAVE DEBTOR
        # ---------------------------------------------------------------------

        debtor_path = (

            DEBTOR_OUTPUT_DIR

            /

            dataset["debtor_filename"]

        )

        debtor_df.write_parquet(

            debtor_path

        )

        logger.info(

            "Debtor Saved : %s",

            debtor_path.name,

        )

    # =========================================================================
    # DOCUMENTATION
    # =========================================================================

    logger.info("")
    logger.info("=" * 80)
    logger.info("GENERATE DOCUMENTATION")
    logger.info("=" * 80)

    def align_schema(dfs):

        schema = {}

        for df in dfs:

            for name, dtype in df.schema.items():

                if name not in schema:

                    schema[name] = dtype

        columns = sorted(schema.keys())

        result = []

        for df in dfs:

            missing = [

                c

                for c in columns

                if c not in df.columns

            ]

            if missing:

                df = df.with_columns(

                    [

                        pl.lit(None)

                        .cast(schema[c])

                        .alias(c)

                        for c in missing

                    ]

                )

            result.append(

                df.select(columns)

            )

        return result

    debtor_results = align_schema(
        debtor_results
    )

    all_debtor = pl.concat(
        debtor_results
    )

    pipeline_info = {

        "project": PROJECT_NAME,

        "version": VERSION,

        "generated_at": datetime.now().strftime(

            "%Y-%m-%d %H:%M:%S"

        ),

        "total_file": len(datasets),

        "raw_rows": total_raw_rows,

        "facility_rows": total_facility_rows,

        "debtor_rows": total_debtor_rows,

        "facility_features": facility_df.width,

        "debtor_features": all_debtor.width,

    }

    create_documentation(

        df=all_debtor,

        output_dir=DOCUMENTATION_DIR,

        pipeline_info=pipeline_info,

    )

    # =========================================================================
    # FINISH
    # =========================================================================

    duration = round(

        time.time() - start_time,

        2,

    )

    logger.info("")
    logger.info("=" * 80)
    logger.info("PIPELINE FINISHED")
    logger.info("=" * 80)

    logger.info(

        "Processed File : %s",

        len(datasets),

    )

    logger.info(

        "Raw Rows       : %s",

        f"{total_raw_rows:,}",

    )

    logger.info(

        "Facility Rows  : %s",

        f"{total_facility_rows:,}",

    )

    logger.info(

        "Debtor Rows    : %s",

        f"{total_debtor_rows:,}",

    )

    logger.info(

        "Duration       : %.2f second(s)",

        duration,

    )

    logger.info("=" * 80)


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":

    main()
