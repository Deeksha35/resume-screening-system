import os
import PyPDF2
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# Extract text from PDF
# -----------------------------
def extract_text_from_pdf(pdf_file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    for page in pdf_reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted

    return text.lower()

# -----------------------------
# Load resumes
# -----------------------------
def load_resumes(folder_path):
    resume_texts = []
    resume_names = []

    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            path = os.path.join(folder_path, file)

            with open(path, "rb") as f:
                text = extract_text_from_pdf(f)

                resume_texts.append(text)
                resume_names.append(file)

    return resume_texts, resume_names

# -----------------------------
# Skill extraction
# -----------------------------
skills_list = [
    "python", "java", "machine learning", "deep learning",
    "sql", "html", "css", "javascript", "nlp",
    "data analysis", "tensorflow", "pandas"
]

def extract_skills(text):
    found_skills = []

    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)

    return found_skills

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Resume Screening System")

st.title("📄 Resume Screening & Ranking System")
st.write("AI-based Resume Ranking using NLP")

job_description = st.text_area(
    "Paste Job Description Here"
)

if st.button("Analyze Resumes"):

    if job_description.strip() == "":
        st.warning("Please enter a job description.")
    else:

        resumes, names = load_resumes("resumes")

        documents = resumes + [job_description.lower()]

        # TF-IDF Vectorization
        tfidf = TfidfVectorizer(stop_words="english")

        tfidf_matrix = tfidf.fit_transform(documents)

        # Cosine Similarity
        similarity_scores = cosine_similarity(
            tfidf_matrix[-1],
            tfidf_matrix[:-1]
        )

        scores = similarity_scores[0]

        ranked_resumes = sorted(
            zip(names, resumes, scores),
            key=lambda x: x[2],
            reverse=True
        )

        st.subheader("📊 AI Resume Screening & Ranking System")

        for rank, (name, text, score) in enumerate(ranked_resumes, start=1):

            matched_skills = extract_skills(text)

            st.markdown(f"## #{rank} - {name}")

            st.progress(float(score))
            st.write(f"✅ Match Score: {round(score * 100, 2)}%")

            st.write("🛠️ Skills Found:")

            if matched_skills:
                st.write(", ".join(matched_skills))
            else:
                st.write("No major skills detected.")

            st.write("---")