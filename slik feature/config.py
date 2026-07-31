"""
===============================================================================
Project     : CBAS SLIK Feature Engineering
File        : config.py
Author      : Ichlasul Amal
Description : Global Configuration
Version     : 1.0.0
===============================================================================
"""

from pathlib import Path

# =============================================================================
# PROJECT
# =============================================================================

PROJECT_NAME = "CBAS SLIK Feature Engineering"

VERSION = "1.0.0"

AUTHOR = "Ichlasul Amal"

DESCRIPTION = (
    "Feature Engineering Library for OJK SLIK Data"
)

# =============================================================================
# DIRECTORY
# =============================================================================

BASE_DIR = Path(__file__).resolve().parent

INPUT_DIR = Path(
    r"D:\Development\cbasslik\v2\Fasilitas Kredit Filter - Copy"
)

OUTPUT_DIR = BASE_DIR / "output"

# =============================================================================
# OUTPUT DIRECTORY
# =============================================================================

FACILITY_OUTPUT_DIR = OUTPUT_DIR / "facility"

DEBTOR_OUTPUT_DIR = OUTPUT_DIR / "debtor"

DOCUMENTATION_DIR = OUTPUT_DIR / "documentation"

REPORT_DIR = OUTPUT_DIR / "report"

LOG_DIR = OUTPUT_DIR / "log"

TEMP_DIR = OUTPUT_DIR / "temp"

CACHE_DIR = OUTPUT_DIR / "cache"

EXPORT_DIR = OUTPUT_DIR / "export"

DIRECTORIES = [

    OUTPUT_DIR,

    FACILITY_OUTPUT_DIR,

    DEBTOR_OUTPUT_DIR,

    DOCUMENTATION_DIR,

    REPORT_DIR,

    LOG_DIR,

    TEMP_DIR,

    CACHE_DIR,

    EXPORT_DIR,

]

for directory in DIRECTORIES:

    directory.mkdir(

        parents=True,

        exist_ok=True,

    )

# =============================================================================
# INPUT
# =============================================================================

FILE_EXTENSION = ".parquet"

RECURSIVE_SEARCH = False

OVERWRITE_OUTPUT = True

SAVE_INTERMEDIATE = False

# =============================================================================
# DOCUMENTATION
# =============================================================================

FEATURE_CATALOG_FILE = "feature_catalog.parquet"

FEATURE_CATALOG_CSV = "feature_catalog.csv"

FEATURE_REPORT_FILE = "feature_report.xlsx"

PIPELINE_INFO_FILE = "pipeline_info.json"

# =============================================================================
# PIPELINE
# =============================================================================

PIPELINE_NAME = PROJECT_NAME

PIPELINE_VERSION = VERSION

ENVIRONMENT = "Development"

LOG_LEVEL = "INFO"

# =============================================================================
# FILE PATTERN
# =============================================================================

COMPANY_PATTERN = [

    "company",

    "corporate",

]

INDIVIDUAL_PATTERN = [

    "individual",

    "retail",

    "personal",

]

# =============================================================================
# KEY
# =============================================================================

# =============================================================================
# PRIMARY KEY
# =============================================================================

FACILITY_KEY = [

    "appno",

    "productid",

]

DEBTOR_KEY = [

    "appno",

]

INDIVIDUAL_KEYS = [

    "appno",

    "ktp",

]

COMPANY_KEYS = [

    "appno",

    "npwp",

]

# =============================================================================
# REQUIRED COLUMN
# =============================================================================

REQUIRED_COLUMNS = [

    "appno",

    "namaDebitur",

    "bakiDebet",

    "plafon",

    "kolektibilitas",

    "jumlahHariTunggakan",

    "tanggalUpdate",

]

# =============================================================================
# NUMERIC COLUMN
# =============================================================================

