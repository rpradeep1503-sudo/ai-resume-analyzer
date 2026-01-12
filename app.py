import streamlit as st
import re

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("🤖 AI Resume Analyzer")
st.markdown("Upload your resume for instant analysis!")

# File upload
uploaded_file = st.file_uploader("Choose a TXT file", type=['txt'])

if uploaded_file:
    # Read file
    text = uploaded_file.getvalue().decode("utf-8")
    
    # Simple analysis
    word_count = len(text.split())
    
    # Check for skills (simple keyword matching)
    skills_keywords = [
        'python', 'java', 'javascript', 'sql', 'html', 'css',
        'react', 'angular', 'vue', 'django', 'flask', 'node',
        'aws', 'docker', 'git', 'linux', 'mysql', 'mongodb'
    ]
    
    found_skills = []
    for skill in skills_keywords:
        if skill in text.lower():
            found_skills.append(skill.title())
    
    # Calculate score
    skill_score = min(len(found_skills) * 10, 100)
    length_score = min(word_count / 3, 100)
    overall_score = (skill_score + length_score) / 2
    
    # Display results
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Overall Score", f"{overall_score:.0f}/100")
    with col2:
        st.metric("Word Count", word_count)
    with col3:
        st.metric("Skills Found", len(found_skills))
    
    # Show skills
    if found_skills:
        st.write("**Skills detected:**", ", ".join(found_skills))
    else:
        st.warning("No technical skills found. Add skills like Python, Java, SQL, etc.")
    
    # Job matching
    st.subheader("Job Description Matching")
    job_desc = st.text_area("Paste a job description:", height=100)
    
    if job_desc:
        # Simple matching
        resume_words = set(re.findall(r'\b[a-z]{4,}\b', text.lower()))
        job_words = set(re.findall(r'\b[a-z]{4,}\b', job_desc.lower()))
        
        if job_words:
            common = resume_words.intersection(job_words)
            match = len(common) / len(job_words) * 100
            st.metric("Match Score", f"{match:.1f}%")
            
            # Missing keywords
            missing = job_words - resume_words
            if missing:
                st.write("**Add these keywords:**", list(missing)[:8])
    
    # Recommendations
    st.subheader("Recommendations")
    if skill_score < 60:
        st.write("• Add more technical skills to your resume")
    if length_score < 70:
        st.write("• Add more details about your experience and projects")
    if word_count < 200:
        st.write("• Your resume seems short. Consider adding more content")
    
else:
    st.info("👈 Upload a .txt file to get started")

st.markdown("---")
st.caption("Convert your resume to .txt format for best results")