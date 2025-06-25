# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# from search_engine import search_similar_images
# import os
#
# app = Flask(__name__)
# CORS(app)
#
# UPLOAD_FOLDER = "query"
# DATASET_FOLDER = "dataset"
#
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(DATASET_FOLDER, exist_ok=True)
#
# @app.route("/")
# def home():
#     return "✅ Image Search Engine API Running"
#
# @app.route("/dataset/<filename>")
# def dataset_file(filename):
#     return send_from_directory(DATASET_FOLDER, filename)
#
# # Dataset Upload API
# @app.route("/upload-dataset", methods=["POST"])
# def upload_dataset():
#     if "images" not in request.files:
#         return jsonify({"error": "No images uploaded"}), 400
#
#     files = request.files.getlist("images")
#     saved_files = []
#
#     for file in files:
#         if file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
#             save_path = os.path.join(DATASET_FOLDER, file.filename)
#             file.save(save_path)
#             saved_files.append(file.filename)
#
#     return jsonify({"message": f"{len(saved_files)} image(s) uploaded", "files": saved_files})
#
# # Search API
# @app.route("/search", methods=["POST"])
# def search():
#     if "image" not in request.files:
#         return jsonify({"error": "No image uploaded"}), 400
#
#     image_file = request.files["image"]
#     if image_file.filename == "":
#         return jsonify({"error": "Invalid file name"}), 400
#
#     query_path = os.path.join(UPLOAD_FOLDER, "query.jpg")
#     image_file.save(query_path)
#
#     threshold = float(request.form.get("threshold", 0.65))
#     results = search_similar_images(query_path, DATASET_FOLDER, threshold=threshold)
#
#     # results = search_similar_images(query_path, threshold=threshold)
#
#     return jsonify([
#         {"image": file, "score": round(float(score), 2)}
#         for file, score in results
#     ])
#
# if __name__ == "__main__":
#     app.run(debug=True)

                      #-------- FAISS  --------

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from search_engine import search_similar_images
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "query"
DATASET_FOLDER = "dataset"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATASET_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "✅ FAISS Image Search Engine API Running"

@app.route("/dataset/<filename>")
def dataset_file(filename):
    return send_from_directory(DATASET_FOLDER, filename)

# Upload dataset images
@app.route("/upload-dataset", methods=["POST"])
def upload_dataset():
    if "images" not in request.files:
        return jsonify({"error": "No images uploaded"}), 400

    files = request.files.getlist("images")
    saved_files = []

    for file in files:
        if file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            save_path = os.path.join(DATASET_FOLDER, file.filename)
            file.save(save_path)
            saved_files.append(file.filename)

    return jsonify({"message": f"{len(saved_files)} image(s) uploaded", "files": saved_files})

# Search similar images using FAISS
@app.route("/search", methods=["POST"])
def search():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image_file = request.files["image"]
    if image_file.filename == "":
        return jsonify({"error": "Invalid file name"}), 400

    query_path = os.path.join(UPLOAD_FOLDER, "query.jpg")
    image_file.save(query_path)

    # Get top_k value if sent, else default to 5
    top_k = int(request.form.get("top_k", 15))
    results = search_similar_images(query_path, top_k=top_k)

    return jsonify([
        {"image": file, "distance": round(float(dist), 2)}
        for file, dist in results
    ])

if __name__ == "__main__":
    app.run(debug=True)
