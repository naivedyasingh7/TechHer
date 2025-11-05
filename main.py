import streamlit as st
import pandas as pd
import json
import hashlib

# Page configuration
st.set_page_config(
    page_title="STEMVerse",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Helper functions for authentication
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    try:
        with open('data/users.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"users": []}

def save_users(users_data):
    with open('data/users.json', 'w', encoding='utf-8') as f:
        json.dump(users_data, f, indent=2)

def authenticate_user(username, password):
    users_data = load_users()
    password_hash = hash_password(password)
    
    for user in users_data['users']:
        if user['username'] == username and user['password'] == password_hash:
            return True, user
    return False, None

def register_user(username, email, password):
    users_data = load_users()
    
    # Check if username already exists
    for user in users_data['users']:
        if user['username'] == username:
            return False, "Username already exists"
    
    # Create new user
    new_user = {
        "username": username,
        "email": email,
        "password": hash_password(password),
        "joined_date": str(pd.Timestamp.now()),
        "level": 1,
        "xp": 0
    }
    
    users_data['users'].append(new_user)
    save_users(users_data)
    return True, "Registration successful!"

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'username' not in st.session_state:
    st.session_state.username = None

if 'user_data' not in st.session_state:
    st.session_state.user_data = None

# Custom CSS for stunning login page
st.markdown("""
    <style>
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main background with image */
    .stApp {
        background: linear-gradient(135deg, rgba(255, 107, 157, 0.9) 0%, rgba(201, 160, 220, 0.9) 100%),
                    url('https://images.unsplash.com/photo-1557683316-973673baf926?w=1920&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* Glassmorphism login box */
    .login-box {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 30px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        padding: 3rem;
        max-width: 450px;
        width: 100%;
        margin: 0 auto;
    }
    
    /* Headers */
    .login-title {
        font-size: 3rem;
        font-weight: 800;
        color: #ffffff;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3);
    }
    
    .login-subtitle {
        font-size: 1.2rem;
        color: #ffffff;
        text-align: center;
        margin-bottom: 2.5rem;
        opacity: 0.9;
    }
    
    /* Brand */
    .brand {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .brand-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #ffffff;
        text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3);
        margin-bottom: 0.5rem;
    }
    
    .brand-tagline {
        font-size: 1rem;
        color: #ffffff;
        opacity: 0.9;
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.2) !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 15px !important;
        color: #ffffff !important;
        padding: 1rem !important;
        font-size: 1rem !important;
        backdrop-filter: blur(10px);
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.7) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: rgba(255, 255, 255, 0.6) !important;
        box-shadow: 0 0 15px rgba(255, 255, 255, 0.3) !important;
    }
    
    .stTextInput > label {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #ff6b9d 0%, #c9a0dc 100%) !important;
        color: white !important;
        border-radius: 25px !important;
        border: none !important;
        padding: 1rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        width: 100% !important;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4) !important;
    }
    
    /* Checkbox */
    .stCheckbox {
        color: #ffffff !important;
    }
    
    .stCheckbox > label {
        color: #ffffff !important;
        font-weight: 500 !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background: transparent;
        border-bottom: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: rgba(255, 255, 255, 0.7);
        font-size: 1.2rem;
        font-weight: 600;
        padding: 1rem 2rem;
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        color: #ffffff !important;
        border-bottom: 3px solid #ffffff;
    }
    
    /* Links */
    a {
        color: #ffffff !important;
        text-decoration: none !important;
        font-weight: 600 !important;
    }
    
    a:hover {
        text-decoration: underline !important;
    }
    
    /* Success/Error messages */
    .stAlert {
        background: rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 15px !important;
        color: #ffffff !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
    }
    
    /* Feature cards */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1.5rem;
        margin-top: 3rem;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 2px solid rgba(255, 255, 255, 0.2);
        padding: 2rem;
        text-align: center;
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        background: rgba(255, 255, 255, 0.25);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        color: #ffffff;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        color: rgba(255, 255, 255, 0.9);
        font-size: 0.95rem;
    }
    
    .divider {
        margin: 2rem 0;
        text-align: center;
        color: rgba(255, 255, 255, 0.7);
    }
    
    .stForm {
        margin-top: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Check if user is logged in
if not st.session_state.logged_in:
    # SHOW LOGIN PAGE
    st.markdown("""
    <div class='brand'>
        <h1 class='brand-title'>🌸 STEMVerse</h1>
        <p class='brand-tagline'>Empowering Women in STEM</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div class='login-box'>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["LOGIN", "SIGN UP"])
        
        with tab1:
            st.markdown("<h2 class='login-title'>Welcome Back! 💕</h2>", unsafe_allow_html=True)
            st.markdown("<p class='login-subtitle'>Login to continue your journey</p>", unsafe_allow_html=True)
            
            with st.form("login_form"):
                username = st.text_input("Username", placeholder="Enter your username", label_visibility="visible")
                password = st.text_input("Password", type="password", placeholder="Enter your password", label_visibility="visible")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    remember = st.checkbox("Remember me")
                with col_b:
                    st.markdown("<div style='text-align: right; padding-top: 0.5rem;'><a href='#'>Forgot Password?</a></div>", unsafe_allow_html=True)
                
                submit = st.form_submit_button("🚀 Login")
                
                if submit:
                    if username and password:
                        success, user_data = authenticate_user(username, password)
                        if success:
                            st.session_state.logged_in = True
                            st.session_state.username = username
                            st.session_state.user_data = user_data
                            st.success("✨ Login successful! Redirecting...")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error("❌ Invalid username or password")
                    else:
                        st.warning("⚠️ Please fill in all fields")
            
            st.markdown("<div class='divider'>Don't have an account? Switch to Sign Up</div>", unsafe_allow_html=True)
        
        with tab2:
            st.markdown("<h2 class='login-title'>Join Us! 🎉</h2>", unsafe_allow_html=True)
            st.markdown("<p class='login-subtitle'>Create your account and start leveling up</p>", unsafe_allow_html=True)
            
            with st.form("signup_form"):
                new_username = st.text_input("Username", placeholder="Choose a unique username", label_visibility="visible")
                new_email = st.text_input("Email", placeholder="your.email@example.com", label_visibility="visible")
                new_password = st.text_input("Password", type="password", placeholder="Create a strong password", label_visibility="visible")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password", label_visibility="visible")
                
                agree = st.checkbox("I agree to empower women in STEM! 💪")
                
                signup_submit = st.form_submit_button("✨ Create Account")
                
                if signup_submit:
                    if not all([new_username, new_email, new_password, confirm_password]):
                        st.warning("⚠️ Please fill in all fields")
                    elif new_password != confirm_password:
                        st.error("❌ Passwords don't match")
                    elif len(new_password) < 6:
                        st.error("❌ Password must be at least 6 characters")
                    elif not agree:
                        st.warning("⚠️ Please agree to join our community")
                    else:
                        success, message = register_user(new_username, new_email, new_password)
                        if success:
                            st.success("🎉 " + message + " Please login to continue!")
                            st.balloons()
                        else:
                            st.error("❌ " + message)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='feature-grid'>
        <div class='feature-card'>
            <div class='feature-icon'>🎮</div>
            <div class='feature-title'>Gamified Learning</div>
            <div class='feature-desc'>Earn XP and level up your skills</div>
        </div>
        <div class='feature-card'>
            <div class='feature-icon'>🎓</div>
            <div class='feature-title'>Scholarships</div>
            <div class='feature-desc'>Find exclusive opportunities</div>
        </div>
        <div class='feature-card'>
            <div class='feature-icon'>✨</div>
            <div class='feature-title'>Inspiration</div>
            <div class='feature-desc'>Learn from role models</div>
        </div>
        <div class='feature-card'>
            <div class='feature-icon'>🚀</div>
            <div class='feature-title'>Career Paths</div>
            <div class='feature-desc'>Structured roadmaps</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    # USER IS LOGGED IN - REDIRECT TO APP
    st.switch_page("pages/app.py")