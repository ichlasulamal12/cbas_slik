"""
==============================================================================
Project : CBAS SLIK Preprocessing
File    : config.py
Author  : Ichlasul Amal
Version : 2.0.0
==============================================================================

Configuration
"""

from pathlib import Path

# =============================================================================
# PROJECT
# =============================================================================

PROJECT_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = PROJECT_DIR / "output"

# =============================================================================
# INPUT DIRECTORY
# =============================================================================

APPLICATION_DIR = Path("D:/Development/v2/Data/dataset")
AGGREGATE_DIR = Path("D:/Development/CBAS_SLIK_FEATURE/output/debtor")
FEATURE_DIR = Path("D:/Development/CBAS_SLIK_PREPROCESSING_V2")


# =============================================================================
# OUTPUT DIRECTORY
# =============================================================================

DATASET_OUTPUT_DIR = OUTPUT_DIR / "dataset"

MODEL_OUTPUT_DIR = OUTPUT_DIR / "model"

TABLE_OUTPUT_DIR = OUTPUT_DIR / "table"

SUMMARY_OUTPUT_DIR = OUTPUT_DIR / "summary"

# =============================================================================
# APPLICATION DATASET
# =============================================================================

COMPANY_APPLICATION_FILE = (

    APPLICATION_DIR /

    "dataset company 012022_052026.xlsx"

)

INDIVIDUAL_APPLICATION_FILE = (

    APPLICATION_DIR /

    "dataset individual all 012022_052026.xlsx"

)

# =============================================================================
# FEATURE LIST
# =============================================================================

FEATURE_LIST_FILE = (

    FEATURE_DIR /

    "feature_list.xlsx"

)

FEATURE_NAME_COLUMN = "Variable"

FEATURE_USE_COLUMN = "Use"

FEATURE_USE_VALUE = "Y"

FEATURE_TYPE_COLUMN = "Type"

# =============================================================================
# AGGREGATE
# =============================================================================

AGGREGATE_PREFIX = "Debitur"

COMPANY_SEGMENT = "Company"

INDIVIDUAL_SEGMENT = "Individual"

# =============================================================================
# PROCESS PERIOD
# =============================================================================

PROCESS_START_PERIOD = "202301"

PROCESS_END_PERIOD = "202512"

# =============================================================================
# DATA SPLIT
# =============================================================================

DEVELOPMENT_END_PERIOD = "202505"

OOT_START_PERIOD = "202506"

# =============================================================================
# COLUMN
# =============================================================================

IDLIMIT_COLUMN = "IDLimit"

CIF_COLUMN = "CIF"

DATE_COLUMN = "TglMulai"

TARGET_COLUMN = "flag_30_12MoB"

SEGMENT_COLUMN = "SEGMENT"

SNAPSHOT_COLUMN = "SNAPSHOT_PERIOD"

SNAPSHOT_DATE_COLUMN = "SNAPSHOT_DATE"

# =============================================================================
# IDENTIFIER
# =============================================================================

COMPANY_AGGREGATE_KEY = "npwp"

INDIVIDUAL_AGGREGATE_KEY = "ktp"

COMPANY_APPLICATION_KEY = "NPWP"

INDIVIDUAL_APPLICATION_KEY = "Identity Number"

# =============================================================================
# APPLICATION COLUMN
# =============================================================================

APPLICATION_COLUMNS = [

    IDLIMIT_COLUMN,

    CIF_COLUMN,

    DATE_COLUMN,

    COMPANY_APPLICATION_KEY,

    INDIVIDUAL_APPLICATION_KEY,

    TARGET_COLUMN,

]

# =============================================================================
# FEATURE ENGINEERING
# =============================================================================

MAX_BINS = 6

MIN_BIN_SIZE = 0.05

IV_THRESHOLD = 0.02

WOE_SMOOTHING = 0.05

VIF_THRESHOLD = 10.0

# =============================================================================
# MODEL
# =============================================================================

BINNING_MODEL_FILE = "binning_model.pkl"

WOE_MODEL_FILE = "woe_model.pkl"

# =============================================================================
# RANDOM
# =============================================================================

RANDOM_STATE = 12345

# =============================================================================
# FILE FORMAT
# =============================================================================

PARQUET_EXTENSION = ".parquet"

EXCEL_EXTENSION = ".xlsx"

# =============================================================================
# LOGGING
# =============================================================================

LOG_SEPARATOR = "=" * 80

SUB_SEPARATOR = "-" * 80

MODEL_ID_COLUMNS = [

    IDLIMIT_COLUMN,

    CIF_COLUMN,

    DATE_COLUMN,

    SEGMENT_COLUMN,

    SNAPSHOT_COLUMN,

    TARGET_COLUMN,

]
