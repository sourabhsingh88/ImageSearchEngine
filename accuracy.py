import json
from search_engine import search_similar_images

# Load ground truth
with open("ground_truth.json") as f:
    ground_truth = json.load(f)

correct = 0
total = len(ground_truth)

for query_image, expected_similars in ground_truth.items():
    query_path = f"query/{query_image}"
    results = search_similar_images(query_path)

    retrieved = [r[0] for r in results]

    print(f"\nQuery: {query_image}")
    print(f"Expected: {expected_similars}")
    print(f"Retrieved: {retrieved}")

    match = any(img in retrieved for img in expected_similars)
    if match:
        correct += 1

accuracy = (correct / total) * 100
print(f"\n✅ Accuracy = {accuracy:.2f}% ({correct}/{total})")
