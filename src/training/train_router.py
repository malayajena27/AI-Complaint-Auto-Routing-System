import json
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity

from src.preprocessing.feature_engineering import generate_embedding

with open("officers.json", "r") as f:
    officers = json.load(f)

officer_embeddings = []

for officer in officers:

    profile = (
        officer["department"] + " " +
        " ".join(officer["skills"])
    )

    emb = generate_embedding(profile)

    officer_embeddings.append(emb)

officer_embeddings = np.array(officer_embeddings)

np.save(
    "models/officer_embeddings.npy",
    officer_embeddings
)

print("Officer embeddings saved")