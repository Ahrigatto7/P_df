"""Utility functions for extracting text from documents."""

from docx import Document
from PyPDF2 import PdfReader

def extract_text_from_pdf(file_path):
    """Extract text from a PDF file using PyPDF2."""
    text = []
    with open(file_path, "rb") as f:
        reader = PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
    return "\n".join(text).strip()

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs]).strip()

def extract_text_from_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

def extract_text_from_file(file_path):
    ext = file_path.lower().split('.')[-1]
    if ext == "pdf":
        return extract_text_from_pdf(file_path)
    elif ext == "docx":
        return extract_text_from_docx(file_path)
    elif ext == "txt":
        return extract_text_from_txt(file_path)
    else:
        return ""
