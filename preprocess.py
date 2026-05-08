import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'heart.csv')

FEATURE_COLS = ['Age', 'Blood Pressure', 'Cholesterol', 'Gender',
                'BMI', 'Glucose', 'Smoking', 'Alcohol', 'Family History']

CONDITIONS = ['Arthritis','Asthma','Cancer','Diabetes',
              'Healthy','Hypertension','Obesity']

def load_data():
    df = pd.read_csv(DATA_PATH)
    df.rename(columns={'c': 'Age'}, inplace=True)
    return df

def encode_gender(df):
    df = df.copy()
    df['Gender'] = (df['Gender'] == 'Male').astype(int)
    return df

def get_features_target(df):
    df = encode_gender(df)
    X = df[FEATURE_COLS].copy()
    le = LabelEncoder()
    le.fit(CONDITIONS)
    y = le.transform(df['Medical Condition'])
    return X, y, le

def scale_features(X_train, X_test=None):
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    if X_test is not None:
        X_test_scaled = scaler.transform(X_test)
        return X_train_scaled, X_test_scaled, scaler
    return X_train_scaled, scaler
