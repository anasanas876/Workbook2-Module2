import filetype
from pypdf import PdfReader
from docx import Document
import re

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import spacy
import nltk
from datetime import datetime




nlp = spacy.load("en_core_web_sm")

# NLTK data location
nltk.data.path = [
    r"C:\Users\B23F0542AI156\nltk_data"
]

# creating Date time object
def find_date(normalized_text):
    normalized_text=re.search (r"\d{2}-\d{4}-\d{2}-\d{4}")
    return normalized_text

now = datetime.now()

# Writing a Function to Find Company Name and Job Title
delimiter_pattern = re.compile(
    r"^\s*(?P<job>.+?)\s*[–-]\s*"
    r"(?P<company>[^|]+?)\s*\|\s*"
    r"(?P<location>[^|]+?)\s*\|\s*"
    r"(?P<date>.+?)\s*$",
    re.IGNORECASE
)
def normalize_dates(text):

    months = {
        "jan": "01", "january": "01",
        "feb": "02", "february": "02",
        "mar": "03", "march": "03",
        "apr": "04", "april": "04",
        "may": "05",
        "jun": "06", "june": "06",
        "jul": "07", "july": "07",
        "aug": "08", "august": "08",
        "sep": "09", "september": "09",
        "oct": "10", "october": "10",
        "nov": "11", "november": "11",
        "dec": "12", "december": "12"
    }

    month_pattern = r"(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)"

    # Month Year - Month Year
    pattern0 = rf"{month_pattern}\.?\s*(\d{{4}})\s*[-–]\s*{month_pattern}\.?\s*(\d{{4}})"

    if re.search(pattern0, text, re.IGNORECASE):
        return re.sub(
            pattern0,
            lambda m: (
                f"{months[m.group(1).lower()]}-{m.group(2)}-"
                f"{months[m.group(3).lower()]}-{m.group(4)}"
            ),
            text,
            flags=re.IGNORECASE
        )

    # MM/YYYY - MM/YYYY
    pattern1 = r"(\d{2})/(\d{4})\s*[-–]\s*(\d{2})/(\d{4})"

    if re.search(pattern1, text):
        return re.sub(
            pattern1,
            r"\1-\2-\3-\4",
            text
        )

    # YYYY/MM - YYYY/MM
    pattern2 = r"(\d{4})/(\d{2})\s*[-–]\s*(\d{4})/(\d{2})"

    if re.search(pattern2, text):
        return re.sub(
            pattern2,
            r"\2-\1-\4-\3",
            text
        )

    # Month Year - Present
    pattern3 = rf"({month_pattern})\.?\s*(\d{{4}})\s*[-–]\s*(present|now|current|ongoing|today)"

    if re.search(pattern3, text, re.IGNORECASE):
        return re.sub(
            pattern3,
            lambda m: (
                f"{months[m.group(1).lower()]}-{m.group(2)}-"
                f"{now.month:02d}-{now.year}"
            ),
            text,
            flags=re.IGNORECASE
        )

    return text
                   
         
     



skills_section = [
        "skills",
        "technical skills",
        "professional skills"
    ]

target_skills = [
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
]
target_skills=[skill.lower() for skill in target_skills]
keywords=["Python","Django","Web-Development","Javascript","Data Science","Artifical Intelligence"]

def count_keywords(keywords,extracted_text):
    total_keywords=0
    for keyword in keywords:
        if keyword in extracted_text:
            extracted_text_list=extracted_text.split()
            count_frequency=extracted_text_list.count(keyword)
            total_keywords+=count_frequency
        average_keyword_score=len(keywords)/len(total_keywords)
        return total_keywords,average_keyword_score
    

def skills_check(target_skills,skills):
    detected_skills = []
    resume_score=""
    for skill in target_skills:
        for resume_text in skills:
         if skill in resume_text:
            detected_skills.append(skill)
    # Counting total detected skills
    detected_skills_percentage=len(detected_skills)/len(target_skills)*100
    
        
    
    return detected_skills,detected_skills_percentage
    




    



    
def scoring_function(skills):
# Extracts detected skills from a skills_check function
    detected_skills = skills[0]

    skills_weight = 40

    skill_score = (
        len(detected_skills) / len(target_skills)
    ) * skills_weight

    return skill_score
    

    

        

        
        

                

    return detected_skills



