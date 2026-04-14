📊 Netflix Activity Analysis

An interactive Streamlit app that transforms Netflix viewing history into clear insights about user behavior, binge patterns, and content preferences.

🚀 Features

- Profile‑based analysis (separate stats for each Netflix profile)
- Time Spent: Total hours watched per profile
- Last Watched: Most recent title viewed
- Most Watched: Top movies and series by frequency and duration
- Watch Graphs: Heatmap of activity across weekdays and hours
- Title Search: Search for specific titles and see last watched timestamp

🛠️ Tech Stack

- Python (data wrangling & analysis)
- Pandas, NumPy (cleaning, aggregation)
- Matplotlib, Seaborn (visualizations)
- Streamlit (interactive UI)
- Pillow (image handling)

📂 Data Input

Export your ViewingActivity.csv from Netflix and place it in the project directory.
The app automatically:
- Cleans and parses timestamps
- Converts durations to hours/minutes
- Drops irrelevant columns

▶️ Run Locally

git clone https://github.com/aadilshajahan12/Netflix_Activity_Analysis.git 
cd Netflix_Activity_Analysis 
pip install -r requirements.txt 
streamlit run app.py 



🌐 Live Demo

The app is deployed on Streamlit Cloud:
👉 Try it here (https://aadil-netflix-analysis.streamlit.app in Bing)

🎯 Why It Matters

This project demonstrates:
- Data wrangling: turning raw CSV logs into structured insights
- Visualization & storytelling: recruiter‑ready plots and clear UI
- App development: polished Streamlit interface
- Business impact: understanding user engagement and content consumption patterns

📌 Next Steps

- Add monthly/weekly trend analysis
- Enhance UI with filters and interactivity
- Deploy advanced recommendation insights

<img width="1865" height="871" alt="Screenshot 2026-04-14 114305" src="https://github.com/user-attachments/assets/3e8dc111-0b8a-462a-a4ac-93ff875c1820" />

<img width="1886" height="865" alt="Screenshot 2026-04-14 114327" src="https://github.com/user-attachments/assets/1f5e8bf4-0379-4db0-b438-bea3c9b60339" />


