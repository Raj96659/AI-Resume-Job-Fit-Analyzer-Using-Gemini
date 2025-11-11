from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class ResumeJobMatcher:
    def __init__(self, model_name='sentence-transformers/all-MiniLM-L6-v2'):
        """
        Initialize the Sentence-BERT model
        all-MiniLM-L6-v2 creates 384-dimensional embeddings
        """
        self.model = SentenceTransformer(model_name)
    
    def generate_embeddings(self, text):
        """
        Generate embeddings for input text
        Returns a 384-dimensional vector
        """
        embedding = self.model.encode(text, convert_to_tensor=False)
        return embedding
    
    def calculate_similarity(self, resume_text, jd_text):
        """
        Calculate cosine similarity between resume and job description
        Returns similarity score as percentage (0-100%)
        """
        # Generate embeddings
        resume_embedding = self.generate_embeddings(resume_text)
        jd_embedding = self.generate_embeddings(jd_text)
        
        # Reshape for sklearn cosine_similarity
        resume_embedding = resume_embedding.reshape(1, -1)
        jd_embedding = jd_embedding.reshape(1, -1)
        
        # Calculate cosine similarity
        similarity = cosine_similarity(resume_embedding, jd_embedding)[0][0]
        
        # Convert to percentage
        similarity_percentage = round(similarity * 100, 2)
        
        return similarity_percentage
    
    def get_match_category(self, score):
        """
        Categorize match score into quality levels
        """
        if score >= 80:
            return "Excellent Match", "success"
        elif score >= 60:
            return "Moderate Match", "info"
        elif score >= 40:
            return "Partial Fit", "warning"
        else:
            return "Poor Fit", "error"
