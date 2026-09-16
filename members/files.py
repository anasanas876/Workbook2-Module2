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


#nltk.data.path = [
    #path for path in nltk.data.path
    #if not path.startswith("E:\\")
#]


file_path = input("Enter your File Path: ")

try:
    check_file_path = filetype.guess(file_path)

    if check_file_path is None:
        print("Not a valid file")

    else:
        print(check_file_path)

        extension = check_file_path.extension
        mime = check_file_path.mime

        

        if extension == "pdf":
                
                reader = PdfReader(file_path)
                extracted_text=""
                for page in reader.pages:
                    extracted_text+=page.extract_text()
                print(extracted_text)

                
        elif extension=="docx":
            from docx import Document

get_content = Document(file_path)

skills = [
    "Python", "Django", "SQL", "AWS", "React",
    "Javascript", "MongoDB", "Git", "Artificial Intelligence",
    "Data Science", "Azure"
]

detected_skills = []

skills_section = [
    "Skills",
    "Technical Skills",
    "Professional Skills"
]

print("Number of paragraphs:", len(get_content.paragraphs))

paragraphs = get_content.paragraphs

for i, paragraph in enumerate(paragraphs):

    if (
        paragraph.style.name == "Heading 1"
        and paragraph.text.strip() in skills_section
    ):

        for next_paragraph in paragraphs[i + 1:]:

            
            if next_paragraph.style.name.startswith("Heading"):
                break

            
            for skill in skills:

                if skill.lower() in next_paragraph.text.lower():
                    detected_skills.append(skill)

            print("Detected Skills:", detected_skills)
                    
                 

            print(paragraph.text, ">", paragraph.style.name)

            text+=paragraph.text + "\n"
            print(text)
            print(len(text))
            # Counting Words 
            print(len(text.split()))
            
            text=text.lower().strip()
            #Removing Punctuation
            

            cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '',text)
            print(cleaned_text)

            # Creating tokens for Words
            tokens=word_tokenize(cleaned_text)
            print(tokens)

            # Loading StopWords

            stop_words = set(stopwords.words('english'))
             #Using List Comprehension to remove common stopwords
            filtered_tokens=[word for word in tokens if word not in stop_words]
            print(filtered_tokens)

            #Creating Object for Word Net 
            lemmatizer = WordNetLemmatizer()
            lemmatized = [lemmatizer.lemmatize(word) for word in filtered_tokens]

            
            
             #Making list consistent with Resume.
            skills=[skill.lower() for skill in skills]
            skill_count = 0
            detected_skills=[]

            for skill in lemmatized:
             if any(re.search(r'\b' + re.escape(skill) + r'\b', s) for s in skills):
              detected_skills.append(skill)
              skill_count += 1
              # Returning detected skills as a list
              

            #print(skill_count)
        
            nlp=spacy.load('en_core_web_sm')
            doc=nlp(text)
            print(doc.ents)





                
        else:
            print("Not supported file type for Resume")

except FileNotFoundError:
    print("The path entered does not exist.")