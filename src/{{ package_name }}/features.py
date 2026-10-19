"""Feature engineering and preprocessing helpers."""

from typing import Any

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


class MissingIndicatorTransformer(BaseEstimator, TransformerMixin):
    """Transformer that flags missing values in specified columns."""

    def __init__(self, columns: list[str] | None = None) -> None:
        self.columns = columns

    def fit(
        self,
        X: pd.DataFrame,
        y: Any = None,
    ) -> "MissingIndicatorTransformer":
        """Fit method (stateless)."""
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Add binary indicator columns for missing values."""
        X_out = X.copy()
        cols = self.columns if self.columns is not None else list(X.columns)
        for col in cols:
            if col in X_out.columns:
                X_out[f"{col}_isnan"] = X_out[col].isna().astype(int)
        return X_out


def create_feature_pipeline(
    categorical_cols: list[str],
    numeric_cols: list[str],
) -> ColumnTransformer:
    """Create a standard scikit-learn ColumnTransformer pipeline."""
    num_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    cat_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("num", num_pipeline, numeric_cols),
            ("cat", cat_pipeline, categorical_cols),
        ]
    )
