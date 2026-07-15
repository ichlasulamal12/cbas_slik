"""
==========================================================
CBAS SLIK FILTER
Processor
==========================================================
"""

import os
import re
import time

import polars as pl

from datetime import datetime
from dateutil.relativedelta import relativedelta

from config import (
    COMPANY_KEY,
    INDIVIDUAL_KEY,
    SLIK_NPWP,
    SLIK_KTP,
    PARQUET_COMPRESSION,
    SHOW_LOG,
    SPECIAL_FILE_2022
)


# ==========================================================
# YYYYMM
# ==========================================================

def get_yyyymm(file_name):

    m = re.search(r"(\d{6})", file_name)

    if m is None:
        raise ValueError(f"YYYYMM tidak ditemukan pada {file_name}")

    return m.group(1)


# ==========================================================
# LOOKUP
# ==========================================================

def get_lookup(
    file_name,
    company_lookup,
    individual_lookup,
    company_2022,
    individual_2022
):

    if SPECIAL_FILE_2022 in file_name:

        return company_2022, individual_2022

    ym = get_yyyymm(file_name)

    next_month = (
        datetime.strptime(ym, "%Y%m")
        + relativedelta(months=1)
    ).strftime("%Y%m")

    company_target = (
        company_lookup.get(ym, set())
        |
        company_lookup.get(next_month, set())
    )

    individual_target = (
        individual_lookup.get(ym, set())
        |
        individual_lookup.get(next_month, set())
    )

    return company_target, individual_target


# ==========================================================
# PROCESS
# ==========================================================

def process_file(
    file,
    folder,
    output_folder,
    company_lookup,
    individual_lookup,
    company_2022,
    individual_2022
):

    start = time.perf_counter()

    if SHOW_LOG:
        print("=" * 80)
        print(file)
        print("=" * 80)

    company_target, individual_target = get_lookup(
        file,
        company_lookup,
        individual_lookup,
        company_2022,
        individual_2022
    )

    if SHOW_LOG:
        print(f"Company Target    : {len(company_target):,}")
        print(f"Individual Target : {len(individual_target):,}")

    # =====================================================
    # READ PARQUET
    # =====================================================

    t0 = time.perf_counter()

    df = pl.read_parquet(
        os.path.join(folder, file)
    )

    if SHOW_LOG:
        print(f"Read Parquet : {time.perf_counter()-t0:.2f} sec")
        print(f"Rows : {df.height:,}")

    # =====================================================
    # FILTER COMPANY
    # =====================================================

    t0 = time.perf_counter()

    company_result = df.filter(
        pl.col(SLIK_NPWP).is_in(company_target)
    )

    if SHOW_LOG:
        print(f"Company Filter : {time.perf_counter()-t0:.2f} sec")

    # =====================================================
    # FILTER INDIVIDUAL
    # =====================================================

    t0 = time.perf_counter()

    individual_result = df.filter(
        pl.col(SLIK_KTP).is_in(individual_target)
    )

    if SHOW_LOG:
        print(f"Individual Filter : {time.perf_counter()-t0:.2f} sec")

    # =====================================================
    # SAVE
    # =====================================================

    company_output = os.path.join(
        output_folder,
        file.replace(".parquet", "_Company.parquet")
    )

    individual_output = os.path.join(
        output_folder,
        file.replace(".parquet", "_Individual.parquet")
    )

    company_result.write_parquet(
        company_output,
        compression=PARQUET_COMPRESSION
    )

    individual_result.write_parquet(
        individual_output,
        compression=PARQUET_COMPRESSION
    )

    # =====================================================
    # LOG
    # =====================================================

    if SHOW_LOG:

        print(f"Company Match    : {company_result.height:,}")
        print(f"Individual Match : {individual_result.height:,}")

        print(
            f"Total : {time.perf_counter()-start:.2f} sec"
        )

        print()
