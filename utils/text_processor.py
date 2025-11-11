import pymupdf
import re
import string
import nltk
from nltk.corpus import stopwords
from bs4 import BeautifulSoup

# Download NLTK stopwords (run once)
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

def extract_text_from_pdf(file):
    """Extract text from PDF file using PyMuPDF"""
    try:
        # Read the uploaded file bytes
        pdf_bytes = file.read()
        
        # Open PDF from bytes
        doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
        
        # Extract text from all pages
        text = ""
        for page in doc:
            text += page.get_text()
        
        doc.close()
        return text
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"

def extract_text_from_txt(file):
    """Extract text from TXT file"""
    try:
        # Read text file
        text = file.read().decode('utf-8')
        return text
    except Exception as e:
        return f"Error reading TXT: {str(e)}"

def clean_text(text):
    """
    Clean and preprocess text for NLP analysis
    - Convert to lowercase
    - Remove special characters and numbers
    - Remove extra whitespaces
    - Remove stopwords
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove HTML tags if any
    text = BeautifulSoup(text, "html.parser").get_text()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Remove extra whitespaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = text.split()
    filtered_words = [word for word in words if word not in stop_words]
    
    # Join words back
    cleaned_text = ' '.join(filtered_words)
    
    return cleaned_text
