import requests
import PyPDF2
from transformers import pipeline

# Extract text from the PDF
pdf_file = open('paper.pdf', 'rb')
pdf_reader = PyPDF2.PdfReader(pdf_file, strict=False)
text = ''
for page in range(len(pdf_reader.pages)):
    page_obj = pdf_reader.pages[page]
    text += page_obj.extract_text()

# Analyze the text using SciBERT
nlp = pipeline("text2text-generation", model="allenai/scibert_scivocab_uncased", tokenizer="allenai/scibert_scivocab_uncased")
summary = nlp(text, max_length=512, do_sample=False)

# Identify the limitations
limitations = []
for sentence in summary[0]['generated_text'].split('. '):
    if 'limitation' in sentence or 'limitations' in sentence:
        limitations.append(sentence.strip())

print("Limitations discussed in the paper:")
for limitation in limitations:
    print("- " + limitation)
