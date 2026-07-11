import streamlit as st
import pandas as pd
import pickle

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Heart Failure Survival Predictor",
    page_icon="❤️",
    layout="centered"
)

# -----------------------------
# LOAD MODEL
# -----------------------------
@st.cache_resource
def load_model():
    with open("heart_model.pkl", "rb") as file:
        data = pickle.load(file)
    return data["model"], data["columns"]

model, columns = load_model()

# -----------------------------
# HEADER
# -----------------------------
st.title("❤️ Heart Failure Survival Predictor")
st.write(
    "Fill in the patient's clinical details below, and the model will "
    "predict the likelihood of survival."
)
st.divider()

# -----------------------------
# USER INPUTS
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", min_value=1, max_value=120, value=60)
    creatinine_phosphokinase = st.number_input(
        "Creatinine Phosphokinase (mcg/L)", min_value=0, value=250
    )
    ejection_fraction = st.number_input(
        "Ejection Fraction (%)", min_value=0, max_value=100, value=38
    )
    platelets = st.number_input(
        "Platelets (kiloplatelets/mL)", min_value=0.0, value=250000.0, step=1000.0
    )
    serum_creatinine = st.number_input(
        "Serum Creatinine (mg/dL)", min_value=0.0, value=1.1, step=0.1
    )
    serum_sodium = st.number_input(
        "Serum Sodium (mEq/L)", min_value=0, value=137
    )
    time = st.number_input(
        "Follow-up Period (days)", min_value=0, value=100
    )

with col2:
    anaemia = st.radio("Anaemia", ["No", "Yes"], horizontal=True)
    diabetes = st.radio("Diabetes", ["No", "Yes"], horizontal=True)
    high_blood_pressure = st.radio("High Blood Pressure", ["No", "Yes"], horizontal=True)
    sex = st.radio("Sex", ["Female", "Male"], horizontal=True)
    smoking = st.radio("Smoking", ["No", "Yes"], horizontal=True)

st.divider()

# -----------------------------
# PREDICTION
# -----------------------------
if st.button("Predict Survival", type="primary", use_container_width=True):

    # Convert Yes/No and Male/Female to 1/0 (same encoding as training data)
    input_dict = {
        "age": age,
        "anaemia": 1 if anaemia == "Yes" else 0,
        "creatinine_phosphokinase": creatinine_phosphokinase,
        "diabetes": 1 if diabetes == "Yes" else 0,
        "ejection_fraction": ejection_fraction,
        "high_blood_pressure": 1 if high_blood_pressure == "Yes" else 0,
        "platelets": platelets,
        "serum_creatinine": serum_creatinine,
        "serum_sodium": serum_sodium,
        "sex": 1 if sex == "Male" else 0,
        "smoking": 1 if smoking == "Yes" else 0,
        "time": time,
    }

    # Make sure column order matches training data exactly
    input_df = pd.DataFrame([input_dict])[columns]

    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0]

    st.subheader("Result")

    if prediction == 1:
        st.error(f"⚠️ High risk — predicted **DEATH_EVENT: Yes**")
        st.write(f"Model confidence: **{probability[1]:.1%}**")
    else:
        st.success(f"✅ Low risk — predicted **DEATH_EVENT: No (Survived)**")
        st.write(f"Model confidence: **{probability[0]:.1%}**")

    with st.expander("See input data used for prediction"):
        st.dataframe(input_df)

st.divider()
st.caption(
    "⚠️ This tool is for educational purposes only and is not a substitute "
    "for professional medical advice."
)
