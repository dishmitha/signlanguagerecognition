import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import joblib

df = pd.read_csv("word_data.csv", header=None)

X = df.iloc[:, :-1]
y = df.iloc[:, -1]

label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = RandomForestClassifier(
    n_estimators=300,
    random_state=42
)

model.fit(X_train, y_train)

pred = model.predict(X_test)

print(
    "Accuracy:",
    accuracy_score(y_test, pred) * 100
)

joblib.dump(model, "word_model.pkl")
joblib.dump(
    label_encoder,
    "word_label_encoder.pkl"
)

print("Saved successfully")