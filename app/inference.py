import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

import json
import joblib
import faiss
import numpy as np
import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity

from src.preprocessing.feature_engineering import generate_embedding

priority_model = joblib.load(
    "models/priority_model.pkl"
)

eta_model = joblib.load(
    "models/eta_model.pkl"
)

officer_embeddings = np.load(
    "models/officer_embeddings.npy"
)

faiss_index = faiss.read_index(
    "models/faiss_index.bin"
)

with open("officers.json", "r") as f:
    officers = json.load(f)

df = pd.read_csv("data/raw/complaints.csv")

def process_complaint(text):

    emb = generate_embedding(text)

    priority = priority_model.predict([emb])[0]

    eta = eta_model.predict([emb])[0]

    similarity_scores = cosine_similarity(
        [emb],
        officer_embeddings
    )[0]

    best_index = np.argmax(similarity_scores)

    assigned_officer = officers[best_index]

    query = np.array([emb]).astype("float32")

    D, I = faiss_index.search(query, k=3)

    similar_cases = []

    for idx in I[0]:
        similar_cases.append(
            df.iloc[idx]["complaint_text"]
        )

    return {
        "priority": priority,
        "eta_days": round(float(eta), 2),
        "assigned_officer": assigned_officer,
        "similar_cases": similar_cases
    }