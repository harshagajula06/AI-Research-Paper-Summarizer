import json

# Load normalized JSON
input_path = "../output/json/AI_Health_06_normalized.json"
output_path = "../output/json/AI_Health_06_entities.json"

with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

text = data["abstract"] + " " + data["full_text"]

# ---- ENTITY DICTIONARIES (RULE-BASED) ----
diseases_list = [
    "heart disease",
    "diabetes",
    "cancer",
    "cardiovascular disease"
]

algorithms_list = [
    "xgboost",
    "random forest",
    "decision tree",
    "naive bayes",
    "knn",
    "support vector machine",
    "logistic regression"
]

metrics_list = [
    "accuracy",
    "precision",
    "recall",
    "f1-score"
]

datasets_list = [
    "kaggle",
    "uci",
    "heart disease dataset"
]

# ---- EXTRACTION FUNCTION ----
def extract_entities(entity_list, text):
    found = set()
    for item in entity_list:
        if item in text:
            found.add(item)
    return list(found)

entities = {
    "diseases": extract_entities(diseases_list, text),
    "algorithms": extract_entities(algorithms_list, text),
    "metrics": extract_entities(metrics_list, text),
    "datasets": extract_entities(datasets_list, text)
}

# Add entities to JSON
data["entities"] = entities

# Save entity JSON
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("Entity extraction completed successfully")
print("Entities extracted:", entities)
