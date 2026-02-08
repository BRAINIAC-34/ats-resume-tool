import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ---
# We will set the API key in the deployment settings later
# DO NOT paste your API key here directly for security reasons

# --- PAGE SETUP ---
st.set_page_config(page_title="ATS Resume Crusher", page_icon="🚀")

# --- CSS FOR CLEAN LOOK ---
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- AUTHENTICATION (THE PAYWALL) ---
def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        if st.session_state["password"] == st.secrets["ACCESS_CODE"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # specific logic to clean up
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.header("🔒 Premium Access Only")
        st.write("Enter the Access Code you received on Whop after purchase.")
        st.text_input("Access Code", type="password", on_change=password_entered, key="password")
        st.info("Don't have a code? [Get Lifetime Access Here](https://whop.com/checkout/plan_hcdZ7zla5FK21)") # <--- PASTE YOUR WHOP LINK HERE
        return False
    elif not st.session_state["password_correct"]:
        # Password incorrect, show input again.
        st.header("🔒 Premium Access Only")
        st.text_input("Access Code", type="password", on_change=password_entered, key="password")
        st.error("😕 Invalid Code. Please check your email/Whop dashboard.")
        return False
    else:
        # Password correct.
        return True

if check_password():
    # --- APP LOGIC STARTS HERE ---
    
    # Configure Gemini
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-2.5-flash')
    except Exception as e:
        st.error("System Error: API Key not found.")
        st.stop()

    st.title("🚀 ATS Resume Optimizer")
    st.write("Paste your current resume and the job description. AI will rewrite your bullets to match the keywords.")

    # Inputs
    col1, col2 = st.columns(2)
    with col1:
        resume_text = st.text_area("Paste Your Resume Here", height=300)
    with col2:
        job_desc = st.text_area("Paste Job Description Here", height=300)

    # The Logic
    if st.button("✨ Optimize My Resume Now"):
        if not resume_text or not job_desc:
            st.warning("Please fill in both boxes.")
        else:
            with st.spinner("Analyzing keywords and rewriting..."):
                try:
                    prompt = f"""
                    Act as an expert Resume Writer and ATS Algorithm Specialist.
                    
                    Here is my RESUME:
                    {resume_text}
                    
                    Here is the JOB DESCRIPTION:
                    {job_desc}
                    
                    TASK:
                    1. Identify the top 5 missing keywords from the job description that are missing in my resume.
                    2. Rewrite 3-4 bullet points from my resume to naturally include these keywords.
                    3. Keep the tone professional and result-oriented.
                    4. Do not lie, just rephrase.
                    
                    OUTPUT FORMAT:
                    **Missing Keywords:** [List them]
                    
                    **Optimized Bullet Points:**
                    [List the new versions]
                    """
                    
                    response = model.generate_content(prompt)
                    st.success("Optimization Complete!")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"An error occurred: {e}")
