"""
train_model.py
Trains a RandomForestClassifier on the heart failure dataset
and saves it as heart_model.pkl for use in the Streamlit app.

Run this once: python train_model.py
"""

import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# 1. LOAD DATA
df = pd.read_csv("heart_failure_clinical_records_dataset.csv")

# 2. FEATURES / TARGET
X = df.drop(["DEATH_EVENT"], axis=1)
y = df["DEATH_EVENT"]

# 3. TRAIN-TEST SPLIT
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 4. TRAIN MODEL
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. EVALUATE
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2%}")
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

# 6. SAVE MODEL (also save the column order — important for the app!)
with open("heart_model.pkl", "wb") as file:
    pickle.dump({"model": model, "columns": list(X.columns)}, file)

print("Model saved successfully as heart_model.pkl")
