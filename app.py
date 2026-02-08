import streamlit as st
import google.generativeai as genai

st.title("🛠 API Debugger")

# Configure
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error(f"API Key Error: {e}")

if st.button("List Available Models"):
    try:
        st.write("Contacting Google...")
        models = genai.list_models()
        found = False
        for m in models:
            if 'generateContent' in m.supported_generation_methods:
                st.success(f"✅ AVAILABLE MODEL: {m.name}")
                found = True
        if not found:
            st.error("No text generation models found for this API Key.")
    except Exception as e:
        st.error(f"Error listing models: {e}")
