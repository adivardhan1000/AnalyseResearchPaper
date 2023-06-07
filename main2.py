import PyPDF2
from transformers import GPT2Tokenizer, GPT2LMHeadModel

# Load the pre-trained model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

# Extract text from the PDF
pdf_file = open('paper.pdf', 'rb')
pdf_reader = PyPDF2.PdfReader(pdf_file, strict=False)
text = ''
for page in range(len(pdf_reader.pages)):
    page_obj = pdf_reader.pages[page]
    text += page_obj.extract_text()

# Split the text into chunks of maximum length 250
max_length = 250
text = text.split()
chunks = [' '.join(text[i:i + max_length]) for i in range(0, len(text), max_length)]

# Analyze each chunk separately
limitations = []
for chunk in chunks:
    # Tokenize the text
    inputs = tokenizer.encode(chunk, return_tensors='pt')

    # Pass the inputs through the model
    outputs = model.generate(inputs, max_length=512)

    # Decode the summary
    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Identify the limitations
    for sentence in summary.split('. '):
        if 'limitation' in sentence or 'limitations' in sentence:
            limitations.append(sentence.strip())
    print(summary)

print("Limitations discussed in the paper:")
for limitation in limitations:
    print("- " + limitation)
