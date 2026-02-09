import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="ATS Resume Crusher",
    page_icon="🚀",
    layout="centered"
)

# --- CUSTOM CSS FOR "LANDING PAGE" VIBE ---
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        color: #1E1E1E;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.5rem;
        text-align: center;
        color: #4CAF50;
        margin-bottom: 30px;
    }
    .feature-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .price-tag {
        font-size: 2rem;
        font-weight: bold;
        color: #FF4B4B;
        text-align: center;
    }
    .stButton>button {
        width: 100%;
        font-weight: bold;
        border-radius: 8px;
        height: 50px;
    }
</style>
""", unsafe_allow_html=True)

# --- AUTHENTICATION LOGIC ---
def check_password():
    """Returns `True` if the user had the correct password."""
    
    def password_entered():
        if st.session_state["password"] == st.secrets["ACCESS_CODE"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # User has not entered a password yet. Show the LANDING PAGE.
        return False
    elif not st.session_state["password_correct"]:
        # User entered incorrect password.
        st.error("😕 Invalid Code. Check your email or Whop dashboard.")
        return False
    else:
        # Password correct.
        return True

# --- MAIN APP ROUTING ---

if not check_password():
    # ==========================
    # LANDING PAGE (SALES PAGE)
    # ==========================
    
    # Hero Section
    st.markdown('<div class="main-header">🚀 Beat the ATS Bots</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Stop getting auto-rejected. Optimize your resume keywords in 5 seconds using AI.</div>', unsafe_allow_html=True)

    # The Problem & Solution
    col1, col2 = st.columns(2)
    with col1:
        st.info("❌ **The Problem**\n\n75% of resumes are rejected by ATS bots before a human ever sees them because they miss specific keywords.")
    with col2:
        st.success("✅ **The Solution**\n\nThis tool scans the Job Description and rewrites your resume bullets to include the EXACT keywords missing.")

    st.markdown("---")

    # How it Works (Visuals)
    st.subheader("⚙️ How It Works")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### 1. Paste")
        st.write("Paste your Resume & the Job Description.")
    with c2:
        st.markdown("### 2. Scan")
        st.write("AI identifies missing keywords instantly.")
    with c3:
        st.markdown("### 3. Hired")
        st.write("Get rewritten bullet points that pass the bot.")

    st.markdown("---")

    # Pricing Section
    st.markdown('<div style="text-align: center"><h2>💸 Launch Price: Lifetime Access</h2></div>', unsafe_allow_html=True)
    
    p_col1, p_col2, p_col3 = st.columns([1, 2, 1])
    with p_col2:
        st.markdown('<div class="feature-box" style="text-align: center;">', unsafe_allow_html=True)
        st.markdown("<s>Standard Price: $49</s>", unsafe_allow_html=True)
        st.markdown('<div class="price-tag">$9 ONLY</div>', unsafe_allow_html=True)
        st.write("✅ Unlimited Resume Scans")
        st.write("✅ Lifetime Access (No subscriptions)")
        st.write("✅ Instant Access Code Delivery")
        
        # BUY BUTTON
        st.link_button("👉 GET INSTANT ACCESS ($9)", "YOUR_WHOP_CHECKOUT_LINK") 
        st.caption("Secure payment via Whop. Instant access.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # LOGIN SECTION (For existing users)
    with st.expander("🔑 Already have an access code? Login here"):
        st.text_input("Enter Access Code", type="password", on_change=password_entered, key="password")
        
else:
    # ==========================
    # THE TOOL (LOGGED IN USER)
    # ==========================
    
    # Configure Gemini
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-2.5-flash')
    except Exception as e:
        st.error("System Error: API Key not found.")
        st.stop()

    st.title("🚀 ATS Resume Optimizer")
    st.write("Welcome back! Let's get you that interview.")

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
            
    if st.button("Logout"):
        del st.session_state["password_correct"]
        st.rerun()
