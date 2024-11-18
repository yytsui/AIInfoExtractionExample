from typing import Dict

import PyPDF2
from loguru import logger


def read_pdf(pdf_path: str) -> Dict:
    """Extract text from PDF file."""
    page_text = {}
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for i, page in enumerate(pdf_reader.pages):
                page_text[i+1] = page.extract_text()
    except Exception as e:
        logger.error(f"Error reading PDF: {e}")
        page_text = {"error": f"Error reading PDF: {e}"}
    return page_text