NUMERIC_COLUMNS = [

    "bakiDebet",

    "plafon",

    "plafonAwal",

    "angsuran",

    "jumlahHariTunggakan",

    "kolektibilitas",

    "tunggakanPokok",

    "tunggakanBunga",

    "denda",

    "frekuensiRestrukturisasi",

    "nilaiProyek",

    "realisasiBulanBerjalan",

    "nilaiDalamMataUangAsal",

    "sukuBunga",

]

# =============================================================================
# DATE COLUMN
# =============================================================================

DATE_COLUMNS = [

    "tanggalDibentuk",

    "tanggalUpdate",

    "tanggalAkadAwal",

    "tanggalAkadAkhir",

    "tanggalAwalKredit",

    "tanggalMulai",

    "tanggalJatuhTempo",

    "tanggalMacet",

    "tanggalRestrukturisasiAkhir",

    "tanggalKondisi",

]

# =============================================================================
# STRING COLUMN
# =============================================================================

STRING_COLUMNS = [

    "namaDebitur",

    "ljk",

    "ljkKet",

    "cabang",

    "jenisKredit",

    "akadPembiayaan",

    "jenisPenggunaan",

    "sektorEkonomi",

    "kodeValuta",

    "CreditType",

]

# =============================================================================
# HISTORY CONFIGURATION
# =============================================================================

# Total histori tersedia pada data SLIK
HISTORY_MONTH = 24

# =============================================================================
# HISTORY WINDOW
# =============================================================================

HISTORY_WINDOWS = [

    3,

    6,

    12,

    24,

]

HISTORY_WINDOW_NAME = {

    3: "recent",

    6: "short",

    12: "medium",

    24: "long",

}

# Rolling window
ROLLING_WINDOWS = [

    3,

    6,

    12,

    24,

]

# =============================================================================
# HISTORY COLUMN
# =============================================================================

KOL_COLUMNS = [

    f"tahunBulan{i:02d}Kol"

    for i in range(

        1,

        HISTORY_MONTH + 1

    )

]

HT_COLUMNS = [

    f"tahunBulan{i:02d}Ht"

    for i in range(

        1,

        HISTORY_MONTH + 1

    )

]

PERIOD_COLUMNS = [

    f"tahunBulan{i:02d}"

    for i in range(

        1,

        HISTORY_MONTH + 1

    )

]

# =============================================================================
# HISTORY FEATURE
# =============================================================================

ENABLE_HISTORY_STATISTICS = True

ENABLE_HISTORY_COUNT = True

ENABLE_HISTORY_RATIO = True

ENABLE_HISTORY_TRANSITION = True

ENABLE_HISTORY_WEIGHTED = True

ENABLE_HISTORY_TREND = True

ENABLE_HISTORY_STREAK = True

ENABLE_HISTORY_RECENCY = True

ENABLE_HISTORY_NORMALIZED = True

# =============================================================================
# HISTORY WINDOW
# =============================================================================

SHORT_WINDOW = 6

MEDIUM_WINDOW = 12

LONG_WINDOW = 24

# =============================================================================
# HISTORY THRESHOLD
# =============================================================================

RECENCY_KOL = [

    2,

    3,

    4,

    5,

]

RECENCY_DPD = [

    30,

    60,

    90,

    120,

    180,

]

STREAK_THRESHOLD = [

    2,

    3,

    4,

    5,

]

DPD_STREAK = [

    30,

    60,

    90,

    120,

    180,

]

# =============================================================================
# WEIGHTED HISTORY
# =============================================================================

LINEAR_WEIGHT = list(

    range(

        HISTORY_MONTH,

        0,

        -1,

    )

)

EXPONENTIAL_ALPHA = 0.90

# =============================================================================
# TREND
# =============================================================================

TREND_WINDOWS = [

    3,

    6,

    12,

    24,

]

# =============================================================================
# CURRENT FEATURE
# =============================================================================

