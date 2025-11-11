import streamlit as st
from utils.text_processor import extract_text_from_pdf, extract_text_from_txt, clean_text
from utils.feature_extractor import ResumeJobMatcher
from utils.skill_extractor import SkillExtractor
from utils.llm_suggester import GeminiSuggester
from utils.visualizations import (
    create_gauge_chart, 
    create_skill_comparison_chart,
    create_category_breakdown_chart
)
from utils.database import AnalysisDatabase
import plotly.express as px
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI Resume & Job Fit Analyzer",
    page_icon="🧩",
    layout="wide"
)

# Initialize models and database
@st.cache_resource
def load_models():
    matcher = ResumeJobMatcher()
    skill_extractor = SkillExtractor()
    try:
        llm_suggester = GeminiSuggester()
    except ValueError as e:
        st.error(f"⚠️ {str(e)}")
        llm_suggester = None
    return matcher, skill_extractor, llm_suggester

matcher, skill_extractor, llm_suggester = load_models()

# Initialize database
db = AnalysisDatabase()

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1F77B4;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar for navigation
with st.sidebar:
    st.title("📊 Navigation")
    page = st.radio(
        "Choose a section:",
        ["🔍 New Analysis", "📜 History", "📈 Statistics"]
    )
    
    st.markdown("---")
    st.markdown("### About")
    st.info("AI-powered resume analyzer using Sentence-BERT and Gemini AI")

# Main content based on page selection
if page == "🔍 New Analysis":
    # App title
    st.markdown('<p class="main-header">🧩 AI Resume & Job Fit Analyzer</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Upload your resume and job description to get AI-powered insights</p>', unsafe_allow_html=True)

    # Create two columns for side-by-side upload
    col1, col2 = st.columns(2)

    # Column 1: Resume Upload
    with col1:
        st.subheader("📄 Upload Resume")
        resume_file = st.file_uploader(
            "Choose your resume (PDF or TXT)", 
            type=["pdf", "txt"],
            key="resume"
        )
        
        if resume_file is not None:
            st.success(f"✅ Resume uploaded: {resume_file.name}")

    # Column 2: Job Description Upload
    with col2:
        st.subheader("💼 Upload Job Description")
        jd_file = st.file_uploader(
            "Choose job description (PDF or TXT)", 
            type=["pdf", "txt"],
            key="jd"
        )
        
        if jd_file is not None:
            st.success(f"✅ Job Description uploaded: {jd_file.name}")

    # Analyze button
    if resume_file and jd_file:
        if st.button("🔍 Analyze Job Fit", type="primary", use_container_width=True):
            with st.spinner("🔄 Processing documents and generating AI insights..."):
                
                # Extract Resume Text
                if resume_file.type == "application/pdf":
                    resume_text = extract_text_from_pdf(resume_file)
                else:
                    resume_text = extract_text_from_txt(resume_file)
                
                # Extract Job Description Text
                if jd_file.type == "application/pdf":
                    jd_text = extract_text_from_pdf(jd_file)
                else:
                    jd_text = extract_text_from_txt(jd_file)
                
                # Clean both texts
                resume_cleaned = clean_text(resume_text)
                jd_cleaned = clean_text(jd_text)
                
                # Calculate metrics
                resume_word_count = len(resume_cleaned.split())
                jd_word_count = len(jd_cleaned.split())
                
                # Calculate semantic similarity score
                similarity_score = matcher.calculate_similarity(resume_cleaned, jd_cleaned)
                match_category, status_type = matcher.get_match_category(similarity_score)
                
                # Extract and compare skills
                skill_analysis = skill_extractor.compare_skills(resume_text, jd_text)
                
                # Save to database
                analysis_id = db.save_analysis(
                    resume_file.name,
                    jd_file.name,
                    similarity_score,
                    skill_analysis,
                    match_category,
                    resume_word_count,
                    jd_word_count
                )
                
                st.success(f"✅ Analysis completed and saved! (ID: {analysis_id})")
                
                # Display Gauge Charts
                st.markdown("---")
                st.subheader("📊 Match Score Visualization")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    gauge1 = create_gauge_chart(similarity_score, "Semantic Match Score")
                    st.plotly_chart(gauge1, use_container_width=True)
                
                with col2:
                    gauge2 = create_gauge_chart(skill_analysis['skill_match_percentage'], "Skills Match Score")
                    st.plotly_chart(gauge2, use_container_width=True)
                
                # Display Key Metrics
                st.markdown("---")
                st.subheader("📈 Key Performance Indicators")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        label="Overall Match",
                        value=f"{similarity_score}%",
                        delta=match_category
                    )
                
                with col2:
                    st.metric(
                        label="Matched Skills",
                        value=skill_analysis['total_matched'],
                        delta=f"{skill_analysis['skill_match_percentage']}%"
                    )
                
                with col3:
                    st.metric(
                        label="Missing Skills",
                        value=len(skill_analysis['missing_skills']),
                        delta="Needs work" if len(skill_analysis['missing_skills']) > 0 else "Perfect",
                        delta_color="inverse"
                    )
                
                with col4:
                    st.metric(
                        label="Bonus Skills",
                        value=len(skill_analysis['extra_skills']),
                        delta="Added value"
                    )
                
                # Skill Comparison Chart
                st.markdown("---")
                skill_comparison = create_skill_comparison_chart(
                    skill_analysis['total_matched'],
                    len(skill_analysis['missing_skills']),
                    len(skill_analysis['extra_skills'])
                )
                st.plotly_chart(skill_comparison, use_container_width=True)
                
                # AI-Powered Suggestions
                if llm_suggester:
                    st.markdown("---")
                    st.subheader("🤖 AI-Powered Career Coaching")
                    
                    with st.spinner("🧠 Gemini AI is analyzing your profile..."):
                        suggestions = llm_suggester.generate_suggestions(
                            similarity_score,
                            skill_analysis['skill_match_percentage'],
                            skill_analysis['matched_skills'],
                            skill_analysis['missing_skills'],
                            skill_analysis['extra_skills']
                        )
                    
                    st.markdown(suggestions)
                    
                    # Quick Tip
                    if skill_analysis['missing_skills']:
                        with st.expander("💡 Priority Action Item", expanded=True):
                            quick_tip = llm_suggester.generate_quick_tip(skill_analysis['missing_skills'])
                            st.info(quick_tip)
                
                # Detailed Skill Analysis (condensed for space)
                st.markdown("---")
                st.subheader("🎯 Detailed Skill Breakdown")
                
                tab1, tab2, tab3 = st.tabs(["✅ Matched", "❌ Missing", "➕ Bonus"])
                
                with tab1:
                    if skill_analysis['matched_skills']:
                        st.success(f"**{len(skill_analysis['matched_skills'])} matched skills**")
                        st.write(", ".join(skill_analysis['matched_skills'][:20]))
                
                with tab2:
                    if skill_analysis['missing_skills']:
                        st.error(f"**{len(skill_analysis['missing_skills'])} missing skills**")
                        st.write(", ".join(skill_analysis['missing_skills'][:20]))
                
                with tab3:
                    if skill_analysis['extra_skills']:
                        st.info(f"**{len(skill_analysis['extra_skills'])} bonus skills**")
                        st.write(", ".join(skill_analysis['extra_skills'][:20]))

