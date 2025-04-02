import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets Authentication using Service Account
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

try:
    # Direct credentials
    creds = {
        "type": "service_account",
        "project_id": "gen-lang-client-0825677129",
        "private_key_id": "65f8068623bb08e2a09f82daf250edad3daf20fe",
        "private_key": """-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCtYR/SqwX0Amy7
0VUaHe0x01B20FPgQQvFTXLxgNdTk6g2wIcj997NQ2I3gboV5htkax18NBQZ6KZy
g7il4e9oQYa7VBaEXyqgDKrrFlpzt+KHGzQLF0jdRbWJuL5U4hBFpoHIr5vC7Oc6
y6uKRHRqhGuYWV5BBx4EGtWsFRQ5JXuJDiF64wioh170xAAsEgnKIcpjg3kG1c+n
3BruIsP0p5hbM5azCTpdVHbBL7F/RCYqULgov6LrrYXsAbgXaISYdbs0msUpp2ze
FlGqOA5ywHgRDOj/vzf2C1UG0aNODi+gfndxkkTV5+//eq/n5+DZk11hxJ8VuOZp
NcGReau3AgMBAAECggEAFsfTKZgFETmcVdU8bFEQUGKmiOX4j1ecl1EE0EyQfk/B
Y2hKmWRBJxE6f3aRH717TedxGVeyaHEUJam/AjS8gyNQ854p0zy52guwDXGDcv7v
Sbc+UFK/5Sr6nlzizT5iyvQEy3yfZ64+94+5O1KhRTme9YaQhtTLkdiAyLqATL2z
nIq2gmKjyCz2KviaaGF5OvyEHOrl38UQMxkBjbE1muxJGPa3CXsbH4JxdSeoljc+
JFc1LRqFzasdamWxIWL02pGWFWyIZw9iwyKmGD5paB44hS3p5XRhEC3deMiPuLHi
uSO9XHEgsq48Jv7GolQJaEx1xEs+r1k6O1BUA+ccyQKBgQDd5EqdYwKQLWbgSFU8
HyYiS2mvYBSFqpE33dpgCkbYigBD/SKHXuHnBd535LYScplYv8EIaUlYN8qICYF5
gdjibM3LX8l4OlQQKQUp3FUQlYDwyI4WXjxDdAI2YIqq1RFEJ5/GQU/XuN0Q/14J
mLYIFjrjDDGYAhvmXkMqKXkacwKBgQDIB9AANe3I0Lm9X/m1uKv/Yj70h9kPpJn6
Cj70CfquQl+fISgZo5Yb7/xYAIDxQUsXwI7eUxt4oQLMuhDVKVBNfEx/3rqXqDB+
rCprLJ6JAwuaFwrgNNAHMO+XsDxP/Qcp/gs93NqbYMw8dn8f3q28sENl1Ar8iOX/
lKrYNaMErQKBgQCXwYjed1bLcKHJhu70fYFBNz6CuT2P5YYIJW0y/hRSCKAB3+B7
oQLzU+pBKWT03PfP4OWOcSO+d/nGbGnmxk2lHjDphQtvdMUFgGiNpqlu/DEBfMjg
t3aT04Wn1wM/rxVt/YOivgxzR3W6KE0SVyU4BqwjmLVadybJuXJKJa8zzQKBgQDG
pqOWIfik700W2kLGisEdnjdBZ8xUcbaNEDHW8DYpazdFdIs7cy93TU1BJDbp4Vsv
GoeIGeb1VInQQZTH7QCYAzKB5vNN+7U1h8uUpjpHfWO/QtUFNs3F5n57GYW8NmAv
/uCxLi1YE7ig71lukBnggvhcH0pN47LusHk+wX3E/QKBgHQP6jf1iALdJm7fEnPu
Y6BdUP8Sl0Ps/1QN5/9ZyqczCsVLd5G6XXEgDhUESTHsYMIMNfEEfjuaNtKd8d1Q
VA9ot2yW/IqKGDpdBRWEHmFFJI2c4X812RTFbibS6FjvgLY+CR2ee7uh0WKEGcyf
tiYUBwODxZRuycZYl3eOICdP
-----END PRIVATE KEY-----""",
        "client_email": "data-774@gen-lang-client-0825677129.iam.gserviceaccount.com",
        "client_id": "101552404875723380663",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/data-774%40gen-lang-client-0825677129.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
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
