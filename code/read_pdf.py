from PyPDF2 import PdfReader

# Path to ONE sample PDF
pdf_path = "../data/pdf/AI_Health_06.pdf"   # you can change paper later

# Load PDF
reader = PdfReader(pdf_path)

pdf_text = ""
for page_num, page in enumerate(reader.pages):
    page_text = page.extract_text()
    if page_text:
        pdf_text += page_text + "\n"

print("PDF read successfully")
print("Total pages:", len(reader.pages))
print("\nSample PDF text:")
print(pdf_text[:500])   # first 500 characters