def list_missing_skills(target_skills,detected_skills):
    target_skills = [
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
    if target_skills not in detected_skills:
        return list(target_skills)




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

            detected_skills = []
            

            skills_section = [
        "skills",
        "technical skills",
        "professional skills"
    ]
            experience_section=["experience","professional experience","previous experience","employment experience","employment history","work experience"]

            
        
            inside_skills = False
            inside_experience = False

            skills = []
            experience = ""
            text=""
            jobs={"Job-Title":[]}
            jobs_list=[]
            job_pattern=re.search(r"\b[A-Za-z]+(?:[/&|-][A-Za-z]+)?(?:\s+[A-Za-z]+(?:[/&|-][A-Za-z]+)?){1,4}\b",text)
            company_pattern=re.search(r"\b[A-Za-z][A-Za-z&@.-]*(?:\s+[A-Za-z][A-Za-z&@.-]*){0,5}\b",text)
            location_pattern = re.search(r"^(?:[A-Z][A-Za-z.'-]*(?:\s+[A-Z][A-Za-z.'-]*)*)\s*,\s*(?:[A-Z]{2}|[A-Z][A-Za-z.'-]*(?:\s+[A-Z][A-Za-z.'-]*)*)(?:\s*,\s*[A-Z][A-Za-z.'-]*(?:\s+[A-Z][A-Za-z.'-]*)*)?$",text)
                
            for index, paragraph in enumerate (get_content.paragraphs):
                index+=1
#     # Skills heading
                if paragraph.style.name.startswith("Heading 2") and paragraph.text.lower().rstrip(":") in skills_section:
                     inside_skills = True
                     inside_experience = False
                     continue
                
#     # Experience heading
                if paragraph.style.name.startswith("Heading 2") and paragraph.text.lower().rstrip(":") in experience_section:
                     inside_experience = True
                     inside_skills = False
                     continue
                normalized_text=normalize_dates(paragraph.text)
                if find_date(normalized_text):
                    date_index=index
                pattern4=(r"[A-Z]+\s+[A-Z]+\s+[A-Z]*\s*[A-Z]*\s*")
                pattern5=(r"[A-Z]+\s+[A-Z]*\s+[A-Z]*,([A-Z]+)|([A-Z]+,[A-Z]+)")
                for i in range(date_index -1,-1,-1):
                    for information in get_content.paragraphs[i]:
                        for run in information.runs:
                            if run.bold :
                                if re.search(pattern4,run.text):
                                    jobs_list.append(run.text)
                                    jobs.setdefault("Job-Title",[]).append(run.text)
                                    match = delimiter_pattern.search(paragraph.text)

                                if match:
                                 job = match.group("job").strip()
                                 company = match.group("company").strip()
                                 location = match.group("location").strip()
                                 date = match.group("date").strip()

   
                                #elif call_find_job_function:
                                    #if re.search(r"{call_find_job_function[0]}\-\s*{call_find_job_function[1]}\|\s*{call_find_job_function[2]}")
                                    

                        #if run=="bold":
                         #job_title=run.text


                months={
                    "january":"jan",
                    "feburary":"feb",
                    "march":"mar",
                    "april":"apr",
                    "may":"may",
                    "june":"jun",
                    "july":"jul",
                    "august":"aug",
                    "september":"sep",
                    "october":"oct",
                    "november":"nov",
                    "descember":"dec"
                }
                for find_text in text:

                 for month,short in months.items():

                    text=re.sub(month,short,text)
                    find_date=normalize_dates(text)
                    

                # finding date in Normalized text
                
                    
#      Skills content
                if paragraph.style.name.startswith("Heading 2"):
                      inside_skills=False
                      inside_experience=False
                      continue
                if inside_skills:
                      skills.append(paragraph.text)

# #     # Experience content
                if inside_experience:
                     experience += paragraph.text + " "
#         experience=experience.lower()
#         experience=re.sub("r[^a-zA-Z0-9_]"," ",experience)
#         # extracting Job Entries
#         find_boundary=re.search(r"(\d{2}\-\d{4}\-\d{2}\-\d{4})").group()
#         if find_boundary:
#             re.search("()")
        #experience=re.sub("[a-zA-Z]\s-\d+"," ",experience)
        skills = [skill.lower() for skill in skills]
            
        counting_matched_skills = skills_check(target_skills, skills)
        #print(experience)
        doc=nlp(experience)
        for ent in doc.ents:
            print(ent.text, ent.label_)

        # experience_tokens=word_tokenize(experience)
        # experience_tokens = " ".join(experience_tokens)
        # experience_entities=nlp(experience_tokens)
        # dates=""
        # organizations=""
        # for entity in experience_entities.ents:
        #         if entity.label_=="DATE": 
        #             dates+=entity.text +" "
        #         elif entity.label_=="ORG":
        #             organizations+=entity.text + " "
        #         print(f"Dates  {dates} Organizations {organizations}")
        # Extracting Years of Experience from Resume
        #years = re.search(r"\d+\s+years of experience", experience)

        #if years:
            #print(years.group())
        months={"jan":"01",
            "feb":"02",
            "mar":"03",
            "apr":"04",
            "may":"05",
            "jun":"06",
            "jul":"07",
            "aug":"08",
            "sep":"09",
            "oct":"10",
            "nov":"11",
            "dec":"12"
                    }
        pattern = r'([a-z]+)[-\s](\d{4})'
        date = re.sub(
    pattern,
    lambda m: f"{months[m.group(1)[:3]]}-{m.group(2)}",
    experience
)
        
        
        find_dates = re.findall(r"\d{2}-\d{4}",date)
        print(find_dates[:3])

        
except:
     pass
    



#print(counting_matched_skills)
##print(skills)


     




        

        
            
           
            

    



        
   


                        
                            




           



            






            



            

            



        









# def score_resume(target_skills,detected_skills):
#     detected_skills=skills_check()
#     skills_count=target_skills/detected_skills
#     skills_count=skills_count*100
#     return skills_count