CURRENT_COLUMNS = [

    "kolektibilitas",

    "jumlahHariTunggakan",

    "bakiDebet",

    "plafon",

    "plafonAwal",

    "angsuran",

    "tunggakanPokok",

    "tunggakanBunga",

    "denda",

    "frekuensiRestrukturisasi",

    "sukuBunga",

]

# =============================================================================
# FLAG FEATURE
# =============================================================================

FLAG_COLUMNS = [

    "flag_active",

    "flag_closed",

    "flag_restruktur",

    "flag_default_current",

    "flag_dpd",

    "flag_dpd30",

    "flag_dpd60",

    "flag_dpd90",

    "flag_dpd120",

    "flag_dpd180",

    "flag_kol2",

    "flag_kol3",

    "flag_kol4",

    "flag_kol5",

    "flag_new_loan",

    "flag_near_maturity",

    "flag_matured",

    "flag_high_interest",

    "flag_very_high_interest",

]

# =============================================================================
# CATEGORY FEATURE
# =============================================================================

CATEGORY_ENGINE = {

    "ljk":{

        "prefix":"ljk"

    },

    "cabang":{

        "prefix":"cabang"

    },

    "jenisKredit":{

        "prefix":"jenis_kredit"

    },

    "jenisPenggunaan":{

        "prefix":"penggunaan"

    },

    "akadPembiayaan":{

        "prefix":"akad"

    },

    "sektorEkonomi":{

        "prefix":"sektor"

    },

    "kodeValuta":{

        "prefix":"valuta"

    },

    "CreditType":{

        "prefix":"credit_type"

    },

}

# =============================================================================
# FEATURE REGISTRY
# =============================================================================

