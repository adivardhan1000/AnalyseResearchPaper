import os
import fitz
import spacy

# load the English language model from spaCy
nlp = spacy.load("en_core_web_lg")

# define the input and output folders
input_folder = "input"
output_folder = "output"

# create the output folder if it does not exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# define a function to check if a sentence contains a limitation
def contains_limitation(sentence):
    for token in sentence:
        if token.dep_ == "neg" or token.text in ["not", "no"]:
            continue
        if token.dep_ in ["amod", "advmod", "compound"] and token.head.text in ["limitation", "limitations"]:
            return True
        if token.text in ["limitation", "limitations"] and token.head.dep_ in ["nsubj", "nsubjpass"]:
            return True
        if token.text in ['restricted', 'constraints', 'further research', 'weaknesses', 'inadequacies', 'challenges', 'future scope', 'future challenges', 'room for improvement', 'future limitations', 'limitations and future directions', 'needs further investigation', 'lacking', 'restricted by', 'constraint', 'shortcomings', 'future work', 'limitations', 'flaw', 'obstacle', 'limitations and future research', 'limiting factor', 'shortcoming', 'deficiencies', 'flaws', 'limitations of research', 'future research', 'obstacles', 'future directions', 'what remains to be done', 'challenge', 'inadequate', 'lack', 'drawbacks', 'limitations and suggestions for future research', 'limitations and implications', 'weakness', 'drawback', 'limitations of the study', 'future studies', 'future prospects', 'deficiency']:
            return True
    return False

# process each PDF file in the input folder
for file_name in os.listdir(input_folder):
    if file_name.endswith(".pdf"):
        # open the PDF file
        input_file_path = os.path.join(input_folder, file_name)
        doc = fitz.open(input_file_path)

        # iterate over the pages of the PDF
        for i in range(doc.page_count):
            # get the page text
            page = doc.load_page(i)
            text = page.get_text()

            # parse the text using spaCy
            parsed_text = nlp(text)

            # find sentences containing limitations
            sentences = []
            for sentence in parsed_text.sents:
                if contains_limitation(sentence):
                    sentences.append(str(sentence))

            # highlight the sentences
            for sentence in sentences:
                matches = page.search_for(sentence)
                for match in matches:
                    highlight = page.add_highlight_annot(match)
                    highlight.update()

        # save the modified PDF in the output folder
        output_file_path = os.path.join(output_folder, file_name)
        doc.save(output_file_path)
        doc.close()
