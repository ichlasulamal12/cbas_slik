"""
==========================================================
CBAS SLIK FILTER
Loader
==========================================================
"""

import pandas as pd

from config import (
    COMPANY_KEY,
    COMPANY_DATE,
    INDIVIDUAL_KEY,
    INDIVIDUAL_DATE,
    SPECIAL_START_DATE,
    SPECIAL_END_DATE,
    SHOW_LOG
)


# ==========================================================
# LOAD COMPANY
# ==========================================================

def load_company(file_path):

    if SHOW_LOG:
        print("Loading Company...")

    df = pd.read_excel(
        file_path,
        dtype={
            COMPANY_KEY: str
        }
    )

    df[COMPANY_DATE] = pd.to_datetime(df[COMPANY_DATE])

    df["YYYYMM"] = (
        df[COMPANY_DATE]
        .dt
        .strftime("%Y%m")
    )

    if SHOW_LOG:
        print(f"Company : {len(df):,} rows")

    return df


# ==========================================================
# LOAD INDIVIDUAL
# ==========================================================

def load_individual(file_path):

    if SHOW_LOG:
        print("Loading Individual...")

    df = pd.read_excel(
        file_path,
        dtype={
            INDIVIDUAL_KEY: str
        }
    )

    df[INDIVIDUAL_DATE] = pd.to_datetime(df[INDIVIDUAL_DATE])

    df["YYYYMM"] = (
        df[INDIVIDUAL_DATE]
        .dt
        .strftime("%Y%m")
    )

    if SHOW_LOG:
        print(f"Individual : {len(df):,} rows")

    return df


# ==========================================================
# BUILD LOOKUP
# ==========================================================

def build_lookup(df, key):

    lookup = {}

    for ym, group in df.groupby("YYYYMM"):

        lookup[ym] = set(

            group[key]
            .dropna()
            .astype(str)

        )

    return lookup


# ==========================================================
# SPECIAL LOOKUP (2022)
# ==========================================================

def build_special_lookup(df, key):

    return set(

        df.loc[

            (
                df[COMPANY_DATE] >= SPECIAL_START_DATE
            )
            &
            (
                df[COMPANY_DATE] < SPECIAL_END_DATE
            ),

            key

        ]

        .dropna()

        .astype(str)

    )


# ==========================================================
# LOAD ALL
# ==========================================================

def load_all(company_file, individual_file):

    company = load_company(company_file)

    individual = load_individual(individual_file)

    if SHOW_LOG:
        print("Building Company Lookup...")

    company_lookup = build_lookup(
        company,
        COMPANY_KEY
    )

    if SHOW_LOG:
        print("Building Individual Lookup...")

    individual_lookup = build_lookup(
        individual,
        INDIVIDUAL_KEY
    )

    if SHOW_LOG:
        print("Building Special Lookup...")

    company_2022 = build_special_lookup(
        company,
        COMPANY_KEY
    )

    individual_2022 = build_special_lookup(
        individual,
        INDIVIDUAL_KEY
    )

    del company
    del individual

    return (
        company_lookup,
        individual_lookup,
        company_2022,
        individual_2022
    )
