import pandas as pd
import json
import re
from docx import Document
from PyPDF2 import PdfReader
import os

# ---------- LOAD METADATA ----------
df = pd.read_excel("../data/excel/AI_Healthcare_Metadata.xlsx")
paper_ids = df["Paper ID"].tolist()

# ---------- READ ABSTRACTS ONCE ----------
doc = Document("../data/word/AI_Healthcare_Abstracts.docx")
abstract_text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

# ---------- TEXT CLEAN FUNCTION ----------
def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()

# ---------- ENTITY LISTS ----------
diseases = ["heart disease", "diabetes", "cancer"]
algorithms = ["xgboost", "random forest", "decision tree", "knn", "naive bayes"]
metrics = ["accuracy", "precision", "recall"]

# ---------- PROCESS EACH PAPER ----------
for paper_id in paper_ids:
    print(f"Processing {paper_id}...")

    row = df[df["Paper ID"] == paper_id].iloc[0]

    # ---- READ PDF ----
    pdf_path = f"../data/pdf/{paper_id}.pdf"
    reader = PdfReader(pdf_path)
    full_text = ""
    for page in reader.pages:
        if page.extract_text():
            full_text += page.extract_text()

    full_text = clean_text(full_text)

    # ---- NORMALIZATION ----
    keywords = [k.strip().lower() for k in str(row["Keywords"]).split(",")]

    # ---- ENTITY EXTRACTION ----
    def extract(items, text):
        return [i for i in items if i in text]

    entities = {
        "diseases": extract(diseases, full_text),
        "algorithms": extract(algorithms, full_text),
        "metrics": extract(metrics, full_text)
    }

    # ---- TRIPLE CREATION ----
    triples = []
    for a in entities["algorithms"]:
        for d in entities["diseases"]:
            triples.append([a, "used_for", d])
        for m in entities["metrics"]:
            triples.append([a, "evaluated_by", m])

    triples.append([paper_id, "published_in", row["Journal"]])

    # ---- FINAL JSON ----
    final_json = {
        "paper_id": paper_id,
        "title": row["Paper Title"],
        "authors": row["Authors"],
        "year": int(row["Year"]),
        "journal": row["Journal"],
        "keywords": keywords,
        "abstract": clean_text(abstract_text),
        "entities": entities,
        "triples": triples
    }

    # ---- SAVE OUTPUT ----
    output_path = f"../output/json/{paper_id}_final.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_json, f, indent=4, ensure_ascii=False)

print("Pipeline executed for ALL papers successfully.")
