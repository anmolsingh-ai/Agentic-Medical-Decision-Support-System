"""
app.py — SympTrack Streamlit UI (clean structured output version).
Run with: streamlit run app.py
"""

import logging
import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.WARNING)   # suppress INFO noise in terminal

from main import run
from streaming_utils import stream_text
from validators import validate_patient_inputs

# ── Page config ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="SympTrack – AI Medical Assistant",
    page_icon="🏥",
    layout="wide",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────

st.markdown("""
<style>
.patient-card {
    background: #f0f4ff;
    border-left: 4px solid #4a6cf7;
    border-radius: 8px;
    padding: 14px 20px;
    margin-bottom: 20px;
}
.section-header {
    font-size: 1.1rem;
    font-weight: 700;
    color: #1a1a2e;
    margin-bottom: 6px;
}
.flag-item {
    background: #fff3cd;
    border-left: 3px solid #ffc107;
    padding: 6px 12px;
    border-radius: 4px;
    margin: 4px 0;
    font-size: 0.9rem;
}
.clinic-card {
    background: #f8f9ff;
    border: 1px solid #d0d7ff;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 12px;
}
.disclaimer-box {
    background: #fff8e1;
    border: 1px solid #ffe082;
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 0.85rem;
    color: #5a4a00;
    margin-top: 24px;
}
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────────────────────

st.markdown("## 🏥 SympTrack — AI Symptoms Analyzer")
st.caption("Describe your symptoms and get an AI-powered educational analysis.")

# ── API key validation (silent — no UI message on success) ──────────────────

_missing = [k for k in ("ZHIPU_API_KEY", "SERPER_API_KEY") if not os.getenv(k)]
if _missing:
    st.error(f"❌ Missing API keys: {', '.join(_missing)}. Add them to your .env file.")
    st.stop()

# ── Input form ───────────────────────────────────────────────────────────────

with st.form("patient_form"):
    c1, c2, c3, c4 = st.columns([1, 1, 1, 2])
    with c1:
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    with c2:
        age = st.number_input("Age", min_value=1, max_value=120, value=25, step=1)
    with c3:
        city = st.text_input("City", placeholder="e.g., Lucknow")
    with c4:
        symptoms = st.text_input(
            "Symptoms",
            placeholder="e.g., fever, cough, sore throat",
        )
    submitted = st.form_submit_button("🔍 Analyze", use_container_width=True, type="primary")

# ── On submit ────────────────────────────────────────────────────────────────

if submitted:
    age_str = str(int(age))
    errors = validate_patient_inputs(gender, age_str, symptoms, city)

    if errors:
        for e in errors:
            st.warning(f"⚠️ {e}")
        st.stop()

    # ── Patient summary card ─────────────────────────────────────────────────
    st.markdown(f"""
    <div class="patient-card">
        <div class="section-header">👤 Patient Profile</div>
        <b>Gender:</b> {gender} &nbsp;|&nbsp;
        <b>Age:</b> {age_str} years &nbsp;|&nbsp;
        <b>City:</b> {city} &nbsp;|&nbsp;
        <b>Symptoms:</b> {symptoms}
    </div>
    """, unsafe_allow_html=True)

    # ── Run crew ─────────────────────────────────────────────────────────────
    with st.spinner("🤖 Analyzing symptoms…"):
        try:
            diagnosis_text, clinics_text = run(gender, age_str, symptoms, city)
        except Exception as exc:
            st.error(f"❌ Analysis failed: {exc}")
            st.stop()

    # ── Output tabs ──────────────────────────────────────────────────────────
    tab1, tab2 = st.tabs(["🧠 Diagnosis & Treatment", "🏥 Clinic Recommendations"])

    with tab1:
        container = st.empty()
        rendered = ""
        for chunk in stream_text(diagnosis_text, chunk_size=3, delay=0.01):
            rendered += chunk
            container.markdown(rendered)

    with tab2:
        container = st.empty()
        rendered = ""
        for chunk in stream_text(clinics_text, chunk_size=3, delay=0.01):
            rendered += chunk
            container.markdown(rendered)

    # ── Disclaimer ───────────────────────────────────────────────────────────
    st.markdown("""
    <div class="disclaimer-box">
        ⚠️ <b>Medical Disclaimer:</b> This analysis is for <b>educational purposes only</b>
        and is not a substitute for professional medical advice, diagnosis, or treatment.
        Always consult a qualified healthcare professional. In an emergency, call your
        local emergency services immediately.
    </div>
    """, unsafe_allow_html=True)