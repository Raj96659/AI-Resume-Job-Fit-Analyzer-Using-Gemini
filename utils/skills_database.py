# Comprehensive skill database organized by category
SKILLS_DATABASE = {
    "programming_languages": [
        "python", "java", "javascript", "c++", "c#", "php", "ruby", "go", "golang",
        "swift", "kotlin", "typescript", "r", "matlab", "scala", "perl", "rust",
        "sql", "html", "css", "bash", "shell scripting"
    ],
    "frameworks_libraries": [
        "react", "angular", "vue", "nodejs", "django", "flask", "spring", "spring boot",
        "express", "fastapi", "tensorflow", "pytorch", "keras", "scikit-learn", "pandas",
        "numpy", "scipy", "matplotlib", "seaborn", "opencv", "nltk", "spacy", "transformers",
        "hugging face", "streamlit", "gradio", "bootstrap", "jquery", "redux"
    ],
    "databases": [
        "mysql", "postgresql", "mongodb", "redis", "elasticsearch", "cassandra",
        "oracle", "sql server", "dynamodb", "firebase", "sqlite", "mariadb"
    ],
    "cloud_devops": [
        "aws", "azure", "google cloud", "gcp", "docker", "kubernetes", "jenkins",
        "git", "github", "gitlab", "terraform", "ansible", "ci/cd", "devops"
    ],
    "data_science_ml": [
        "machine learning", "deep learning", "nlp", "natural language processing",
        "computer vision", "data analysis", "data visualization", "statistical analysis",
        "predictive modeling", "time series", "recommendation systems", "neural networks",
        "cnn", "rnn", "lstm", "transformers", "bert", "gpt", "llm"
    ],
    "soft_skills": [
        "communication", "leadership", "teamwork", "problem solving", "critical thinking",
        "project management", "agile", "scrum", "collaboration", "time management"
    ],
    "tools": [
        "tableau", "power bi", "excel", "jupyter", "vs code", "pycharm", "intellij",
        "postman", "jira", "confluence", "slack", "figma", "photoshop"
    ]
}

# Flatten all skills into a single set for matching
ALL_SKILLS = set()
for category, skills in SKILLS_DATABASE.items():
    ALL_SKILLS.update(skills)
