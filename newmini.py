import re
import pandas as pd
from collections import Counter
from datasets import load_dataset
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import nltk

nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    words = [word for word in words if word not in stop_words]
    stemmer = PorterStemmer()
    words = [stemmer.stem(word) for word in words]
    return words

def calculate_ats_score(resume_text, job_description_text):
    resume_words = preprocess_text(resume_text)
    job_description_words = preprocess_text(job_description_text)
    job_description_counter = Counter(job_description_words)
    resume_counter = Counter(resume_words)
    keywords = job_description_counter.keys()
    keyword_match_count = sum(min(job_description_counter[keyword], resume_counter[keyword]) for keyword in keywords)
    total_keywords = len(keywords)
    keyword_match_score = (keyword_match_count / total_keywords) * 100 if total_keywords else 0
    return keyword_match_score

dataset = load_dataset('InferencePrince555/Resume-Dataset')
df = pd.DataFrame(dataset['train'])
csv_file = 'resume_dataset.csv'
df.to_csv(csv_file, index=False)
print(df.head())
print(df.columns)

resume_column = 'Resume_test'
resume_text = df.loc[0, resume_column]

# Predefined job description text for matching
job_description_text = """
We are looking for a software engineer with experience in Python, machine learning, and natural language processing. 
The ideal candidate should have a strong understanding of data structures, algorithms, and software development principles.
"""

ats_score = calculate_ats_score(resume_text, job_description_text)
print(f"ATS Score: {ats_score:.2f}%")
print(f"Dataset saved to {csv_file}")
