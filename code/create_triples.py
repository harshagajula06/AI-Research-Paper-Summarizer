import json

# Load entity-extracted JSON
input_path = "../output/json/AI_Health_06_entities.json"
output_path = "../output/json/AI_Health_06_triples.json"

with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

entities = data.get("entities", {})
triples = []

# ---- CREATE RELATIONSHIPS ----

# Algorithm → Disease
for algo in entities.get("algorithms", []):
    for disease in entities.get("diseases", []):
        triples.append([algo, "used_for", disease])

# Algorithm → Metric
for algo in entities.get("algorithms", []):
    for metric in entities.get("metrics", []):
        triples.append([algo, "evaluated_by", metric])

# Paper → Journal
paper_node = f"paper_{data['paper_id']}"
journal = data.get("journal", "")
if journal:
    triples.append([paper_node, "published_in", journal])

# Add triples to JSON
data["triples"] = triples

# Save triples JSON
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("Triples creation completed successfully")
print("Total triples created:", len(triples))
