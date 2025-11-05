import streamlit as st
import pandas as pd
import json
import random
from difflib import SequenceMatcher
import hashlib

# Page configuration
st.set_page_config(
    page_title="STEMVerse - Empowering Women in STEM",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for aesthetic design with white & baby pink theme
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #fff5f7 0%, #ffe4e9 50%, #ffd4e5 100%);
    }
    
    /* Headers */
    .main-header {
        font-size: 3.5rem;
        background: linear-gradient(135deg, #ff6b9d 0%, #c9a0dc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: 800;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(255, 182, 193, 0.3);
    }
    
    .sub-header {
        font-size: 1.8rem;
        color: #ff6b9d;
        margin-top: 2rem;
        font-weight: 600;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffe4e9 0%, #ffd4e5 100%);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #d946a6;
        font-weight: 500;
    }
    
    /* Opportunity cards - soft pink cards */
    .opportunity-card {
        background: linear-gradient(135deg, #ffffff 0%, #ffe4f0 100%);
        padding: 1.8rem;
        border-radius: 20px;
        border: 3px solid #ffb3d9;
        margin: 1.5rem 0;
        box-shadow: 0 8px 20px rgba(255, 107, 157, 0.2);
        transition: transform 0.3s ease;
    }
    
    .opportunity-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(255, 107, 157, 0.3);
    }
    
    .opportunity-card h3 {
        color: #ff6b9d;
        margin-bottom: 0.8rem;
        font-size: 1.5rem;
    }
    
    .opportunity-card strong {
        color: #d946a6;
    }
    
    .opportunity-card p {
        color: #6b4668;
    }
    
    /* Profile cards - gradient pink cards */
    .profile-card {
        background: linear-gradient(135deg, #ff6b9d 0%, #c9a0dc 100%);
        color: white;
        padding: 2rem;
        border-radius: 25px;
        margin: 1rem 0;
        box-shadow: 0 10px 25px rgba(255, 107, 157, 0.4);
        transition: transform 0.3s ease;
    }
    
    .profile-card:hover {
        transform: scale(1.05);
    }
    
    .profile-card h2, .profile-card h3, .profile-card h4 {
        color: #fff;
    }
    
    /* Quest/Game styling */
    .quest-level {
        background: linear-gradient(135deg, #ffffff 0%, #ffeef5 100%);
        padding: 2rem;
        border-radius: 20px;
        border-left: 8px solid #ff6b9d;
        margin: 2rem 0;
        box-shadow: 0 8px 20px rgba(255, 107, 157, 0.15);
    }
    
    .quest-level h3 {
        color: #ff6b9d;
        font-size: 1.8rem;
        margin-bottom: 1rem;
    }
    
    .xp-badge {
        background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
        color: #6b4668;
        padding: 0.5rem 1.2rem;
        border-radius: 25px;
        font-weight: 700;
        font-size: 1.1rem;
        display: inline-block;
        margin: 0.5rem;
        box-shadow: 0 4px 10px rgba(255, 215, 0, 0.4);
    }
    
    .level-badge {
        background: linear-gradient(135deg, #ff6b9d 0%, #c9a0dc 100%);
        color: white;
        padding: 0.5rem 1.2rem;
        border-radius: 25px;
        font-weight: 700;
        font-size: 1.1rem;
        display: inline-block;
        margin: 0.5rem;
        box-shadow: 0 4px 10px rgba(255, 107, 157, 0.4);
    }
    
    .achievement-badge {
        background: linear-gradient(135deg, #c9a0dc 0%, #a78bfa 100%);
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        margin: 1rem 0.5rem;
        box-shadow: 0 6px 15px rgba(201, 160, 220, 0.4);
    }
    
    /* Chat messages */
    .stChatMessage {
        background: linear-gradient(135deg, #ffffff 0%, #fff5f7 100%);
        border-radius: 15px;
        border: 2px solid #ffb3d9;
    }
    
    /* Make chat text darker and more visible */
    .stChatMessage p {
        color: #2d3748 !important;
        font-weight: 500 !important;
    }
    
    /* Chat input styling */
    .stChatInput textarea {
        color: #2d3748 !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #ff6b9d 0%, #c9a0dc 100%);
        color: white;
        border-radius: 25px;
        border: none;
        padding: 0.6rem 2rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(255, 107, 157, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 107, 157, 0.5);
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #ff6b9d 0%, #ffd700 100%);
        border-radius: 10px;
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        border-radius: 15px;
        border: 2px solid #ffb3d9;
        background: white;
    }
    
    /* Login page styling */
    .welcome-banner {
        background: linear-gradient(135deg, #ff6b9d 0%, #c9a0dc 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(255, 107, 157, 0.4);
    }
    
    /* Home page cards */
    .feature-card {
        background: linear-gradient(135deg, #ffffff 0%, #ffe4f0 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        border: 3px solid #ffb3d9;
        box-shadow: 0 8px 20px rgba(255, 107, 157, 0.2);
        transition: transform 0.3s ease;
        height: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 12px 30px rgba(255, 107, 157, 0.3);
    }
    
    .stats-card {
        background: linear-gradient(135deg, #ff6b9d 0%, #c9a0dc 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(255, 107, 157, 0.3);
    }
    
    .stats-number {
        font-size: 3rem;
        font-weight: 800;
        color: #ffd700;
    }
    
    /* Expandable sections */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #ffe4f0 0%, #ffd4e5 100%);
        border-radius: 15px;
        color: #d946a6;
        font-weight: 600;
    }
    
    /* Expander content - make text dark and visible */
    .streamlit-expanderContent {
        background: #ffffff;
        color: #2d3748 !important;
    }
    
    .streamlit-expanderContent p,
    .streamlit-expanderContent div {
        color: #2d3748 !important;
        font-weight: 500 !important;
    }
    
    /* All text in main content area */
    .main .block-container p {
        color: #2d3748;
    }
    
    /* Make all markdown text darker */
    .element-container p,
    .element-container div,
    .element-container span {
        color: #2d3748;
    }
    </style>
""", unsafe_allow_html=True)

# Load data functions with caching
@st.cache_data
def load_faq():
    try:
        with open('data/faq.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"faqs": []}

@st.cache_data
def load_opportunities():
    try:
        return pd.read_csv('data/opportunities.csv', encoding='utf-8')
    except FileNotFoundError:
        return pd.DataFrame()
    except UnicodeDecodeError:
        try:
            return pd.read_csv('data/opportunities.csv', encoding='latin-1')
        except:
            return pd.DataFrame()

@st.cache_data
def load_stories():
    try:
        with open('data/stories.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"stories": []}

@st.cache_data
def load_roadmap():
    try:
        with open('data/roadmap.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"paths": []}

# Calculate XP and level
def calculate_xp(completed_goals):
    total_completed = sum(sum(level_goals) for path_goals in completed_goals.values() for level_goals in path_goals.values())
    xp = total_completed * 100
    level = (xp // 500) + 1
    return xp, level

# Fuzzy matching function for chatbot
def find_best_match(query, faqs):
    query_lower = query.lower()
    best_match = None
    best_score = 0
    
    for faq in faqs['faqs']:
        # Check if any keyword appears in the query
        keyword_matches = sum(1 for keyword in faq['keywords'] if keyword.lower() in query_lower)
        
        # If multiple keywords match, it's a strong match
        if keyword_matches >= 2:
            return faq
        
        # Otherwise, try fuzzy matching on each keyword
        for keyword in faq['keywords']:
            # Check if keyword is contained in query
            if keyword.lower() in query_lower:
                return faq
            
            # Fuzzy match
            score = SequenceMatcher(None, query_lower, keyword.lower()).ratio()
            if score > best_score:
                best_score = score
                best_match = faq
    
    # Return match if score is above threshold
    if best_score > 0.5:
        return best_match
    return None

# Initialize session state
if 'username' not in st.session_state:
    st.session_state.username = "Guest"

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'completed_goals' not in st.session_state:
    st.session_state.completed_goals = {}

if 'selected_path' not in st.session_state:
    st.session_state.selected_path = None

if 'bookmarks' not in st.session_state:
    st.session_state.bookmarks = []

# Sidebar navigation with user info
st.sidebar.markdown(f"""
<div class='welcome-banner'>
    <h3 style='margin: 0;'>Welcome!</h3>
    <h2 style='margin: 0.5rem 0;'>👋 {st.session_state.username}</h2>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<h1 style='text-align: center; color: #ff6b9d;'>🌸 STEMVerse</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; font-style: italic; color: #d946a6;'>Empowering Women in STEM</p>", unsafe_allow_html=True)

# Display user stats in sidebar
xp, level = calculate_xp(st.session_state.completed_goals)
st.sidebar.markdown("---")
st.sidebar.markdown(f"""
<div class='stats-card'>
    <p style='margin: 0; font-size: 0.9rem;'>Your Level</p>
    <p class='stats-number'>{level}</p>
    <p style='margin: 0; font-size: 1rem;'>⭐ {xp} XP</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "🗺️ Navigate Your Quest",
    ["🏠 Home", "💬 Ask STEMVerse", "🎓 Opportunities", "✨ Inspiration Hub", "🎮 STEMQuest", "📋 Resume Tips"],
    label_visibility="visible"
)

# Logout button
st.sidebar.markdown("---")
if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.user_data = None
    st.switch_page("main.py")

# HOME PAGE
if page == "🏠 Home":
    st.markdown("<h1 class='main-header'>🌸 Welcome to STEMVerse 🌸</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.3rem; color: #2d3748; font-weight: 600;'>Your magical journey to success in STEM starts here ✨</p>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class='feature-card'>
            <div style='font-size: 3rem;'>💬</div>
            <h3 style='color: #ff6b9d;'>Ask STEMVerse</h3>
            <p style='color: #6b4668;'>Get instant answers about scholarships and resources</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class='feature-card'>
            <div style='font-size: 3rem;'>🎓</div>
            <h3 style='color: #ff6b9d;'>Opportunities</h3>
            <p style='color: #6b4668;'>Discover amazing scholarships and internships</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class='feature-card'>
            <div style='font-size: 3rem;'>✨</div>
            <h3 style='color: #ff6b9d;'>Inspiration</h3>
            <p style='color: #6b4668;'>Learn from pioneering women in STEM</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown("""
        <div class='feature-card'>
            <div style='font-size: 3rem;'>🎮</div>
            <h3 style='color: #ff6b9d;'>STEMQuest</h3>
            <p style='color: #6b4668;'>Gamified career roadmap with XP and levels</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Motivational quote section
    st.markdown("""
    <div style='background: linear-gradient(135deg, #ff6b9d 0%, #c9a0dc 100%); 
                padding: 2rem; border-radius: 20px; text-align: center; 
                box-shadow: 0 10px 30px rgba(255, 107, 157, 0.3);'>
        <h2 style='color: white; margin: 0;'>💪 Your Journey, Your Rules</h2>
        <p style='color: #fff; font-size: 1.2rem; margin-top: 1rem;'>
            Every expert was once a beginner. Start your quest today! 🚀
        </p>
    </div>
    """, unsafe_allow_html=True)

# ASK STEMVERSE - CHATBOT
elif page == "💬 Ask STEMVerse":
    st.markdown("<h1 class='main-header'>💬 Ask STEMVerse</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #2d3748; font-size: 1.1rem; font-weight: 600;'>Ask me anything about scholarships, resources, or women in STEM! 💜</p>", unsafe_allow_html=True)
    
    faq_data = load_faq()
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    user_query = st.chat_input("✨ Type your question here...")
    
    if user_query:
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        
        # Find matching FAQ
        match = find_best_match(user_query, faq_data)
        
        if match:
            response = match['answer']
        else:
            response = "I'm not sure about that specific question, but you can explore our **Opportunities** section for scholarships or check the **Inspiration Hub** for motivational stories! 💜"
        
        # Add assistant response to history
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        # Rerun to display new messages
        st.rerun()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

# OPPORTUNITIES SECTION
elif page == "🎓 Opportunities":
    st.markdown("<h1 class='main-header'>🎓 Opportunities</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #2d3748; font-size: 1.1rem; font-weight: 600;'>Discover scholarships, internships, and programs designed for you! ✨</p>", unsafe_allow_html=True)
    
    df = load_opportunities()
    
    if df.empty:
        st.warning("No opportunities data available. Please add opportunities.csv file.")
    else:
        # Search and filter
        col1, col2 = st.columns([3, 1])
        
        with col1:
            search_query = st.text_input("🔍 Search opportunities", placeholder="e.g., AI, scholarship, Google")
        
        with col2:
            category_filter = st.multiselect("📂 Filter by type", options=df['category'].unique() if 'category' in df.columns else [])
        
        # Apply filters
        filtered_df = df.copy()
        
        if search_query:
            filtered_df = filtered_df[
                filtered_df.apply(lambda row: search_query.lower() in str(row).lower(), axis=1)
            ]
        
        if category_filter:
            filtered_df = filtered_df[filtered_df['category'].isin(category_filter)]
        
        st.markdown(f"<p style='color: #ff6b9d; font-size: 1.2rem; font-weight: 600;'>✨ Found {len(filtered_df)} amazing opportunities</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Display opportunities as cards
        for idx, row in filtered_df.iterrows():
            with st.container():
                st.markdown(f"""
                <div class='opportunity-card'>
                    <h3>🌟 {str(row['name'])}</h3>
                    <p><strong>🏢 Organization:</strong> {str(row['organization'])}</p>
                    <p><strong>📁 Category:</strong> {str(row['category'])}</p>
                    <p><strong>✅ Eligibility:</strong> {str(row['eligibility'])}</p>
                    <p><strong>📅 Deadline:</strong> {str(row['deadline'])}</p>
                    <p style='margin-top: 1rem;'>{str(row['description'])}</p>
                </div>
                """, unsafe_allow_html=True)
                
                col_a, col_b = st.columns([1, 5])
                with col_a:
                    st.markdown(f"[🔗 Learn More]({row['link']})")
                
                with col_b:
                    bookmark_key = f"bookmark_{idx}"
                    if idx in st.session_state.bookmarks:
                        if st.button("⭐ Bookmarked", key=bookmark_key):
                            st.session_state.bookmarks.remove(idx)
                            st.rerun()
                    else:
                        if st.button("☆ Bookmark", key=bookmark_key):
                            st.session_state.bookmarks.append(idx)
                            st.rerun()

# INSPIRATION HUB
elif page == "✨ Inspiration Hub":
    st.markdown("<h1 class='main-header'>✨ Inspiration Hub ✨</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #2d3748; font-size: 1.1rem; font-weight: 600;'>Be inspired by the incredible women who paved the way in STEM! 💪</p>", unsafe_allow_html=True)
    
    stories_data = load_stories()
    
    if not stories_data['stories']:
        st.warning("No stories available. Please add stories.json file.")
    else:
        # Inspire Me button
        if st.button("🎲 Inspire Me!", use_container_width=True):
            random_story = random.choice(stories_data['stories'])
            st.session_state.featured_story = random_story
        
        # Display featured story if exists
        if 'featured_story' in st.session_state:
            story = st.session_state.featured_story
            st.markdown(f"""
            <div class='profile-card'>
                <h2>✨ {story['name']}</h2>
                <h4>{story['role']}</h4>
                <p><strong>Field:</strong> {story['field']}</p>
                <p style='margin-top: 1rem; font-size: 1.1rem;'>{story['short_bio']}</p>
                <p style='margin-top: 1rem;'><strong>🏆 Achievement:</strong> {story['achievement']}</p>
                <p style='margin-top: 1rem; font-style: italic; font-size: 1.1rem;'>"{story['quote']}"</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("<h2 style='color: #ff6b9d; text-align: center;'>All Inspiring Women 👑</h2>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Display all stories in grid
        cols = st.columns(3)
        for idx, story in enumerate(stories_data['stories']):
            with cols[idx % 3]:
                st.markdown(f"""
                <div class='profile-card'>
                    <h3>{story['name']}</h3>
                    <p><strong>{story['role']}</strong></p>
                    <p>{story['field']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("📖 Read More"):
                    st.markdown(f"""
                    <div style='color: #2d3748; background: white; padding: 1rem; border-radius: 10px;'>
                        <p style='color: #2d3748; font-weight: 500;'>{story['short_bio']}</p>
                        <p style='color: #2d3748; font-weight: 600;'><strong>🏆 Achievement:</strong> {story['achievement']}</p>
                        <p style='color: #2d3748; font-style: italic;'>"{story['quote']}"</p>
                    </div>
                    """, unsafe_allow_html=True)

# STEMQUEST - CAREER GAME
elif page == "🎮 STEMQuest":
    st.markdown("<h1 class='main-header'>🎮 STEMQuest</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #2d3748; font-size: 1.1rem; font-weight: 600;'>Choose your path, complete quests, and level up your STEM career! 🚀</p>", unsafe_allow_html=True)
    
    # Display current stats
    xp, level = calculate_xp(st.session_state.completed_goals)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class='stats-card'>
            <p style='margin: 0; font-size: 0.9rem;'>Current Level</p>
            <p class='stats-number'>{level}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='stats-card'>
            <p style='margin: 0; font-size: 0.9rem;'>Total XP</p>
            <p class='stats-number'>{xp}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_goals = sum(sum(level_goals) for path_goals in st.session_state.completed_goals.values() for level_goals in path_goals.values())
        st.markdown(f"""
        <div class='stats-card'>
            <p style='margin: 0; font-size: 0.9rem;'>Quests Completed</p>
            <p class='stats-number'>{total_goals}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    roadmap_data = load_roadmap()
    
    if not roadmap_data['paths']:
        st.warning("No roadmap data available. Please add roadmap.json file.")
    else:
        # Path selection
        path_names = [path['name'] for path in roadmap_data['paths']]
        selected_path_name = st.selectbox("🛤️ Choose Your Career Path", path_names)
        
        # Get selected path data
        selected_path = next((p for p in roadmap_data['paths'] if p['name'] == selected_path_name), None)
        
        if selected_path:
            path_id = selected_path['id']
            st.session_state.selected_path = path_id
            
            # Initialize progress if not exists
            if path_id not in st.session_state.completed_goals:
                st.session_state.completed_goals[path_id] = {}
            
            st.markdown(f"<p style='text-align: center; color: #d946a6; font-size: 1.2rem; font-weight: 500;'>📖 {selected_path['description']}</p>", unsafe_allow_html=True)
            st.markdown("---")
            
            # Display levels as quest cards
            for level in selected_path['levels']:
                level_num = level['level']
                level_key = f"level_{level_num}"
                
                # Initialize level goals if not exists
                if level_key not in st.session_state.completed_goals[path_id]:
                    st.session_state.completed_goals[path_id][level_key] = [False] * len(level['goals'])
                
                # Calculate progress
                completed = st.session_state.completed_goals[path_id][level_key]
                progress = sum(completed) / len(completed) * 100
                completed_count = sum(completed)
                total_count = len(completed)
                
                # Level card
                st.markdown(f"""
                <div class='quest-level'>
                    <h3>🎯 Level {level_num}: {level['title']}</h3>
                    <span class='level-badge'>Level {level_num}</span>
                    <span class='xp-badge'>+{completed_count * 100} XP</span>
                    <p style='color: #6b4668; margin-top: 1rem;'>⏱️ Estimated Time: {level['estimated_time']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Progress bar
                st.progress(progress / 100)
                st.markdown(f"<p style='color: #ff6b9d; font-weight: 600;'>Progress: {int(progress)}% ({completed_count}/{total_count} quests completed)</p>", unsafe_allow_html=True)
                
                # Display goals with checkboxes
                for goal_idx, goal in enumerate(level['goals']):
                    checkbox_key = f"{path_id}_{level_key}_{goal_idx}"
                    is_completed = st.checkbox(
                        f"{'✅' if completed[goal_idx] else '⬜'} {goal}",
                        value=completed[goal_idx],
                        key=checkbox_key
                    )
                    
                    # Update completion status
                    if is_completed != completed[goal_idx]:
                        st.session_state.completed_goals[path_id][level_key][goal_idx] = is_completed
                        
                        # Check if level completed
                        if all(st.session_state.completed_goals[path_id][level_key]):
                            st.balloons()
                            st.success(f"🎉 Amazing! You've completed Level {level_num}! +{total_count * 100} XP earned!")
                        
                        st.rerun()
                
                # Show resources
                if level.get('resources'):
                    with st.expander("📚 Learning Resources"):
                        for resource in level['resources']:
                            st.write(f"• {resource}")
                
                st.markdown("<br>", unsafe_allow_html=True)
            
            # Show achievement badges
            if xp >= 500:
                st.markdown("<h3 style='color: #ff6b9d; text-align: center;'>🏆 Your Achievements</h3>", unsafe_allow_html=True)
                badges = []
                if xp >= 500:
                    badges.append("🌟 Getting Started")
                if xp >= 1000:
                    badges.append("💪 Committed Learner")
                if xp >= 2000:
                    badges.append("🚀 Rising Star")
                if xp >= 3000:
                    badges.append("👑 STEM Queen")
                
                for badge in badges:
                    st.markdown(f"<span class='achievement-badge'>{badge}</span>", unsafe_allow_html=True)

# RESUME TIPS
elif page == "📋 Resume Tips":
    st.markdown("<h1 class='main-header'>📋 Resume Tips</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #2d3748; font-size: 1.1rem; font-weight: 600;'>Craft a standout resume for your STEM career! ✨</p>", unsafe_allow_html=True)
    
    tips = [
        {
            "title": "Highlight Technical Skills",
            "icon": "💻",
            "content": "List programming languages, tools, and technologies prominently. Include proficiency levels and projects where you used them.",
            "example": "✅ Python (Advanced), TensorFlow, React.js - Used in 3 AI projects"
        },
        {
            "title": "Quantify Your Achievements",
            "icon": "📊",
            "content": "Use numbers to show impact. Instead of 'improved system', say 'improved system performance by 40%'.",
            "example": "✅ Developed algorithm that reduced processing time by 35%"
        },
        {
            "title": "Include Leadership & Diversity Work",
            "icon": "👑",
            "content": "Mention roles in women-in-tech groups, mentoring, or DEI initiatives. These show leadership and community impact.",
            "example": "✅ Founded Women in CS club with 50+ members, organized 3 workshops"
        },
        {
            "title": "Tailor for Each Application",
            "icon": "🎯",
            "content": "Customize your resume for each job. Use keywords from the job description and emphasize relevant experience.",
            "example": "✅ Match job requirements: 'Machine Learning' → highlight ML projects"
        },
        {
            "title": "Show Continuous Learning",
            "icon": "📚",
            "content": "Include certifications, online courses, hackathons, and side projects to demonstrate passion and growth.",
            "example": "✅ Completed Google ML Crash Course, won 2nd place at HackHER2024"
        },
        {
            "title": "Use Action Verbs",
            "icon": "⚡",
            "content": "Start bullet points with strong verbs: developed, engineered, optimized, designed, implemented, led.",
            "example": "✅ Engineered RESTful API serving 10K daily requests"
        },
        {
            "title": "Keep It Clean & ATS-Friendly",
            "icon": "✨",
            "content": "Use simple formatting, standard fonts, and avoid images/graphics. Ensure it passes Applicant Tracking Systems.",
            "example": "✅ Use PDF format, Arial/Calibri font, clear section headers"
        }
    ]
    
    for idx, tip in enumerate(tips, 1):
        st.markdown(f"""
        <div class='quest-level'>
            <h3>{tip['icon']} Tip {idx}: {tip['title']}</h3>
            <p style='color: #6b4668; margin-top: 1rem;'>{tip['content']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.info(tip['example'])
        st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.success("💡 Pro Tip: Have your resume reviewed by mentors or career services before applying!")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("<p style='text-align: center; color: #d946a6;'>Made with 💜 for women in STEM</p>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; color: #d946a6;'>© 2025 STEMVerse</p>", unsafe_allow_html=True)