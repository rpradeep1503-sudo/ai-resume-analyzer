import streamlit as st
import pandas as pd
import numpy as np
import re

# Page config
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 2rem;
    }
    .score-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        padding: 20px;
        color: white;
        text-align: center;
        margin: 10px;
    }
</style>
""", unsafe_allow_html=True)

class SimpleResumeAnalyzer:
    def __init__(self):
        self.skills_db = {
            'Programming': ['Python', 'Java', 'C++', 'JavaScript', 'SQL'],
            'Web': ['HTML', 'CSS', 'React', 'Angular', 'Vue', 'Django', 'Flask'],
            'Data': ['Pandas', 'NumPy', 'ML', 'TensorFlow', 'PyTorch'],
            'Cloud': ['AWS', 'Azure', 'Docker', 'Kubernetes'],
            'Tools': ['Git', 'Linux', 'JIRA', 'Jenkins']
        }
    
    def extract_text(self, file):
        """Extract text from uploaded file"""
        if file.name.endswith('.txt'):
            return file.getvalue().decode("utf-8")
        else:
            # For PDF/DOCX, return simple text (actual parsing removed for simplicity)
            return "Upload a TXT file for best results. PDF/DOCX support coming soon."
    
    def analyze_resume(self, text):
        """Simple resume analysis"""
        text_lower = text.lower()
        
        # Extract skills
        found_skills = []
        for category, skills in self.skills_db.items():
            for skill in skills:
                if skill.lower() in text_lower:
                    found_skills.append({
                        'skill': skill,
                        'category': category
                    })
        
        # Calculate scores
        skills_score = min(len(found_skills) * 10, 100)
        length_score = min(len(text.split()) / 5, 100)
        completeness_score = 70  # Base score
        
        # Check for key sections
        sections = ['experience', 'education', 'skills', 'project']
        for section in sections:
            if section in text_lower:
                completeness_score += 5
        
        overall = (skills_score + length_score + completeness_score) / 3
        
        return {
            'skills': found_skills,
            'scores': {
                'Overall': round(overall, 1),
                'Skills': round(skills_score, 1),
                'Completeness': round(completeness_score, 1),
                'Length': round(length_score, 1)
            }
        }
    
    def match_job(self, resume_text, job_desc):
        """Simple job matching"""
        resume_words = set(re.findall(r'\b[a-z]{4,}\b', resume_text.lower()))
        job_words = set(re.findall(r'\b[a-z]{4,}\b', job_desc.lower()))
        
        if not job_words:
            return {'match': 50, 'missing': []}
        
        common = resume_words.intersection(job_words)
        match_percent = len(common) / len(job_words) * 100
        missing = list(job_words - resume_words)[:10]
        
        return {
            'match': round(match_percent, 1),
            'missing': missing
        }

def main():
    st.markdown("<h1 class='main-header'>🤖 AI Resume Analyzer</h1>", unsafe_allow_html=True)
    
    analyzer = SimpleResumeAnalyzer()
    
    # Sidebar
    with st.sidebar:
        st.header("📤 Upload Resume")
        resume_file = st.file_uploader("Upload Resume (TXT recommended)", type=['txt', 'pdf', 'docx'])
        
        st.header("📝 Job Description")
        job_desc = st.text_area("Paste Job Description", height=150,
                               placeholder="Paste job description here...")
        
        # Sample data
        if st.button("Load Sample Data"):
            st.session_state['sample_resume'] = """John Doe - Software Engineer
Email: john@email.com | Phone: 123-456-7890

SKILLS
Programming: Python, Java, JavaScript
Web: Django, React, HTML, CSS
Tools: Git, Docker, AWS, Linux

EDUCATION
B.Sc. Computer Science - University ABC (2020-2024)

EXPERIENCE
Software Intern at TechCorp (2023)
- Built web applications with Django
- Created REST APIs
- Worked with AWS services

PROJECTS
E-commerce Website with Django
Machine Learning model for predictions"""
            
            st.session_state['sample_job'] = """Software Engineer with Python experience
Requirements:
- Python programming
- Django or Flask framework
- REST API development
- SQL databases
- Git version control
- AWS cloud services

