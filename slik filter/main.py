"""
==========================================================
CBAS SLIK FILTER
Main
==========================================================
"""

import os
import time

from config import (
    COMPANY_FILE,
    INDIVIDUAL_FILE,
    SLIK_FOLDER,
    OUTPUT_FOLDER,
    INPUT_EXTENSION,
    SHOW_LOG
)

from loader import load_all

from processor import process_file


# ==========================================================
# CHECK OUTPUT
# ==========================================================

def output_exists(file_name):

    company_output = os.path.join(
        OUTPUT_FOLDER,
        file_name.replace(
            ".parquet",
            "_Company.parquet"
        )
    )

    individual_output = os.path.join(
        OUTPUT_FOLDER,
        file_name.replace(
            ".parquet",
            "_Individual.parquet"
        )
    )

    return (
        os.path.exists(company_output)
        and
        os.path.exists(individual_output)
    )


# ==========================================================
# MAIN
# ==========================================================

def main():

    start = time.perf_counter()

    print("=" * 80)
    print("CBAS SLIK FILTER")
    print("=" * 80)

    # ------------------------------------------------------
    # LOAD LOOKUP
    # ------------------------------------------------------

    (
        company_lookup,
        individual_lookup,
        company_2022,
        individual_2022
    ) = load_all(
        COMPANY_FILE,
        INDIVIDUAL_FILE
    )

    # ------------------------------------------------------
    # FILE LIST
    # ------------------------------------------------------

    files = sorted(

        [

            f

            for f in os.listdir(SLIK_FOLDER)

            if f.lower().endswith(INPUT_EXTENSION)

        ]

    )

    total = len(files)

    processed = 0
    skipped = 0
    failed = 0

    # ------------------------------------------------------
    # LOOP
    # ------------------------------------------------------

    for i, file in enumerate(files, start=1):

        print()
        print("=" * 80)
        print(f"[{i}/{total}] {file}")
        print("=" * 80)

        # ----------------------------------------------
        # RESUME
        # ----------------------------------------------

        if output_exists(file):

            if SHOW_LOG:
                print("Skip")

            skipped += 1

            continue

        # ----------------------------------------------
        # PROCESS
        # ----------------------------------------------

        try:

            process_file(

                file=file,

                folder=SLIK_FOLDER,

                output_folder=OUTPUT_FOLDER,

                company_lookup=company_lookup,

                individual_lookup=individual_lookup,

                company_2022=company_2022,

                individual_2022=individual_2022

            )

            processed += 1

        except Exception as e:

            failed += 1

            print()
            print("ERROR")
            print(file)
            print(e)

    # ------------------------------------------------------
    # SUMMARY
    # ------------------------------------------------------

    elapsed = time.perf_counter() - start

    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)

    print(f"Total File : {total}")
    print(f"Processed  : {processed}")
    print(f"Skipped    : {skipped}")
    print(f"Failed     : {failed}")
    print(f"Elapsed    : {elapsed:.2f} sec")

    print("=" * 80)


# ==========================================================
# RUN
# ==========================================================

if __name__ == "__main__":

    main()
