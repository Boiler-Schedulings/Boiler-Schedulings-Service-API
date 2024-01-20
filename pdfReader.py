import fitz
import re

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as pdf_document:
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text += page.get_text()
    text = text.replace('\n', ' ')

    pattern = re.compile(r'\b[A-Z]{2,4} \d{5}\b')
    matches = pattern.findall(text)
    return matches

pdf_path = "Academic_Transcript.pdf"
matches = extract_text_from_pdf(pdf_path)
unique_matches = list(set(matches))
print(unique_matches)


