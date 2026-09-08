from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

from preprocess import clean_data, load_data, prepare_features

MODEL_DIR = Path(__file__).resolve().parents[1] / "models"
MODEL_DIR.mkdir(exist_ok=True)


def train_and_compare() -> dict:
    df = clean_data(load_data())
    X, y = prepare_features(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    models = {
        "logistic_regression": LogisticRegression(max_iter=1000, class_weight="balanced"),
        "decision_tree": DecisionTreeClassifier(random_state=42, class_weight="balanced"),
        "random_forest": RandomForestClassifier(n_estimators=200, random_state=42, class_weight="balanced"),
    }

    results = {}

    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        results[name] = {
            "accuracy": accuracy_score(y_test, preds),
            "precision": precision_score(y_test, preds, zero_division=0),
            "recall": recall_score(y_test, preds, zero_division=0),
            "f1": f1_score(y_test, preds, zero_division=0),
            "report": classification_report(y_test, preds, zero_division=0),
        }

        joblib.dump(model, MODEL_DIR / f"{name}.joblib")

    best_model_name = max(results, key=lambda name: results[name]["f1"])
    best_model = joblib.load(MODEL_DIR / f"{best_model_name}.joblib")
    joblib.dump(best_model, MODEL_DIR / "best_model.joblib")

    return {"best_model": best_model_name, "results": results}


if __name__ == "__main__":
    outcome = train_and_compare()
    print("Best model:", outcome["best_model"])
    for name, metrics in outcome["results"].items():
        print(f"\n{name}:")
        print(f"Accuracy: {metrics['accuracy']:.4f}")
        print(f"Precision: {metrics['precision']:.4f}")
        print(f"Recall: {metrics['recall']:.4f}")
        print(f"F1: {metrics['f1']:.4f}")
