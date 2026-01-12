import streamlit as st
import re

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("🤖 AI Resume Analyzer")
st.markdown("---")

# File upload
uploaded_file = st.file_uploader("📤 Upload your resume (TXT format)", type=['txt'])

if uploaded_file:
    # Read file
    text = uploaded_file.getvalue().decode("utf-8")
    
    # Simple analysis
    word_count = len(text.split())
    char_count = len(text)
    
    # Check for common skills
    common_skills = [
        'Python', 'Java', 'JavaScript', 'C++', 'SQL',
        'HTML', 'CSS', 'React', 'Angular', 'Vue',
        'Django', 'Flask', 'Node.js', 'AWS', 'Azure',
        'Docker', 'Git', 'Linux', 'MySQL', 'MongoDB'
    ]
    
    found_skills = []
    for skill in common_skills:
        if skill.lower() in text.lower():
            found_skills.append(skill)
    
    # Calculate scores
    skill_score = min(len(found_skills) * 10, 100)
    length_score = 100 if word_count > 300 else (word_count / 300) * 100
    
    # Check sections
    sections = ['experience', 'education', 'skills', 'project', 'contact']
    sections_found = sum(1 for section in sections if section in text.lower())
    section_score = (sections_found / len(sections)) * 100
    
    overall_score = (skill_score + length_score + section_score) / 3
    
    # Display results
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Overall Score", f"{overall_score:.0f}/100")
    
    with col2:
        st.metric("Word Count", word_count)
    
    with col3:
        st.metric("Skills Found", len(found_skills))
    
    with col4:
        st.metric("Sections", f"{sections_found}/5")
    
    # Skills section
    st.subheader("🛠 Detected Skills")
    if found_skills:
        st.write(", ".join(found_skills))
    else:
        st.warning("No skills detected. Add technical skills to your resume.")
    
    # Job matching section
    st.subheader("🎯 Job Description Matching")
    job_desc = st.text_area("Paste a job description to check match:", height=150)
    
    if job_desc:
        # Simple keyword matching
        resume_words = set(re.findall(r'\b[a-z]{4,}\b', text.lower()))
        job_words = set(re.findall(r'\b[a-z]{4,}\b', job_desc.lower()))
        
        # Remove very common words
        common_words = {'with', 'from', 'this', 'that', 'have', 'more', 'will', 'team'}
        resume_words = resume_words - common_words
        job_words = job_words - common_words
        
        if job_words:
            common_keywords = resume_words.intersection(job_words)
            match_percent = len(common_keywords) / len(job_words) * 100
            missing_keywords = list(job_words - resume_words)[:10]
            
            # Display match
            st.metric("Match Score", f"{match_percent:.1f}%")
            
            if missing_keywords:
                st.write("**Add these keywords:**")
                cols = st.columns(3)
                for i, keyword in enumerate(missing_keywords[:6]):
                    with cols[i % 3]:
                        st.info(f"• {keyword}")
    
    # Recommendations
    st.subheader("💡 Recommendations")
    recommendations = []
    
    if skill_score < 60:
        recommendations.append("Add more technical skills (aim for 10+ specific skills)")
    if length_score < 70:
        recommendations.append("Add more details to your experience and projects")
    if section_score < 80:
        recommendations.append("Ensure all main sections are present: Experience, Education, Skills, Projects, Contact")
    
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            st.write(f"{i}. {rec}")
    else:
        st.success("Your resume looks good! Consider adding quantifiable achievements.")
    
    # Preview
    with st.expander("📄 View Resume Text"):
        st.text(text[:2000] + "..." if len(text) > 2000 else text)

else:
    # Landing page
    st.info("""
    ### 📤 How to use:
    1. Upload your resume as a **.txt file**
    2. Get instant analysis and scores
    3. Paste a job description for matching (optional)
    4. Follow recommendations to improve
    
    ### 🎯 For best results:
    - Convert your resume to plain text (.txt)
    - Include specific technical skills
    - Add detailed experience descriptions
    - Use action verbs (Developed, Created, Managed)
    """)
    
    # Sample button
    if st.button("Try with Sample Resume"):
        sample_text = """John Doe - Software Engineer
Email: john@email.com | Phone: 123-456-7890

SKILLS
Programming: Python, Java, JavaScript, SQL
Web: Django, React, HTML, CSS
Tools: Git, Docker, AWS, Linux

EDUCATION
B.Sc. Computer Science - University ABC (2020-2024)
GPA: 3.8/4.0

EXPERIENCE
Software Development Intern - TechCorp (Summer 2023)
- Developed REST APIs using Django
- Built user authentication system
- Improved application performance by 40%

PROJECTS
AI Resume Analyzer - Python, Streamlit
- Created web application for resume analysis
- Implemented job matching algorithm

E-commerce Platform - Django, React
- Full-stack development of online store
- Integrated payment processing"""
        
        # Create a file-like object
        import io
        sample_file = io.BytesIO(sample_text.encode())
        sample_file.name = "sample_resume.txt"
        
        # Rerun with sample
        st.session_state['sample_file'] = sample_file
        st.rerun()

st.markdown("---")
st.caption("Note: For PDF/DOCX support, please convert to TXT format first.")