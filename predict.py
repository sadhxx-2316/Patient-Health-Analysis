"""
CART Decision Tree — Binary: High Risk / Low Risk
Uses risk score from 9 clinical features with domain thresholds
"""
import numpy as np, pandas as pd, joblib, os
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.utils import resample
from modules.preprocess import load_data, FEATURE_COLS

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'cart_binary.pkl')

def get_risk_score(age, bp, chol, bmi, glucose, smoking, alcohol, fam_hx):
    score = 0
    if glucose >= 140: score += 30
    elif glucose >= 100: score += 15
    if bp >= 140: score += 25
    elif bp >= 120: score += 10
    if bmi >= 30: score += 20
    elif bmi >= 25: score += 8
    if age >= 60: score += 15
    elif age >= 45: score += 8
    if smoking == 1: score += 15
    if fam_hx == 1: score += 10
    if alcohol == 1: score += 5
    if chol >= 240: score += 10
    elif chol >= 200: score += 5
    return min(score, 100)

def train_and_save():
    df    = load_data()
    df_e  = df.copy()
    df_e['Gender'] = (df_e['Gender'] == 'Male').astype(int)
    X = df_e[FEATURE_COLS]
    y = (df['Medical Condition'] != 'Healthy').astype(int).values

    # Balanced 600 vs 600
    X_df = X.copy(); X_df['__y__'] = y
    H  = X_df[X_df['__y__']==0]
    D  = X_df[X_df['__y__']==1]
    Hu = resample(H, n_samples=600, random_state=42, replace=True)
    Dd = resample(D, n_samples=600, random_state=42, replace=False)
    bal = pd.concat([Hu, Dd]).sample(frac=1, random_state=42)
    y_b = bal.pop('__y__').values
    X_b = bal.reset_index(drop=True)

    Xtr, Xte, ytr, yte = train_test_split(X_b, y_b, test_size=0.2,
                                           random_state=42, stratify=y_b)
    best_model, best_acc = None, 0
    for depth in [4, 6, 8, 10, None]:
        cart = DecisionTreeClassifier(criterion='gini', max_depth=depth,
                                      min_samples_leaf=3, random_state=42)
        cart.fit(Xtr, ytr)
        acc = accuracy_score(yte, cart.predict(Xte))
        if acc > best_acc:
            best_acc, best_model = acc, cart

    _, Xorig, _, yorig = train_test_split(X, y, test_size=0.2,
                                           random_state=42, stratify=y)
    y_pred = best_model.predict(Xorig)
    acc    = accuracy_score(yorig, y_pred)
    cm     = confusion_matrix(yorig, y_pred)
    report = classification_report(yorig, y_pred,
                                   target_names=['Low Risk','High Risk'],
                                   output_dict=True)
    fi = dict(zip(FEATURE_COLS, best_model.feature_importances_.tolist()))
    joblib.dump({'model': best_model, 'fi': fi}, MODEL_PATH)
    return best_model, acc, cm, report, Xorig, yorig, y_pred, fi

def load_bundle():
    if os.path.exists(MODEL_PATH): return joblib.load(MODEL_PATH)
    train_and_save(); return joblib.load(MODEL_PATH)

def predict_risk(age, bp, cholesterol, gender, bmi, glucose, smoking, alcohol, family_history):
    bundle = load_bundle()
    model  = bundle['model']
    gender_enc = 1 if gender == 'Male' else 0
    raw   = np.array([[age, bp, cholesterol, gender_enc,
                       bmi, glucose, smoking, alcohol, family_history]])
    score = get_risk_score(age, bp, cholesterol, bmi, glucose, smoking, alcohol, family_history)
    proba_cart = model.predict_proba(raw)[0]
    # Blend CART probability with domain score
    high_risk_prob = 0.5 * proba_cart[1] + 0.5 * (score / 100)
    low_risk_prob  = 1 - high_risk_prob
    label = 'High Risk' if high_risk_prob >= 0.5 else 'Low Risk'
    proba = np.array([low_risk_prob, high_risk_prob])
    return label, proba, int(high_risk_prob >= 0.5)
