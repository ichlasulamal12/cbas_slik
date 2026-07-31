"""
==============================================================================
Project : CBAS SLIK Preprocessing
File    : feature_engine/woe.py
Author  : Ichlasul Amal
Version : 2.0.0
==============================================================================

Weight of Evidence
"""

from dataclasses import dataclass
from pathlib import Path
import pickle

import polars as pl

from config import (
    TARGET_COLUMN,
    WOE_SMOOTHING,
    WOE_MODEL_FILE,
)

from feature_engine.binning import (
    NumericBinningModel,
    CategoricalBinningModel,
)


# =============================================================================
# MODEL
# =============================================================================

@dataclass
class WOEModel:
    """
    Weight of Evidence model.
    """

    variable: str

    mapping: dict[int, float]

    description: dict[int, str]

    iv: float


# =============================================================================
# NUMERIC BIN
# =============================================================================

def assign_numeric_bin(
    series: pl.Series,
    model: NumericBinningModel,
) -> pl.Series:
    """
    Assign numeric feature into bin.
    """

    cut_points = model.cut_points

    values = []

    for value in series.to_list():

        if value is None:

            values.append(0)

            continue

        bin_id = 1

        for cut in cut_points:

            if value > cut:

                bin_id += 1

            else:

                break

        values.append(
            bin_id
        )

    return pl.Series(

        series.name,

        values,

    )


# =============================================================================
# CATEGORY BIN
# =============================================================================

def assign_categorical_bin(
    series: pl.Series,
    model: CategoricalBinningModel,
) -> pl.Series:
    """
    Assign categorical feature.
    """

    values = [

        model.mapping.get(
            value,
            0,
        )

        if value is not None

        else 0

        for value in series.to_list()

    ]

    return pl.Series(

        series.name,

        values,

    )


# =============================================================================
# ASSIGN BIN
# =============================================================================

def assign_bin(
    series: pl.Series,
    model,
) -> pl.Series:
    """
    Assign feature into bin.
    """

    if isinstance(
        model,
        NumericBinningModel,
    ):

        return assign_numeric_bin(
            series,
            model,
        )

    return assign_categorical_bin(
        series,
        model,
    )


# =============================================================================
# NUMERIC DESCRIPTION
# =============================================================================

def numeric_description(
    model: NumericBinningModel,
) -> dict[int, str]:
    """
    Create numeric bin description.
    """

    cut_points = model.cut_points

    description = {}

    if len(cut_points) == 0:

        description[1] = "All"

        return description

    description[1] = f"<= {cut_points[0]:.6g}"

    for idx in range(1, len(cut_points)):

        description[idx + 1] = (

            f"({cut_points[idx - 1]:.6g}, "

            f"{cut_points[idx]:.6g}]"

        )

    description[len(cut_points) + 1] = (

        f"> {cut_points[-1]:.6g}"

    )

    description[0] = "Missing"

    return description


# =============================================================================
# CATEGORY DESCRIPTION
# =============================================================================

def categorical_description(
    model: CategoricalBinningModel,
) -> dict[int, str]:
    """
    Create category description.
    """

    description = {

        0: "Missing"

    }

    reverse = {}

    for category, bin_id in model.mapping.items():

        reverse.setdefault(

            bin_id,

            []

        ).append(

            str(category)

        )

    for bin_id, values in reverse.items():

        description[bin_id] = ", ".join(

            sorted(values)

        )

    return description


# =============================================================================
# BIN DESCRIPTION
# =============================================================================

def build_description(
    model,
) -> dict[int, str]:
    """
    Create bin description.
    """

    if isinstance(

        model,

        NumericBinningModel,

    ):

        return numeric_description(
            model,
        )

    return categorical_description(
        model,
    )

# =============================================================================
# BIN STATISTICS
# =============================================================================

