import streamlit as st
from doc_utils import extract_text_from_pdf, extract_text_from_docx, extract_headings
from groq_llm import ask_groq

st.set_page_config(page_title="Doc Chatbot with LLaMA3", layout="centered")
st.title("📄🤖 Structured Document Q&A using LLaMA3 + Groq")

uploaded_file = st.file_uploader("Upload a PDF or DOCX file", type=["pdf", "docx"])

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        document_text = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        document_text = extract_text_from_docx(uploaded_file)
    else:
        st.error("Unsupported file type.")
        st.stop()

    st.success("✅ File uploaded and processed!")



    query = st.text_input("Ask a question based on the uploaded document:")
    if query:
        with st.spinner("Getting answer from LLaMA..."):
            chunks = [document_text[i:i+3000] for i in range(0, len(document_text), 3000)]
            answers = [ask_groq(query, chunk) for chunk in chunks[:3]]
            final_answer = "\n---\n".join(answers)
            st.markdown("### 📢 Answer")
            st.write(final_answer)
