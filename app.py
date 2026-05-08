import streamlit as st
import pandas as pd
import numpy as np
import sys, os, warnings
warnings.filterwarnings('ignore')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(
    page_title="Health Patient Analysis",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=Space+Grotesk:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif !important; }
.stApp { background: #080814 !important; }
.main .block-container { padding: 2rem 2.5rem 3rem !important; max-width: 1300px !important; }

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0E0E20 0%, #160810 100%) !important;
    border-right: 1px solid rgba(192,21,43,0.2) !important;
}
section[data-testid="stSidebar"] * { color: #E8E8F0 !important; }

h1,h2,h3,h4 { font-family: 'Syne', sans-serif !important; color: #F0F0FA !important; }
p, li { font-family: 'Space Grotesk', sans-serif !important; color: #C8C8D8 !important; }
code, pre { font-family: 'DM Mono', monospace !important; }

@keyframes fadeUp { from{opacity:0;transform:translateY(16px)} to{opacity:1;transform:translateY(0)} }
@keyframes pulse  { 0%,100%{transform:scale(1)} 50%{transform:scale(1.1)} }
@keyframes glow   { 0%,100%{box-shadow:0 0 20px rgba(192,21,43,0.3)} 50%{box-shadow:0 0 50px rgba(192,21,43,0.65)} }
@keyframes spin   { to{transform:rotate(360deg)} }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #C0152B, #7A0018) !important;
    color: white !important; border: none !important;
    border-radius: 14px !important; padding: 0.8rem 1.5rem !important;
    font-family: 'Syne', sans-serif !important; font-weight: 700 !important;
    font-size: 1rem !important; letter-spacing: 0.04em !important;
    width: 100% !important; transition: all 0.25s !important;
    box-shadow: 0 4px 24px rgba(192,21,43,0.4) !important;
}
.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 12px 40px rgba(192,21,43,0.6) !important;
}

/* Sliders */
.stSlider > div > div > div > div { background: #C0152B !important; }

/* Select boxes */
.stSelectbox > div > div, .stMultiSelect > div > div {
    background: rgba(20,20,40,0.9) !important;
    border: 1px solid rgba(192,21,43,0.3) !important;
    color: #E8E8F0 !important;
}

/* Radio */
.stRadio label {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 10px !important; padding: 0.6rem 1rem !important;
    font-family: 'Space Grotesk', sans-serif !important;
    color: #E8E8F0 !important; cursor: pointer !important;
    transition: all 0.2s !important;
}
.stRadio label:hover {
    background: rgba(192,21,43,0.15) !important;
    border-color: rgba(192,21,43,0.4) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(20,20,40,0.8) !important;
    border-radius: 12px !important; padding: 0.3rem !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important; color: #8892A4 !important;
    border-radius: 8px !important; font-family: 'Space Grotesk', sans-serif !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(192,21,43,0.25) !important; color: #F0F0FA !important;
}

label { font-family: 'Space Grotesk', sans-serif !important; color: #A8A8C0 !important; font-size: 0.85rem !important; }

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #080814; }
::-webkit-scrollbar-thumb { background: #C0152B; border-radius: 3px; }
hr { border-color: rgba(192,21,43,0.18) !important; }
</style>
""", unsafe_allow_html=True)

# ── UI Components ──────────────────────────────────────────────────────────────
def hero(title, sub):
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,rgba(192,21,43,0.12) 0%,rgba(20,20,46,0.7) 55%,rgba(8,8,20,0) 100%);
         border:1px solid rgba(192,21,43,0.28);border-radius:22px;padding:2.5rem 3rem 2rem;
         margin-bottom:2rem;position:relative;overflow:hidden;animation:fadeUp 0.5s ease;">
      <div style="position:absolute;top:-60%;right:-8%;width:480px;height:480px;
           background:radial-gradient(circle,rgba(192,21,43,0.1) 0%,transparent 68%);pointer-events:none;"></div>
      <h1 style="font-family:'Syne',sans-serif;font-size:2.3rem;font-weight:800;
                 color:#F0F0FA;margin-bottom:0.45rem;letter-spacing:-0.02em;">{title}</h1>
      <p style="font-size:0.97rem;color:#7A8499;max-width:640px;line-height:1.65;
                font-family:'Space Grotesk',sans-serif;margin:0;">{sub}</p>
    </div>""", unsafe_allow_html=True)

def sec(t, badge=None):
    b = (f'<span style="background:rgba(192,21,43,0.18);border:1px solid rgba(192,21,43,0.38);'
         f'border-radius:5px;padding:0.12rem 0.55rem;font-family:DM Mono,monospace;'
         f'font-size:0.67rem;color:#E8304A;">{badge}</span>') if badge else ''
    st.markdown(
        f'<div style="display:flex;align-items:center;gap:0.7rem;border-bottom:1px solid rgba(192,21,43,0.22);'
        f'padding-bottom:0.6rem;margin:1.4rem 0 0.9rem;">'
        f'<h3 style="margin:0;font-size:1.05rem;font-weight:700;color:#F0F0FA;font-family:Syne,sans-serif;">{t}</h3>'
        f'{b}</div>', unsafe_allow_html=True)

def cards(items):
    cols = st.columns(len(items))
    for col,(val,lbl) in zip(cols,items):
        with col:
            st.markdown(
                f'<div style="background:linear-gradient(135deg,rgba(22,22,44,0.95),rgba(18,8,18,0.9));'
                f'border:1px solid rgba(192,21,43,0.28);border-radius:16px;padding:1.2rem;text-align:center;">'
                f'<div style="font-family:Syne,sans-serif;font-size:1.85rem;font-weight:800;color:#C0152B;">{val}</div>'
                f'<div style="font-size:0.68rem;color:#8892A4;text-transform:uppercase;letter-spacing:0.1em;'
                f'margin-top:0.2rem;font-family:Space Grotesk,sans-serif;">{lbl}</div></div>',
                unsafe_allow_html=True)

def info_box(text, color="#8892A4"):
    st.markdown(
        f'<div style="background:rgba(22,22,44,0.7);border-left:3px solid {color};'
        f'border-radius:0 10px 10px 0;padding:0.75rem 1rem;margin:0.4rem 0;">'
        f'<span style="font-family:Space Grotesk,sans-serif;font-size:0.83rem;color:{color};">{text}</span></div>',
        unsafe_allow_html=True)

def tag(color, text):
    st.markdown(
        f'<div style="margin-top:-0.25rem;margin-bottom:0.6rem;">'
        f'<span style="font-size:0.76rem;color:{color};font-family:Space Grotesk,sans-serif;font-weight:600;">'
        f'→ {text}</span></div>', unsafe_allow_html=True)

def kv(k, v):
    st.markdown(
        f'<div style="display:flex;justify-content:space-between;padding:0.38rem 0;'
        f'border-bottom:1px solid rgba(255,255,255,0.04);">'
        f'<span style="font-size:0.79rem;color:#6A6A88;font-family:Space Grotesk,sans-serif;">{k}</span>'
        f'<span style="font-size:0.79rem;color:#E0E0F0;font-family:DM Mono,monospace;">{v}</span></div>',
        unsafe_allow_html=True)

def pill(text):
    st.markdown(
        f'<div style="display:inline-block;background:linear-gradient(90deg,#C0152B,#7A0018);'
        f'border-radius:50px;padding:0.32rem 1.2rem;font-family:DM Mono,monospace;font-size:0.76rem;'
        f'color:white;letter-spacing:0.06em;margin-bottom:1.1rem;">⚙ {text}</div>',
        unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        '<div style="text-align:center;padding:1.8rem 0 1.2rem;">'
        '<span style="font-size:3.4rem;display:block;margin-bottom:0.5rem;">🫀</span>'
        '<div style="font-family:Syne,sans-serif;font-size:1.5rem;font-weight:800;color:#C0152B;letter-spacing:0.04em;">CardioSense</div>'
        '<div style="font-size:0.64rem;color:#44445A;letter-spacing:0.22em;text-transform:uppercase;'
        'font-family:Space Grotesk,sans-serif;margin-top:0.25rem;">AI Health Platform</div></div>',
        unsafe_allow_html=True)
    st.markdown('<hr>', unsafe_allow_html=True)
    page = st.radio("", [
        "🏠  Home",
        "🤖  Risk Prediction",
        "👥  My Patient Group",
        "💡  Health Patterns",
        "🌡  Health Check",
    ], label_visibility="collapsed")
    st.markdown('<hr>', unsafe_allow_html=True)
    st.markdown(
        '<div style="font-family:DM Mono,monospace;font-size:0.68rem;">'
        '<div style="color:#C0152B;font-weight:600;margin-bottom:0.5rem;letter-spacing:0.05em;">MODULES</div>'
        '<div style="color:#383858;margin-bottom:0.3rem;">🌳 CART Decision Tree</div>'
        '<div style="color:#383858;margin-bottom:0.3rem;">🔵 DBSCAN Clustering</div>'
        '<div style="color:#383858;margin-bottom:0.3rem;">🌿 FP-Growth Mining</div>'
        '<div style="margin-top:1rem;color:#1E1E38;font-size:0.6rem;">v5.0 · 5,650 clinical records</div></div>',
        unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 🏠 HOME
# ══════════════════════════════════════════════════════════════════════════════
if "Home" in page:
    hero("🫀 Welcome to AI Health Patients Analysis",
         "Your personal cardiovascular health intelligence platform. Enter your health data to get "
         "instant risk prediction, discover your patient group, and uncover hidden health patterns.")

    st.markdown("""
    <div style="background:linear-gradient(135deg,rgba(192,21,43,0.08),rgba(20,20,50,0.6));
         border:1px solid rgba(192,21,43,0.2);border-radius:18px;padding:2rem 2.5rem;
         margin-bottom:2rem;animation:fadeUp 0.5s ease 0.1s both;">
      <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;
                  color:#F0F0FA;margin-bottom:1.2rem;">🚀 What can you do here?</div>
      <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:1rem;">
    """ + "".join([
        f'<div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);'
        f'border-radius:12px;padding:1.1rem;">'
        f'<div style="font-size:1.6rem;margin-bottom:0.5rem;">{ico}</div>'
        f'<div style="font-family:Syne,sans-serif;font-size:0.92rem;font-weight:700;color:#E8E8F0;margin-bottom:0.3rem;">{ttl}</div>'
        f'<div style="font-family:Space Grotesk,sans-serif;font-size:0.78rem;color:#5A5A78;line-height:1.6;">{dsc}</div></div>'
        for ico,ttl,dsc in [
            ("🤖","Risk Prediction","Enter 8 vitals — AI predicts High Risk or Low Risk with probability score"),
            ("👥","My Patient Group","Discover which patient cluster you belong to based on your health profile"),
            ("💡","Health Patterns","See what combinations of risk factors are most dangerous together"),
            ("🌡","Health Check","Instant snapshot — enter any metric and get clinical context"),
        ]
    ]) + "</div></div>", unsafe_allow_html=True)

    cards([
        ("🤖","CART Prediction"),
        ("🔵","DBSCAN Groups"),
        ("🌿","FP-Growth Patterns"),
        ("9","Input Features"),
    ])

    st.markdown("<br>", unsafe_allow_html=True)
    sec("📋 How to Use This App")
    steps = [
        ("1","Use the sidebar","Click any page in the left sidebar to navigate."),
        ("2","Enter your health data","Each page has sliders and dropdowns — fill them in."),
        ("3","Click Analyze / Find / Discover","Hit the big button to run the AI model."),
        ("4","Read your results","Get plain-English insights with color-coded risk levels."),
    ]
    c1,c2 = st.columns(2)
    for i,(num,ttl,dsc) in enumerate(steps):
        col = c1 if i < 2 else c2
        with col:
            st.markdown(
                f'<div style="display:flex;gap:1rem;align-items:flex-start;padding:0.8rem 0;'
                f'border-bottom:1px solid rgba(255,255,255,0.04);">'
                f'<div style="min-width:32px;height:32px;background:rgba(192,21,43,0.25);border:1px solid rgba(192,21,43,0.4);'
                f'border-radius:8px;display:flex;align-items:center;justify-content:center;'
                f'font-family:Syne,sans-serif;font-size:0.9rem;font-weight:700;color:#E8304A;">{num}</div>'
                f'<div><div style="font-family:Syne,sans-serif;font-size:0.88rem;font-weight:700;color:#E8E8F0;">{ttl}</div>'
                f'<div style="font-family:Space Grotesk,sans-serif;font-size:0.78rem;color:#5A5A78;margin-top:0.15rem;">{dsc}</div>'
                f'</div></div>',
                unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 🤖 RISK PREDICTION
# ══════════════════════════════════════════════════════════════════════════════
elif "Risk Prediction" in page:
    hero("🤖 Cardiovascular Risk Prediction",
         "Fill in your 8 health metrics below. The CART AI model will instantly assess your cardiovascular risk level.")
    pill("CART Decision Tree — Binary Risk Classification")

    ci, co = st.columns([1.05, 1])

    with ci:
        sec("👤 Enter Your Health Details")
        st.markdown(
            '<div style="background:linear-gradient(135deg,rgba(22,22,44,0.97),rgba(14,7,16,0.94));'
            'border:1px solid rgba(192,21,43,0.25);border-radius:18px;padding:1.8rem;">',
            unsafe_allow_html=True)

        # Age
        st.markdown('<div style="font-size:0.82rem;color:#A8A8C0;margin-bottom:0.18rem;">🎂 Age (years)</div>', unsafe_allow_html=True)
        age = st.slider("age", 18, 90, 45, label_visibility="collapsed")
        if age < 35:   tag('#22C55E','✅ Low-risk age group (under 35)')
        elif age < 55: tag('#F59E0B','🟡 Moderate-risk age (35–54 yrs)')
        else:          tag('#C0152B','🔴 High-risk age group (55+ yrs)')

        # BP
        st.markdown('<div style="font-size:0.82rem;color:#A8A8C0;margin-bottom:0.18rem;">🩺 Blood Pressure (mmHg)</div>', unsafe_allow_html=True)
        bp = st.slider("bp", 60, 200, 120, label_visibility="collapsed")
        if bp < 120:   tag('#22C55E','✅ Normal blood pressure (< 120)')
        elif bp < 140: tag('#F59E0B','🟡 Elevated (120–139) — watch closely')
        else:          tag('#C0152B','🔴 Hypertension range (≥ 140)')

        # Cholesterol
        st.markdown('<div style="font-size:0.82rem;color:#A8A8C0;margin-bottom:0.18rem;">🧪 Total Cholesterol (mg/dL)</div>', unsafe_allow_html=True)
        chol = st.slider("chol", 100, 300, 180, label_visibility="collapsed")
        if chol < 170:   tag('#22C55E','✅ Desirable cholesterol (< 170)')
        elif chol < 200: tag('#F59E0B','🟡 Borderline high (170–199)')
        else:            tag('#C0152B','🔴 High cholesterol (≥ 200)')

        # Gender
        st.markdown('<div style="font-size:0.82rem;color:#A8A8C0;margin-bottom:0.18rem;">⚧ Gender</div>', unsafe_allow_html=True)
        gender = st.selectbox("gender", ["Male","Female"], label_visibility="collapsed")

        # BMI
        st.markdown('<div style="font-size:0.82rem;color:#A8A8C0;margin-bottom:0.18rem;">⚖️ BMI (Body Mass Index)</div>', unsafe_allow_html=True)
        bmi = st.slider("bmi", 10.0, 55.0, 25.0, 0.1, label_visibility="collapsed")
        if bmi < 18.5:   tag('#F59E0B','🟡 Underweight (< 18.5)')
        elif bmi < 25:   tag('#22C55E','✅ Normal weight (18.5–24.9)')
        elif bmi < 30:   tag('#F59E0B','🟡 Overweight (25–29.9)')
        else:            tag('#C0152B','🔴 Obese (≥ 30) — elevated risk')

        # Glucose
        st.markdown('<div style="font-size:0.82rem;color:#A8A8C0;margin-bottom:0.18rem;">🩸 Blood Glucose (mg/dL)</div>', unsafe_allow_html=True)
        glucose = st.slider("glucose", 50, 300, 90, label_visibility="collapsed")
        if glucose < 100:   tag('#22C55E','✅ Normal fasting glucose (< 100)')
        elif glucose < 126: tag('#F59E0B','🟡 Pre-diabetic range (100–125)')
        else:               tag('#C0152B','🔴 Diabetic range (≥ 126)')

        st.markdown('<hr style="border-color:rgba(192,21,43,0.15);margin:0.6rem 0;">', unsafe_allow_html=True)

        # Smoking
        st.markdown('<div style="font-size:0.82rem;color:#A8A8C0;margin-bottom:0.18rem;">🚬 Smoking Status</div>', unsafe_allow_html=True)
        smk_opt = st.select_slider("smk", ["Non-Smoker","Former Smoker","Current Smoker"],
                                   value="Non-Smoker", label_visibility="collapsed")
        smoking = 1 if smk_opt == "Current Smoker" else 0
        if smk_opt == "Current Smoker":  tag('#C0152B','⚠️ Active smoker — major risk factor')
        elif smk_opt == "Former Smoker": tag('#F59E0B','ℹ️ Former smoker — residual risk')
        else:                            tag('#22C55E','✅ Non-smoker')

        # Family History
        st.markdown('<div style="font-size:0.82rem;color:#A8A8C0;margin-bottom:0.18rem;">🧬 Family History of Heart Disease</div>', unsafe_allow_html=True)
        fam_opt = st.select_slider("fam", ["None","One Relative","Multiple Relatives"],
                                   value="None", label_visibility="collapsed")
        fam_hx = 0 if fam_opt == "None" else 1
        if fam_opt == "Multiple Relatives": tag('#C0152B','⚠️ Strong genetic predisposition')
        elif fam_opt == "One Relative":     tag('#F59E0B','ℹ️ Moderate genetic risk')
        else:                               tag('#22C55E','✅ No family history')

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<br>', unsafe_allow_html=True)
        btn = st.button("🫀  Analyze My Cardiovascular Risk", use_container_width=True)

    with co:
        sec("📊 Your Risk Assessment")
        if btn:
            with st.spinner("AI analyzing your health profile..."):
                try:
                    from modules.predict import predict_risk
                    label, proba, pred = predict_risk(
                        age, bp, chol, gender, bmi, glucose, smoking, 0, fam_hx)
                    hr = proba[1]*100
                    lr = proba[0]*100
                    col = '#C0152B' if pred==1 else '#22C55E'
                    ico = '🔴' if pred==1 else '🟢'
                    ttl = 'HIGH RISK' if pred==1 else 'LOW RISK'
                    msg = ('Significant cardiovascular risk factors detected. Please consult a physician.'
                           if pred==1 else
                           'Your profile shows low cardiovascular risk. Maintain your healthy habits!')

                    st.markdown(
                        f'<div style="background:linear-gradient(135deg,{col}20,{col}08);'
                        f'border:2px solid {col};border-radius:20px;padding:2rem;text-align:center;'
                        f'margin-bottom:1rem;{"animation:glow 2s infinite;" if pred==1 else ""}">'
                        f'<div style="font-size:3.8rem;margin-bottom:0.3rem;">{ico}</div>'
                        f'<div style="font-family:Syne,sans-serif;font-size:2.1rem;font-weight:800;'
                        f'color:{col};letter-spacing:0.03em;">{ttl}</div>'
                        f'<div style="font-family:DM Mono,monospace;font-size:2rem;color:{col}CC;'
                        f'margin-top:0.5rem;font-weight:700;">{hr:.0f}%</div>'
                        f'<div style="font-size:0.72rem;color:#8892A4;font-family:Space Grotesk,sans-serif;">risk probability</div>'
                        f'<div style="margin-top:0.8rem;font-family:Space Grotesk,sans-serif;font-size:0.84rem;'
                        f'color:#8892A4;max-width:300px;margin-left:auto;margin-right:auto;">{msg}</div></div>',
                        unsafe_allow_html=True)

                    # Risk bar
                    sec("📊 Risk Probability Breakdown")
                    for lbl2, val, c2 in [("🟢 Low Risk", lr, "#22C55E"), ("🔴 High Risk", hr, "#C0152B")]:
                        st.markdown(
                            f'<div style="margin:0.5rem 0;">'
                            f'<div style="display:flex;justify-content:space-between;margin-bottom:0.3rem;">'
                            f'<span style="font-family:Space Grotesk,sans-serif;font-size:0.82rem;color:#C8C8D8;">{lbl2}</span>'
                            f'<span style="font-family:DM Mono,monospace;font-size:0.82rem;color:{c2};font-weight:600;">{val:.1f}%</span></div>'
                            f'<div style="height:10px;background:rgba(255,255,255,0.06);border-radius:5px;overflow:hidden;">'
                            f'<div style="height:100%;width:{val}%;background:{c2};border-radius:5px;'
                            f'transition:width 1s ease;"></div></div></div>',
                            unsafe_allow_html=True)

                    # Risk factor table
                    sec("⚠️ Your Risk Factor Summary")
                    factors = [
                        ("🩸 Glucose",      glucose, 126, f"{glucose} mg/dL"),
                        ("💉 Blood Pressure",bp,     140, f"{bp} mmHg"),
                        ("⚖️ BMI",          bmi,     30,  f"{bmi:.1f}"),
                        ("🔢 Age",           age,     55,  f"{age} yrs"),
                        ("🚬 Smoking",       smoking,  1,  smk_opt),
                        ("🧬 Family History",fam_hx,   1,  fam_opt),
                    ]
                    for fname, fval, thresh, disp in factors:
                        risk_flag = fval >= thresh
                        fc = '#EF4444' if risk_flag else '#22C55E'
                        icon2 = '⚠️' if risk_flag else '✅'
                        st.markdown(
                            f'<div style="display:flex;align-items:center;justify-content:space-between;'
                            f'padding:0.42rem 0.8rem;margin:0.22rem 0;background:rgba(22,22,44,0.7);'
                            f'border-radius:10px;border-left:3px solid {fc};">'
                            f'<span style="font-family:Space Grotesk,sans-serif;font-size:0.8rem;color:#C8C8D8;">{fname}</span>'
                            f'<span style="font-family:DM Mono,monospace;font-size:0.78rem;color:{fc};">'
                            f'{icon2} {disp}</span></div>',
                            unsafe_allow_html=True)

                    # Recommendation
                    sec("💊 Recommendations")
                    recs = []
                    if bp >= 140:   recs.append(("💉","Monitor blood pressure daily. Reduce sodium intake and stress."))
                    if glucose>=126:recs.append(("🩸","Check HbA1c with your doctor. Consider dietary changes."))
                    if bmi >= 30:   recs.append(("⚖️","Aim for 150 min/week exercise. Consult a nutritionist."))
                    if smoking:     recs.append(("🚬","Quitting smoking reduces risk by 50% within 1 year."))
                    if age >= 55:   recs.append(("🔢","Annual cardiovascular screening strongly advised."))
                    if not recs:    recs.append(("✅","Keep up your healthy lifestyle! Annual check-up recommended."))
                    for r_ico, r_txt in recs:
                        st.markdown(
                            f'<div style="display:flex;gap:0.8rem;align-items:flex-start;padding:0.6rem 0.8rem;'
                            f'margin:0.3rem 0;background:rgba(22,22,44,0.6);border-radius:10px;'
                            f'border:1px solid rgba(255,255,255,0.05);">'
                            f'<span style="font-size:1.1rem;margin-top:0.1rem;">{r_ico}</span>'
                            f'<span style="font-family:Space Grotesk,sans-serif;font-size:0.8rem;color:#A8A8C0;line-height:1.6;">{r_txt}</span>'
                            f'</div>',
                            unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Prediction error: {e}")
                    import traceback; st.code(traceback.format_exc())
        else:
            st.markdown(
                '<div style="text-align:center;padding:6rem 2rem;background:rgba(20,20,40,0.5);'
                'border-radius:18px;border:1px dashed rgba(192,21,43,0.25);">'
                '<div style="font-size:4.5rem;margin-bottom:1rem;">🫀</div>'
                '<div style="font-family:Syne,sans-serif;font-size:1.15rem;color:#3A3A5A;">Fill in your details on the left</div>'
                '<div style="font-family:DM Mono,monospace;font-size:0.85rem;color:#C0152B;margin-top:0.5rem;">'
                '→ then click Analyze</div></div>',
                unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 👥 MY PATIENT GROUP
# ══════════════════════════════════════════════════════════════════════════════
elif "Patient Group" in page:
    hero("👥 Discover Your Patient Group",
         "Enter your health profile to find which group of similar patients you belong to, "
         "and understand the shared characteristics of your group.")
    pill("DBSCAN Density-Based Clustering + PCA")

    c1,c2 = st.columns([1,1.2])
    with c1:
        sec("🔬 Your Health Profile")
        st.markdown(
            '<div style="background:rgba(22,22,44,0.95);border:1px solid rgba(192,21,43,0.22);'
            'border-radius:18px;padding:1.6rem;">',
            unsafe_allow_html=True)

        st.markdown('<div style="font-size:0.82rem;color:#A8A8C0;margin-bottom:0.18rem;">🔢 Age</div>', unsafe_allow_html=True)
        g_age = st.slider("g_age", 18, 90, 50, label_visibility="collapsed")

        st.markdown('<div style="font-size:0.82rem;color:#A8A8C0;margin-bottom:0.18rem;">💉 Blood Pressure (mmHg)</div>', unsafe_allow_html=True)
        g_bp = st.slider("g_bp", 60, 220, 130, label_visibility="collapsed")

        st.markdown('<div style="font-size:0.82rem;color:#A8A8C0;margin-bottom:0.18rem;">🧪 Cholesterol (mg/dL)</div>', unsafe_allow_html=True)
        g_chol = st.slider("g_chol", 100, 300, 200, label_visibility="collapsed")

        st.markdown('<div style="font-size:0.82rem;color:#A8A8C0;margin-bottom:0.18rem;">⚖️ BMI</div>', unsafe_allow_html=True)
        g_bmi = st.slider("g_bmi", 10.0, 55.0, 27.0, 0.1, label_visibility="collapsed")

        st.markdown('<div style="font-size:0.82rem;color:#A8A8C0;margin-bottom:0.18rem;">🩸 Glucose (mg/dL)</div>', unsafe_allow_html=True)
        g_gluc = st.slider("g_gluc", 50, 300, 100, label_visibility="collapsed")

        st.markdown('<div style="font-size:0.82rem;color:#A8A8C0;margin-bottom:0.18rem;">👤 Gender</div>', unsafe_allow_html=True)
        g_gender = st.selectbox("g_gender", ["Male","Female"], label_visibility="collapsed")

        st.markdown('<div style="font-size:0.82rem;color:#A8A8C0;margin-bottom:0.18rem;">🚬 Smoking</div>', unsafe_allow_html=True)
        g_smk = st.selectbox("g_smk", ["Non-Smoker","Current Smoker"], label_visibility="collapsed")

        st.markdown('<div style="font-size:0.82rem;color:#A8A8C0;margin-bottom:0.18rem;">🧬 Family History</div>', unsafe_allow_html=True)
        g_fam = st.selectbox("g_fam", ["No","Yes"], label_visibility="collapsed")

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<br>', unsafe_allow_html=True)
        grp_btn = st.button("🔵 Find My Patient Group", use_container_width=True)

    with c2:
        sec("👥 Your Group & Similar Patients")
        if grp_btn:
            with st.spinner("Analyzing patient clusters..."):
                try:
                    from modules.cluster import run_dbscan
                    from sklearn.preprocessing import StandardScaler
                    from sklearn.decomposition import PCA

                    result_df, n_clust, n_noise, sil, explained, insights = run_dbscan(2.5, 5)

                    # Find closest cluster for user's input
                    g_smk_enc = 1 if g_smk=="Current Smoker" else 0
                    g_fam_enc = 1 if g_fam=="Yes" else 0
                    g_gen_enc = 1 if g_gender=="Male" else 0
                    user_vals = [g_age, g_bp, g_chol, g_gen_enc, g_bmi, g_gluc, g_smk_enc, 0, g_fam_enc]

                    # Find nearest non-noise point
                    feat_cols = ['Age','Blood Pressure','Cholesterol','BMI','Glucose']
                    user_simple = np.array([g_age, g_bp, g_chol, g_bmi, g_gluc])
                    dists = []
                    for _, row in result_df.iterrows():
                        row_vals = np.array([row['Age'], row['Blood Pressure'],
                                             row['Cholesterol'], row['BMI'], row['Glucose']])
                        dists.append(np.linalg.norm(user_simple - row_vals))
                    result_df = result_df.copy()
                    result_df['__dist__'] = dists
                    nearest = result_df.nsmallest(1,'__dist__').iloc[0]
                    user_cluster = nearest['Cluster']

                    # Show which group
                    if user_cluster == '-1':
                        gc = '#F59E0B'
                        glabel = '⚠️ Unique Profile (Outlier)'
                        gdesc = 'Your health profile is unusual — you don\'t fit neatly into any cluster. This may indicate a unique or complex health condition worth discussing with a doctor.'
                    else:
                        gnum = int(user_cluster) + 1
                        info = insights.get(user_cluster, {})
                        hr_pct = info.get('high_risk_pct', 50)
                        gc = '#C0152B' if hr_pct >= 60 else '#22C55E' if hr_pct <= 30 else '#F59E0B'
                        glabel = f'Group {gnum} — {info.get("label","").split("—",1)[-1].strip()}'
                        gdesc = info.get('note','Similar patients share your clinical pattern.')

                    st.markdown(
                        f'<div style="background:linear-gradient(135deg,{gc}18,{gc}06);'
                        f'border:2px solid {gc};border-radius:18px;padding:1.8rem;text-align:center;margin-bottom:1rem;">'
                        f'<div style="font-size:3rem;margin-bottom:0.4rem;">👥</div>'
                        f'<div style="font-family:Syne,sans-serif;font-size:1.4rem;font-weight:800;color:{gc};">{glabel}</div>'
                        f'<div style="font-family:Space Grotesk,sans-serif;font-size:0.83rem;color:#8892A4;'
                        f'margin-top:0.7rem;max-width:320px;margin-left:auto;margin-right:auto;line-height:1.6;">{gdesc}</div>'
                        f'</div>',
                        unsafe_allow_html=True)

                    # Show all groups
                    sec("📋 All Patient Groups Overview")
                    cards([(str(n_clust),"Groups Found"),(str(n_noise),"Unique Profiles"),
                           (f"{sil:.3f}" if sil else "N/A","Group Quality")])
                    st.markdown('<br>', unsafe_allow_html=True)

                    for cid, info in insights.items():
                        hr   = info['high_risk_pct']
                        bc   = '#EF4444' if cid=='-1' else '#C0152B' if hr>=60 else '#22C55E' if hr<=30 else '#F59E0B'
                        is_me = (cid == user_cluster)
                        border_extra = f'box-shadow:0 0 0 2px {bc};' if is_me else ''
                        me_tag = ' <span style="background:#C0152B;color:white;font-size:0.62rem;padding:0.1rem 0.4rem;border-radius:4px;font-family:DM Mono,monospace;">YOU</span>' if is_me else ''
                        st.markdown(
                            f'<div style="background:rgba(22,22,44,0.88);border-left:4px solid {bc};'
                            f'border-radius:0 14px 14px 0;padding:0.9rem 1.2rem;margin:0.4rem 0;{border_extra}">'
                            f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                            f'<div style="font-family:Syne,sans-serif;font-size:0.9rem;font-weight:700;color:#F0F0FA;">'
                            f'{info["label"]}{me_tag}</div>'
                            f'<span style="font-family:DM Mono,monospace;font-size:0.7rem;color:{bc};'
                            f'background:{bc}18;padding:0.1rem 0.5rem;border-radius:4px;">{hr:.0f}% high risk</span></div>'
                            f'<div style="margin-top:0.35rem;font-family:Space Grotesk,sans-serif;font-size:0.77rem;color:#5A5A7A;">'
                            f'n={info["n"]:,} patients | Avg Age:{info["avg_age"]:.0f} | '
                            f'BP:{info["avg_bp"]:.0f} | Glucose:{info["avg_glucose"]:.0f} | '
                            f'BMI:{info["avg_bmi"]:.1f}</div>'
                            f'<div style="margin-top:0.3rem;font-family:Space Grotesk,sans-serif;font-size:0.76rem;color:#4A4A68;">'
                            f'{info["note"]}</div></div>',
                            unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Grouping error: {e}")
                    import traceback; st.code(traceback.format_exc())
        else:
            st.markdown(
                '<div style="text-align:center;padding:6rem 2rem;background:rgba(20,20,40,0.5);'
                'border-radius:18px;border:1px dashed rgba(192,21,43,0.25);">'
                '<div style="font-size:4.5rem;margin-bottom:1rem;">👥</div>'
                '<div style="font-family:Syne,sans-serif;font-size:1.1rem;color:#3A3A5A;">Enter your profile and click</div>'
                '<div style="font-family:DM Mono,monospace;font-size:0.85rem;color:#C0152B;margin-top:0.4rem;">'
                '→ Find My Patient Group</div></div>',
                unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 💡 HEALTH PATTERNS
# ══════════════════════════════════════════════════════════════════════════════
elif "Health Patterns" in page:
    hero("💡 Health Pattern Discovery",
         "Discover which combinations of risk factors most strongly predict serious conditions. "
         "Powered by FP-Growth frequent pattern mining.")
    pill("FP-Growth — Frequent Pattern Mining")

    c1,c2 = st.columns([1,2])
    with c1:
        sec("🎛 Pattern Settings")
        min_sup  = st.slider("Minimum Frequency",   0.05, 0.5,  0.20, 0.01,
                             help="How often this pattern must appear in patient data")
        min_conf = st.slider("Minimum Confidence",  0.30, 0.95, 0.55, 0.01,
                             help="How reliable the rule must be (0 = unreliable, 1 = always true)")
        min_lift = st.slider("Minimum Strength",    1.0,  5.0,  1.2,  0.1,
                             help="How much stronger than random chance (>1 = meaningful)")
        max_show = st.slider("Rules to Display",    3,    30,   12)
        mine_btn = st.button("🌿 Discover Health Patterns", use_container_width=True)

        st.markdown('<br>', unsafe_allow_html=True)
        sec("📖 Reading a Rule")
        for term,color,desc in [
            ("FREQUENCY","#F59E0B","How common this pattern is in all patients"),
            ("CONFIDENCE","#A5B4FC","If A is present, how often B also appears"),
            ("STRENGTH","#86EFAC","How much stronger than pure coincidence"),
        ]:
            st.markdown(
                f'<div style="padding:0.5rem 0.7rem;margin:0.3rem 0;background:rgba(22,22,44,0.7);'
                f'border-radius:8px;border-left:2px solid {color};">'
                f'<span style="font-family:DM Mono,monospace;font-size:0.72rem;color:{color};font-weight:600;">{term}</span>'
                f'<div style="font-family:Space Grotesk,sans-serif;font-size:0.75rem;color:#5A5A78;margin-top:0.15rem;">{desc}</div>'
                f'</div>',
                unsafe_allow_html=True)

        # User profile for pattern matching
        st.markdown('<br>', unsafe_allow_html=True)
        sec("🔍 Match Patterns to My Profile")
        p_bp      = st.checkbox("I have High Blood Pressure (≥140)")
        p_gluc    = st.checkbox("I have High Glucose (≥140 mg/dL)")
        p_bmi     = st.checkbox("I have High BMI (≥30)")
        p_smk     = st.checkbox("I am a Smoker")
        p_fam     = st.checkbox("I have Family History")
        p_chol    = st.checkbox("I have High Cholesterol (≥200)")
        p_age     = st.checkbox("I am Senior (Age ≥ 60)")

    with c2:
        if mine_btn:
            with st.spinner("Mining health patterns..."):
                try:
                    from modules.patterns import run_fpgrowth
                    _, rules = run_fpgrowth(min_sup, min_conf, min_lift)

                    if rules.empty:
                        st.warning("No patterns found with these settings. Try lowering Frequency or Confidence.")
                    else:
                        cards([(str(len(rules)),"Patterns Found"),
                               (f"{rules['Confidence'].max():.2f}","Strongest Confidence"),
                               (f"{rules['Lift'].max():.2f}","Highest Strength")])

                        # Filter rules relevant to user's profile
                        user_flags = []
                        if p_bp:   user_flags.append("High_BP")
                        if p_gluc: user_flags.append("High_Glucose")
                        if p_bmi:  user_flags.append("High_BMI")
                        if p_smk:  user_flags.append("Smoker")
                        if p_fam:  user_flags.append("Family_Hx")
                        if p_chol: user_flags.append("High_Cholesterol")
                        if p_age:  user_flags.append("Senior")

                        if user_flags:
                            matched = rules[rules['Antecedents (IF)'].apply(
                                lambda x: any(f in x for f in user_flags)
                            )]
                            if not matched.empty:
                                sec("⚠️ Patterns That Match YOUR Profile","Personalized")
                                for _,row in matched.head(5).iterrows():
                                    ant=row['Antecedents (IF)']; con=row['Consequents (THEN)']
                                    conf=row['Confidence']; lift=row['Lift']; sup=row['Support']
                                    st.markdown(
                                        f'<div style="background:rgba(192,21,43,0.12);border-left:3px solid #C0152B;'
                                        f'border:1px solid rgba(192,21,43,0.3);border-radius:12px;'
                                        f'padding:1rem 1.2rem;margin:0.4rem 0;">'
                                        f'<div style="font-family:DM Mono,monospace;font-size:0.83rem;color:#E8E8F0;line-height:1.6;">'
                                        f'<span style="color:#8892A4;">IF </span><strong style="color:#FFAAAA;">{ant}</strong>'
                                        f'<span style="color:#C0152B;margin:0 0.4rem;">→</span>'
                                        f'<span style="color:#8892A4;">THEN </span><strong style="color:#FF6060;">{con}</strong></div>'
                                        f'<div style="margin-top:0.4rem;display:flex;gap:0.6rem;flex-wrap:wrap;">'
                                        f'<span style="background:rgba(245,158,11,0.18);color:#F59E0B;border:1px solid rgba(245,158,11,0.28);'
                                        f'font-family:DM Mono,monospace;font-size:0.68rem;padding:0.1rem 0.45rem;border-radius:4px;">'
                                        f'FREQ {sup:.3f}</span>'
                                        f'<span style="background:rgba(99,102,241,0.18);color:#A5B4FC;border:1px solid rgba(99,102,241,0.28);'
                                        f'font-family:DM Mono,monospace;font-size:0.68rem;padding:0.1rem 0.45rem;border-radius:4px;">'
                                        f'CONF {conf:.3f}</span>'
                                        f'<span style="background:rgba(34,197,94,0.18);color:#86EFAC;border:1px solid rgba(34,197,94,0.28);'
                                        f'font-family:DM Mono,monospace;font-size:0.68rem;padding:0.1rem 0.45rem;border-radius:4px;">'
                                        f'STRENGTH {lift:.2f}x</span></div></div>',
                                        unsafe_allow_html=True)

                        sec("🏆 Top Health Patterns","FP-Growth")
                        for _,row in rules.head(max_show).iterrows():
                            ant=row['Antecedents (IF)']; con=row['Consequents (THEN)']
                            sup=row['Support']; conf=row['Confidence']; lift=row['Lift']
                            lift_color = '#EF4444' if lift>=2.5 else '#F59E0B' if lift>=1.5 else '#86EFAC'
                            st.markdown(
                                f'<div style="background:rgba(22,22,44,0.9);border-left:3px solid #C0152B;'
                                f'border-radius:0 12px 12px 0;padding:0.85rem 1.1rem;margin:0.35rem 0;">'
                                f'<div style="font-family:DM Mono,monospace;font-size:0.82rem;color:#E8E8F0;line-height:1.6;">'
                                f'<span style="color:#5A5A78;">IF </span><strong style="color:#D0D0E8;">{ant}</strong>'
                                f'<span style="color:#C0152B;margin:0 0.4rem;">→</span>'
                                f'<span style="color:#5A5A78;">THEN </span><strong style="color:#E8304A;">{con}</strong></div>'
                                f'<div style="margin-top:0.35rem;display:flex;gap:0.55rem;flex-wrap:wrap;">'
                                f'<span style="background:rgba(245,158,11,0.15);color:#F59E0B;'
                                f'font-family:DM Mono,monospace;font-size:0.67rem;padding:0.1rem 0.45rem;border-radius:4px;">'
                                f'FREQ {sup:.3f}</span>'
                                f'<span style="background:rgba(99,102,241,0.15);color:#A5B4FC;'
                                f'font-family:DM Mono,monospace;font-size:0.67rem;padding:0.1rem 0.45rem;border-radius:4px;">'
                                f'CONF {conf:.3f}</span>'
                                f'<span style="background:rgba(34,197,94,0.15);color:{lift_color};'
                                f'font-family:DM Mono,monospace;font-size:0.67rem;padding:0.1rem 0.45rem;border-radius:4px;">'
                                f'STRENGTH {lift:.2f}x</span></div></div>',
                                unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Pattern mining error: {e}")
                    import traceback; st.code(traceback.format_exc())
        else:
            st.markdown(
                '<div style="text-align:center;padding:6rem 2rem;background:rgba(20,20,40,0.5);'
                'border-radius:18px;border:1px dashed rgba(192,21,43,0.25);">'
                '<div style="font-size:4.5rem;margin-bottom:1rem;">🌿</div>'
                '<div style="font-family:Syne,sans-serif;font-size:1.1rem;color:#3A3A5A;">Set settings and click</div>'
                '<div style="font-family:DM Mono,monospace;font-size:0.85rem;color:#C0152B;margin-top:0.4rem;">'
                '→ Discover Health Patterns</div></div>',
                unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 🌡 HEALTH CHECK
# ══════════════════════════════════════════════════════════════════════════════
elif "Health Check" in page:
    hero("🌡 Quick Health Check",
         "Enter any single health metric for an instant clinical context, normal range, "
         "and personalised advice — no full profile needed.")

    metric_choice = st.selectbox(
        "Select a health metric to check:",
        ["🩸 Blood Glucose","💉 Blood Pressure","⚖️ BMI","🧪 Cholesterol",
         "🫀 Heart Rate","😴 Sleep Hours","🏃 Physical Activity","😤 Stress Level"],
        label_visibility="visible"
    )
    st.markdown('<br>', unsafe_allow_html=True)

    METRIC_CONFIG = {
        "🩸 Blood Glucose": {
            "unit":"mg/dL","min":50,"max":400,"default":95,"step":1,
            "ranges":[(0,99,"#22C55E","Normal","Fasting glucose under 100 mg/dL is healthy."),
                      (100,125,"#F59E0B","Pre-diabetic","Fasting glucose 100–125 mg/dL. Diet and exercise can reverse this."),
                      (126,400,"#C0152B","Diabetic Range","≥ 126 mg/dL suggests diabetes. Consult your doctor immediately.")],
            "tips":["Avoid sugary drinks and processed carbs","Exercise for 30 min daily","Get HbA1c tested every 3–6 months"],
        },
        "💉 Blood Pressure": {
            "unit":"mmHg","min":60,"max":220,"default":120,"step":1,
            "ranges":[(0,119,"#22C55E","Normal","BP under 120 mmHg is ideal."),
                      (120,139,"#F59E0B","Elevated","Monitor closely and reduce sodium intake."),
                      (140,220,"#C0152B","Hypertension","BP ≥ 140 mmHg requires medical attention.")],
            "tips":["Reduce salt to < 2,300mg/day","Exercise 30 min daily","Manage stress with meditation"],
        },
        "⚖️ BMI": {
            "unit":"kg/m²","min":10.0,"max":55.0,"default":24.0,"step":0.1,
            "ranges":[(0,18.4,"#F59E0B","Underweight","BMI < 18.5 may indicate malnutrition."),
                      (18.5,24.9,"#22C55E","Normal Weight","Healthy BMI range — maintain your lifestyle."),
                      (25,29.9,"#F59E0B","Overweight","BMI 25–29.9 increases cardiovascular risk."),
                      (30,55,"#C0152B","Obese","BMI ≥ 30 significantly raises disease risk.")],
            "tips":["Aim for 150 min/week moderate exercise","Consult a nutritionist","Track calorie intake"],
        },
        "🧪 Cholesterol": {
            "unit":"mg/dL","min":100,"max":350,"default":180,"step":1,
            "ranges":[(0,169,"#22C55E","Desirable","Total cholesterol < 170 is optimal."),
                      (170,199,"#F59E0B","Borderline","Monitor diet — reduce saturated fats."),
                      (200,350,"#C0152B","High","≥ 200 mg/dL increases heart attack risk.")],
            "tips":["Eat more fibre (oats, beans, fruit)","Reduce red meat and full-fat dairy","Exercise raises good HDL cholesterol"],
        },
        "🫀 Heart Rate": {
            "unit":"bpm","min":30,"max":200,"default":72,"step":1,
            "ranges":[(0,59,"#F59E0B","Low (Bradycardia)","Resting HR < 60 can be normal in athletes, but seek advice if symptomatic."),
                      (60,100,"#22C55E","Normal","Resting heart rate 60–100 bpm is healthy."),
                      (101,200,"#C0152B","High (Tachycardia)","HR > 100 at rest may signal stress, thyroid issues or arrhythmia.")],
            "tips":["Practice deep breathing exercises","Limit caffeine intake","Regular aerobic exercise lowers resting HR"],
        },
        "😴 Sleep Hours": {
            "unit":"hrs/night","min":2.0,"max":12.0,"default":7.0,"step":0.5,
            "ranges":[(0,5.9,"#C0152B","Insufficient","< 6 hrs increases heart disease, diabetes and obesity risk."),
                      (6,9,"#22C55E","Optimal","7–9 hrs is the recommended range for adults."),
                      (9.1,12,"#F59E0B","Excessive","Sleeping > 9 hrs regularly may indicate underlying health issues.")],
            "tips":["Maintain a consistent sleep schedule","Avoid screens 1 hour before bed","Keep bedroom cool and dark"],
        },
        "🏃 Physical Activity": {
            "unit":"hrs/week","min":0.0,"max":20.0,"default":3.0,"step":0.5,
            "ranges":[(0,1.9,"#C0152B","Sedentary","< 2 hrs/week significantly raises cardiovascular risk."),
                      (2,4.9,"#F59E0B","Moderate","Getting better! Aim for 2.5+ hrs of moderate activity."),
                      (5,20,"#22C55E","Active","5+ hrs/week is excellent for heart health.")],
            "tips":["Start with a 20-minute daily walk","Mix cardio with strength training","Take the stairs instead of the elevator"],
        },
        "😤 Stress Level": {
            "unit":"/10","min":1,"max":10,"default":4,"step":1,
            "ranges":[(0,3,"#22C55E","Low Stress","Good! Chronic stress is a major cardiovascular risk factor."),
                      (4,6,"#F59E0B","Moderate Stress","Manageable — incorporate regular relaxation techniques."),
                      (7,10,"#C0152B","High Stress","Chronic high stress raises BP, cortisol and heart disease risk.")],
            "tips":["Practice 10 min daily meditation","Exercise is the best stress reliever","Talk to someone — social support matters"],
        },
    }

    cfg = METRIC_CONFIG.get(metric_choice)
    if cfg:
        m_col, r_col = st.columns([1, 1.3])
        with m_col:
            sec(f"Enter Your {metric_choice}")
            st.markdown(
                '<div style="background:rgba(22,22,44,0.95);border:1px solid rgba(192,21,43,0.22);'
                'border-radius:18px;padding:1.6rem;">',
                unsafe_allow_html=True)
            if isinstance(cfg['step'], float):
                val = st.slider(f"val_{metric_choice}", float(cfg['min']), float(cfg['max']),
                                float(cfg['default']), cfg['step'], label_visibility="collapsed")
            else:
                val = st.slider(f"val_{metric_choice}", int(cfg['min']), int(cfg['max']),
                                int(cfg['default']), int(cfg['step']), label_visibility="collapsed")

            st.markdown(
                f'<div style="text-align:center;padding:1rem;margin:0.5rem 0;'
                f'background:rgba(192,21,43,0.1);border-radius:12px;border:1px solid rgba(192,21,43,0.2);">'
                f'<div style="font-family:Syne,sans-serif;font-size:2.5rem;font-weight:800;color:#C0152B;">'
                f'{val}</div>'
                f'<div style="font-family:DM Mono,monospace;font-size:0.82rem;color:#8892A4;">{cfg["unit"]}</div>'
                f'</div>',
                unsafe_allow_html=True)

            # Normal ranges reference
            sec("📏 Reference Ranges")
            for lo, hi, color, label, _ in cfg['ranges']:
                is_me = lo <= val <= hi
                border = f'border:1px solid {color};' if is_me else 'border:1px solid rgba(255,255,255,0.05);'
                me_tag2 = f' ← <span style="color:{color};font-weight:700;">You</span>' if is_me else ''
                st.markdown(
                    f'<div style="display:flex;align-items:center;justify-content:space-between;'
                    f'padding:0.45rem 0.8rem;margin:0.2rem 0;background:rgba(22,22,44,0.7);'
                    f'border-radius:8px;{border}">'
                    f'<span style="font-family:Space Grotesk,sans-serif;font-size:0.78rem;color:#C8C8D8;">{label}</span>'
                    f'<span style="font-family:DM Mono,monospace;font-size:0.72rem;color:{color};">'
                    f'{lo}–{hi} {cfg["unit"]}{me_tag2}</span></div>',
                    unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with r_col:
            sec("🩺 Your Result")
            # Determine status
            status_color, status_label, status_desc = '#22C55E','Normal',''
            for lo,hi,color,label,desc in cfg['ranges']:
                if lo <= val <= hi:
                    status_color, status_label, status_desc = color, label, desc
                    break

            # Result card
            st.markdown(
                f'<div style="background:linear-gradient(135deg,{status_color}18,{status_color}06);'
                f'border:2px solid {status_color};border-radius:18px;padding:1.8rem;'
                f'text-align:center;margin-bottom:1rem;">'
                f'<div style="font-family:Syne,sans-serif;font-size:1.6rem;font-weight:800;'
                f'color:{status_color};margin-bottom:0.3rem;">{status_label}</div>'
                f'<div style="font-family:DM Mono,monospace;font-size:2.4rem;font-weight:800;'
                f'color:{status_color}CC;">{val} <span style="font-size:1rem;">{cfg["unit"]}</span></div>'
                f'<div style="font-family:Space Grotesk,sans-serif;font-size:0.83rem;color:#8892A4;'
                f'margin-top:0.7rem;max-width:300px;margin-left:auto;margin-right:auto;line-height:1.6;">'
                f'{status_desc}</div></div>',
                unsafe_allow_html=True)

            # Gauge bar
            max_val = cfg['max']
            pct = min((val - cfg['min']) / (max_val - cfg['min']) * 100, 100)
            sec("📊 Where You Stand")
            st.markdown(
                f'<div style="margin:0.5rem 0;">'
                f'<div style="position:relative;height:18px;background:linear-gradient(90deg,'
                f'#22C55E 0%,#F59E0B 50%,#C0152B 100%);border-radius:9px;overflow:hidden;">'
                f'<div style="position:absolute;left:{pct}%;top:50%;transform:translate(-50%,-50%);'
                f'width:18px;height:18px;background:white;border-radius:50%;'
                f'box-shadow:0 0 6px rgba(0,0,0,0.5);"></div></div>'
                f'<div style="display:flex;justify-content:space-between;margin-top:0.3rem;">'
                f'<span style="font-family:DM Mono,monospace;font-size:0.68rem;color:#22C55E;">Low</span>'
                f'<span style="font-family:DM Mono,monospace;font-size:0.68rem;color:#F59E0B;">Moderate</span>'
                f'<span style="font-family:DM Mono,monospace;font-size:0.68rem;color:#C0152B;">High</span></div></div>',
                unsafe_allow_html=True)

            # Tips
            sec("💊 Health Tips")
            for tip in cfg['tips']:
                st.markdown(
                    f'<div style="display:flex;gap:0.7rem;align-items:flex-start;padding:0.55rem 0.8rem;'
                    f'margin:0.28rem 0;background:rgba(22,22,44,0.65);border-radius:10px;'
                    f'border:1px solid rgba(255,255,255,0.04);">'
                    f'<span style="color:#C0152B;font-size:1rem;margin-top:0.05rem;">💡</span>'
                    f'<span style="font-family:Space Grotesk,sans-serif;font-size:0.8rem;'
                    f'color:#A8A8C0;line-height:1.6;">{tip}</span></div>',
                    unsafe_allow_html=True)

            # Overall tip
            if status_color == '#C0152B':
                st.markdown(
                    '<div style="margin-top:1rem;background:rgba(192,21,43,0.12);border:1px solid rgba(192,21,43,0.3);'
                    'border-radius:12px;padding:0.9rem;text-align:center;">'
                    '<div style="font-family:Syne,sans-serif;font-size:0.88rem;font-weight:700;color:#FF6060;">⚠️ Action Required</div>'
                    '<div style="font-family:Space Grotesk,sans-serif;font-size:0.78rem;color:#8892A4;margin-top:0.3rem;">'
                    'This reading is in the high-risk range. Please consult a healthcare professional.</div></div>',
                    unsafe_allow_html=True)
