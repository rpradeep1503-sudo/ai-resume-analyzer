import streamlit as st
import pandas as pd
import numpy as np
import re
import warnings
warnings.filterwarnings('ignore')

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

class ResumeAnalyzerNoSpaCy:
    def __init__(self):
        self.skills_db = self.load_skills_database()
        self.stop_words = set(['the', 'and', 'is', 'in', 'to', 'of', 'for', 'with', 'on', 'at'])
    
    def load_skills_database(self):
        """Load predefined skills database"""
        return {
            'Programming': ['Python', 'Java', 'C++', 'JavaScript', 'C#', 'Go', 'Rust', 'SQL'],
            'Web Development': ['HTML', 'CSS', 'React', 'Angular', 'Vue', 'Django', 'Flask', 'Node.js'],
            'Data Science': ['Pandas', 'NumPy', 'Scikit-learn', 'TensorFlow', 'PyTorch', 'ML', 'Deep Learning'],
            'Cloud': ['AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'CI/CD'],
            'Databases': ['MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Firebase'],
            'Tools': ['Git', 'Linux', 'JIRA', 'Jenkins', 'AWS Lambda']
        }
    
    def extract_text(self, file):
        """Extract text from uploaded file"""
        if file.name.endswith('.txt'):
            return file.getvalue().decode("utf-8")
        elif file.name.endswith('.pdf'):
            # Simple PDF text extraction (basic)
            try:
                import PyPDF2
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
            except:
                return "PDF parsing requires PyPDF2. Please upload TXT file."
        else:
            return "Upload TXT file for best results. Other formats coming soon."
    
    def analyze_resume(self, text):
        """Perform resume analysis without spaCy"""
        text_lower = text.lower()
        
        # Extract skills
        found_skills = []
        for category, skills in self.skills_db.items():
            for skill in skills:
                if skill.lower() in text_lower:
                    found_skills.append({
                        'skill': skill,
                        'category': category,
                        'frequency': text_lower.count(skill.lower())
                    })
        
        # Calculate scores
        unique_skills = len(set([s['skill'] for s in found_skills]))
        skills_score = min(unique_skills * 10, 100)
        
        # Check for sections
        sections_present = 0
        sections_to_check = ['experience', 'education', 'skill', 'project', 'contact']
        for section in sections_to_check:
            if section in text_lower:
                sections_present += 1
        
        completeness_score = (sections_present / len(sections_to_check)) * 100
        
        # Length score
        word_count = len(text.split())
        if word_count < 200:
            length_score = 30
        elif word_count < 400:
            length_score = 60
        else:
            length_score = 90
        
        # Action verbs score
        action_verbs = ['developed', 'created', 'built', 'implemented', 'managed', 
                       'improved', 'increased', 'reduced', 'led', 'designed']
        verb_count = sum(1 for verb in action_verbs if verb in text_lower)
        verb_score = min(verb_count * 10, 100)
        
        overall = np.mean([skills_score, completeness_score, length_score, verb_score])
        
        return {
            'skills': found_skills,
            'scores': {
                'Overall': round(overall, 1),
                'Skills': round(skills_score, 1),
                'Completeness': round(completeness_score, 1),
                'Length': round(length_score, 1),
                'Action Verbs': round(verb_score, 1)
            }
        }
    
    def match_job_description(self, resume_text, job_desc):
        """Simple job matching without sklearn"""
        if not job_desc.strip():
            return {'match_score': 0, 'missing_keywords': []}
        
        resume_words = set(re.findall(r'\b[a-z]{4,}\b', resume_text.lower()))
        job_words = set(re.findall(r'\b[a-z]{4,}\b', job_desc.lower()))
        
        # Remove common stop words
        common_words = resume_words.intersection(self.stop_words)
        resume_words = resume_words - common_words
        job_words = job_words - common_words
        
        if not job_words:
            return {'match_score': 0, 'missing_keywords': []}
        
        common = resume_words.intersection(job_words)
        match_score = (len(common) / len(job_words)) * 100 if job_words else 0
        missing_keywords = list(job_words - resume_words)[:15]
        
        return {
            'match_score': round(match_score, 1),
            'missing_keywords': missing_keywords
        }

def main():
    st.markdown("<h1 class='main-header'>🤖 AI Resume Analyzer</h1>", unsafe_allow_html=True)
    
    analyzer = ResumeAnalyzerNoSpaCy()
    
    # Sidebar
    with st.sidebar:
        st.header("📤 Upload Files")
        resume_file = st.file_uploader("Upload Resume (TXT/PDF)", type=['txt', 'pdf'])
        
        st.header("📝 Job Description")
        job_desc = st.text_area("Paste Job Description", height=150,
                               placeholder="Paste the job description here...")
        
        # Sample data
        if st.button("Load Sample Data"):
            sample_resume = """John Doe - Software Engineer
Email: john@email.com | Phone: 123-456-7890
LinkedIn: linkedin.com/in/johndoe

SKILLS
Programming: Python, Java, JavaScript, SQL
Web Development: Django, React, HTML, CSS
Databases: MySQL, MongoDB
Cloud & Tools: AWS, Docker, Git, Linux

EDUCATION
Bachelor of Computer Science
ABC University | 2020-2024 | GPA: 3.8/4.0

EXPERIENCE
Software Development Intern - TechCorp (Summer 2023)
- Developed REST APIs using Django REST Framework
- Built user authentication system
- Improved API response time by 40%
- Collaborated with frontend team on React components

PROJECTS
AI Resume Analyzer - Python, Streamlit, NLP
- Created web application for resume analysis
- Implemented job matching algorithm
- Deployed on cloud platform

E-commerce Platform - Django, React, PostgreSQL
- Full-stack development of online store
- Integrated payment gateway
- Implemented user reviews and ratings"""
            
            sample_job = """Software Engineer - Python Developer

Requirements:
- Strong Python programming skills
- Experience with Django or Flask web frameworks
- Knowledge of REST API development
- SQL database experience (MySQL, PostgreSQL)
- Version control with Git
- Cloud platform experience (AWS preferred)

Responsibilities:
- Develop and maintain web applications
- Design and implement REST APIs
- Write clean, efficient, and documented code
- Collaborate with cross-functional teams
- Participate in code reviews

Nice to have:
- React.js or other frontend framework
- Docker and containerization
- CI/CD pipelines
- Machine learning basics"""
            
            st.session_state['sample_resume'] = sample_resume
            st.session_state['sample_job'] = sample_job
            st.success("Sample data loaded! Click analyze.")
    
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
        if use_sample:
            st.info("📊 Analyzing Sample Resume")
        
        # Analyze resume
        analysis = analyzer.analyze_resume(resume_text)
        
        # Display scores
        st.subheader("📈 Resume Analysis")
        cols = st.columns(5)
        
        for idx, (metric, score) in enumerate(analysis['scores'].items()):
            with cols[idx]:
                color = "🟢" if score > 70 else "🟡" if score > 50 else "🔴"
                st.markdown(f"""
                <div class='score-card'>
                    <h4>{metric}</h4>
                    <h2>{score}</h2>
                    <small>{color}</small>
                </div>
                """, unsafe_allow_html=True)
        
        # Skills Analysis
        st.subheader("🛠 Skills Analysis")
        if analysis['skills']:
            # Create DataFrame for display
            skills_df = pd.DataFrame(analysis['skills'])
            
            # Group by category
            st.write("**Skills by Category:**")
            categories = skills_df['category'].unique()
            for category in categories:
                skills_in_category = skills_df[skills_df['category'] == category]['skill'].tolist()
                if skills_in_category:
                    st.write(f"**{category}:** {', '.join(skills_in_category)}")
            
            # Show table
            with st.expander("View Detailed Skills Table"):
                st.dataframe(skills_df[['skill', 'category', 'frequency']].sort_values('frequency', ascending=False))
        else:
            st.warning("No technical skills detected. Add specific skills like Python, Java, React, etc.")
        
        # Job Matching
        if job_desc:
            st.subheader("🎯 Job Match Analysis")
            match_result = analyzer.match_job_description(resume_text, job_desc)
            
            # Display match score
            col1, col2 = st.columns([1, 2])
            with col1:
                st.metric(label="Match Score", value=f"{match_result['match_score']}%")
            
            # Missing keywords
            if match_result['missing_keywords']:
                st.write("**Keywords to add to your resume:**")
                # Display as badges
                keywords_html = ""
                for keyword in match_result['missing_keywords'][:12]:
                    keywords_html += f'<span style="background-color: #e0f2fe; padding: 6px 12px; margin: 4px; border-radius: 20px; display: inline-block;">🔸 {keyword}</span> '
                st.markdown(keywords_html, unsafe_allow_html=True)
            else:
                st.success("Good job! Your resume contains most keywords from the job description.")
        
        # Recommendations
        st.subheader("💡 Improvement Recommendations")
        recommendations = []
        scores = analysis['scores']
        
        if scores['Skills'] < 60:
            recommendations.append("**Add more technical skills** - Include 10+ specific skills relevant to your target role")
        if scores['Completeness'] < 70:
            recommendations.append("**Complete all sections** - Ensure you have Experience, Education, Skills, Projects, and Contact")
        if scores['Action Verbs'] < 50:
            recommendations.append("**Use more action verbs** - Start bullet points with words like Developed, Created, Implemented, Improved")
        if scores['Length'] < 50:
            recommendations.append("**Add more details** - Describe your experience and projects with specific accomplishments")
        
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                st.markdown(f"{i}. {rec}")
        else:
            st.success("Your resume looks strong! Consider adding quantifiable achievements.")
        
        # Resume Preview
        with st.expander("📄 View Resume Text"):
            st.text_area("Resume Content", resume_text[:3000] + "..." if len(resume_text) > 3000 else resume_text, height=300)
    
    else:
        # Landing page
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("""
            ### 🚀 Get Started:
            1. **Upload your resume** (TXT format works best)
            2. **Paste a job description** (optional)
            3. **Get instant analysis** and improvement tips
            
            ### 📊 What you'll get:
            - Resume score breakdown
            - Skills analysis
            - Job matching score
            - Personalized recommendations
            """)
        
        with col2:
            st.success("""
            ### 💡 Tips for best results:
            - Use **plain text (.txt)** format
            - Include **specific technical skills**
            - Add **quantifiable achievements**
            - Use **action verbs** (Developed, Created, etc.)
            - Keep it **1-2 pages** in length
            
            ### 🎯 Perfect for:
            - Job seekers
            - Career changers
            - Students & graduates
            - Resume optimization
            """)
            
            if st.button("Try with Sample Data", type="primary"):
                st.session_state['use_sample'] = True
                st.rerun()

if __name__ == "__main__":
    main()