FEATURE_REGISTRY = {

    # =====================================================================
    # EXPOSURE
    # =====================================================================

    "bakiDebet": {

        "enabled": True,

        "display_name": "Outstanding Balance",

        "description": "Current outstanding balance.",

        "module": "Exposure",

        "category": "Exposure",

        "level": "Facility",

        "prefix": "os",

        "datatype": "Float",

        "unit": "Currency",

        "statistics": [

            "sum",

            "mean",

            "median",

            "max",

            "min",

            "std",

            "var",

            "range",

            "cv",

            "p25",

            "p75",

            "p90",

            "p95",

        ],

    },

    "plafon": {

        "enabled": True,

        "display_name": "Current Credit Limit",

        "description": "Current approved credit limit.",

        "module": "Exposure",

        "category": "Exposure",

        "level": "Facility",

        "prefix": "limit",

        "datatype": "Float",

        "unit": "Currency",

        "statistics": [

            "sum",

            "mean",

            "median",

            "max",

            "min",

            "std",

            "var",

            "range",

            "cv",

            "p25",

            "p75",

            "p90",

            "p95",

        ],

    },

    "plafonAwal": {

        "enabled": True,

        "display_name": "Original Credit Limit",

        "description": "Original approved credit limit.",

        "module": "Exposure",

        "category": "Exposure",

        "level": "Facility",

        "prefix": "original_limit",

        "datatype": "Float",

        "unit": "Currency",

        "statistics": [

            "sum",

            "mean",

            "median",

            "max",

            "min",

            "std",

        ],

    },

    "angsuran": {

        "enabled": True,

        "display_name": "Installment",

        "description": "Monthly installment.",

        "module": "Exposure",

        "category": "Installment",

        "level": "Facility",

        "prefix": "installment",

        "datatype": "Float",

        "unit": "Currency",

        "statistics": [

            "sum",

            "mean",

            "median",

            "max",

            "min",

            "std",

        ],

    },

    # =====================================================================
    # INTEREST
    # =====================================================================

    "sukuBunga": {

        "enabled": True,

        "display_name": "Interest Rate",

        "description": "Contract interest rate.",

        "module": "Interest",

        "category": "Interest",

        "level": "Facility",

        "prefix": "interest",

        "datatype": "Float",

        "unit": "Percent",

        "statistics": [

            "mean",

            "median",

            "max",

            "min",

            "std",

        ],

    },

    # =====================================================================
    # DELINQUENCY
    # =====================================================================

    "kolektibilitas": {

        "enabled": True,

        "display_name": "Current KOL",

        "description": "Current collectibility status.",

        "module": "Delinquency",

        "category": "Current",

        "level": "Facility",

        "prefix": "kol",

        "datatype": "Integer",

        "unit": "Level",

        "statistics": [

            "mean",

            "median",

            "max",

            "min",

            "std",

        ],

    },

    "jumlahHariTunggakan": {

        "enabled": True,

        "display_name": "Current Days Past Due",

        "description": "Current DPD.",

        "module": "Delinquency",

        "category": "Current",

        "level": "Facility",

        "prefix": "dpd",

        "datatype": "Integer",

        "unit": "Day",

        "statistics": [

            "mean",

            "median",

            "max",

            "min",

            "std",

            "var",

            "range",

            "p90",

            "p95",

        ],

    },

    "tunggakanPokok": {

        "enabled": True,

        "display_name": "Principal Overdue",

        "description": "Principal overdue amount.",

        "module": "Delinquency",

        "category": "Overdue",

        "level": "Facility",

        "prefix": "principal_overdue",

        "datatype": "Float",

        "unit": "Currency",

        "statistics": [

            "sum",

            "mean",

            "max",

            "std",

        ],

    },

    "tunggakanBunga": {

        "enabled": True,

        "display_name": "Interest Overdue",

        "description": "Interest overdue amount.",

        "module": "Delinquency",

        "category": "Overdue",

        "level": "Facility",

        "prefix": "interest_overdue",

        "datatype": "Float",

        "unit": "Currency",

        "statistics": [

            "sum",

            "mean",

            "max",

            "std",

        ],

    },

    "denda": {

        "enabled": True,

        "display_name": "Penalty",

        "description": "Penalty amount.",

        "module": "Delinquency",

        "category": "Overdue",

        "level": "Facility",

        "prefix": "penalty",

        "datatype": "Float",

        "unit": "Currency",

        "statistics": [

            "sum",

            "mean",

            "max",

            "std",

        ],

    },

    # =====================================================================
    # RESTRUCTURING
    # =====================================================================

    "frekuensiRestrukturisasi": {

        "enabled": True,

        "display_name": "Restructuring Frequency",

        "description": "Number of restructuring events.",

        "module": "Restructuring",

        "category": "Restructuring",

        "level": "Facility",

        "prefix": "restruktur",

        "datatype": "Integer",

        "unit": "Count",

        "statistics": [

            "sum",

            "mean",

            "max",

        ],

    },

}

AGGREGATE_NUMERIC_COLUMNS = [

    # Exposure
    "bakiDebet",
    "plafon",
    "plafonAwal",

    # Utilization
    "utilization",

    # Interest
    "interest_rate",

    # Delinquency
    "jumlahHariTunggakan",
    "total_overdue",

    # Tenor
    "credit_age_days",
    "remaining_tenor_days",

]

FLAG_COLUMNS = [

    # Delinquency
    "flag_kol2",
    "flag_kol3",
    "flag_kol4",
    "flag_kol5",

    "flag_dpd30",
    "flag_dpd60",
    "flag_dpd90",

    # Default
    "flag_default_current",

    # Restructuring
    "flag_restruktur",

    # Exposure
    "flag_overlimit",

]

AGGREGATE_SUM_COLUMNS = [

    "bakiDebet",

    "plafon",

    "plafonAwal",

    "total_overdue",

]

AGGREGATE_MAX_COLUMNS = [

    "bakiDebet",

    "plafon",

    "plafonAwal",

    "utilization",

    "interest_rate",

    "jumlahHariTunggakan",

    "total_overdue",

    "credit_age_days",

    "remaining_tenor_days",

]
