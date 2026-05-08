import pandas as pd
import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

from src.preprocessing.feature_engineering import generate_embedding

df = pd.read_csv("data/raw/complaints.csv")

X = []

for text in df["complaint_text"]:
    emb = generate_embedding(text)
    X.append(emb)

y = df["eta_days"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestRegressor()

model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("MAE:", mean_absolute_error(y_test, predictions))

joblib.dump(model, "models/eta_model.pkl")