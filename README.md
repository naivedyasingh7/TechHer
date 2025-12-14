# STEMVerse 🌸💻

**Empowering Women in STEM – One Level at a Time**

STEMVerse is a beautiful, gamified web platform built with Streamlit, designed to inspire, guide, and support women on their journey in Science, Technology, Engineering, and Mathematics (STEM).

With a soft pink & white aesthetic, interactive features, and motivational content, it makes learning STEM fun and empowering! ✨

## 🚀 Features

- **Gamified Learning Paths (STEMQuest)** 🎮  
  Choose from structured roadmaps in AI/ML, Web Development, Data Science, or Core CS. Complete levels, earn XP, unlock badges, and track progress!

- **Inspiration Hub** ✨  
  Stories of iconic women in STEM like Grace Hopper, Mae Jemison, Fei-Fei Li, and more.

- **Curated Opportunities** 🎓  
  Scholarships, internships, and programs specifically for women in tech (loaded from CSV).

- **Smart Chat Assistant** 💬  
  Ask questions and get tailored advice using keyword-based FAQ matching.

- **Resume Tips Section** 📋  
  Practical, actionable advice to craft standout STEM resumes.

- **User Authentication** 🔐  
  Sign up / login with progress saving (XP, level).

- **Stunning UI** 🌸  
  Custom CSS with baby pink gradients, glassmorphism login, cards, badges, and balloons on achievements!

## 🛠 Tech Stack

- **Streamlit** – For the interactive web app
- **Pandas** – Data handling (opportunities, users)
- **JSON/CSV** – Storage for roadmaps, stories, FAQs, opportunities
- **Python** – Core logic, hashing for passwords

## 📂 Project Structure
├── app.py                  # Main dashboard app (after login)
├── main.py                 # Landing / Login page (Streamlit multi-page entry)
├── pages/
│   └── app.py              # Core dashboard (STEMQuest, Inspiration, etc.)
├── data/
│   └── users.json          # User data & progress
├── opportunities.csv       # List of scholarships & internships
├── roadmap.json            # Gamified learning paths
├── stories.json            # Inspiring women profiles
├── faq.json                # Chat assistant knowledge base
├── requirements.txt
└── README.md               # This file!

## 🚀 How to Run Locally

1. Clone the repository:
   ```bash
  git clone https://github.com/jiacode777/TechHer.git
  cd TechHer
2. Create a virtual environment (recommended):
     python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install dependencies
   pip install -r requirements.txt
4. Run the app
   streamlit run main.py
5. Sign up or log in, then start your STEM journey! 🌟

🤝 Contributing
Contributions are very welcome! You can:

Add more opportunities to opportunities.csv
Expand learning paths in roadmap.json
Add new inspiring stories in stories.json
Improve the UI or add new features


