from utils.skills_database import ALL_SKILLS, SKILLS_DATABASE
import re

class SkillExtractor:
    def __init__(self):
        self.all_skills = ALL_SKILLS
        self.skills_by_category = SKILLS_DATABASE
    
    def extract_skills(self, text):
        """
        Extract skills from text using pattern matching
        Returns set of found skills
        """
        text_lower = text.lower()
        found_skills = set()
        
        for skill in self.all_skills:
            # Use word boundary regex for accurate matching
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.add(skill)
        
        return found_skills
    
    def categorize_skills(self, skills):
        """
        Categorize extracted skills by domain
        """
        categorized = {}
        
        for category, skill_list in self.skills_by_category.items():
            category_skills = [skill for skill in skills if skill in skill_list]
            if category_skills:
                categorized[category] = sorted(category_skills)
        
        return categorized
    
    def compare_skills(self, resume_text, jd_text):
        """
        Compare skills between resume and job description
        Returns matched, missing, and extra skills
        """
        # Extract skills from both texts
        resume_skills = self.extract_skills(resume_text)
        jd_skills = self.extract_skills(jd_text)
        
        # Calculate skill gaps
        matched_skills = resume_skills.intersection(jd_skills)
        missing_skills = jd_skills - resume_skills
        extra_skills = resume_skills - jd_skills
        
        # Calculate match percentage
        if len(jd_skills) > 0:
            skill_match_percentage = round((len(matched_skills) / len(jd_skills)) * 100, 2)
        else:
            skill_match_percentage = 0.0
        
        return {
            "matched_skills": sorted(list(matched_skills)),
            "missing_skills": sorted(list(missing_skills)),
            "extra_skills": sorted(list(extra_skills)),
            "skill_match_percentage": skill_match_percentage,
            "total_jd_skills": len(jd_skills),
            "total_resume_skills": len(resume_skills),
            "total_matched": len(matched_skills)
        }
