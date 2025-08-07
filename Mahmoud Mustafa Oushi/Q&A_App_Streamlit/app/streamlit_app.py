import streamlit as st
from app.document_qa import DocumentQA
from app.config import Config

def main():
    st.title("Document QA Prototype")

    uploaded_file = st.file_uploader("Upload document", type=[ext.strip('.') for ext in Config.SUPPORTED_FILE_TYPES])
    model = st.selectbox("Select Model", ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768'], index=0)
    question = st.text_area("Enter your question here")

    if st.button("Ask"):
        if not uploaded_file:
            st.warning("Please upload a document first.")
            return
        if not question.strip():
            st.warning("Please enter a question.")
            return

        if "qa" not in st.session_state or st.session_state.get("last_file") != uploaded_file.name:
            qa = DocumentQA()
            content = uploaded_file.read()
            qa.load_file(content, uploaded_file.name)
            st.session_state.qa = qa
            st.session_state.last_file = uploaded_file.name
        else:
            qa = st.session_state.qa

        with st.spinner("Generating answer..."):
            answer = qa.ask(question, model)
            st.markdown(f"**Question:** {question}")
            st.markdown(f"**Answer:** {answer}")

if __name__ == "__main__":
    main()
