import json
import pandas as pd
from docx import Document
from PyPDF2 import PdfReader

# ----------- READ EXCEL -----------
excel_path = "../data/excel/AI_Healthcare_Metadata.xlsx"
df = pd.read_excel(excel_path)

# Pick ONE paper (example: AI_Health_06)
paper_id = "AI_Health_06"
paper_row = df[df["Paper ID"] == paper_id].iloc[0]

print(df.columns)


# ----------- READ WORD (ABSTRACT) -----------
doc = Document("../data/word/AI_Healthcare_Abstracts.docx")
abstract_lines = []
for para in doc.paragraphs:
    if para.text.strip():
        abstract_lines.append(para.text.strip())

abstract_text = "\n".join(abstract_lines)

# ----------- READ PDF -----------
pdf_path = f"../data/pdf/{paper_id}.pdf"
reader = PdfReader(pdf_path)

pdf_text = ""
for page in reader.pages:
    if page.extract_text():
        pdf_text += page.extract_text() + "\n"

# ----------- CREATE JSON OBJECT -----------
paper_json = {
    "paper_id": paper_id,
    "title": paper_row["Paper Title"],
    "authors": paper_row["Authors"],
    "affiliations": paper_row["Author Affiliations"],
    "year": int(paper_row["Year"]),
    "journal": paper_row["Journal"],
    "keywords": paper_row["Keywords"],
    "abstract": abstract_text,
    "full_text": pdf_text
}

# ----------- SAVE JSON -----------
output_path = f"../output/json/{paper_id}.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(paper_json, f, indent=4, ensure_ascii=False)

print("JSON file created successfully:", output_path)
