"""
==============================================================================
Project : CBAS SLIK Feature Engineering
File    : common.py
Author  : Ichlasul Amal
Version : 1.0.0
==============================================================================

Common Constants

"""

# =============================================================================
# BOOLEAN
# =============================================================================

YES = "Y"
NO = "N"

TRUE = 1
FALSE = 0


# =============================================================================
# STATUS
# =============================================================================

STATUS_ACTIVE = "ACTIVE"
STATUS_CLOSED = "CLOSED"

STATUS_SUCCESS = "SUCCESS"
STATUS_FAILED = "FAILED"
STATUS_WARNING = "WARNING"


# =============================================================================
# DATA TYPE
# =============================================================================

NUMERIC_TYPES = [

    "Int8",
    "Int16",
    "Int32",
    "Int64",

    "UInt8",
    "UInt16",
    "UInt32",
    "UInt64",

    "Float32",
    "Float64",

]

INTEGER_TYPES = [

    "Int8",
    "Int16",
    "Int32",
    "Int64",

    "UInt8",
    "UInt16",
    "UInt32",
    "UInt64",

]

FLOAT_TYPES = [

    "Float32",
    "Float64",

]

STRING_TYPES = [

    "String",

]

DATE_TYPES = [

    "Date",

]

DATETIME_TYPES = [

    "Datetime",

]


# =============================================================================
# FEATURE LEVEL
# =============================================================================

LEVEL_FACILITY = "Facility"

LEVEL_DEBTOR = "Debtor"


# =============================================================================
# FEATURE CATEGORY
# =============================================================================

CATEGORY_BASIC = "Basic"

CATEGORY_FACILITY = "Facility"

CATEGORY_EXPOSURE = "Exposure"

CATEGORY_UTILIZATION = "Utilization"

CATEGORY_DELINQUENCY = "Delinquency"

CATEGORY_RESTRUCTURING = "Restructuring"

CATEGORY_TENOR = "Tenor"

CATEGORY_INTEREST = "Interest"

CATEGORY_HISTORY = "History"

CATEGORY_RATIO = "Ratio"

CATEGORY_CROSS = "Cross"

CATEGORY_AGGREGATE = "Aggregate"


# =============================================================================
# DOCUMENTATION
# =============================================================================

REPORT_NAME = "feature_report.xlsx"

FEATURE_CATALOG = "feature_catalog.csv"

FEATURE_CATALOG_PARQUET = "feature_catalog.parquet"


# =============================================================================
# PIPELINE
# =============================================================================

PIPELINE_LOAD = "Load"

PIPELINE_VALIDATE = "Validate"

PIPELINE_FEATURE = "Feature Engineering"

PIPELINE_AGGREGATE = "Aggregate"

PIPELINE_DOCUMENTATION = "Documentation"

PIPELINE_SAVE = "Save"


# =============================================================================
# HISTORY
# =============================================================================

WINDOW_24 = 24
WINDOW_12 = 12
WINDOW_6 = 6


# =============================================================================
# DELINQUENCY
# =============================================================================

KOL_GOOD = 1

KOL_SPECIAL = 2

KOL_SUBSTANDARD = 3

KOL_DOUBTFUL = 4

KOL_LOSS = 5
