import os
import streamlit as st
from dotenv import load_dotenv
from services.llm_service import LLMService

load_dotenv()

st.set_page_config(
    page_title="Sri Lanka Smart Tourism Assistant",
    page_icon="🌴",
    layout="wide"
)

st.title("🌴 Sri Lanka Smart Tourism Assistant")

openrouter_key = os.getenv("OPENROUTER_API_KEY")
groq_key = os.getenv("GROQ_API_KEY")

if openrouter_key:
    st.success("✅ OpenRouter API Loaded")
else:
    st.error("❌ OpenRouter API Missing")

if groq_key:
    st.success("✅ Groq API Loaded")
else:
    st.error("❌ Groq API Missing")

question = st.text_area(
    "Ask your tourism question",
    height=120
)

if st.button("Ask AI"):
    if question:
        with st.spinner("Thinking..."):
            try:
                service = LLMService()
                answer = service.ask(question)
                st.success(answer)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a question.")