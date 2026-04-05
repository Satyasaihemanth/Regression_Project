from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import pickle
import numpy as np

# ----------------------------
# Load model correctly
# ----------------------------
with open("model.pkl", "rb") as f:
    saved_objects = pickle.load(f)

model = saved_objects["model"]
scaler = saved_objects["scaler"]
columns = saved_objects["columns"]

app = FastAPI(title="Laptop Price Prediction API")

# ----------------------------
# Input schema
# ----------------------------
class Laptop(BaseModel):
    Company: str
    TypeName: str
    Inches: float
    ScreenResolution: str
    Cpu: str
    Ram: int
    Memory: str
    Gpu: str
    OpSys: str
    Weight: float

# ----------------------------
# Home route
# ----------------------------
@app.get("/")
def root():
    return {"message": "API running 🚀"}

# ----------------------------
# Preprocessing
# ----------------------------
def preprocess(df):
    df = df.copy()

    # One-hot encoding
    df = pd.get_dummies(df)

    # Match training columns
    df = df.reindex(columns=columns, fill_value=0)

    # Scale
    df = scaler.transform(df)

    return df

# ----------------------------
# Prediction route
# ----------------------------
@app.post("/predict")
def predict(data: Laptop):
    try:
        df = pd.DataFrame([data.dict()])

        df_processed = preprocess(df)

        pred = model.predict(df_processed)[0]

        # Reverse log
        price = np.exp(pred)

        return {
            "predicted_price": round(float(price), 2)
        }

    except Exception as e:
        return {"error": str(e)}