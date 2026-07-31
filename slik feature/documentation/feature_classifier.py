"""
==============================================================================
Project : CBAS SLIK Feature Engineering
File    : feature_classifier.py
Author  : Ichlasul Amal
Version : 2.0.0
==============================================================================

Feature Classifier

Automatic feature classification.

"""

# =============================================================================
# MODULE
# =============================================================================

MODULE_RULES = {

    "Aggregate": (

        "sum_",
        "mean_",
        "max_",
        "min_",
        "std_",
        "nunique_",
        "facility_count",

    ),

    "History": (

        "hist",

    ),

    "Ratio": (

        "ratio_",

    ),

    "Flag": (

        "flag_",

    ),

    "Basic": (

        "utilization",
        "credit_age",
        "remaining_tenor",
        "interest_rate",
        "tenor_bucket",
        "kol_bucket",
        "dpd_bucket",

    ),

}


# =============================================================================
# CATEGORY
# =============================================================================

CATEGORY_RULES = {

    "Sum": ("sum_",),

    "Mean": ("mean_",),

    "Maximum": ("max_",),

    "Minimum": ("min_",),

    "Standard Deviation": ("std_",),

    "Unique Count": ("nunique_",),

    "Ratio": ("ratio_",),

    "Flag": ("flag_",),

    "History": ("hist",),

    "Count": ("count",),

    "Bucket": ("bucket",),

}


# =============================================================================
# DOMAIN
# =============================================================================

DOMAIN_RULES = {

    "Exposure": (

        "plafon",
        "baki",
        "os",
        "limit",
        "util",
        "drawdown",
        "unused",
        "available",
        "overlimit",

    ),

    "Delinquency": (

        "kol",
        "dpd",
        "delinq",
        "severity",
        "overdue",

    ),

    "Restructuring": (

        "restruktur",
        "restructure",

    ),

    "Interest": (

        "interest",
        "bunga",
        "rate",

    ),

    "Tenor": (

        "tenor",
        "credit_age",
        "remaining",
        "maturity",
        "umur",

    ),

    "History": (

        "hist",

    ),

    "Customer": (

        "gender",
        "umurDebitur",
        "tanggalLahir",
        "jenisKelamin",
        "pekerjaan",
        "debitur",

    ),

}


# =============================================================================
# LEVEL
# =============================================================================

def get_level(
    feature: str,
) -> str:

    if feature.startswith(

        (

            "sum_",
            "mean_",
            "max_",
            "min_",
            "std_",
            "nunique_",

        )

    ):

        return "Debtor"

    return "Facility"


# =============================================================================
# GENERIC MATCH
# =============================================================================

def match_rule(
    feature: str,
    rules: dict,
    default: str,
) -> str:

    name = feature.lower()

    for label, keywords in rules.items():

        for keyword in keywords:

            if keyword.lower() in name:

                return label

    return default


# =============================================================================
# MODULE
# =============================================================================

def get_module(
    feature: str,
) -> str:

    return match_rule(

        feature,

        MODULE_RULES,

        "Basic",

    )


# =============================================================================
# DOMAIN
# =============================================================================

def get_domain(
    feature: str,
) -> str:

    return match_rule(

        feature,

        DOMAIN_RULES,

        "General",

    )


# =============================================================================
# CATEGORY
# =============================================================================

def get_category(
    feature: str,
) -> str:

    return match_rule(

        feature,

        CATEGORY_RULES,

        "Feature",

    )


# =============================================================================
# CLASSIFIER
# =============================================================================

def classify_feature(
    feature: str,
) -> dict:

    return {

        "module": get_module(feature),

        "domain": get_domain(feature),

        "category": get_category(feature),

        "level": get_level(feature),

    }
