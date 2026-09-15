import filetype
from pypdf import PdfReader
from docx import Document
import re

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import spacy 
import nltk

# Downloading all models


nltk.data.path = [
    path for path in nltk.data.path
    if not path.startswith("E:\\")
]

nltk.download("all")
file_path = input("Enter your File Path: ")

try:
    check_file_path = filetype.guess(file_path)

    if check_file_path is None:
        print("Not a valid file")

    else:
        print(check_file_path)

        extension = check_file_path.extension
        mime = check_file_path.mime

        if extension in ("pdf", "docx"):
            print(f"File type is {extension}")

        if extension == "pdf":
                reader = PdfReader(file_path)
                extracted_text=""
                for page in reader.pages:
                    extracted_text+=page.extract_text()
                print(extracted_text)

                
        elif extension=="docx":
            get_content=Document(file_path)
            print("Number of paragraphs:", len(get_content.paragraphs))
            for paragraph in get_content.paragraphs:
                text+=paragraph.text + "\n"
                print(text)
            print(len(text))
            # Counting Words 
            print(len(text.spit()))
            #
            text=text.lowercase.strip()
            # Removing Punctuation
            

            cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '',text)
            print(cleaned_text)

            # Creating tokens for Words
            tokens=word_tokenize(cleaned_text)
            print(tokens)

            # Loading StopWords
            stop_words={stopwords.words('english')}
            # Using List Comprehension to remove common stopwords
            filtered_tokens=[word for word in tokens if word not in stop_words]
            print(filtered_tokens)

            # Creating Object for Word Net 
            lemmitizer=WordNetLemmatizer()
            # Applying Lemmitization:
            lemmitized=[lemmitizer.lemmitize(word) for word in filtered_tokens]

            # Creating Skills List
            skills=["Python","Django","SQL","AWS","React","Javascript","MongoDB","Git","Artifical Intelligence","DataScience","Azure"]
            skill_count = 0

            for skill in lemmitized:
             if any(re.search(r'\b' + re.escape(skill) + r'\b', s) for s in skills):
              detected_skills+=skill
              skill_count += 1
              # Returning detected skills as a list
              skills_list=list(detected_skills)

            print(skill_count)
        # Using NER 
            nlp=spacy.load('en_core_web_sm')
            doc=nlp(lemmitized)





                
        else:
            print("Not supported file type for Resume")

except FileNotFoundError:
    print("The path entered does not exist.")