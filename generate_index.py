import os
import numpy as np
import faiss
import pickle
from model_utils import extract_features

dataset_dir = "dataset"
features = []
filenames = []

for file in os.listdir(dataset_dir):
    path = os.path.join(dataset_dir, file)
    feat = extract_features(path)
    features.append(feat)
    filenames.append(file)

features_np = np.array(features).astype("float32")

# FAISS index
index = faiss.IndexFlatL2(features_np.shape[1])
index.add(features_np)

faiss.write_index(index, "faiss_index.index")

with open("filenames.pkl", "wb") as f:
    pickle.dump(filenames, f)

print("[INFO] FAISS index and filenames saved.")

