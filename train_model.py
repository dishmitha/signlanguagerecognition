import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
import joblib

# =========================
# 1. Load Dataset
# =========================
df = pd.read_csv("sign_data.csv", header=None)

X = df.iloc[:, :-1]
y = df.iloc[:, -1]

print("Dataset Shape:", df.shape)

# =========================
# 2. Encode Labels
# =========================
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# =========================
# 3. Train Test Split
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))

# =========================
# 4. Improved Random Forest
# =========================
model = RandomForestClassifier(
    n_estimators=500,
    max_depth=20,
    min_samples_split=5,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# =========================
# 5. Evaluate
# =========================
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print(f"\nAccuracy: {accuracy*100:.2f}%")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# =========================
# 6. Save
# =========================
joblib.dump(model, "sign_model.pkl")
joblib.dump(label_encoder, "label_encoder.pkl")

print("\nModel + LabelEncoder saved successfully!")