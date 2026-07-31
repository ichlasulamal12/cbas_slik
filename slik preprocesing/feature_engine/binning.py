"""
==============================================================================
Project : CBAS SLIK Preprocessing
File    : feature_engine/binning.py
Author  : Ichlasul Amal
Version : 2.0.0
==============================================================================

Binning Model
"""

from dataclasses import dataclass
from pathlib import Path
import pickle

import numpy as np
import polars as pl

from config import (
    MAX_BINS,
    BINNING_MODEL_FILE,
)


# =============================================================================
# BINNING MODEL
# =============================================================================

@dataclass
class NumericBinningModel:
    """
    Numeric binning model.
    """

    variable: str

    cut_points: list[float]


@dataclass
class CategoricalBinningModel:
    """
    Categorical binning model.
    """

    variable: str

    mapping: dict


# =============================================================================
# DATA TYPE
# =============================================================================

def is_numeric(
    series: pl.Series,
) -> bool:
    """
    Check numeric dtype.
    """

    return series.dtype.is_numeric()


# =============================================================================
# VALIDATION
# =============================================================================

def valid_feature(
    series: pl.Series,
) -> bool:
    """
    Validate feature.
    """

    if len(series) == 0:

        return False

    if series.null_count() == len(series):

        return False

    if series.drop_nulls().n_unique() <= 1:

        return False

    return True


# =============================================================================
# CUT POINT
# =============================================================================

def create_cut_points(
    series: pl.Series,
) -> list[float]:
    """
    Create quantile cut points.
    """

    values = (

        series

        .drop_nulls()

        .cast(pl.Float64)

        .to_numpy()

    )

    if len(values) == 0:

        return []

    quantiles = np.linspace(

        0,

        1,

        MAX_BINS + 1,

    )

    cut_points = np.quantile(

        values,

        quantiles,

    )

    cut_points = np.unique(
        cut_points
    )

    if len(cut_points) <= 2:

        return []

    return cut_points[
        1:-1
    ].tolist()


# =============================================================================
# FIT NUMERIC
# =============================================================================

def fit_numeric(
    series: pl.Series,
) -> NumericBinningModel:
    """
    Fit numeric feature.
    """

    return NumericBinningModel(

        variable=series.name,

        cut_points=create_cut_points(
            series,
        ),

    )


# =============================================================================
# FIT CATEGORICAL
# =============================================================================

def fit_categorical(
    series: pl.Series,
) -> CategoricalBinningModel:
    """
    Fit categorical feature.
    """

    categories = (

        series

        .drop_nulls()

        .unique()

        .sort()

        .to_list()

    )

    mapping = {

        value: idx + 1

        for idx, value in enumerate(
            categories
        )

    }

    return CategoricalBinningModel(

        variable=series.name,

        mapping=mapping,

    )

# =============================================================================
# FIT FEATURE
# =============================================================================

def fit_feature(
    series: pl.Series,
):
    """
    Fit one feature.
    """

    if not valid_feature(
        series,
    ):

        return None

    if is_numeric(
        series,
    ):

        return fit_numeric(
            series,
        )

    return fit_categorical(
        series,
    )


# =============================================================================
# FIT MODEL
# =============================================================================

def fit(
    df: pl.DataFrame,
    feature_list: list[str],
) -> dict:
    """
    Fit binning model.
    """

    model = {}

    total = len(
        feature_list,
    )

    for idx, feature in enumerate(

        feature_list,

        start=1,

    ):

        if feature not in df.columns:

            continue

        print(

            f"[{idx:03d}/{total:03d}] "

            f"Fit {feature}"

        )

        fitted = fit_feature(

            df.get_column(
                feature,
            )

        )

        if fitted is None:

            continue

        model[
            feature
        ] = fitted

    return model


# =============================================================================
# MODEL SUMMARY
# =============================================================================

def summary(
    model: dict,
) -> pl.DataFrame:
    """
    Binning model summary.
    """

    rows = []

    for feature, fitted in model.items():

        if isinstance(

            fitted,

            NumericBinningModel,

        ):

            rows.append(

                {

                    "Variable": feature,

                    "Type": "Numeric",

                    "Bin": len(
                        fitted.cut_points
                    ) + 1,

                }

            )

        else:

            rows.append(

                {

                    "Variable": feature,

                    "Type": "Categorical",

                    "Bin": len(
                        fitted.mapping
                    ),

                }

            )

    if len(rows) == 0:

        return pl.DataFrame()

    return (

        pl.DataFrame(rows)

        .sort(

            "Variable"

        )

    )


# =============================================================================
# PRINT SUMMARY
# =============================================================================

def print_summary(
    model: dict,
) -> None:
    """
    Print summary.
    """

    table = summary(
        model,
    )

    numeric = table.filter(

        pl.col("Type")

        ==

        "Numeric"

    ).height

    categorical = table.filter(

        pl.col("Type")

        ==

        "Categorical"

    ).height

    print()

    print("=" * 80)

    print("BINNING SUMMARY")

    print("=" * 80)

    print(

        f"Total Feature : {table.height:,}"

    )

    print(

        f"Numeric       : {numeric:,}"

    )

    print(

        f"Categorical   : {categorical:,}"

    )

    print()

    # =============================================================================
# SAVE MODEL
# =============================================================================

def save(
    model: dict,
    output_dir: Path,
) -> None:
    """
    Save binning model.
    """

    output_dir.mkdir(

        parents=True,

        exist_ok=True,

    )

    with open(

        output_dir /

        BINNING_MODEL_FILE,

        "wb",

    ) as file:

        pickle.dump(

            model,

            file,

            protocol=pickle.HIGHEST_PROTOCOL,

        )


# =============================================================================
# LOAD MODEL
# =============================================================================

def load(
    output_dir: Path,
) -> dict:
    """
    Load binning model.
    """

    with open(

        output_dir /

        BINNING_MODEL_FILE,

        "rb",

    ) as file:

        model = pickle.load(
            file,
        )

    return model


# =============================================================================
# INFORMATION
# =============================================================================

def information(
    model: dict,
) -> dict:
    """
    Return model information.
    """

    numeric = 0

    categorical = 0

    total_bin = 0

    for fitted in model.values():

        if isinstance(

            fitted,

            NumericBinningModel,

        ):

            numeric += 1

            total_bin += (

                len(

                    fitted.cut_points

                )

                + 1

            )

        else:

            categorical += 1

            total_bin += len(

                fitted.mapping

            )

    return {

        "total_feature": len(model),

        "numeric_feature": numeric,

        "categorical_feature": categorical,

        "total_bin": total_bin,

    }


# =============================================================================
# PRINT INFORMATION
# =============================================================================

def print_information(
    model: dict,
) -> None:
    """
    Print model information.
    """

    info = information(
        model,
    )

    print()

    print("=" * 80)

    print("BINNING MODEL")

    print("=" * 80)

    print(

        f"Feature           : "

        f"{info['total_feature']:,}"

    )

    print(

        f"Numeric Feature   : "

        f"{info['numeric_feature']:,}"

    )

    print(

        f"Category Feature  : "

        f"{info['categorical_feature']:,}"

    )

    print(

        f"Total Bin         : "

        f"{info['total_bin']:,}"

    )

    print()
