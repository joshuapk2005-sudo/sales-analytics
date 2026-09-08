from __future__ import annotations

from pathlib import Path
import urllib.request

import pandas as pd


DATA_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = DATA_DIR / "data" / "healthcare-dataset-stroke-data.csv"
REMOTE_DATA_URL = "https://raw.githubusercontent.com/gustika17/healthcare-dataset-stroke-data.csv/main/healthcare-dataset-stroke-data.csv"


def _ensure_dataset(path: str | Path = DATA_PATH) -> Path:
    target = Path(path)
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(REMOTE_DATA_URL, target)
    return target


def load_data(path: str | Path = DATA_PATH) -> pd.DataFrame:
    resolved_path = _ensure_dataset(path)
    df = pd.read_csv(resolved_path)
    return _standardize_columns(df)


def _standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned.columns = cleaned.columns.map(lambda col: str(col).strip())

    rename_map = {
        "residence_type": "Residence_type",
        "residence": "Residence_type",
        "avg_glucose_level": "avg_glucose_level",
        "avg_glucose": "avg_glucose_level",
        "bmi": "bmi",
        "ever_married": "ever_married",
        "work_type": "work_type",
        "smoking_status": "smoking_status",
        "gender": "gender",
        "stroke": "stroke",
    }

    cleaned = cleaned.rename(columns={
        col: rename_map.get(str(col).strip().lower(), col)
        for col in cleaned.columns
    })
    return cleaned


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = _standardize_columns(df.copy())

    for col in ["bmi", "smoking_status"]:
        if col in cleaned.columns:
            if col == "bmi":
                cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce")
            else:
                cleaned[col] = cleaned[col].fillna("Unknown").astype(str).str.strip()

    if "gender" in cleaned.columns:
        cleaned["gender"] = cleaned["gender"].replace({"Other": "Female"}).astype(str).str.strip()

    if "Residence_type" in cleaned.columns:
        cleaned["Residence_type"] = cleaned["Residence_type"].astype(str).str.strip()

    cleaned = cleaned.dropna(subset=["bmi"]).reset_index(drop=True)
    return cleaned


def prepare_features(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    feature_columns = [
        "gender",
        "age",
        "hypertension",
        "heart_disease",
        "ever_married",
        "work_type",
        "Residence_type",
        "avg_glucose_level",
        "bmi",
        "smoking_status",
    ]

    missing = [column for column in feature_columns if column not in df.columns]
    if missing:
        raise ValueError(f"Missing expected feature columns: {missing}")

    X = df[feature_columns].copy()
    y = df["stroke"] if "stroke" in df.columns else pd.Series(0, index=X.index)

    X["gender"] = X["gender"].astype(str)
    X["ever_married"] = X["ever_married"].astype(str)
    X["work_type"] = X["work_type"].astype(str)
    X["Residence_type"] = X["Residence_type"].astype(str)
    X["smoking_status"] = X["smoking_status"].astype(str)

    X = pd.get_dummies(
        X,
        columns=["gender", "ever_married", "work_type", "Residence_type", "smoking_status"],
        drop_first=True,
    )
    return X, y
