import sqlite3
import pandas as pd
from datetime import datetime
import json

class AnalysisDatabase:
    def __init__(self, db_name='resume_analysis.db'):
        """Initialize SQLite database connection"""
        self.db_name = db_name
        self.create_tables()
    
    def create_tables(self):
        """Create tables if they don't exist"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Create analysis history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analysis_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                resume_filename TEXT,
                jd_filename TEXT,
                semantic_score REAL,
                skill_match_score REAL,
                total_matched_skills INTEGER,
                total_missing_skills INTEGER,
                total_extra_skills INTEGER,
                matched_skills TEXT,
                missing_skills TEXT,
                extra_skills TEXT,
                match_category TEXT,
                resume_word_count INTEGER,
                jd_word_count INTEGER
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_analysis(self, resume_filename, jd_filename, similarity_score, 
                     skill_analysis, match_category, resume_word_count, jd_word_count):
        """Save analysis results to database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Convert skill lists to JSON strings
        matched_skills_json = json.dumps(skill_analysis['matched_skills'])
        missing_skills_json = json.dumps(skill_analysis['missing_skills'])
        extra_skills_json = json.dumps(skill_analysis['extra_skills'])
        
        cursor.execute('''
            INSERT INTO analysis_history 
            (resume_filename, jd_filename, semantic_score, skill_match_score,
             total_matched_skills, total_missing_skills, total_extra_skills,
             matched_skills, missing_skills, extra_skills, match_category,
             resume_word_count, jd_word_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            resume_filename,
            jd_filename,
            similarity_score,
            skill_analysis['skill_match_percentage'],
            skill_analysis['total_matched'],
            len(skill_analysis['missing_skills']),
            len(skill_analysis['extra_skills']),
            matched_skills_json,
            missing_skills_json,
            extra_skills_json,
            match_category,
            resume_word_count,
            jd_word_count
        ))
        
        conn.commit()
        conn.close()
        
        return cursor.lastrowid
    
    def get_all_analyses(self):
        """Retrieve all analysis records"""
        conn = sqlite3.connect(self.db_name)
        df = pd.read_sql_query('''
            SELECT id, timestamp, resume_filename, jd_filename, 
                   semantic_score, skill_match_score, total_matched_skills,
                   total_missing_skills, match_category
            FROM analysis_history
            ORDER BY timestamp DESC
        ''', conn)
        conn.close()
        return df
    
    def get_analysis_by_id(self, analysis_id):
        """Get detailed analysis by ID"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM analysis_history WHERE id = ?
        ''', (analysis_id,))
        
        result = cursor.fetchone()
        conn.close()
        return result
    
    def get_statistics(self):
        """Get overall statistics from all analyses"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        stats = {
            'total_analyses': 0,
            'avg_semantic_score': 0,
            'avg_skill_match': 0,
            'best_match': {},
            'recent_analyses': []
        }
        
        # Total analyses
        cursor.execute('SELECT COUNT(*) FROM analysis_history')
        stats['total_analyses'] = cursor.fetchone()[0]
        
        # Average scores
        cursor.execute('''
            SELECT AVG(semantic_score), AVG(skill_match_score)
            FROM analysis_history
        ''')
        avg_scores = cursor.fetchone()
        stats['avg_semantic_score'] = round(avg_scores[0] or 0, 2)
        stats['avg_skill_match'] = round(avg_scores[1] or 0, 2)
        
        # Best match
        cursor.execute('''
            SELECT resume_filename, jd_filename, semantic_score, timestamp
            FROM analysis_history
            ORDER BY semantic_score DESC
            LIMIT 1
        ''')
        best = cursor.fetchone()
        if best:
            stats['best_match'] = {
                'resume': best[0],
                'job': best[1],
                'score': best[2],
                'date': best[3]
            }
        
        conn.close()
        return stats
    
    def export_to_csv(self, filename='analysis_export.csv'):
        """Export all analyses to CSV"""
        df = self.get_all_analyses()
        df.to_csv(filename, index=False)
        return filename
    
    def delete_analysis(self, analysis_id):
        """Delete an analysis record"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM analysis_history WHERE id = ?', (analysis_id,))
        conn.commit()
        conn.close()
