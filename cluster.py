import numpy as np, pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from modules.preprocess import load_data, FEATURE_COLS

def run_dbscan(eps=2.0, min_samples=5):
    df   = load_data()
    df_e = df.copy()
    df_e['Gender'] = (df_e['Gender']=='Male').astype(int)
    X    = df_e[FEATURE_COLS].dropna()
    cond = df.loc[X.index,'Medical Condition'].values
    risk = (df.loc[X.index,'Medical Condition']!='Healthy').astype(int).values

    scaler   = StandardScaler()
    Xs       = scaler.fit_transform(X)
    db       = DBSCAN(eps=eps, min_samples=min_samples)
    labels   = db.fit_predict(Xs)
    pca      = PCA(n_components=3)
    Xp       = pca.fit_transform(Xs)
    explained= pca.explained_variance_ratio_

    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise    = list(labels).count(-1)
    sil = None
    if n_clusters > 1:
        mask = labels != -1
        if mask.sum() > 10:
            try: sil = silhouette_score(Xs[mask], labels[mask])
            except: pass

    res = pd.DataFrame({
        'PC1': Xp[:,0], 'PC2': Xp[:,1], 'PC3': Xp[:,2],
        'Cluster': labels.astype(str), 'Condition': cond, 'Risk': risk,
        'Age': X['Age'].values, 'BMI': X['BMI'].values,
        'Glucose': X['Glucose'].values,
        'Blood Pressure': X['Blood Pressure'].values,
        'Cholesterol': X['Cholesterol'].values,
        'Smoking': X['Smoking'].values,
    })

    insights = {}
    for c in sorted(res['Cluster'].unique(), key=lambda x: (x=='-1', x)):
        sub = res[res['Cluster']==c]
        hr  = sub['Risk'].mean()*100
        top_cond = sub['Condition'].value_counts().index[0]
        avg_age  = sub['Age'].mean()
        avg_bp   = sub['Blood Pressure'].mean()
        avg_gluc = sub['Glucose'].mean()
        avg_bmi  = sub['BMI'].mean()
        if c == '-1':
            tag  = '⚠️ Outliers / Anomalies'
            note = 'Extreme/unusual health profiles. May need special clinical attention.'
        elif hr >= 60:
            tag  = '🔴 High Risk Group'
            note = f'Older patients (avg {avg_age:.0f} yrs) with elevated BP ({avg_bp:.0f}) and glucose ({avg_gluc:.0f}). High disease burden.'
        elif hr <= 30:
            tag  = '🟢 Low Risk Group'
            note = f'Younger patients (avg {avg_age:.0f} yrs) with moderate vitals. Lower disease prevalence.'
        else:
            tag  = '🟡 Mixed Risk Group'
            note = f'Mixed profile (avg age {avg_age:.0f}, BMI {avg_bmi:.1f}). Monitor for emerging risk factors.'
        insights[c] = {'label': tag, 'n': len(sub), 'high_risk_pct': hr,
                       'avg_age': avg_age, 'avg_bp': avg_bp,
                       'avg_glucose': avg_gluc, 'avg_bmi': avg_bmi,
                       'top_condition': top_cond, 'note': note}
    return res, n_clusters, n_noise, sil, explained, insights
