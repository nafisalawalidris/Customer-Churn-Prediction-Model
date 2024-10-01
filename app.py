import streamlit as st
import pandas as pd
import joblib

# Load the trained model
model = joblib.load('best_rf_model.pkl')

# Function to make predictions
def predict(input_data):
    return model.predict(input_data)

# Set page configuration
st.set_page_config(page_title="Customer Churn Prediction", layout="wide")

# Title and description
st.title("Customer Churn Prediction")
st.markdown("""
Welcome to the **Customer Churn Prediction** app! 
Enter customer details below to predict whether they are likely to churn. 
This application uses a machine learning model to analyse customer behaviour and provide insights.
""")

# Create a sidebar for input fields
st.sidebar.header("👤 Customer Information")
st.sidebar.write("Please fill in the details below:")

# Input fields for user data
tenure = st.sidebar.number_input("Tenure (months)", min_value=0, max_value=100, value=0)
monthly_charges = st.sidebar.number_input("Monthly Charges ($)", min_value=0.0, format="%.2f")
total_charges = st.sidebar.number_input("Total Charges ($)", min_value=0.0, format="%.2f")

# Categorical fields
gender = st.sidebar.selectbox("Gender", options=["Select", "Male", "Female"])
partner = st.sidebar.selectbox("Partner", options=["Select", "Yes", "No"])
dependents = st.sidebar.selectbox("Dependents", options=["Select", "Yes", "No"])
phone_service = st.sidebar.selectbox("Phone Service", options=["Select", "Yes", "No"])
multiple_lines = st.sidebar.selectbox("Multiple Lines", options=["Select", "Yes", "No", "No phone service"])
internet_service = st.sidebar.selectbox("Internet Service", options=["Select", "DSL", "Fiber optic", "No"])
online_security = st.sidebar.selectbox("Online Security", options=["Select", "Yes", "No", "No internet service"])
online_backup = st.sidebar.selectbox("Online Backup", options=["Select", "Yes", "No", "No internet service"])
device_protection = st.sidebar.selectbox("Device Protection", options=["Select", "Yes", "No", "No internet service"])
tech_support = st.sidebar.selectbox("Tech Support", options=["Select", "Yes", "No", "No internet service"])
streaming_tv = st.sidebar.selectbox("Streaming TV", options=["Select", "Yes", "No", "No internet service"])
streaming_movies = st.sidebar.selectbox("Streaming Movies", options=["Select", "Yes", "No", "No internet service"])
contract = st.sidebar.selectbox("Contract Type", options=["Select", "Month-to-month", "One year", "Two year"])
paperless_billing = st.sidebar.selectbox("Paperless Billing", options=["Select", "Yes", "No"])
payment_method = st.sidebar.selectbox("Payment Method", options=["Select", "Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"])

# Button to make prediction
if st.sidebar.button("Predict Churn"):
    # Check if all fields have valid selections
    if (gender != "Select" and partner != "Select" and dependents != "Select" and 
        phone_service != "Select" and multiple_lines != "Select" and 
        internet_service != "Select" and online_security != "Select" and 
        online_backup != "Select" and device_protection != "Select" and 
        tech_support != "Select" and streaming_tv != "Select" and 
        streaming_movies != "Select" and contract != "Select" and 
        paperless_billing != "Select" and payment_method != "Select"):
        
        # Encoding categorical variables
        gender_encoded = 1 if gender == "Female" else 0
        partner_encoded = 1 if partner == "Yes" else 0
        dependents_encoded = 1 if dependents == "Yes" else 0
        phone_service_encoded = 1 if phone_service == "Yes" else 0
        multiple_lines_encoded = 1 if multiple_lines == "Yes" else (0 if multiple_lines == "No" else -1)
        internet_service_encoded = {"DSL": 0, "Fiber optic": 1, "No": 2}[internet_service]
        online_security_encoded = 1 if online_security == "Yes" else (0 if online_security == "No" else -1)
        online_backup_encoded = 1 if online_backup == "Yes" else (0 if online_backup == "No" else -1)
        device_protection_encoded = 1 if device_protection == "Yes" else (0 if device_protection == "No" else -1)
        tech_support_encoded = 1 if tech_support == "Yes" else (0 if tech_support == "No" else -1)
        streaming_tv_encoded = 1 if streaming_tv == "Yes" else (0 if streaming_tv == "No" else -1)
        streaming_movies_encoded = 1 if streaming_movies == "Yes" else (0 if streaming_movies == "No" else -1)
        contract_encoded = {"Month-to-month": 0, "One year": 1, "Two year": 2}[contract]
        paperless_billing_encoded = 1 if paperless_billing == "Yes" else 0
        payment_method_encoded = {"Electronic check": 0, "Mailed check": 1, "Bank transfer (automatic)": 2, "Credit card (automatic)": 3}[payment_method]

        # Prepare input data for prediction
        input_data = pd.DataFrame({
            'tenure': [tenure],
            'MonthlyCharges': [monthly_charges],
            'TotalCharges': [total_charges],
            'gender': [gender_encoded],
            'partner': [partner_encoded],
            'dependents': [dependents_encoded],
            'phone_service': [phone_service_encoded],
            'multiple_lines': [multiple_lines_encoded],
            'internet_service': [internet_service_encoded],
            'online_security': [online_security_encoded],
            'online_backup': [online_backup_encoded],
            'device_protection': [device_protection_encoded],
            'tech_support': [tech_support_encoded],
            'streaming_tv': [streaming_tv_encoded],
            'streaming_movies': [streaming_movies_encoded],
            'contract': [contract_encoded],
            'paperless_billing': [paperless_billing_encoded],
            'payment_method': [payment_method_encoded],
        })

        prediction = predict(input_data)
        prediction_text = "Churn" if prediction[0] == 1 else "Not Churn"

        # Display results with a compelling layout
        st.subheader("🎉 Prediction Result")
        st.markdown(f"""
        **Prediction:** **{prediction_text}**  
        The customer is **{prediction_text}** based on the provided information.
        """)

        if prediction[0] == 1:
            st.warning("🔴 Action Required: Consider strategies to retain this customer!")
        else:
            st.success("🟢 Great! This customer is likely to stay!")

    else:
        st.error("🚫 Please fill in all fields with valid selections.")
