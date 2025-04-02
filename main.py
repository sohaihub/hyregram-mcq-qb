import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets Authentication using Streamlit secrets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

try:
    # Access credentials from Streamlit secrets
    creds = {
        "type": st.secrets["type"],
        "project_id": st.secrets["project_id"],
        "private_key_id": st.secrets["private_key_id"],
        "private_key": st.secrets["private_key"].replace("\\n", "\n"),
        "client_email": st.secrets["client_email"],
        "client_id": st.secrets["client_id"],
        "auth_uri": st.secrets["auth_uri"],
        "token_uri": st.secrets["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["client_x509_cert_url"]
    }

    client = gspread.service_account_from_dict(creds)
    spreadsheet = client.open_by_url(
        "https://docs.google.com/spreadsheets/d/1K2HJSL0U0vay4UaW4s3QPAIkQ_noj742ZRQJxbTTbQ0/edit?gid=0"
    )
    worksheet = spreadsheet.get_worksheet(0)
    data = pd.DataFrame(worksheet.get_all_records())
    st.success("✅ Successfully connected to Google Sheets!")
except Exception as e:
    st.error(f"❌ Error connecting to Google Sheets: {str(e)}")
    st.stop()

# Page Configuration
st.set_page_config(page_title="📚 MCQ Quiz", layout="wide")
st.title("📚 MCQ Question Bank")

# Sidebar: Page Selection
page = st.sidebar.selectbox("📑 Select a Page", ["Quiz", "Topic Stats"])

# Quiz Page
if page == "Quiz":
    # Sidebar: Topic Selection
    topics = data['Topic'].unique()
    selected_topic = st.sidebar.selectbox("📌 Select a Topic", topics)

    # Filter by Topic
    filtered_data = data[data['Topic'] == selected_topic]

    # Sidebar: Difficulty Filter
    difficulty_levels = ['All'] + list(filtered_data['Difficulty'].unique())
    selected_difficulty = st.sidebar.selectbox("🎚️ Select Difficulty", difficulty_levels)

    if selected_difficulty != 'All':
        filtered_data = filtered_data[filtered_data['Difficulty'] == selected_difficulty]

    st.markdown("---")

    # Function to map correct answers (A, B, C, D) to indexes (0, 1, 2, 3)
    def get_correct_option_index(correct_answer):
        option_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
        return option_map.get(correct_answer.strip(), -1)

    # Display Questions in Styled Format
    for index, row in filtered_data.iterrows():
        st.markdown(f"""
        <div style="padding: 10px; border-radius: 10px; background-color: black;">
            <h4 style="color: white;">📘 {row['Topic']} Question {index + 1}:</h4>
            <p style="color: white;"><b>{row['Question']}</b></p>
        </div>
        """, unsafe_allow_html=True)

        # Split and display options
        options = row['Options'].split(";")
        option_labels = ["A", "B", "C", "D"]

        for i, option in enumerate(options):
            st.markdown(f"""
            <div style="
                border: 1px solid #e0e0e0;
                padding: 10px;
                border-radius: 8px;
                margin-bottom: 8px;
                background-color: black;
                color: white;">
            {option_labels[i]}. {option.strip()}
            </div>
            """, unsafe_allow_html=True)

        # Find correct option index
        correct_index = get_correct_option_index(row['Correct Answer'])

        # Answer section
        st.markdown(f"""
        <div style="
            margin-top: 20px;
            padding: 10px;
            background-color: #d1e7dd;
            border-radius: 8px;
            color: black;">
            ✅ <b>Answer:</b> {option_labels[correct_index]}. {options[correct_index].strip()}
        </div>
        <hr>
        """, unsafe_allow_html=True)

# Topic Stats Page
if page == "Topic Stats":
    # Calculate the number of questions for each topic
    topic_stats = data.groupby('Topic').agg(
        total_questions=('Question', 'count')
    ).reset_index()

    st.subheader("📊 Topic Statistics")
    st.table(topic_stats)
