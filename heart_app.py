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
            linear-gradient(160deg, rgba(15,4,40,0.85) 0%, rgba(40,6,60,0.75) 35%, rgba(90,10,40,0.78) 100%),
            url('{BACKGROUND_URL}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }}
 
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{background: transparent !important;}}
 
    .block-container {{
        max-width: 740px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }}
 
    /* ---------- TITLE ---------- */
    .app-title {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.2rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(90deg, #ff5f7e 0%, #b967ff 50%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
        text-shadow: 0 0 25px rgba(185,103,255,0.3);
    }}
    .app-subtitle {{
        text-align: center;
        color: #e8e2ff;
        font-size: 0.95rem;
        font-weight: 300;
        margin-top: 0.3rem;
        margin-bottom: 1.7rem;
        opacity: 0.9;
    }}
 
    /* ---------- EQUAL-HEIGHT COLUMNS ---------- */
    div[data-testid="stHorizontalBlock"] {{
        align-items: stretch !important;
    }}
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {{
        display: flex !important;
        flex-direction: column !important;
    }}
    div[data-testid="column"] > div {{
        height: 100% !important;
    }}
    div[data-testid="column"] div[data-testid="stVerticalBlock"] {{
        height: 100% !important;
    }}
 
    /* ---------- GLASS CARD (visibly translucent) ---------- */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background: rgba(255, 255, 255, 0.16) !important;
        backdrop-filter: blur(20px) saturate(140%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(140%) !important;
        border: 1px solid rgba(255, 255, 255, 0.30) !important;
        border-radius: 20px !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255,255,255,0.25);
        padding: 1.3rem 1.3rem 1rem 1.3rem;
        height: 100% !important;
        display: flex !important;
        flex-direction: column !important;
    }}
    div[data-testid="stVerticalBlockBorderWrapper"] > div {{
        background: transparent !important;
        flex-grow: 1;
        display: flex;
        flex-direction: column;
    }}
 
    .section-heading {{
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        font-size: 1.08rem;
        color: #ffb3c6;
        margin-bottom: 1rem;
        letter-spacing: 0.3px;
        text-align: center;
    }}
    .section-heading.blue {{ color: #9fd3ff; }}
 
    /* ---------- NUMBER INPUTS ---------- */
    div[data-testid="stNumberInput"] label p {{
        color: #f8f5ff !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
    }}
    div[data-testid="stNumberInput"] input {{
        background: rgba(255,255,255,0.18) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        border-radius: 10px !important;
    }}
 
    /* ---------- TOGGLE ROWS (health background) ---------- */
    div[data-testid="stToggle"] label p {{
        color: #f8f5ff !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
    }}
    div[data-testid="stToggle"] {{
        background: rgba(255,255,255,0.10);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 12px;
        padding: 0.6rem 0.9rem;
        margin-bottom: 0.6rem;
    }}
 
    /* ---------- SEX SEGMENTED CONTROL ---------- */
    div[data-testid="stRadio"] label p {{
        color: #f8f5ff !important;
        font-weight: 500 !important;
    }}
    div[data-testid="stRadio"] > div {{
        background: rgba(255,255,255,0.10);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 12px;
        padding: 8px 10px;
        justify-content: center;
    }}
 
    /* ---------- PREDICT BUTTON (normal width, centered) ---------- */
    div[data-testid="stButton"] {{
        display: flex;
        justify-content: center;
    }}
    div[data-testid="stButton"] button {{
        background: linear-gradient(90deg, #ff5f7e 0%, #b967ff 50%, #4facfe 100%);
        color: white;
        font-weight: 700;
        font-size: 1rem;
        border: none;
        border-radius: 14px;
        padding: 0.6rem 2.4rem;
        box-shadow: 0 0 22px rgba(185, 103, 255, 0.45);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }}
    div[data-testid="stButton"] button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 0 32px rgba(185, 103, 255, 0.65);
        color: white;
    }}
 
    /* ---------- RESULT CARD ---------- */
    .result-card {{
        text-align: center;
        border-radius: 22px;
        padding: 1.8rem 1.4rem;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.25);
        margin-top: 1.2rem;
        margin-bottom: 1rem;
    }}
    .result-card.survive {{
        background: linear-gradient(135deg, rgba(79,172,254,0.32), rgba(185,103,255,0.26));
        box-shadow: 0 0 40px rgba(79,172,254,0.4);
    }}
    .result-card.risk {{
        background: linear-gradient(135deg, rgba(255,95,126,0.36), rgba(185,103,255,0.24));
        box-shadow: 0 0 40px rgba(255,95,126,0.4);
    }}
    .result-title {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.7rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.3rem;
        text-shadow: 0 0 18px rgba(255,255,255,0.3);
    }}
    .result-sub {{
        font-size: 0.95rem;
        color: #f8f5ff;
        opacity: 0.95;
        margin-bottom: 1.3rem;
    }}
 
    /* ---------- CONFIDENCE BARS ---------- */
    .conf-label {{
        display: flex;
        justify-content: space-between;
        font-weight: 600;
        font-size: 0.92rem;
        color: #ffffff;
        margin-bottom: 4px;
    }}
    .conf-track {{
        width: 100%;
        height: 14px;
        background: rgba(255,255,255,0.18);
        border-radius: 8px;
        overflow: hidden;
        margin-bottom: 1rem;
    }}
    .conf-fill-survive {{
        height: 100%;
        border-radius: 8px;
        background: linear-gradient(90deg, #4facfe, #b967ff);
        box-shadow: 0 0 12px rgba(79,172,254,0.6);
    }}
    .conf-fill-risk {{
        height: 100%;
        border-radius: 8px;
        background: linear-gradient(90deg, #ff5f7e, #ff9f6b);
        box-shadow: 0 0 12px rgba(255,95,126,0.6);
    }}
 
    .disclaimer {{
        text-align: center;
        color: #f0eaff;
        opacity: 0.8;
        font-size: 0.82rem;
        margin-top: 1.5rem;
    }}
 
    /* ---------- MOBILE ---------- */
    @media (max-width: 600px) {{
        .app-title {{ font-size: 1.6rem; }}
        .app-subtitle {{ font-size: 0.82rem; }}
        .result-title {{ font-size: 1.35rem; }}
        .block-container {{ padding-left: 0.8rem; padding-right: 0.8rem; }}
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {{
            display: block !important;
        }}
        div[data-testid="stVerticalBlockBorderWrapper"] {{
            height: auto !important;
            margin-bottom: 1rem;
        }}
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
col1, col2 = st.columns(2, gap="medium")
 
with col1:
    with st.container(border=True):
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
 
with col2:
    with st.container(border=True):
        st.markdown('<div class="section-heading blue">📋 Health Background</div>', unsafe_allow_html=True)
        anaemia = st.toggle("🩸 Anaemia", value=False)
        diabetes = st.toggle("🍬 Diabetes", value=False)
        high_blood_pressure = st.toggle("💢 High Blood Pressure", value=False)
        smoking = st.toggle("🚬 Smoking", value=False)
        sex = st.radio("⚧ Sex", ["Female", "Male"], horizontal=True)
 
        anaemia = "Yes" if anaemia else "No"
        diabetes = "Yes" if diabetes else "No"
        high_blood_pressure = "Yes" if high_blood_pressure else "No"
        smoking = "Yes" if smoking else "No"
 
st.write("")
predict_clicked = st.button("✨ Predict Survival", type="primary")
 
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
 
    card_class = "risk" if prediction == 1 else "survive"
    title = "⚠️ High Risk Predicted" if prediction == 1 else "✅ Likely to Survive"
    subtitle = (
        "The model predicts a higher likelihood of a death event"
        if prediction == 1 else
        "The model predicts a lower likelihood of a death event"
    )
 
    st.markdown(
        f"""
        <div class="result-card {card_class}">
            <div class="result-title">{title}</div>
            <div class="result-sub">{subtitle}</div>
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
