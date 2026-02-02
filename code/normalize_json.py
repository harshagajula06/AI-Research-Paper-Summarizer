import json
import re

# Input & output paths
input_path = "../output/json/AI_Health_06.json"
output_path = "../output/json/AI_Health_06_normalized.json"

# Load JSON
with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# ---- NORMALIZATION ----

# 1. Normalize year
try:
    data["year"] = int(data["year"])
except:
    data["year"] = None

# 2. Normalize journal name
data["journal"] = data["journal"].strip().lower()

# 3. Normalize keywords
if isinstance(data["keywords"], str):
    data["keywords"] = [k.strip().lower() for k in data["keywords"].split(",")]

# 4. Normalize text (remove extra spaces)
def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()

data["abstract"] = clean_text(data["abstract"])
data["full_text"] = clean_text(data["full_text"])

# Save normalized JSON
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("Normalization completed successfully")
print("Normalized file saved at:", output_path)