def calculate_statistics(
    variable: str,
    bin_series: pl.Series,
    target: pl.Series,
    description: dict[int, str],
) -> tuple[
    pl.DataFrame,
    float,
]:
    """
    Calculate WOE statistics.
    """

    df = pl.DataFrame(

        {

            "BIN": bin_series,

            TARGET_COLUMN: target,

        }

    )

    statistics = (

        df

        .group_by("BIN")

        .agg(

            [

                pl.len().alias("Total"),

                (pl.col(TARGET_COLUMN) == 0)

                .sum()

                .alias("Good"),

                (pl.col(TARGET_COLUMN) == 1)

                .sum()

                .alias("Bad"),

            ]

        )

        .sort("BIN")

    )

    total = statistics["Total"].sum()

    total_good = statistics["Good"].sum()

    total_bad = statistics["Bad"].sum()

    statistics = statistics.with_columns(

        [

            (

                pl.col("Total")

                / total

            )

            .alias("Portion"),

            (

                pl.col("Bad")

                /

                pl.col("Total")

            )

            .fill_nan(0)

            .fill_null(0)

            .alias("Bad Rate"),

            (

                (

                    pl.col("Good")

                    +

                    WOE_SMOOTHING

                )

                /

                (

                    total_good

                    +

                    WOE_SMOOTHING

                )

            )

            .alias("Good Dist"),

            (

                (

                    pl.col("Bad")

                    +

                    WOE_SMOOTHING

                )

                /

                (

                    total_bad

                    +

                    WOE_SMOOTHING

                )

            )

            .alias("Bad Dist"),

        ]

    )

    statistics = statistics.with_columns(

        [

            (

                (

                    pl.col("Good Dist")

                    /

                    pl.col("Bad Dist")

                )

                .log()

            )

            .alias("WOE")

        ]

    )

    statistics = statistics.with_columns(

        (

            (

                pl.col("Good Dist")

                -

                pl.col("Bad Dist")

            )

            *

            pl.col("WOE")

        )

        .alias("IV")

    )

    description_df = pl.DataFrame(

        {

            "BIN": list(description.keys()),

            "Range / Category": list(description.values()),

        }

    )

    statistics = statistics.join(

        description_df,

        on="BIN",

        how="left",

    )

    statistics = statistics.with_columns(

        pl.lit(variable)

        .alias("Variable")

    )

    statistics = statistics.select(

        [

            "Variable",

            "BIN",

            "Range / Category",

            "Total",

            "Good",

            "Bad",

            "Portion",

            "Bad Rate",

            "Good Dist",

            "Bad Dist",

            "WOE",

            "IV",

        ]

    )

    iv = float(

        statistics["IV"].sum()

    )

    return (

        statistics,

        iv,

    )


# =============================================================================
# BUILD MODEL
# =============================================================================

def build_model(
    variable: str,
    statistics: pl.DataFrame,
    description: dict[int, str],
    iv: float,
) -> WOEModel:
    """
    Build WOE model.
    """

    mapping = dict(

        zip(

            statistics["BIN"].to_list(),

            statistics["WOE"].to_list(),

        )

    )

    return WOEModel(

        variable=variable,

        mapping=mapping,

        description=description,

        iv=iv,

    )

# =============================================================================
# FIT FEATURE
# =============================================================================

def fit_feature(
    series: pl.Series,
    target: pl.Series,
    binning_model,
) -> tuple[
    WOEModel,
    pl.DataFrame,
]:
    """
    Fit WOE for one feature.
    """

    description = build_description(
        binning_model,
    )

    bin_series = assign_bin(
        series,
        binning_model,
    )

    statistics, iv = calculate_statistics(

        variable=series.name,

        bin_series=bin_series,

        target=target,

        description=description,

    )

    model = build_model(

        variable=series.name,

        statistics=statistics,

        description=description,

        iv=iv,

    )

    return (

        model,

        statistics,

    )


# =============================================================================
# FIT MODEL
# =============================================================================

def fit(
    development: pl.DataFrame,
    binning_model: dict,
) -> tuple[
    dict,
    pl.DataFrame,
]:
    """
    Fit all features.
    """

    target = development.get_column(
        TARGET_COLUMN,
    )

    model = {}

    tables = []

    total = len(
        binning_model,
    )

    for idx, feature in enumerate(

        sorted(
            binning_model.keys()
        ),

        start=1,

    ):

        if feature not in development.columns:

            continue

        print(

            f"[{idx:03d}/{total:03d}] "

            f"WOE : {feature}"

        )

        fitted_model, statistics = (

            fit_feature(

                development.get_column(
                    feature,
                ),

                target,

                binning_model[
                    feature
                ],

            )

        )

        model[
            feature
        ] = fitted_model

        tables.append(
            statistics
        )

    if len(tables) == 0:

        table = pl.DataFrame()

    else:

        table = pl.concat(

            tables,

            how="vertical",

        )

    return (

        model,

        table,

    )


