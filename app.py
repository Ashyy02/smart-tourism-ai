import os
import traceback
import streamlit as st
from dotenv import load_dotenv

from services.llm_service import LLMService

load_dotenv()

st.set_page_config(
    page_title="Sri Lanka Smart Tourism Assistant",
    page_icon="🌴",
    layout="wide"
)

# -------------------------
# Custom CSS
# -------------------------

st.markdown("""
<style>

.main-title{
    text-align:center;
    font-size:42px;
    font-weight:bold;
    color:#0E7C86;
}

.subtitle{
    text-align:center;
    font-size:18px;
    color:gray;
}

.response-box{
    background:#f5f7fa;
    padding:20px;
    border-radius:10px;
    border-left:6px solid #0E7C86;
}

.agent-box{
    background:#E8F8F5;
    padding:15px;
    border-radius:10px;
}

.knowledge-box{
    background:#FFF8E1;
    padding:15px;
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# Header
# -------------------------

st.markdown("<div class='main-title'>🌴 Sri Lanka Smart Tourism Assistant</div>", unsafe_allow_html=True)

st.markdown("<div class='subtitle'>Multi-Agent AI + RAG + OpenRouter + Streamlit</div>", unsafe_allow_html=True)

st.divider()

# -------------------------
# Sidebar
# -------------------------

with st.sidebar:

    st.header("🌍 About")

    st.write("""
This AI Assistant can help you with:

- 📍 Tourist Attractions
- 🏨 Hotels
- 🗺 Travel Plans
- 🌦 Weather
- 🚗 Transportation
""")

    st.divider()

    st.subheader("API Status")

    if os.getenv("OPENROUTER_API_KEY"):
        st.success("✅ OpenRouter Connected")
    else:
        st.error("❌ OpenRouter Missing")

    if os.getenv("GROQ_API_KEY"):
        st.success("✅ Groq Connected")
    else:
        st.warning("⚠️ Groq Not Configured")

# -------------------------
# Chat History
# -------------------------

if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------
# Input
# -------------------------

question = st.text_area(
    "💬 Ask anything about Sri Lanka",
    placeholder="Example: Recommend a hotel in Kandy",
    height=120
)

if st.button("🚀 Ask AI", use_container_width=True):

    if question.strip() == "":
        st.warning("Please enter a question.")

    else:

        with st.spinner("🤖 AI is thinking..."):

            try:

                service = LLMService()

                category, knowledge, answer = service.ask(question)

                st.session_state.history.append({
                    "question": question,
                    "category": category,
                    "knowledge": knowledge,
                    "answer": answer
                })

            except Exception:

                st.error("An error occurred.")
                st.code(traceback.format_exc())

# -------------------------
# Display Chat History
# -------------------------

if st.session_state.history:

    st.divider()

    st.header("💬 Conversation")

    for chat in reversed(st.session_state.history):

        st.markdown("### 👤 You")
        st.info(chat["question"])

        st.markdown("### 🤖 Selected Agent")
        st.markdown(
            f"<div class='agent-box'>{chat['category']}</div>",
            unsafe_allow_html=True
        )

        st.markdown("### 📚 Retrieved Knowledge")

        if chat["knowledge"]:
            st.markdown(
                f"<div class='knowledge-box'>{chat['knowledge']}</div>",
                unsafe_allow_html=True
            )
        else:
            st.info("No matching knowledge found.")

        st.markdown("### 🤖 AI Response")

        st.markdown(
            f"<div class='response-box'>{chat['answer']}</div>",
            unsafe_allow_html=True
        )

        st.divider()