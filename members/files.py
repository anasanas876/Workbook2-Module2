import filetype
from pypdf import PdfReader
from docx import Document
import re

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import spacy
import nltk




nlp = spacy.load("en_core_web_sm")

# NLTK data location
nltk.data.path = [
    r"C:\Users\B23F0542AI156\nltk_data"
]


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

            extracted_text = ""

            for page in reader.pages:
                page_text = page.extract_text()

                if page_text:
                    extracted_text += page_text + "\n"

            print(extracted_text)

       

        elif extension == "docx":

            get_content = Document(file_path)
            extracted_text=""
            for text in get_content.paragraphs.text():
                extracted_text+=text
                extracted_text=extracted_text.lower()
                extracted_text=re.sub(r"[^a-zA-Z\d+@]"," ",extracted_text)
                extracted_text=extracted_text.strip()

            skills = [
                "Python",
                "Django",
                "SQL",
                "AWS",
                "React",
                "Javascript",
                "MongoDB",
                "Git",
                "Artificial Intelligence",
                "Data Science",
                "Azure"
            ]

            detected_skills = []

            skills_section = [
                "Skills",
                "Technical Skills",
                "Professional Skills"
            ]

            # Convert section names to lowercase
            skills_section = [
                section.lower()
                for section in skills_section
            ]
            find_skills=re.search("skills|technical skills|professional skills.(?=:\s+)",extracted_text)
            print(find_skills)

            print(
                "Number of paragraphs:",
                len(get_content.paragraphs)
            )

            
            paragraphs = get_content.paragraphs
            text = ""

            

            for paragraph in paragraphs:

                text += paragraph.text + "\n"

           

            for i, paragraph in enumerate(paragraphs):

                paragraph_text = paragraph.text.strip().lower()

                if (
                    paragraph.style.name.startswith("Heading")
                    and paragraph_text in skills_section
                ):

                    print(
                        "Section:",
                        paragraph.text,
                        ">",
                        paragraph.style.name
                    )

                    # Read paragraphs after Skills heading
                    for next_paragraph in paragraphs[i + 1:]:

                        # Stop when another heading is reached
                        if next_paragraph.style.name.startswith("Heading"):
                            break

                        paragraph_text = (
                            next_paragraph.text.strip().lower()
                        )

                        # Check skills only inside Skills section
                        for skill in skills:

                            if skill.lower() in paragraph_text:

                                if skill not in detected_skills:
                                    detected_skills.append(skill)

            print(
                "Detected Skills:",
                detected_skills
            )
            # Designing Rubric System
            skills_percentage=40
            experience=30
            keywords=30
            calculate_score=len(detected_skills)/len(skills)*100
            print(calculate_score)

            # Getting Experience
            experience_section=["Professional Experience",
                                "Technical Experience","Experience"]
            experience_section=[experience.lower() for experience in experience_section]
            for i,paragraph in enumerate(paragraphs):
                if (paragraph.style.name.startswith("Heading 1") and paragraph.text in experience_section):
                    for get_experience in paragraph[i+1:]:
                        if get_experience.style.name.startswith("Heading 1"):
                            break
                        record_experience=get_experience.text
                        experience_years=nlp(record_experience)
                        print(experience_years.ents)
                        
                            


            text = text.lower().strip()

            #print("Resume Text:")
            #print(text)

            # Counting Words
            print(
                "Word Count:",
                len(text.split())
            )

           
            cleaned_text = re.sub(
                r'[^a-zA-Z0-9\s]',
                '',
                text
            )

            print("Cleaned Text:")
            #print(cleaned_text)

           

            tokens = word_tokenize(cleaned_text)

            print("Tokens:")
            print(tokens)

            

            stop_words = set(
                stopwords.words("english")
            )

            filtered_tokens = [
                word
                for word in tokens
                if word not in stop_words
            ]

            print("After Stopword Removal:")
            print(filtered_tokens)

            

            lemmatizer = WordNetLemmatizer()

            lemmatized = [
                lemmatizer.lemmatize(word)
                for word in filtered_tokens
            ]

            print("Lemmatized:")
            print(lemmatized)

            

            

            doc = nlp(text)

            print("Named Entities:")

            for entity in doc.ents:

                print(
                    entity.text,
                    ">",
                    entity.label_
                )

        

        else:

            print(
                "Not supported file type for Resume"
            )


except FileNotFoundError:

    print(
        "The path entered does not exist."
    )