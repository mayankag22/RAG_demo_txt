import streamlit as st

from src.rag_pipeline.qa_chain import BankingPolicyQA

st.set_page_config(page_title="Banking Policy Q&A", layout="wide")
st.title("🏦 Banking Policy Q&A – Local RAG + MCP")

if st.button("Reset Page"):
    st.session_state.clear()
    st.rerun()

if "qa" not in st.session_state:
    st.session_state.qa = BankingPolicyQA()

question = st.text_input(
    "Ask a question about banking policies:",
    value="What's the maximum wire transfer amount without manager approval?",
)

if st.button("Ask") and question:
    with st.spinner("Thinking..."):
        result = st.session_state.qa.answer(question)

    st.subheader("Answer")
    st.write(result["answer"])

    st.subheader("Citations")
    for c in result["citations"]:
        st.write("-", c)

    st.subheader("MCP Sections")
    for sec in result["mcp_sections"]:
        st.markdown(
            f"**{sec['title']} – Section {sec['section_id']}**  \n{sec['text']}"
        )

    st.subheader("Compliance Check")
    st.json(result["compliance"])
