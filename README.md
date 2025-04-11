# 🔍 GitHunt – Intelligent Tech Talent Sourcing on GitHub

GitHunt is an interactive Streamlit web app designed to help tech recruiters and sourcers discover high-quality **tech profiles** directly from GitHub. By analyzing user metadata, activity, and technical stacks, GitHunt provides a curated, filterable, and visually rich interface for exploring potential candidates.

## 🎯 Project Goal

Recruiting tech talent through GitHub is often time-consuming and inefficient. The goal of GitHunt is to streamline that process by:

- 🧠 Automating profile enrichment and scoring based on GitHub activity  
- 🎯 Allowing recruiters to filter tech profiles by city, position, technologies, and communication potential  
- 📬 Highlighting contact information such as email, LinkedIn, and personal websites  
- 📈 Offering visual insight into recent GitHub activity to spot engaged contributors  

Whether you’re sourcing backend engineers in Berlin or looking for frontend or data talent in Munich with recent repo activity, GitHunt helps you identify and explore relevant tech profiles faster and more intelligently.

## 🖼️ Overview

- 🔎 Filter and explore thousands of GitHub tech profiles  
- 📍 Target users by location (e.g., Berlin, Munich)  
- 🧰 Search by technology stack, position, or profile quality  
- 💌 Email, LinkedIn, Twitter & website links included  
- 📈 Activity visualizations per user  
- 🎨 Clean, compact and blue-themed UI for smooth navigation  

## 🧱 Project Structure

Githunt/  
├── githunt_app.py → Main Streamlit app  
├── df_merged.csv → Merged dataset of GitHub profiles  
├── Githunt1.2.ipynb → Data exploration & feature engineering notebook  
├── README.md → Project description and usage  
├── .gitignore → Ignores venv, CSVs, .env, etc.  
└── requirements.txt → Python dependencies  

## ⚙️ How to Use

Make sure Python 3.8+ is installed.

1. Install the dependencies:  
   `pip install -r requirements.txt`  

2. Run the app:  
   `streamlit run githunt_app.py`  

Your browser will open at `http://localhost:8501`.

## 📊 Dataset

The file `df_merged.csv` contains structured GitHub profile data enriched with:

- Name, city, position (inferred or from bio)  
- Languages used (`top_languages`)  
- Public contact info (email, Twitter, LinkedIn, blog)  
- GitHub stats (stars, followers, repo activity by month)  
- Profile scoring and matching based on usage and filters  

## 📦 Features Breakdown

• **City Filter** – Filter profiles by German cities (e.g., Berlin, Munich)  
• **Position & Techs** – Filter based on role (Frontend, Backend, Data...) and tech stack  
• **Email Only** – Restrict view to profiles with a public email address  
• **Matching Score** – Prioritize profiles with better GitHub presence  
• **Activity Chart** – View recent monthly GitHub repo contributions  
• **Links** – Clickable GitHub, LinkedIn, Twitter, Website, and Email  
• **Profile Reliability** – Highlights if the position was inferred confidently  

## 📸 Screenshot

_Add a screenshot here to showcase the interface (optional)._

## 🧪 Tech Stack

- Streamlit  
- Pandas  
- Matplotlib  
- GitHub dataset (scraped or downloaded)  

## 📄 License

This project is provided for educational and portfolio purposes.  
Please use responsibly and respect user privacy if sourcing real profiles.

## 🤝 Contributions

Open to ideas and improvements! Feel free to fork or submit pull requests.