Nice to have:
- React.js
- Docker
- Machine Learning"""
    
    # Get sample data if available
    sample_resume = st.session_state.get('sample_resume', '')
    sample_job = st.session_state.get('sample_job', '')
    
    if sample_resume and not resume_file:
        resume_text = sample_resume
        use_sample = True
    elif resume_file:
        resume_text = analyzer.extract_text(resume_file)
        use_sample = False
    else:
        resume_text = ""
        use_sample = False
    
    if sample_job and not job_desc:
        job_desc = sample_job
    
    # Main content
    if resume_text:
        # Analyze resume
        analysis = analyzer.analyze_resume(resume_text)
        
        if use_sample:
            st.info("📊 Analyzing Sample Resume")
        
        # Display scores
        st.subheader("📈 Resume Score")
        cols = st.columns(4)
        
        for idx, (metric, score) in enumerate(analysis['scores'].items()):
            with cols[idx]:
                st.markdown(f"""
                <div class='score-card'>
                    <h3>{metric}</h3>
                    <h1>{score}/100</h1>
                </div>
                """, unsafe_allow_html=True)
        
        # Skills section
        st.subheader("🛠 Detected Skills")
        if analysis['skills']:
            # Group by category
            skills_df = pd.DataFrame(analysis['skills'])
            categories = skills_df['category'].unique()
            
            for category in categories:
                cat_skills = skills_df[skills_df['category'] == category]['skill'].tolist()
                st.write(f"**{category}:** {', '.join(cat_skills)}")
        else:
            st.warning("No skills detected. Add technical skills to your resume.")
        
        # Job matching
        if job_desc:
            st.subheader("🎯 Job Match Analysis")
            match_result = analyzer.match_job(resume_text, job_desc)
            
            # Match gauge
            match_color = "🟢" if match_result['match'] > 70 else "🟡" if match_result['match'] > 50 else "🔴"
            st.metric(label="Match Score", value=f"{match_result['match']}%", delta=match_color)
            
            # Missing keywords
            if match_result['missing']:
                st.write("**Keywords to add:**")
                cols = st.columns(3)
                for idx, keyword in enumerate(match_result['missing'][:9]):
                    with cols[idx % 3]:
                        st.info(f"🔸 {keyword}")
        
        # Recommendations
        st.subheader("💡 Recommendations")
        recs = []
        
        if analysis['scores']['Skills'] < 60:
            recs.append("Add more technical skills specific to your target role")
        if analysis['scores']['Length'] < 50:
            recs.append("Add more details about your experience and projects")
        if analysis['scores']['Completeness'] < 70:
            recs.append("Ensure all sections (Experience, Education, Skills, Projects) are present")
        
        if recs:
            for i, rec in enumerate(recs, 1):
                st.write(f"{i}. {rec}")
        else:
            st.success("Your resume looks good! Consider adding quantifiable achievements.")
        
        # Raw text (collapsible)
        with st.expander("View Resume Text"):
            st.text(resume_text[:2000] + "..." if len(resume_text) > 2000 else resume_text)
    
    else:
        # Landing page
        st.write("""
        ## Welcome to AI Resume Analyzer! 🤖
        
        This tool helps you analyze and improve your resume:
        
        **Features:**
        - 📊 **Instant Resume Scoring** - Get scores on key metrics
        - 🛠 **Skill Detection** - Identify technical skills automatically
        - 🎯 **Job Matching** - See how well your resume matches job descriptions
        - 💡 **Smart Recommendations** - Get personalized improvement tips
        
        **How to use:**
        1. Upload your resume (TXT format works best)
        2. Paste a job description (optional)
        3. Get instant analysis and improvement tips
        
        **For best results:**
        - Use plain text (.txt) format
        - Include technical skills explicitly
        - Add detailed experience descriptions
        - Include projects and achievements
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            st.info("""
            **Quick Start:**
            Click "Load Sample Data" in the sidebar to see a demo analysis with sample resume and job description.
            """)
        
        with col2:
            st.success("""
            **Tips for better scores:**
            - Include 10+ technical skills
            - Add quantifiable achievements
            - Use action verbs (developed, created, improved)
            - Keep it concise but complete
            """)

if __name__ == "__main__":
    main()