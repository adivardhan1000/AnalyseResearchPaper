import os
import fitz
import re

# define keywords related to limitations
keywords = ['limitation', 'limitations', 'limiting factor', 'restricted', 'restricted by', 'obstacle', 'obstacles', 'constraint', 'constraints', 'challenges', 'challenge', 'shortcoming', 'shortcomings', 'flaw', 'flaws', 'drawback', 'drawbacks', 'weakness', 'weaknesses', 'deficiency', 'deficiencies', 'inadequate', 'inadequacies', 'lacking', 'lack',"limitations","limitations of the study","limitations of research","limitations and future research","limitations and implications","limitations and future directions","limitations and suggestions for future research","drawbacks","future scope","future research","future studies","future work","what remains to be done","further research","future challenges","future limitations","future directions","future prospects","room for improvement","needs further investigation"
            ]

# define the input and output folders
input_folder = "input"
output_folder = "output"

# create the output folder if it does not exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

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

            # find sentences containing keywords
            sentences = re.findall(
                r'([^.]*?(?:{})[^.]*\.)'.format('|'.join(keywords)), text, re.IGNORECASE)

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
