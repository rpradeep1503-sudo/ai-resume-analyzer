import streamlit as st
import re
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import time

# Page config with fancy theme
st.set_page_config(
    page_title="AI Resume Analyzer Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== CUSTOM CSS ==========
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Main container */
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Header with gradient */
    .gradient-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
        padding: 1rem;
    }
    
    /* Subheader */
    .gradient-subheader {
        background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.8rem;
        font-weight: 600;
        margin: 1rem 0;
    }
    
    /* Score cards with animations */
    .score-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        border-left: 5px solid;
        height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .score-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
    }
    
    /* Skill tags */
    .skill-tag {
        display: inline-block;
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        margin: 0.3rem;
        font-size: 0.9rem;
        font-weight: 500;
        box-shadow: 0 4px 15px rgba(79, 172, 254, 0.3);
        transition: all 0.3s ease;
    }
    
    .skill-tag:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(79, 172, 254, 0.4);
    }
    
    /* Progress bars */
    .progress-container {
        background: #f0f0f0;
        border-radius: 10px;
        height: 20px;
        margin: 1rem 0;
        overflow: hidden;
    }
    
    .progress-bar {
        height: 100%;
        border-radius: 10px;
        transition: width 1s ease-in-out;
    }
    
    /* Upload area styling */
    .upload-area {
        border: 3px dashed #667eea;
        border-radius: 15px;
        padding: 3rem;
        text-align: center;
        background: rgba(102, 126, 234, 0.05);
        transition: all 0.3s ease;
        margin: 1rem 0;
    }
    
    .upload-area:hover {
        background: rgba(102, 126, 234, 0.1);
        border-color: #764ba2;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.2rem;
    }
    
    .badge-success {
        background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%);
        color: white;
    }
    
    .badge-warning {
        background: linear-gradient(90deg, #fa709a 0%, #fee140 100%);
        color: white;
    }
    
    .badge-danger {
        background: linear-gradient(90deg, #ff6b6b 0%, #ee5a52 100%);
        color: white;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 10px 10px 0 0;
        padding: 1rem 2rem;
        font-weight: 600;
    }
    
    /* Custom metric cards */
    .metric-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        margin: 0.5rem;
        border-top: 4px solid;
    }
    
    /* Animation classes */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.8s ease-out;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
</style>
""", unsafe_allow_html=True)

# ========== SIDEBAR ==========
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 1rem;'>
        <h1 style='color: white; font-size: 2rem; margin-bottom: 0;'>🚀</h1>
        <h3 style='color: white; margin-top: 0;'>Resume Analyzer Pro</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # File upload with style
    st.markdown("<div class='upload-area'>", unsafe_allow_html=True)
    st.markdown("### 📤 Upload Resume")
    uploaded_file = st.file_uploader(
        "Drag & drop or click to browse",
        type=['txt', 'pdf'],
        label_visibility="collapsed"
    )
    st.markdown("<small>Supports: TXT, PDF</small>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Job description
    st.markdown("### 📝 Job Description")
    job_description = st.text_area(
        "Paste job description here",
        height=150,
        placeholder="Enter the job description for matching...",
        label_visibility="collapsed"
    )
    
    # Sample data
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📋 Sample Resume", use_container_width=True):
            st.session_state.sample_resume = """JOHN ALEXANDER DOE
Senior Software Engineer | 5+ Years Experience

CONTACT
Email: john.doe@techpro.com
Phone: (415) 555-0199
LinkedIn: linkedin.com/in/johndoe
GitHub: github.com/johndoe

TECHNICAL SKILLS
• Programming: Python, Java, JavaScript, SQL, Go
• Frontend: React, Vue.js, HTML5, CSS3
• Backend: Django, Flask, Node.js, FastAPI
• Cloud: AWS (EC2, S3, Lambda), Docker, Kubernetes
• Databases: PostgreSQL, MongoDB, Redis
• Tools: Git, Jenkins, JIRA, Docker, VS Code

EXPERIENCE
Senior Software Engineer | TechCorp (2021-Present)
• Led team of 5 developers building microservices
• Reduced API latency by 60% through optimization
• Implemented CI/CD pipeline saving 20 hours/week

Software Developer | InnovateInc (2019-2021)
• Built REST APIs serving 100K+ users
• Improved application performance by 40%
• Mentored 3 junior developers

EDUCATION
MS Computer Science | Stanford University
BS Software Engineering | UC Berkeley

PROJECTS
• AI Resume Analyzer: Python, Streamlit, spaCy
• E-commerce Platform: Django, React, PostgreSQL"""
    
    with col2:
        if st.button("🎯 Sample Job", use_container_width=True):
            st.session_state.sample_job = """Senior Full Stack Developer

Requirements:
- 5+ years experience with Python and JavaScript
- Strong expertise in React or Vue.js
- Experience with Django/Flask frameworks
- Knowledge of AWS cloud services
- Familiarity with Docker and Kubernetes
- SQL and NoSQL database experience
- REST API design and development
- Git version control
- Agile/Scrum methodology

Responsibilities:
- Design and develop scalable web applications
- Collaborate with cross-functional teams
- Write clean, maintainable code
- Implement testing and deployment pipelines
- Optimize application performance
- Mentor junior team members

Nice to have:
- Experience with microservices
- Machine learning knowledge
- GraphQL experience
- Open source contributions"""

# ========== MAIN CONTENT ==========
def main():
    # Header with gradient
    st.markdown("""
    <div class='fade-in'>
        <h1 class='gradient-header'>🤖 AI RESUME ANALYZER PRO</h1>
        <p style='text-align: center; color: #666; font-size: 1.2rem; margin-bottom: 2rem;'>
            Get instant feedback, ATS compatibility check, and job matching with AI-powered insights
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize analyzer
    analyzer = ResumeAnalyzer()
    
    # Get resume text
    resume_text = ""
    if uploaded_file:
        resume_text = analyzer.extract_text(uploaded_file)
    elif 'sample_resume' in st.session_state:
        resume_text = st.session_state.sample_resume
        st.success("✅ Using sample resume data")
    
    # Get job description
    job_desc = job_description
    if not job_desc and 'sample_job' in st.session_state:
        job_desc = st.session_state.sample_job
    
    if resume_text:
        # Analyze resume
        with st.spinner("🔍 Analyzing your resume with AI..."):
            time.sleep(1)  # Simulate processing
            analysis = analyzer.analyze_resume(resume_text)
            match_result = analyzer.match_job_description(resume_text, job_desc) if job_desc else None
        
        # ========== SCORE CARDS ==========
        st.markdown("<h2 class='gradient-subheader'>📊 Resume Analysis Dashboard</h2>", unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        scores = analysis['scores']
        with col1:
            display_score_card("Overall", scores['Overall'], "#667eea", "🏆")
        with col2:
            display_score_card("ATS Score", scores['ATS'], "#f093fb", "🤖")
        with col3:
            display_score_card("Skills", scores['Skills'], "#4facfe", "🛠️")
        with col4:
            display_score_card("Completeness", scores['Completeness'], "#43e97b", "✅")
        with col5:
            display_score_card("Readability", scores['Readability'], "#fa709a", "📖")
        
        # ========== TABS ==========
        tab1, tab2, tab3, tab4 = st.tabs(["🔍 Detailed Analysis", "🎯 Job Match", "💡 Recommendations", "📈 Visualizations"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🎯 Key Metrics")
                metrics = [
                    ("Word Count", len(resume_text.split()), "words"),
                    ("Page Length", f"{len(resume_text.split())//300}", "pages"),
                    ("Action Verbs", scores.get('Action_Verbs', 0), "verbs"),
                    ("Skills Found", len(analysis['skills']), "skills")
                ]
                
                for label, value, unit in metrics:
                    st.markdown(f"""
                    <div class='metric-card' style='border-top-color: #667eea;'>
                        <div style='font-size: 0.9rem; color: #666;'>{label}</div>
                        <div style='font-size: 2rem; font-weight: 800; color: #333;'>{value}</div>
                        <div style='font-size: 0.8rem; color: #999;'>{unit}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("### 🏆 Skill Categories")
                if analysis['skills']:
                    skills_df = pd.DataFrame(analysis['skills'])
                    if not skills_df.empty:
                        # Group by category
                        category_counts = skills_df['category'].value_counts().reset_index()
                        category_counts.columns = ['Category', 'Count']
                        
                        fig = px.pie(category_counts, values='Count', names='Category',
                                   color_discrete_sequence=px.colors.sequential.RdBu,
                                   hole=0.4)
                        fig.update_traces(textposition='inside', textinfo='percent+label')
                        fig.update_layout(showlegend=False, height=300)
                        st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            if match_result:
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    # Gauge chart for match score
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number+delta",
                        value=match_result['match_score'],
                        title={'text': "Job Match Score", 'font': {'size': 20}},
                        delta={'reference': 70, 'increasing': {'color': "green"}},
                        gauge={
                            'axis': {'range': [None, 100], 'tickwidth': 1},
                            'bar': {'color': "darkblue"},
                            'bgcolor': "white",
                            'borderwidth': 2,
                            'bordercolor': "gray",
                            'steps': [
                                {'range': [0, 50], 'color': 'lightcoral'},
                                {'range': [50, 75], 'color': 'lightyellow'},
                                {'range': [75, 100], 'color': 'lightgreen'}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': 70
                            }
                        }
                    ))
                    fig.update_layout(height=300, margin=dict(t=50, b=10))
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.markdown("### 📋 Missing Keywords")
                    if match_result['missing_keywords']:
                        st.markdown("<div style='background: rgba(255, 107, 107, 0.1); padding: 1.5rem; border-radius: 10px;'>", unsafe_allow_html=True)
                        cols = st.columns(4)
                        keywords = match_result['missing_keywords'][:12]
                        for idx, keyword in enumerate(keywords):
                            with cols[idx % 4]:
                                st.markdown(f"<div class='skill-tag' style='background: linear-gradient(90deg, #ff6b6b 0%, #ee5a52 100%);'>{keyword}</div>", unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                        st.info("Add these keywords to improve your match score!")
                    else:
                        st.success("🎉 Excellent! Your resume contains all important keywords from the job description.")
        
        with tab3:
            st.markdown("### 💡 AI-Powered Recommendations")
            recommendations = analyzer.generate_recommendations(analysis)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🚨 Critical Issues")
                critical = [r for r in recommendations if 'critical' in r.lower() or scores['Overall'] < 50]
                if critical:
                    for rec in critical[:3]:
                        st.error(f"🔴 {rec}")
                else:
                    st.success("✅ No critical issues found!")
            
            with col2:
                st.markdown("#### 📈 Improvement Opportunities")
                improvements = [r for r in recommendations if r not in critical]
                if improvements:
                    for rec in improvements[:3]:
                        st.warning(f"🟡 {rec}")
                else:
                    st.info("🌟 Your resume is already well-optimized!")
            
            # Progress bars for each metric
            st.markdown("#### 📊 Improvement Progress")
            for metric, score in scores.items():
                if metric != 'Overall':
                    progress_color = "#43e97b" if score > 70 else "#fa709a" if score > 50 else "#ff6b6b"
                    st.markdown(f"""
                    <div style='margin: 1rem 0;'>
                        <div style='display: flex; justify-content: space-between; margin-bottom: 0.5rem;'>
                            <span><strong>{metric}</strong></span>
                            <span><strong>{score}/100</strong></span>
                        </div>
                        <div class='progress-container'>
                            <div class='progress-bar' style='width: {score}%; background: {progress_color};'></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        with tab4:
            # Radar chart
            categories = list(scores.keys())[:-1]
            fig = go.Figure(data=go.Scatterpolar(
                r=[scores[c] for c in categories],
                theta=categories,
                fill='toself',
                fillcolor='rgba(102, 126, 234, 0.3)',
                line=dict(color='#667eea', width=3),
                name='Your Resume'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100],
                        gridcolor='lightgray'
                    ),
                    bgcolor='rgba(255,255,255,0.8)'
                ),
                showlegend=True,
                height=500,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Skills word cloud simulation
            if analysis['skills']:
                st.markdown("### 🔥 Top Skills")
                skills_text = ' '.join([s['skill'] for s in analysis['skills'] for _ in range(s.get('frequency', 1))])
                skills_list = skills_text.split()
                
                cols = st.columns(6)
                top_skills = pd.Series(skills_list).value_counts().head(12)
                for idx, (skill, count) in enumerate(top_skills.items()):
                    size = 1 + (count / top_skills.max()) * 2
                    with cols[idx % 6]:
                        st.markdown(f"<div style='text-align: center; margin: 0.5rem;'>", unsafe_allow_html=True)
                        st.markdown(f"<div class='skill-tag' style='font-size: {size}rem;'>{skill}</div>", unsafe_allow_html=True)
                        st.markdown(f"<small style='color: #666;'>x{count}</small>", unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)
    
    else:
        # Landing page
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class='main-container fade-in'>
                <h2 class='gradient-subheader'>🚀 Get Started</h2>
                <div style='font-size: 1.1rem; color: #555; line-height: 1.6;'>
                    <p>1. <strong>Upload your resume</strong> in TXT or PDF format</p>
                    <p>2. <strong>Paste a job description</strong> for matching (optional)</p>
                    <p>3. <strong>Get instant AI analysis</strong> with scores and feedback</p>
                    <p>4. <strong>Follow recommendations</strong> to improve your resume</p>
                </div>
                
                <div style='margin-top: 2rem; padding: 1.5rem; background: linear-gradient(90deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); border-radius: 10px;'>
                    <h4>🎯 What You'll Get:</h4>
                    <p>✅ <strong>ATS Compatibility Score</strong></p>
                    <p>✅ <strong>Skill Gap Analysis</strong></p>
                    <p>✅ <strong>Job Match Percentage</strong></p>
                    <p>✅ <strong>AI-Powered Recommendations</strong></p>
                    <p>✅ <strong>Visual Analytics Dashboard</strong></p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class='main-container fade-in'>
                <h2 class='gradient-subheader'>💡 Pro Tips</h2>
                
                <div style='background: white; padding: 1rem; border-radius: 10px; margin: 1rem 0; border-left: 4px solid #4facfe;'>
                    <h4>📄 Format Your Resume</h4>
                    <p style='color: #666;'>Use plain text format for best results. Convert from PDF if needed.</p>
                </div>
                
                <div style='background: white; padding: 1rem; border-radius: 10px; margin: 1rem 0; border-left: 4px solid #43e97b;'>
                    <h4>🛠 Include Specific Skills</h4>
                    <p style='color: #666;'>List technical skills clearly: Python, React, AWS, Docker, etc.</p>
                </div>
                
                <div style='background: white; padding: 1rem; border-radius: 10px; margin: 1rem 0; border-left: 4px solid #fa709a;'>
                    <h4>📈 Use Action Verbs</h4>
                    <p style='color: #666;'>Start bullet points with: Developed, Created, Implemented, Improved</p>
                </div>
                
                <div style='background: white; padding: 1rem; border-radius: 10px; margin: 1rem 0; border-left: 4px solid #f093fb;'>
                    <h4>🎯 Quantify Achievements</h4>
                    <p style='color: #666;'>Use numbers: "Increased performance by 40%", "Reduced costs by $20K"</p>
                </div>
                
                <div class='pulse' style='text-align: center; margin-top: 2rem;'>
                    <button style='background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white; border: none; padding: 1rem 3rem; border-radius: 25px; font-size: 1.2rem; font-weight: bold; cursor: pointer;'>
                        👈 Start by Uploading Your Resume
                    </button>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ========== HELPER FUNCTIONS ==========
def display_score_card(title, score, color, icon):
    """Display a beautiful score card"""
    card_color = color
    score_color = "#333"
    
    if score > 80:
        badge = "<span class='badge badge-success'>Excellent</span>"
    elif score > 60:
        badge = "<span class='badge badge-warning'>Good</span>"
    else:
        badge = "<span class='badge badge-danger'>Needs Work</span>"
    
    st.markdown(f"""
    <div class='score-card fade-in' style='border-left-color: {card_color};'>
        <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>{icon}</div>
        <div style='font-size: 0.9rem; color: #666;'>{title}</div>
        <div style='font-size: 2rem; font-weight: 800; color: {score_color};'>{score}</div>
        <div>{badge}</div>
    </div>
    """, unsafe_allow_html=True)

class ResumeAnalyzer:
    def __init__(self):
        self.skills_db = {
            'Programming': ['Python', 'Java', 'JavaScript', 'C++', 'Go', 'Rust', 'SQL', 'TypeScript'],
            'Frontend': ['React', 'Vue.js', 'Angular', 'HTML5', 'CSS3', 'SASS', 'Next.js'],
            'Backend': ['Django', 'Flask', 'Node.js', 'FastAPI', 'Spring', 'Express.js'],
            'Cloud': ['AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Terraform', 'CI/CD'],
            'Databases': ['PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'Firebase', 'DynamoDB'],
            'Data Science': ['Pandas', 'NumPy', 'Scikit-learn', 'TensorFlow', 'PyTorch', 'ML'],
            'Tools': ['Git', 'JIRA', 'Jenkins', 'VS Code', 'Postman', 'Linux', 'Bash']
        }
    
    def extract_text(self, file):
        """Extract text from uploaded file"""
        if file.name.endswith('.txt'):
            return file.getvalue().decode("utf-8")
        else:
            # For PDF, return placeholder (add PyPDF2 in requirements.txt for real support)
            return "PDF parsing enabled in PRO version. Please upload TXT for now."
    
    def analyze_resume(self, text):
        """Comprehensive resume analysis"""
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
        skills_score = min(unique_skills * 8, 100)
        
        # Check sections
        sections = ['experience', 'education', 'skill', 'project', 'contact', 'summary']
        sections_found = sum(1 for section in sections if section in text_lower)
        completeness_score = (sections_found / len(sections)) * 100
        
        # Length score
        word_count = len(text.split())
        if word_count < 200:
            length_score = 40
        elif word_count < 400:
            length_score = 70
        else:
            length_score = 90
        
        # Readability (simple approximation)
        readability_score = 70 + min(word_count / 50, 30)
        
        # ATS score
        ats_score = 60
        if 'table' not in text_lower and 'header' not in text_lower:
            ats_score += 20
        if word_count > 300:
            ats_score += 20
        
        # Action verbs
        action_verbs = ['developed', 'created', 'built', 'implemented', 'managed', 
                       'improved', 'increased', 'reduced', 'led', 'designed']
        verb_count = sum(1 for verb in action_verbs if verb in text_lower)
        verb_score = min(verb_count * 10, 100)
        
        overall = (skills_score + completeness_score + ats_score + readability_score) / 4
        
        return {
            'skills': found_skills,
            'scores': {
                'Overall': round(overall, 1),
                'ATS': round(ats_score, 1),
                'Skills': round(skills_score, 1),
                'Completeness': round(completeness_score, 1),
                'Readability': round(readability_score, 1),
                'Action_Verbs': round(verb_score, 1)
            }
        }
    
    def match_job_description(self, resume_text, job_desc):
        """Match resume with job description"""
        if not job_desc.strip():
            return {'match_score': 0, 'missing_keywords': []}
        
        resume_words = set(re.findall(r'\b[a-z]{4,}\b', resume_text.lower()))
        job_words = set(re.findall(r'\b[a-z]{4,}\b', job_desc.lower()))
        
        # Remove common words
        common_words = {'with', 'from', 'this', 'that', 'have', 'more', 'will', 'team', 'work'}
        resume_words = resume_words - common_words
        job_words = job_words - common_words
        
        if not job_words:
            return {'match_score': 0, 'missing_keywords': []}
        
        common = resume_words.intersection(job_words)
        match_score = (len(common) / len(job_words)) * 100
        missing_keywords = list(job_words - resume_words)[:20]
        
        return {
            'match_score': round(match_score, 1),
            'missing_keywords': missing_keywords
        }
    
    def generate_recommendations(self, analysis):
        """Generate recommendations based on analysis"""
        scores = analysis['scores']
        skills = analysis['skills']
        
        recommendations = []
        
        if scores['Overall'] < 50:
            recommendations.append("CRITICAL: Major improvements needed. Consider professional resume review.")
        
        if scores['Skills'] < 60:
            recommendations.append("Add 10+ specific technical skills relevant to your target industry")
        
        if scores['Completeness'] < 70:
            recommendations.append("Ensure all key sections are present: Experience, Education, Skills, Projects")
        
        if scores['ATS'] < 70:
            recommendations.append("Optimize for ATS: Use standard fonts, avoid tables and headers")
        
        if scores['Action_Verbs'] < 50:
            recommendations.append("Start bullet points with action verbs: Developed, Created, Implemented, Improved")
        
        if len(skills) < 8:
            recommendations.append("Include more technical skills with specific technologies")
        
        if scores['Readability'] < 70:
            recommendations.append("Improve readability: Use clear sections and bullet points")
        
        return recommendations

# ========== RUN APP ==========
if __name__ == "__main__":
    main()