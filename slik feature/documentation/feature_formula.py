"""
==============================================================================
Project : CBAS SLIK Feature Engineering
File    : feature_formula.py
Author  : Ichlasul Amal
Version : 2.0.0
==============================================================================

Feature Formula

Automatic feature formula generator.

"""

import re


# =============================================================================
# MANUAL FORMULA
# =============================================================================

MANUAL_FORMULA = {

    # -------------------------------------------------------------------------
    # BASIC
    # -------------------------------------------------------------------------

    "utilization":
        "bakiDebet / plafon",

    "initial_utilization":
        "bakiDebet / plafonAwal",

    "unused_limit":
        "plafon - bakiDebet",

    "available_limit":
        "plafon - bakiDebet",

    "overlimit_amount":
        "MAX(bakiDebet - plafon, 0)",

    "plafond_change":
        "plafon - plafonAwal",

    "credit_age_days":
        "Today - tanggalAwalKredit",

    "remaining_tenor_days":
        "tanggalJatuhTempo - Today",

    "original_tenor_days":
        "tanggalJatuhTempo - tanggalAwalKredit",

    "tenor_utilization":
        "credit_age_days / original_tenor_days",

    "interest_rate":
        "sukuBunga",

    "total_overdue":
        "tunggakanPokok + tunggakanBunga + denda",

    "overdue_ratio":
        "total_overdue / bakiDebet",

    "delinquency_severity":
        "MAX(kolektibilitas, jumlahHariTunggakan)",

}


# =============================================================================
# PREFIX FORMULA
# =============================================================================

PREFIX_FORMULA = {

    "sum_":
        "SUM({})",

    "mean_":
        "AVG({})",

    "max_":
        "MAX({})",

    "min_":
        "MIN({})",

    "std_":
        "STD({})",

    "median_":
        "MEDIAN({})",

    "var_":
        "VAR({})",

    "range_":
        "MAX({}) - MIN({})",

    "count_":
        "COUNT({})",

    "nunique_":
        "COUNT DISTINCT({})",

}


# =============================================================================
# HISTORY FORMULA
# =============================================================================

def history_formula(
    feature: str,
):

    match = re.match(

        r"hist(\d+)_(.+)",

        feature,

    )

    if not match:

        return None

    window = match.group(1)

    variable = match.group(2)

    return (

        f"{variable} calculated "

        f"using last {window} month(s)"

    )


# =============================================================================
# RATIO FORMULA
# =============================================================================

def ratio_formula(
    feature: str,
):

    if not feature.startswith(

        "ratio_"

    ):

        return None

    name = feature[6:]

    parts = name.split("_")

    if len(parts) < 2:

        return None

    numerator = parts[0]

    denominator = "_".join(

        parts[1:]

    )

    return (

        f"{numerator} / {denominator}"

    )


# =============================================================================
# FLAG FORMULA
# =============================================================================

def flag_formula(
    feature: str,
):

    if not feature.startswith(

        "flag_"

    ):

        return None

    variable = feature[5:]

    return (

        f"Indicator({variable})"

    )


# =============================================================================
# PREFIX
# =============================================================================

def prefix_formula(
    feature: str,
):

    for prefix, template in PREFIX_FORMULA.items():

        if feature.startswith(

            prefix

        ):

            base = feature.replace(

                prefix,

                "",

                1,

            )

            return template.format(

                base

            )

    return None


# =============================================================================
# CREATE FORMULA
# =============================================================================

def get_formula(
    feature: str,
):

    if feature in MANUAL_FORMULA:

        return MANUAL_FORMULA[

            feature

        ]

    formula = prefix_formula(

        feature

    )

    if formula:

        return formula

    formula = ratio_formula(

        feature

    )

    if formula:

        return formula

    formula = history_formula(

        feature

    )

    if formula:

        return formula

    formula = flag_formula(

        feature

    )

    if formula:

        return formula

    return ""