elif page == "📜 History":
    st.title("📜 Analysis History")
    
    # Get all analyses
    history_df = db.get_all_analyses()
    
    if not history_df.empty:
        st.info(f"📊 Total analyses recorded: **{len(history_df)}**")
        
        # Display history table
        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "timestamp": st.column_config.DatetimeColumn("Date", format="DD/MM/YYYY HH:mm"),
                "semantic_score": st.column_config.ProgressColumn("Semantic %", format="%.1f%%", min_value=0, max_value=100),
                "skill_match_score": st.column_config.ProgressColumn("Skills %", format="%.1f%%", min_value=0, max_value=100),
            }
        )
        
        # Export button
        if st.button("📥 Export to CSV"):
            filename = db.export_to_csv()
            st.success(f"✅ Exported to {filename}")
            with open(filename, 'rb') as f:
                st.download_button(
                    label="⬇️ Download CSV",
                    data=f,
                    file_name=filename,
                    mime='text/csv'
                )
    else:
        st.warning("No analysis history yet. Complete your first analysis to see data here!")

elif page == "📈 Statistics":
    st.title("📈 Analytics & Statistics")
    
    stats = db.get_statistics()
    
    if stats['total_analyses'] > 0:
        # Overview metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Analyses", stats['total_analyses'])
        
        with col2:
            st.metric("Avg Semantic Score", f"{stats['avg_semantic_score']}%")
        
        with col3:
            st.metric("Avg Skill Match", f"{stats['avg_skill_match']}%")
        
        # Best match
        if stats['best_match']:
            st.markdown("---")
            st.subheader("🏆 Best Match Record")
            st.success(f"""
            **Resume**: {stats['best_match']['resume']}  
            **Job**: {stats['best_match']['job']}  
            **Score**: {stats['best_match']['score']}%  
            **Date**: {stats['best_match']['date']}
            """)
        
        # Trend chart
        st.markdown("---")
        st.subheader("📊 Score Trends Over Time")
        
        history_df = db.get_all_analyses()
        
        fig = px.line(
            history_df,
            x='timestamp',
            y=['semantic_score', 'skill_match_score'],
            title='Match Scores Trend',
            labels={'value': 'Score (%)', 'timestamp': 'Date'},
        )
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.warning("No statistics available yet. Complete analyses to see trends!")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>🧩 <b>AI Resume & Job Fit Analyzer</b> | Powered by Sentence-BERT & Google Gemini AI</p>
        <p>Built with ❤️ using Streamlit</p>
    </div>
""", unsafe_allow_html=True)

