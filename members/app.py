import streamlit as st
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import re
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag


nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagged_eng')

# Page Setup
st.set_page_config(page_title="Resume_Job_Match_Scorer",layout="wide")
st.markdown("Make ATS Friendly Resumes by checking how well your resume matches with the Job Description")
with st.sidebar:
    st.header("About")
    st.info("""
    This tool helps you measure your resume score and let you check how wwell your resume matches with jo description.
    
    """)
    st.header("How it works")
    st.write("""1-Upload your Resume\n
             2-Paste the Job Description\n
             3-Click Analyze and Review the Scores and sugguestions.
    
    """)



def extract_text(uploaded_file):
    try:
        pdf_reader=PyPDF2.PdfReader(uploaded_file)
        text=""
        for page in pdf_reader.pages:
            text+=page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF file: {e}")
        return ""

def clean_text(text):
    text=text.lower()
    text=re.sub(r"[^a-zA-Z\s+\d+\@\_+]","",text)
    text=re.sub(r"\s+"," ",text).strip()
    return text

def stop_words_removal(text):
    words=word_tokenize(text)
    stop_words=set(stopwords.words('english'))
    # using List comprehensin to get the cleaned text 
    return " ".join(word for word in words if word not in stop_words)

def calculate_similarity(resume_text,job_description):
    resume_processed=stop_words_removal(clean_text(resume_text))
    job_processed=stop_words_removal(clean_text(job_description))
    vectorizer=TfidfVectorizer()
    tfidf_matrix=vectorizer.fit_transform([resume_processed,job_processed])
    score=cosine_similarity(tfidf_matrix[0:1],tfidf_matrix[1:2])[0][0]*100
    return round(score,2)


def extract_keywords(text,num_keywords=10):
    words=word_tokenize(text)
    words=[w for w in words if len(w)>2]
    tagged_words=pos_tag(words)
    nouns=[w for w,pos in tagged_words if pos.startswith("NN") or pos.startswith("JJ")]
    word_frequency=Counter(nouns)


def main():
    uploaded_file=st.file_uploader("Upload your Resume",type=['pdf'])
    job_description=st.text_area("Paste the job description",height=300)
    if st.button("Analyze match",key='analyze_main') and uploaded_file and job_description:
        with st.spinner("Analyzing your Resume"):
         resume_text=extract_text(uploaded_file)
         if not resume_text:
             st.error("Could not extract text")
             return
         similarity_score=calculate_similarity(resume_text,job_description)

         st.subheader("Results")
         st.metric("Match Score"f"{similarity_score:.2f}%")

main()