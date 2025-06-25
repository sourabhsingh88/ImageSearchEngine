import os
import pickle
from model_utils import extract_features

dataset_dir = "dataset"
features_data = []

for file in os.listdir(dataset_dir):
    path = os.path.join(dataset_dir, file)
    features = extract_features(path)
    features_data.append({'filename': file, 'features': features})

with open("features.pkl", "wb") as f:
    pickle.dump(features_data, f)

print("[INFO] Features saved to features.pkl")

