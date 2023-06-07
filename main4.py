import os
import fitz
import re
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Define keywords related to limitations and future scope
keywords = [
    'limitation', 'limitations', 'limited', 'restrict', 'restriction', 'constrain', 'constraint', 
    'challenge', 'challenging', 'difficult', 'difficulty', 'obstacle', 'obstacles', 'drawback', 
    'drawbacks', 'weakness', 'weaknesses', 'inadequate', 'inadequacy', 'need', 'needs', 'require', 
    'requirements', 'necessary', 'necessity', 'future scope', 'future work', 'future research', 
    'future study', 'future investigation', 'future directions', 'future challenges'
]

# Load the pre-trained tokenizer and model
tokenizer = AutoTokenizer.from_pretrained('textattack/bert-base-uncased-MNLI')
model = AutoModelForSequenceClassification.from_pretrained('textattack/bert-base-uncased-MNLI')

# Define the input and output directories
input_dir = 'input'
output_dir = 'output'

# Iterate over the PDF files in the input directory
for filename in os.listdir(input_dir):
    # Check if the file is a PDF
    if not filename.endswith('.pdf'):
        continue
        
    # Define the input and output file paths
    input_file = os.path.join(input_dir, filename)
    print("analyzing",input_file)
    # Open the input PDF file and iterate over its pages
    with fitz.open(input_file) as doc:
        for page in doc:
            # Get the page text
            text = page.get_text()
            
            # Split the text into sentences
            sentences = re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', text)
            
            # Iterate over the sentences and classify them
            for sentence in sentences:
                # Preprocess the sentence
                inputs = tokenizer(sentence, padding=True, truncation=True, return_tensors='pt')
                
                # Classify the sentence as related to limitations/future scope or not
                outputs = model(**inputs)
                predicted_label = 'contradiction' if outputs.logits[0][0] > outputs.logits[0][2] else 'entailment'
                print(outputs.logits)
                # Highlight the sentence if it's related to limitations/future scope
                if predicted_label == 'entailment' and any(keyword in sentence.lower() for keyword in keywords):
                    matches = page.search_for(sentence)
                    for match in matches:
                        highlight = page.add_highlight_annot(match)
                        highlight.update()
        
        # Save the modified PDF with highlighted sentences
        #output_file_path = os.path.join(output_dir, filename)
        #doc.save(output_file_path)
