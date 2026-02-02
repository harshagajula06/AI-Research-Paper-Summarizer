from docx import Document

# Path to Word file
word_path = "../data/word/AI_Healthcare_Abstracts.docx"

# Load Word document
doc = Document(word_path)

# Read all paragraphs
abstracts = []
for para in doc.paragraphs:
    if para.text.strip():
        abstracts.append(para.text.strip())

# Combine text
abstract_text = "\n".join(abstracts)

print("Word file read successfully")
print("Total paragraphs read:", len(abstracts))
print("\nSample abstract text:")
print(abstract_text[:500])  # print first 500 characters
