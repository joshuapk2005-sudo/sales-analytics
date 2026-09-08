from __future__ import annotations

import joblib
import pandas as pd
import streamlit as st

from src.preprocess import clean_data, prepare_features

MODEL_PATH = "models/best_model.joblib"


@st.cache_resource
def get_model():
    try:
        return joblib.load(MODEL_PATH)
    except FileNotFoundError:
        st.error("Model file not found. Train the model first with `py src/train_model.py`.")
        st.stop()


def classify_risk(probability: float) -> str:
    if probability >= 0.7:
        return "High risk"
    if probability >= 0.4:
        return "Moderate risk"
    return "Low risk"


st.set_page_config(page_title="Stroke Prediction System", page_icon="🩺", layout="wide")
st.title("Stroke Prediction System")
st.caption("Estimate stroke risk using a patient health profile.")

with st.form("prediction_form"):
    st.subheader("Patient information")
    col1, col2 = st.columns(2)

    with col1:
        gender = st.selectbox("Gender", ["Male", "Female"])
        age = st.number_input("Age", min_value=0, max_value=120, value=45)
        hypertension = st.selectbox("Hypertension", [0, 1])
        heart_disease = st.selectbox("Heart Disease", [0, 1])
        ever_married = st.selectbox("Ever Married", ["Yes", "No"])
        work_type = st.selectbox("Work Type", ["Private", "Self-employed", "Govt_job", "children"])

    with col2:
        residence_type = st.selectbox("Residence Type", ["Urban", "Rural"])
        avg_glucose_level = st.number_input("Average Glucose Level", min_value=0.0, value=90.0)
        bmi = st.number_input("BMI", min_value=0.0, value=25.0)
        smoking_status = st.selectbox("Smoking Status", ["never smoked", "formerly smoked", "smokes", "Unknown"])

    submitted = st.form_submit_button("Predict stroke risk", use_container_width=True)

if submitted:
    raw = pd.DataFrame(
        [{
            "gender": gender,
            "age": age,
            "hypertension": hypertension,
            "heart_disease": heart_disease,
            "ever_married": ever_married,
            "work_type": work_type,
            "Residence_type": residence_type,
            "avg_glucose_level": avg_glucose_level,
            "bmi": bmi,
            "smoking_status": smoking_status,
            "stroke": 0,
        }]
    )

    cleaned = clean_data(raw)
    X, _ = prepare_features(cleaned)
    model = get_model()

    prediction = model.predict(X)[0]
    probability = model.predict_proba(X)[0][1]
    label = classify_risk(probability)

    st.subheader("Prediction result")
    st.metric("Estimated stroke probability", f"{probability * 100:.1f}%")
    st.progress(min(max(probability, 0.0), 1.0))

    if prediction == 1:
        st.error(f"{label}: the model predicts a higher risk of stroke.")
    else:
        st.success(f"{label}: the model predicts a lower risk of stroke.")

    st.markdown("---")
    st.caption("This result is an ML-based estimate and should not replace medical advice.")
