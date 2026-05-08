import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

from src.preprocessing.feature_engineering import generate_embedding

df = pd.read_csv("data/raw/complaints.csv")

X = []

for text in df["complaint_text"]:
    emb = generate_embedding(text)
    X.append(emb)

y = df["priority"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestClassifier()

model.fit(X_train, y_train)

predictions = model.predict(X_test)

print(classification_report(y_test, predictions))

joblib.dump(model, "models/priority_model.pkl")