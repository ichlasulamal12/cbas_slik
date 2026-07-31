"""
==============================================================================
Project : CBAS SLIK Preprocessing
File    : main.py
Author  : Ichlasul Amal
Version : 2.0.0
==============================================================================

Main Program
"""

from config import (
    DATASET_OUTPUT_DIR,
    TABLE_OUTPUT_DIR,
)

from processor import (
    process,
)

# =============================================================================
# CREATE OUTPUT DIRECTORY
# =============================================================================

def create_output_directory() -> None:
    """
    Create output directory.
    """

    DATASET_OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    TABLE_OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


# =============================================================================
# SAVE DATASET
# =============================================================================

def save_dataset(
    result: dict,
) -> None:
    """
    Save modelling datasets.
    """

    print()
    print("Saving Dataset...")

    # -------------------------------------------------------------------------
    # DEVELOPMENT RAW
    # -------------------------------------------------------------------------

    result["development_raw"].write_parquet(
        DATASET_OUTPUT_DIR / "development_raw.parquet"
    )

    result["development_raw"].write_excel(
        DATASET_OUTPUT_DIR / "development_raw.xlsx"
    )

    # -------------------------------------------------------------------------
    # DEVELOPMENT WOE
    # -------------------------------------------------------------------------

    result["development_woe"].write_parquet(
        DATASET_OUTPUT_DIR / "development_woe.parquet"
    )

    result["development_woe"].write_excel(
        DATASET_OUTPUT_DIR / "development_woe.xlsx"
    )

    # -------------------------------------------------------------------------
    # OOT RAW
    # -------------------------------------------------------------------------

    if result["oot_raw"].height > 0:

        result["oot_raw"].write_parquet(
            DATASET_OUTPUT_DIR / "oot_raw.parquet"
        )

        result["oot_raw"].write_excel(
            DATASET_OUTPUT_DIR / "oot_raw.xlsx"
        )

    # -------------------------------------------------------------------------
    # OOT WOE
    # -------------------------------------------------------------------------

    if result["oot_woe"].height > 0:

        result["oot_woe"].write_parquet(
            DATASET_OUTPUT_DIR / "oot_woe.parquet"
        )

        result["oot_woe"].write_excel(
            DATASET_OUTPUT_DIR / "oot_woe.xlsx"
        )


# =============================================================================
# SAVE TABLE
# =============================================================================

def save_table(
    result: dict,
) -> None:
    """
    Save summary tables.
    """

    print()
    print("Saving Table...")

    result["iv_table"].write_excel(
        TABLE_OUTPUT_DIR / "iv.xlsx"
    )

    result["woe_table"].write_excel(
        TABLE_OUTPUT_DIR / "woe.xlsx"
    )


# =============================================================================
# MAIN
# =============================================================================

def main() -> None:
    """
    Main program.
    """

    print()

    print("=" * 80)
    print("CBAS SLIK PREPROCESSING V2")
    print("=" * 80)

    create_output_directory()

    result = process()

    save_dataset(
        result,
    )

    save_table(
        result,
    )

    print()

    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)

    print()

    print(
        f"Development (Raw) : "
        f"{result['development_raw'].height:,} rows"
    )

    print(
        f"Development (WOE) : "
        f"{result['development_woe'].height:,} rows"
    )

    print(
        f"OOT (Raw)         : "
        f"{result['oot_raw'].height:,} rows"
    )

    print(
        f"OOT (WOE)         : "
        f"{result['oot_woe'].height:,} rows"
    )

    print()

    print(
        f"Selected Feature  : "
        f"{len(result['selected_feature']):,}"
    )

    print(
        f"IV Table          : "
        f"{result['iv_table'].height:,}"
    )

    print(
        f"WOE Table         : "
        f"{result['woe_table'].height:,}"
    )

    print()

    print("=" * 80)
    print("FINISHED")
    print("=" * 80)

    print()


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":

    main()
