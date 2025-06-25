
# import os
# import pickle
# from sklearn.metrics.pairwise import cosine_similarity
# from model_utils import extract_features
#
# def search_similar_images(query_path, dataset_dir="dataset", threshold=0.65):
#     # Load dataset features
#     with open("features.pkl", "rb") as f:
#         features_list = pickle.load(f)
#
#     query_features = extract_features(query_path)
#     results = []
#
#     for entry in features_list:
#         file_name = entry['filename']
#         feat = entry['features']
#         sim = cosine_similarity([query_features], [feat])[0][0]
#
#         if sim >= threshold:
#             results.append((file_name, sim))
#
#     results.sort(key=lambda x: x[1], reverse=True)
#     return results[:15]






                       #  ---------- F AISS ------------

import faiss
import numpy as np
import pickle
from model_utils import extract_features

# Load FAISS index & filenames
index = faiss.read_index("faiss_index.index")
with open("filenames.pkl", "rb") as f:
    filenames = pickle.load(f)

def search_similar_images(query_path, top_k=15):
    query_vec = extract_features(query_path).astype("float32").reshape(1, -1)
    distances, indices = index.search(query_vec, top_k)

    results = []
    for idx, dist in zip(indices[0], distances[0]):
        results.append((filenames[idx], round(float(dist), 2)))

    return results




































