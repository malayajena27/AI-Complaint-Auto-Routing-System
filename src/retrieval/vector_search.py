import faiss
import numpy as np
import pandas as pd

from src.preprocessing.feature_engineering import generate_embedding

df = pd.read_csv("data/raw/complaints.csv")

embeddings = []

for text in df["complaint_text"]:
    emb = generate_embedding(text)
    embeddings.append(emb)

embeddings = np.array(embeddings).astype("float32")

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

faiss.write_index(index, "models/faiss_index.bin")

print("FAISS index saved")