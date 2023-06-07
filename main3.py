import requests
import PyPDF2
from transformers import pipeline

# Load the NER pipeline
ner_pipeline = pipeline('ner', model='dbmdz/bert-large-cased-finetuned-conll03-english', tokenizer='dbmdz/bert-large-cased-finetuned-conll03-english')

# Extract text from the PDF
pdf_file = open('paper.pdf', 'rb')
pdf_reader = PyPDF2.PdfReader(pdf_file, strict=False)
text = ''
for page in range(len(pdf_reader.pages)):
    page_obj = pdf_reader.pages[page]
    text += page_obj.extract_text()

# Analyze the text with the NER pipeline
entities = ner_pipeline(text)

# Extract the limitations discussed in the paper
limitation_entities = [entity['word'] for entity in entities if entity['entity'] == 'MISC' and 'limitation' in entity['word'].lower()]

print("Limitations discussed in the paper:")
for limitation in limitation_entities:
    print("- " + limitation)
