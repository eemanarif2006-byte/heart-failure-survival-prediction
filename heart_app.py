import streamlit as st
import pandas as pd
import pickle
 
# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Heart Failure Survival Predictor",
    page_icon="❤️",
    layout="wide"
)
 
BACKGROUND_URL = "https://i.pinimg.com/1200x/30/da/56/30da565b9ba54887ef1f73ea110c068e.jpg"
 
# -----------------------------
# CUSTOM STYLING
# -----------------------------
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap');
 
    html, body, [class*="css"] {{
        font-family: 'Poppins', sans-serif;
    }}
 
    /* ---------- BACKGROUND ---------- */
    .stApp {{
        background:
            linear-gradient(160deg, rgba(15,4,40,0.82) 0%, rgba(40,6,60,0.72) 35%, rgba(90,10,40,0.75) 100%),
            url('{BACKGROUND_URL}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }}
 
    /* Hide default streamlit chrome */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{background: transparent !important;}}
 
    /* ---------- TITLE ---------- */
    .app-title {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.6rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(90deg, #ff5f7e 0%, #b967ff 50%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
        padding-top: 0.5rem;
    }}
    .app-subtitle {{
        text-align: center;
        color: #e8e2ff;
        font-size: 1.02rem;
        font-weight: 300;
        margin-top: 0.3rem;
        margin-bottom: 1.8rem;
        opacity: 0.9;
    }}
 
    /* ---------- GLASS CARD ---------- */
    .glass-card {{
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        border-radius: 20px;
        padding: 1.6rem 1.8rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
        margin-bottom: 1.2rem;
    }}
 
    .section-heading {{
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        font-size: 1.15rem;
        color: #ffb3c6;
        margin-bottom: 0.8rem;
        letter-spacing: 0.3px;
    }}
    .section-heading.blue {{ color: #9fd3ff; }}
 
    /* ---------- INPUT WIDGETS ---------- */
    div[data-testid="stNumberInput"] label,
    div[data-testid="stRadio"] label {{
        color: #f2eefc !important;
        font-weight: 500 !important;
    }}
 
    div[data-testid="stNumberInput"] input {{
        background: rgba(255,255,255,0.12) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255,255,255,0.25) !important;
        border-radius: 10px !important;
    }}
 
    div[data-testid="stRadio"] > div {{
        background: rgba(255,255,255,0.06);
        border-radius: 12px;
        padding: 6px 10px;
    }}
 
    /* ---------- PREDICT BUTTON ---------- */
    div[data-testid="stButton"] button {{
        background: linear-gradient(90deg, #ff5f7e 0%, #b967ff 50%, #4facfe 100%);
        color: white;
        font-weight: 700;
        font-size: 1.05rem;
        border: none;
        border-radius: 14px;
        padding: 0.7rem 0;
        box-shadow: 0 6px 20px rgba(185, 103, 255, 0.4);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }}
    div[data-testid="stButton"] button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 10px 26px rgba(185, 103, 255, 0.55);
        color: white;
    }}
 
    /* ---------- RESULT CARD ---------- */
    .result-card {{
        text-align: center;
        border-radius: 22px;
        padding: 2rem 1.5rem;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.22);
        margin-top: 1rem;
        margin-bottom: 1rem;
    }}
    .result-card.survive {{
        background: linear-gradient(135deg, rgba(79,172,254,0.28), rgba(185,103,255,0.22));
        box-shadow: 0 8px 30px rgba(79,172,254,0.35);
    }}
    .result-card.risk {{
        background: linear-gradient(135deg, rgba(255,95,126,0.32), rgba(185,103,255,0.20));
        box-shadow: 0 8px 30px rgba(255,95,126,0.35);
    }}
    .result-title {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.3rem;
    }}
    .result-sub {{
        font-size: 1rem;
        color: #f0eaff;
        opacity: 0.9;
        margin-bottom: 1.3rem;
    }}
 
    /* ---------- CONFIDENCE BARS ---------- */
    .conf-label {{
        display: flex;
        justify-content: space-between;
        font-weight: 600;
        font-size: 0.95rem;
        color: #ffffff;
        margin-bottom: 4px;
    }}
    .conf-track {{
        width: 100%;
        height: 14px;
        background: rgba(255,255,255,0.15);
        border-radius: 8px;
        overflow: hidden;
        margin-bottom: 1rem;
    }}
    .conf-fill-survive {{
        height: 100%;
        border-radius: 8px;
        background: linear-gradient(90deg, #4facfe, #b967ff);
    }}
    .conf-fill-risk {{
        height: 100%;
        border-radius: 8px;
        background: linear-gradient(90deg, #ff5f7e, #ff9f6b);
    }}
 
    .disclaimer {{
        text-align: center;
        color: #e5dfff;
        opacity: 0.75;
        font-size: 0.85rem;
        margin-top: 1.5rem;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
 
# -----------------------------
# LOAD MODEL
# -----------------------------
@st.cache_resource
def load_model():
    with open("heart_model.pkl", "rb") as file:
        data = pickle.load(file)
 
    if isinstance(data, dict) and "model" in data:
        model = data["model"]
        columns = data["columns"]
    else:
        model = data
        columns = [
            "age", "anaemia", "creatinine_phosphokinase", "diabetes",
            "ejection_fraction", "high_blood_pressure", "platelets",
            "serum_creatinine", "serum_sodium", "sex", "smoking", "time"
        ]
    return model, columns
 
model, columns = load_model()
 
# -----------------------------
# HEADER
# -----------------------------
st.markdown('<div class="app-title">❤️ Heart Failure Survival Predictor</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="app-subtitle">Enter the patient\'s clinical details to estimate survival likelihood</div>',
    unsafe_allow_html=True
)
 
# -----------------------------
# USER INPUTS
# -----------------------------
col1, col2 = st.columns(2, gap="large")
 
with col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">🩺 Clinical Measurements</div>', unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)
 
with col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading blue">📋 Health Background</div>', unsafe_allow_html=True)
    anaemia = st.radio("Anaemia", ["No", "Yes"], horizontal=True)
    diabetes = st.radio("Diabetes", ["No", "Yes"], horizontal=True)
    high_blood_pressure = st.radio("High Blood Pressure", ["No", "Yes"], horizontal=True)
    sex = st.radio("Sex", ["Female", "Male"], horizontal=True)
    smoking = st.radio("Smoking", ["No", "Yes"], horizontal=True)
    st.markdown('</div>', unsafe_allow_html=True)
 
st.write("")
predict_clicked = st.button("✨ Predict Survival", type="primary", use_container_width=True)
 
# -----------------------------
# PREDICTION
# -----------------------------
if predict_clicked:
 
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
 
    input_df = pd.DataFrame([input_dict])[columns]
 
    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0]
    survive_pct = probability[0] * 100
    death_pct = probability[1] * 100
 
    if prediction == 1:
        st.markdown(
            f"""
            <div class="result-card risk">
                <div class="result-title">⚠️ High Risk Predicted</div>
                <div class="result-sub">The model predicts a higher likelihood of a death event</div>
                <div class="conf-label"><span>💙 Survival Confidence</span><span>{survive_pct:.1f}%</span></div>
                <div class="conf-track"><div class="conf-fill-survive" style="width:{survive_pct}%;"></div></div>
                <div class="conf-label"><span>❤️ Risk Confidence</span><span>{death_pct:.1f}%</span></div>
                <div class="conf-track"><div class="conf-fill-risk" style="width:{death_pct}%;"></div></div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div class="result-card survive">
                <div class="result-title">✅ Likely to Survive</div>
                <div class="result-sub">The model predicts a lower likelihood of a death event</div>
                <div class="conf-label"><span>💙 Survival Confidence</span><span>{survive_pct:.1f}%</span></div>
                <div class="conf-track"><div class="conf-fill-survive" style="width:{survive_pct}%;"></div></div>
                <div class="conf-label"><span>❤️ Risk Confidence</span><span>{death_pct:.1f}%</span></div>
                <div class="conf-track"><div class="conf-fill-risk" style="width:{death_pct}%;"></div></div>
            </div>
            """,
            unsafe_allow_html=True
        )
 
    with st.expander("See input data used for prediction"):
        st.dataframe(input_df)
 
st.markdown(
    '<div class="disclaimer">⚠️ This tool is for educational purposes only and is not a substitute for professional medical advice.</div>',
    unsafe_allow_html=True
)
 
