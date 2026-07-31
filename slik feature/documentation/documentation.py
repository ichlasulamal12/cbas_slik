"""
==============================================================================
Project : CBAS SLIK Feature Engineering
File    : documentation.py
Author  : Ichlasul Amal
Version : 1.0.0
==============================================================================

Documentation Orchestrator

"""

from datetime import datetime
from pathlib import Path
import json

import polars as pl

from config import (
    PROJECT_NAME,
    VERSION,
    FEATURE_CATALOG_FILE,
    FEATURE_CATALOG_CSV,
    FEATURE_REPORT_FILE,
    PIPELINE_INFO_FILE,
)

from documentation.feature_catalog import create_feature_catalog
from documentation.report import create_feature_report

from utils.logger import get_logger

logger = get_logger(__name__)


# =============================================================================
# DOCUMENTATION
# =============================================================================

def create_documentation(
    df: pl.DataFrame,
    output_dir: Path,
    pipeline_info: dict | None = None,
):

    logger.info("=" * 80)
    logger.info("START DOCUMENTATION")
    logger.info("=" * 80)

    output_path = Path(output_dir)

    output_path.mkdir(

        parents=True,

        exist_ok=True,

    )

    # =========================================================================
    # PIPELINE INFO
    # =========================================================================

    if pipeline_info is None:

        pipeline_info = {

            "project": PROJECT_NAME,

            "version": VERSION,

            "generated_at": datetime.now().strftime(

                "%Y-%m-%d %H:%M:%S"

            ),

            "total_records": df.height,

            "total_features": df.width,

        }

    # =========================================================================
    # FEATURE CATALOG
    # =========================================================================

    logger.info("Create Feature Catalog")

    catalog = create_feature_catalog(

        df

    )

    catalog_parquet = (

        output_path

        /

        FEATURE_CATALOG_FILE

    )

    catalog_csv = (

        output_path

        /

        FEATURE_CATALOG_CSV

    )

    catalog.write_parquet(

        catalog_parquet

    )

    catalog.write_csv(

        catalog_csv

    )

    logger.info(

        "Feature Catalog Saved"

    )

    # =========================================================================
    # FEATURE REPORT
    # =========================================================================

    logger.info(

        "Create Feature Report"

    )

    report_file = create_feature_report(

        df=df,

        catalog=catalog,

        output_dir=output_path,

        pipeline_info=pipeline_info,

    )

    logger.info(

        "Feature Report Saved"

    )

    # =========================================================================
    # PIPELINE INFO
    # =========================================================================

    pipeline_file = (

        output_path

        /

        PIPELINE_INFO_FILE

    )

    with open(

        pipeline_file,

        "w",

        encoding="utf-8",

    ) as file:

        json.dump(

            pipeline_info,

            file,

            indent=4,

            ensure_ascii=False,

        )

    logger.info(

        "Pipeline Information Saved"

    )

    logger.info("-" * 80)

    logger.info(

        "Catalog      : %s",

        catalog_csv.name,

    )

    logger.info(

        "Report       : %s",

        Path(report_file).name,

    )

    logger.info(

        "Pipeline Info: %s",

        pipeline_file.name,

    )

    logger.info("=" * 80)
    logger.info("FINISH DOCUMENTATION")
    logger.info("=" * 80)

    return {

        "catalog": catalog,

        "catalog_parquet": catalog_parquet,

        "catalog_csv": catalog_csv,

        "report": report_file,

        "pipeline_info": pipeline_file,

    }
