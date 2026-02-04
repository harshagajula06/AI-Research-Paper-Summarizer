import os

print("CWD:", os.getcwd())
print("Excel exists:", os.path.exists("../data/excel/AI_Healthcare_Metadata.xlsx"))
print("PDF dir exists:", os.path.exists("../data/pdf/"))
print("Output dir exists:", os.path.exists("../output/json/"))


import pandas as pd
import json
import re
from PyPDF2 import PdfReader

# ---------- CONFIG ----------
EXCEL_PATH = "../data/excel/AI_Healthcare_Metadata.xlsx"
PDF_DIR = "../data/pdf/"
OUTPUT_DIR = "../output/json/"

DISEASES = ["heart disease", "diabetes", "cancer"]
ALGORITHMS = ["xgboost", "random forest", "decision tree", "knn", "naive bayes"]
METRICS = ["accuracy", "precision", "recall", "f1-score"]
DATASETS = ["kaggle", "uci"]

def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.lower().strip()

def extract_entities(items, text):
    return [item for item in items if item in text]

# ---------- LOAD METADATA ----------
df = pd.read_excel(EXCEL_PATH)
paper_ids = df["Paper ID"].tolist()

for paper_id in paper_ids:
    print(f"Processing {paper_id}...")

    row = df[df["Paper ID"] == paper_id].iloc[0]

    # ---------- READ PDF ----------
    pdf_path = f"{PDF_DIR}{paper_id}.pdf"
    reader = PdfReader(pdf_path)
    full_text = ""
    for page in reader.pages:
        if page.extract_text():
            full_text += page.extract_text()
    full_text = clean_text(full_text)

    # ---------- ENTITY EXTRACTION ----------
    entities = {
        "diseases": extract_entities(DISEASES, full_text),
        "algorithms": extract_entities(ALGORITHMS, full_text),
        "metrics": extract_entities(METRICS, full_text),
        "datasets": extract_entities(DATASETS, full_text)
    }

    # ---------- RELATIONSHIP + TRIPLES ----------
    relationships = []
    triples = []

    for algo in entities["algorithms"]:
        for disease in entities["diseases"]:
            relationships.append({"source": algo, "relation": "used_for", "target": disease})
            triples.append([algo, "used_for", disease])

        for metric in entities["metrics"]:
            relationships.append({"source": algo, "relation": "evaluated_by", "target": metric})
            triples.append([algo, "evaluated_by", metric])

    # ---------- FINAL JSON ----------
    final_json = {
        "paper_id": paper_id,
        "metadata": {
            "title": row["Paper Title"],
            "authors": row["Authors"],
            "year": int(row["Year"]),
            "journal": row["Journal"]
        },
        "entities": entities,
        "relationships": relationships,
        "triples": triples
    }

    output_path = f"{OUTPUT_DIR}{paper_id}_kg.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_json, f, indent=4, ensure_ascii=False)

print("Knowledge graph JSON created for all papers.")