# =============================================================================
# TRANSFORM FEATURE
# =============================================================================

def transform_feature(
    series: pl.Series,
    binning_model,
    woe_model: WOEModel,
) -> pl.Series:
    """
    Transform feature
    directly into WOE.
    """

    bin_series = assign_bin(

        series,

        binning_model,

    )

    values = [

        woe_model.mapping.get(

            value,

            0.0,

        )

        for value in bin_series.to_list()

    ]

    return pl.Series(

        series.name,

        values,

    )


# =============================================================================
# TRANSFORM DATASET
# =============================================================================

def transform(
    df: pl.DataFrame,
    binning_model: dict,
    woe_model: dict,
) -> pl.DataFrame:
    """
    Transform dataset into
    WOE dataset.
    """

    result = df.clone()

    total = len(
        woe_model,
    )

    for idx, feature in enumerate(

        sorted(
            woe_model.keys()
        ),

        start=1,

    ):

        if feature not in result.columns:

            continue

        print(

            f"[{idx:03d}/{total:03d}] "

            f"Transform : {feature}"

        )

        transformed = transform_feature(

            result.get_column(
                feature,
            ),

            binning_model[
                feature
            ],

            woe_model[
                feature
            ],

        )

        result = result.with_columns(

            transformed.alias(
                feature,
            )

        )

    return result

# =============================================================================
# SUMMARY
# =============================================================================

def summary(
    model: dict,
) -> pl.DataFrame:
    """
    WOE model summary.
    """

    rows = []

    for feature, fitted in model.items():

        rows.append(

            {

                "Variable": feature,

                "IV": fitted.iv,

                "Bin": len(fitted.mapping),

            }

        )

    if len(rows) == 0:

        return pl.DataFrame()

    return (

        pl.DataFrame(rows)

        .sort(

            "IV",

            descending=True,

        )

    )


# =============================================================================
# INFORMATION
# =============================================================================

def information(
    model: dict,
) -> dict:
    """
    WOE model information.
    """

    table = summary(
        model,
    )

    if table.height == 0:

        return {

            "feature": 0,

            "bin": 0,

            "average_iv": 0.0,

            "max_iv": 0.0,

        }

    return {

        "feature": table.height,

        "bin": int(table["Bin"].sum()),

        "average_iv": float(

            table["IV"].mean()

        ),

        "max_iv": float(

            table["IV"].max()

        ),

    }


# =============================================================================
# PRINT INFORMATION
# =============================================================================

def print_information(
    model: dict,
) -> None:
    """
    Print WOE summary.
    """

    info = information(
        model,
    )

    print()

    print("=" * 80)

    print("WOE SUMMARY")

    print("=" * 80)

    print(

        f"Feature        : "

        f"{info['feature']:,}"

    )

    print(

        f"Total Bin      : "

        f"{info['bin']:,}"

    )

    print(

        f"Average IV     : "

        f"{info['average_iv']:.4f}"

    )

    print(

        f"Maximum IV     : "

        f"{info['max_iv']:.4f}"

    )

    print()


# =============================================================================
# SAVE
# =============================================================================

def save(
    model: dict,
    output_dir: Path,
) -> None:
    """
    Save WOE model.
    """

    output_dir.mkdir(

        parents=True,

        exist_ok=True,

    )

    with open(

        output_dir /

        WOE_MODEL_FILE,

        "wb",

    ) as file:

        pickle.dump(

            model,

            file,

            protocol=pickle.HIGHEST_PROTOCOL,

        )


# =============================================================================
# LOAD
# =============================================================================

def load(
    output_dir: Path,
) -> dict:
    """
    Load WOE model.
    """

    with open(

        output_dir /

        WOE_MODEL_FILE,

        "rb",

    ) as file:

        model = pickle.load(
            file,
        )

    return model
