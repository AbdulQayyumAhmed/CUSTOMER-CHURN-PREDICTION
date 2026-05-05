import joblib
import pandas as pd

# Load model once (IMPORTANT)
model = joblib.load("app/ml/model.pkl")

def predict_customer(data: dict):
    df = pd.DataFrame([data])

    pred = model.predict(df)[0]
    prob = model.predict_proba(df)[0][1]

    return {
        "prediction": "Yes" if pred == 1 else "No",
        "probability": float(prob)
    }