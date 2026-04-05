import streamlit as st
import requests

st.set_page_config(page_title="Laptop Price Predictor 💻")

st.title("💻 Laptop Price Prediction")

API_URL = "http://127.0.0.1:8000/predict"

# ----------------------------
# Dropdown Inputs
# ----------------------------

company = st.selectbox(
    "Company",
    ["Apple", "Dell", "HP", "Lenovo", "Asus", "Acer", "MSI"]
)

typename = st.selectbox(
    "Type",
    ["Ultrabook", "Gaming", "Notebook", "2 in 1 Convertible", "Workstation"]
)

screen = st.selectbox(
    "Screen Resolution",
    [
        "Full HD",
        "IPS Panel Retina Display 2560x1600",
        "4K Ultra HD",
        "HD Ready"
    ]
)

cpu = st.selectbox(
    "CPU",
    [
        "Intel Core i3",
        "Intel Core i5 2.3GHz",
        "Intel Core i7",
        "AMD Ryzen 5",
        "AMD Ryzen 7"
    ]
)

memory = st.selectbox(
    "Memory",
    [
        "128GB SSD",
        "256GB SSD",
        "512GB SSD",
        "1TB HDD",
        "1TB SSD"
    ]
)

gpu = st.selectbox(
    "GPU",
    [
        "Intel HD Graphics",
        "Intel Iris Plus Graphics 640",
        "Nvidia GTX 1050",
        "Nvidia RTX 3050",
        "AMD Radeon"
    ]
)

os = st.selectbox(
    "Operating System",
    ["Windows 10", "Windows 11", "macOS", "Linux"]
)

# ----------------------------
# Numeric Inputs
# ----------------------------

inches = st.number_input("Screen Size (inches)", value=13.3)
ram = st.number_input("RAM (GB)", value=8)
weight = st.number_input("Weight (kg)", value=1.3)

# ----------------------------
# Prediction Function
# ----------------------------

def predict_price():
    data = {
        "Company": company,
        "TypeName": typename,
        "Inches": inches,
        "ScreenResolution": screen,
        "Cpu": cpu,
        "Ram": ram,
        "Memory": memory,
        "Gpu": gpu,
        "OpSys": os,
        "Weight": weight
    }

    try:
        response = requests.post(API_URL, json=data)

        if response.status_code == 200:
            result = response.json()

            if "predicted_price" in result:
                return result["predicted_price"]
            else:
                return result.get("error", "Unknown error")

        else:
            return f"Error: {response.status_code}"

    except Exception as e:
        return f"Backend not running: {e}"

# ----------------------------
# Button
# ----------------------------

if st.button("Predict Price"):
    with st.spinner("Predicting..."):
        price = predict_price()

        st.subheader("💰 Predicted Laptop Price")
        st.success(price)