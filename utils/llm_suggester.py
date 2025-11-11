import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GeminiSuggester:
    def __init__(self):
        """Initialize Gemini AI model with fallback options"""
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # Configure Gemini API
        genai.configure(api_key=api_key)
        
        # Try to initialize model with fallback options
        model_names = [
            'gemini-2.5-flash',           # Primary choice - stable and fast
            'gemini-flash-latest',        # Fallback 1 - always latest
            'gemini-2.0-flash',           # Fallback 2 - older stable version
        ]
        
        self.model = None
        for model_name in model_names:
            try:
                self.model = genai.GenerativeModel(model_name)
                print(f"✅ Successfully loaded model: {model_name}")
                break
            except Exception as e:
                print(f"⚠️ Could not load {model_name}: {e}")
                continue
        
        if not self.model:
            raise ValueError("Could not initialize any Gemini model. Please check your API key.")
    
    def generate_suggestions(self, similarity_score, skill_match_percentage, 
                           matched_skills, missing_skills, extra_skills):
        """
        Generate personalized resume improvement suggestions using Gemini AI
        """
        # Create detailed prompt
        prompt = f"""
You are an expert career coach and resume consultant with 15+ years of experience helping candidates optimize their resumes for job applications.

**Candidate Analysis:**
- Semantic Match Score: {similarity_score}%
- Skills Match Score: {skill_match_percentage}%
- Matched Skills: {', '.join(matched_skills[:10]) if matched_skills else 'None'}
- Missing Skills: {', '.join(missing_skills[:10]) if missing_skills else 'None'}
- Additional Skills: {', '.join(extra_skills[:5]) if extra_skills else 'None'}

**Your Task:**
Provide a comprehensive, actionable resume improvement plan with the following sections:

1. **Overall Assessment** (2-3 sentences)
   - Evaluate the candidate's current position
   - Highlight key strengths

2. **Priority Actions** (3-5 bullet points)
   - Specific skills to add or emphasize
   - Resume sections to enhance
   - Keywords to include

3. **Skill Development Roadmap** (3-4 recommendations)
   - Which missing skills are most critical
   - Suggested learning resources or projects
   - Timeline for skill acquisition

4. **Resume Optimization Tips** (3-4 actionable tips)
   - How to better highlight existing skills
   - Formatting and keyword suggestions
   - ATS (Applicant Tracking System) optimization

Keep the tone professional, encouraging, and specific. Focus on actionable advice rather than generic suggestions.
"""
        
        try:
            # Generate response from Gemini with safety settings
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,  # Balanced creativity
                    top_p=0.9,
                    top_k=40,
                    max_output_tokens=2048,
                )
            )
            return response.text
        
        except Exception as e:
            return f"⚠️ Error generating suggestions: {str(e)}\n\nPlease try again or check your API quota."
    
    def generate_quick_tip(self, missing_skills):
        """
        Generate a quick tip focused on the most critical missing skill
        """
        if not missing_skills:
            return "✅ Great job! Your resume covers all required skills. Focus on showcasing your achievements with quantifiable results."
        
        top_skill = missing_skills[0] if missing_skills else "relevant technical skills"
        
        prompt = f"""
As a career coach, provide one specific, actionable tip (2-3 sentences) on how to quickly add "{top_skill}" to a resume, even if the candidate has limited experience with it. Focus on practical learning resources or portfolio projects.
"""
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.8,
                    max_output_tokens=256,
                )
            )
            return response.text
        except Exception as e:
            return f"💡 Quick Tip: Focus on learning {top_skill} through online courses (Coursera, Udemy) and build 2-3 small projects to demonstrate practical knowledge."
