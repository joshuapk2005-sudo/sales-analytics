# Stroke Prediction System

A portfolio-friendly machine learning project for estimating stroke risk from common patient health characteristics.

## Project goal

This project trains and compares a few classification models to predict whether a patient is likely to experience a stroke based on features such as age, hypertension, heart disease, BMI, glucose level, smoking status, and work/residence context.

The app is designed as a simple, interactive prototype that demonstrates end-to-end ML work: data preparation, feature engineering, model comparison, and deployment as a Streamlit dashboard.

## Tech stack

- Python
- pandas
- scikit-learn
- streamlit
- joblib
- matplotlib
- seaborn

## Folder structure

```text
stroke-prediction/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   └── healthcare-dataset-stroke-data.csv
├── src/
│   ├── preprocess.py
│   └── train_model.py
├── models/
│   └── best_model.joblib
└── .gitignore
```

## Setup

1. Create and activate a virtual environment if needed.

2. Install dependencies:

```bash
py -m pip install -r requirements.txt
```

3. Download the public stroke dataset if it is missing:

```bash
py src/download_public_data.py
```

4. Train the models:

```bash
py src/train_model.py
```

5. Run the app:

```bash
py -m streamlit run app.py
```

## Data source

This project uses a public stroke dataset from GitHub:
`https://raw.githubusercontent.com/gustika17/healthcare-dataset-stroke-data.csv/main/healthcare-dataset-stroke-data.csv`

This is a real-world dataset rather than a synthetic prototype, which makes the project stronger for a portfolio.

## Important note on model quality

The real dataset is highly imbalanced: there are far fewer stroke cases than non-stroke cases. That is why the model may show strong accuracy but weaker recall/F1 unless the class imbalance is actively handled with tuning or resampling.

## How the project works

1. Data is loaded from a CSV file.
2. Invalid or missing values are cleaned.
3. Categorical values are converted with one-hot encoding.
4. Models are trained and compared using accuracy, precision, recall, and F1 score.
5. The best-performing model is saved to `models/best_model.joblib`.
6. The Streamlit app loads the model and predicts risk for user-entered patient details.

## Models compared

- Logistic Regression
- Decision Tree Classifier
- Random Forest Classifier

## Notes

- This project is a learning and portfolio example.
- It should not be treated as a medical diagnostic tool.
- The current dataset is synthetic and useful for local development; a real public dataset can be used later for a more realistic version.
