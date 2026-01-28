import streamlit as st
from src.rag_pipeline.qa_chain import BankingPolicyQA

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="Banking Policy Q&A",
    page_icon="🏦",
    layout="wide",
)

# ---------------------------
# Custom CSS for styling
# ---------------------------
st.markdown("""
<style>
/* Main title styling */
.big-title {
    font-size: 36px !important;
    font-weight: 700 !important;
    color: #1a4f8b !important;
    margin-bottom: 0.2em;
}

/* Subtle card-like container */
.response-box {
    padding: 1.2em;
    background-color: #f7f9fc;
    border-radius: 10px;
    border: 1px solid #e3e6eb;
    margin-top: 1em;
}

/* Citation styling */
.citation {
    font-size: 14px;
    color: #4a4a4a;
    margin-left: 0.5em;
}

/* MCP section box */
.mcp-box {
    padding: 1em;
    background-color: #fffdf5;
    border-left: 4px solid #f4c542;
    border-radius: 6px;
    margin-bottom: 1em;
}

/* Reset button styling */
div.stButton > button:first-child {
    background-color: #d9534f;
    color: white;
    border-radius: 6px;
    border: none;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Sidebar
# ---------------------------
st.sidebar.title("⚙️ Controls")

if st.sidebar.button("🔄 Reset Page"):
    st.session_state.clear()
    st.rerun()

st.sidebar.markdown("""
### How to use
1. Ask any banking policy question  
2. The system retrieves relevant policy sections  
3. MCP server validates compliance  
4. You get a clean, cited answer  

### Example questions
- *What's the maximum wire transfer amount without manager approval?*  
- *Who can approve transactions above $100,000?*  
""")

# ---------------------------
# Main Title
# ---------------------------
st.markdown('<div class="big-title">🏦 Banking Policy Q&A Assistant</div>', unsafe_allow_html=True)
st.write("A lightweight RAG + MCP demo running entirely on your laptop.")

# ---------------------------
# Initialize QA system
# ---------------------------
if "qa" not in st.session_state:
    st.session_state.qa = BankingPolicyQA()

# ---------------------------
# Layout: Two Columns
# ---------------------------
left, right = st.columns([1.2, 1])

with left:
    st.subheader("Ask a Question")
    question = st.text_input(
        "Enter your banking policy question:",
        value="What's the maximum wire transfer amount without manager approval?",
        placeholder="Type your question here...",
    )

    if st.button("Ask"):
        with st.spinner("Analyzing policies…"):
            result = st.session_state.qa.answer(question)

        st.markdown("### 🧠 Answer")
        st.markdown(f'<div class="response-box">{result["answer"]}</div>', unsafe_allow_html=True)

        st.markdown("### 📚 Citations")
        for c in result["citations"]:
            st.markdown(f"- <span class='citation'>{c}</span>", unsafe_allow_html=True)

with right:
    st.subheader("📄 MCP Policy Sections")
    for sec in st.session_state.qa.mcp.search_policy(question):
        st.markdown(
            f"""
            <div class="mcp-box">
            <strong>{sec['title']} – Section {sec['section_id']}</strong><br>
            {sec['text']}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.subheader("✔️ Compliance Check")
    if "result" in locals():
        st.json(result["compliance"])
