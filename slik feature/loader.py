"""
==============================================================================
Project : CBAS SLIK Feature Engineering
File    : loader.py
Author  : Ichlasul Amal
Version : 1.0.0
==============================================================================

Data Loader

"""

from pathlib import Path

import polars as pl

from config import (
    INPUT_DIR,
    FILE_EXTENSION,
    RECURSIVE_SEARCH,
    INDIVIDUAL_KEYS,
    COMPANY_KEYS,
)

from utils.logger import get_logger

logger = get_logger(__name__)


# =============================================================================
# GET PARQUET FILES
# =============================================================================

def get_parquet_files() -> list[Path]:
    """
    Get all parquet files from input directory.
    """

    logger.info("Searching parquet files...")

    if RECURSIVE_SEARCH:

        files = sorted(

            INPUT_DIR.rglob(

                f"*{FILE_EXTENSION}"

            )

        )

    else:

        files = sorted(

            INPUT_DIR.glob(

                f"*{FILE_EXTENSION}"

            )

        )

    if len(files) == 0:

        raise FileNotFoundError(

            f"No parquet file found in\n{INPUT_DIR}"

        )

    logger.info(

        "%s parquet file(s) found.",

        len(files),

    )

    return files


# =============================================================================
# LOAD PARQUET
# =============================================================================

def load_parquet(file_path: Path) -> pl.DataFrame:
    """
    Load parquet file.
    """

    logger.info(

        "Loading : %s",

        file_path.name,

    )

    return pl.read_parquet(file_path)


# =============================================================================
# DETECT SEGMENT
# =============================================================================

def detect_segment(df: pl.DataFrame):
    """
    Detect Company / Individual.
    """

    columns = set(df.columns)

    if "ktp" in columns:

        return (

            "Individual",

            INDIVIDUAL_KEYS,

        )

    if "npwp" in columns:

        return (

            "Company",

            COMPANY_KEYS,

        )

    raise ValueError(

        "Cannot determine segment. Column 'ktp' or 'npwp' not found."

    )


# =============================================================================
# DATA INFO
# =============================================================================

def data_info(df: pl.DataFrame):

    return {

        "rows": df.height,

        "columns": df.width,

        "memory_mb": round(

            df.estimated_size("mb"),

            2,

        ),

        "column_names": df.columns,

    }


# =============================================================================
# LOAD DATASET
# =============================================================================

def load_dataset(file_path: Path):

    df = load_parquet(file_path)

    segment, keys = detect_segment(df)

    info = data_info(df)

    # -------------------------------------------------------------------------
    # Output Filename
    # -------------------------------------------------------------------------

    facility_filename = file_path.name

    debtor_filename = (

        file_path.name

        .replace(

            "FasilitasKredit",

            "Debitur",

        )

    )

    logger.info(

        "Segment : %s",

        segment,

    )

    logger.info(

        "Rows    : %s",

        f"{info['rows']:,}",

    )

    logger.info(

        "Columns : %s",

        info["columns"],

    )

    logger.info(

        "Memory  : %.2f MB",

        info["memory_mb"],

    )

    return {

        # ---------------------------------------------------------------------
        # File
        # ---------------------------------------------------------------------

        "filename": facility_filename,

        "filepath": file_path,

        "facility_filename": facility_filename,

        "debtor_filename": debtor_filename,

        # ---------------------------------------------------------------------
        # Dataset
        # ---------------------------------------------------------------------

        "segment": segment,

        "keys": keys,

        "data": df,

        # ---------------------------------------------------------------------
        # Information
        # ---------------------------------------------------------------------

        "rows": info["rows"],

        "columns": info["columns"],

        "memory_mb": info["memory_mb"],

    }


# =============================================================================
# LOAD ALL
# =============================================================================

def load_all():

    logger.info(

        "=" * 80

    )

    logger.info(

        "LOAD DATASET"

    )

    logger.info(

        "=" * 80

    )

    files = get_parquet_files()

    datasets = []

    total_rows = 0

    for file in files:

        dataset = load_dataset(

            file

        )

        datasets.append(

            dataset

        )

        total_rows += dataset["rows"]

    logger.info(

        "-" * 80

    )

    logger.info(

        "Total File : %s",

        len(datasets),

    )

    logger.info(

        "Total Rows : %s",

        f"{total_rows:,}",

    )

    logger.info(

        "=" * 80

    )

    return datasets
