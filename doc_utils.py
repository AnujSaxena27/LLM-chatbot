import pdfplumber
import docx
import re

def extract_text_from_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += "\n--- Page Break ---\n" + page_text
    return text.strip()

def extract_text_from_docx(uploaded_file):
    doc = docx.Document(uploaded_file)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_headings(text):
    headings = re.findall(r'(^\d+(\.\d+)*\s+.+)', text, re.MULTILINE)
    return [h[0] for h in headings]
