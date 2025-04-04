import streamlit as st
import pandas as pd
import gspread
import random
import plotly.express as px
import plotly.graph_objects as go
from oauth2client.service_account import ServiceAccountCredentials

# Set page config with dark theme
st.set_page_config(page_title="📚 MCQ Quiz", layout="wide", initial_sidebar_state="expanded")

# Apply dark theme with CSS
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .stButton button {
        background-color: #4B5DFF;
        color: white;
    }
    .stDataFrame {
        background-color: #262730;
    }
    .css-1d391kg {
        background-color: #262730;
    }
    div[data-testid="stSidebarNav"] {
        background-color: #1E1E1E;
    }
    .explanation-box {
        background-color: #1E2730;
        border-left: 3px solid #4B5DFF;
        padding: 10px;
        margin: 10px 0;
        border-radius: 5px;
    }
    .answer-box {
        background-color: #2D3748;
        padding: 10px;
        margin: 10px 0;
        border-radius: 5px;
        border-left: 3px solid #38A169;
    }
    hr {
        margin: 25px 0;
        border-color: #4A5568;
    }
    .metric-card {
        background-color: #1E2730;
        border-radius: 5px;
        padding: 15px;
        text-align: center;
        margin: 10px 0;
    }
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #4B5DFF;
    }
    .metric-label {
        font-size: 14px;
        color: #A0AEC0;
    }
</style>
""", unsafe_allow_html=True)

st.title("📚 MCQ Question Bank")

# Google Sheets Authentication using Service Account
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

try:
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
    spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1K2HJSL0U0vay4UaW4s3QPAIkQ_noj742ZRQJxbTTbQ0/edit?gid=0")
    worksheet = spreadsheet.get_worksheet(0)
    data = pd.DataFrame(worksheet.get_all_records())
    
except Exception as e:
    st.error(f"❌ Error connecting to Google Sheets: {str(e)}")
    st.stop()

# Function to map correct answers (A, B, C, D) to indexes (0, 1, 2, 3)
def get_correct_option_index(correct_answer):
    option_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
    return option_map.get(correct_answer.strip().upper(), -1)

# Normalize topic names and difficulty to handle duplicates
data['Topic'] = data['Topic'].str.strip().str.title()
data['Difficulty'] = data['Difficulty'].str.strip().str.title()

# Check if 'Domain' column exists, if not, create it based on Topic
if 'Domain' not in data.columns:
    # This is a placeholder. You might want to create a mapping of topics to domains
    # For now, we'll just use Topic as Domain
    data['Domain'] = data['Topic'].apply(lambda x: x.split()[0] if ' ' in x else x)

# Category classification - add a Category column if not present
if 'Category' not in data.columns:
    # This is a placeholder. You might want to create a mapping of topics to categories
    # For now, we'll derive it from the first part of the domain
    data['Category'] = data['Domain'].apply(lambda x: x.split()[0] if ' ' in x else x)

# Page selection
page = st.sidebar.selectbox("📑 Select a Page", ["Questions", "Topic Stats"])

if page == "Topic Stats":
    st.subheader("📊 MCQ Question Bank Analysis")
    
    # Key metrics in a row
    total_questions = len(data)
    total_topics = data['Topic'].nunique()
    total_domains = data['Domain'].nunique()
    total_categories = data['Category'].nunique()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{}</div>
            <div class="metric-label">Total Questions</div>
        </div>
        """.format(total_questions), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{}</div>
            <div class="metric-label">Topics</div>
        </div>
        """.format(total_topics), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{}</div>
            <div class="metric-label">Domains</div>
        </div>
        """.format(total_domains), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{}</div>
            <div class="metric-label">Categories</div>
        </div>
        """.format(total_categories), unsafe_allow_html=True)
    
    # Topic and difficulty distribution
    st.subheader("Topic & Difficulty Distribution")
    
    # Create pivot table for topics and difficulties
    topic_diff_pivot = pd.pivot_table(
        data, 
        index='Topic', 
        columns='Difficulty', 
        aggfunc='size',
        fill_value=0
    )
    
    # Calculate row totals and add the total column
    topic_diff_pivot['Total'] = topic_diff_pivot.sum(axis=1)
    
    # Sort by total
    topic_diff_pivot = topic_diff_pivot.sort_values('Total', ascending=False)
    
    # Remove columns with all zeros
    topic_diff_pivot = topic_diff_pivot.loc[:, (topic_diff_pivot != 0).any(axis=0)]
    
    # Display as table
    st.dataframe(topic_diff_pivot, use_container_width=True)
    
    # Domain-based analysis
    st.subheader("Domain Analysis")
    
    # Create domain statistics
    domain_stats = data.groupby('Domain').agg(
        questions=('Question', 'count'), 
        topics=('Topic', 'nunique'),
        avg_difficulty=('Difficulty', lambda x: 
            sum([{'Easy': 1, 'Medium': 2, 'Hard': 3}.get(d.title(), 0) for d in x]) / len(x)
                     if len(x) > 0 else 0),
        category=('Category', lambda x: x.mode()[0] if not x.mode().empty else 'Unknown')
    ).sort_values('questions', ascending=False)
    
    # Calculate difficulty distribution by domain
    domain_diff_pivot = pd.pivot_table(
        data, 
        index='Domain', 
        columns='Difficulty', 
        aggfunc='size',
        fill_value=0
    )
    
    # Remove columns with all zeros from domain_diff_pivot before merging
    domain_diff_pivot = domain_diff_pivot.loc[:, (domain_diff_pivot != 0).any(axis=0)]
    
    # Merge the two dataframes
    domain_analysis = domain_stats.merge(
        domain_diff_pivot, 
        left_index=True, 
        right_index=True, 
        how='left'
    ).fillna(0)
    
    # Round average difficulty to 2 decimal places
    domain_analysis['avg_difficulty'] = domain_analysis['avg_difficulty'].round(2)
    
    # Display domain analysis
    st.dataframe(domain_analysis, use_container_width=True)
    
    # Visualization section
    st.subheader("Visualizations")
    
    # Create columns for charts
    viz_col1, viz_col2 = st.columns(2)
    
    with viz_col1:
        # Topic distribution pie chart
        topic_counts = data['Topic'].value_counts().head(10)
        fig1 = px.pie(
            values=topic_counts.values,
            names=topic_counts.index,
            title='Top 10 Topics by Question Count',
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
        fig1.update_layout(
            legend_title="Topics",
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with viz_col2:
        # Difficulty distribution bar chart
        diff_counts = data['Difficulty'].value_counts()
        fig2 = px.bar(
            x=diff_counts.index,
            y=diff_counts.values,
            title='Question Distribution by Difficulty',
            labels={'x': 'Difficulty Level', 'y': 'Number of Questions'},
            color=diff_counts.values,
            color_continuous_scale='Blues'
        )
        fig2.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)
    
    # Domain to Topic Heatmap
    st.subheader("Domain to Topic Relationship")
    
    # Create a crosstab of Domain and Topic
    domain_topic_cross = pd.crosstab(data['Domain'], data['Topic'])
    
    # Remove empty columns from the domain_topic_cross
    domain_topic_cross = domain_topic_cross.loc[:, (domain_topic_cross != 0).any(axis=0)]
    
    # Create heatmap
    fig3 = px.imshow(
        domain_topic_cross, 
        labels=dict(x="Topic", y="Domain", color="Question Count"),
        color_continuous_scale='Blues',
        title='Domain to Topic Distribution Heatmap'
    )
    fig3.update_layout(height=500)
    st.plotly_chart(fig3, use_container_width=True)
    
    # Category Classification Table
    st.subheader("Category Classification")
    
    # Create classification table by Category
    category_classification = data.groupby(['Category']).agg(
        total=('Question', 'count'),
        topics=('Topic', 'nunique'),
        domains=('Domain', 'nunique'),
        avg_difficulty=('Difficulty', lambda x: 
            sum([{'Easy': 1, 'Medium': 2, 'Hard': 3}.get(d.title(), 0) for d in x]) / len(x)
                     if len(x) > 0 else 0)
    ).sort_values('total', ascending=False)
    
    # Round average difficulty
    category_classification['avg_difficulty'] = category_classification['avg_difficulty'].round(2)
    
    # Display category classification
    st.dataframe(category_classification, use_container_width=True)
    
    # Topic Classification Table
    st.subheader("Topic Classification")
    
    # Create classification table
    classification = data.groupby(['Topic']).agg(
        total=('Question', 'count'),
        domain=('Domain', lambda x: x.mode()[0] if not x.mode().empty else 'Unknown'),
        category=('Category', lambda x: x.mode()[0] if not x.mode().empty else 'Unknown'),
        medium=('Difficulty', lambda x: sum(1 for i in x if i.lower() == 'medium')),
        hard=('Difficulty', lambda x: sum(1 for i in x if i.lower() == 'hard'))
    ).sort_values('total', ascending=False)
    
    # Reorder columns
    classification = classification[['category', 'domain', 'total', 'medium', 'hard']]
    
    # Display classification table
    st.dataframe(classification, use_container_width=True)

elif page == "Questions":
    # Get unique topics and sort them
    topics = sorted(data['Topic'].unique())
    selected_topic = st.sidebar.selectbox("📌 Select a Topic", topics)
    
    # Filter by topic
    filtered_data = data[data['Topic'] == selected_topic]
    
    # Get unique difficulties for the selected topic
    difficulty_levels = ['All'] + sorted(filtered_data['Difficulty'].unique())
    selected_difficulty = st.sidebar.selectbox("🎚️ Select Difficulty", difficulty_levels)
    
    # Filter by difficulty if not 'All'
    if selected_difficulty != 'All':
        filtered_data = filtered_data[filtered_data['Difficulty'] == selected_difficulty]
    
    # Number of questions filter
    max_questions = len(filtered_data)
    num_questions = st.sidebar.slider("🔢 Number of Questions", 1, max_questions, min(10, max_questions))
    
    # Apply filters
    if len(filtered_data) > num_questions:
        filtered_data = filtered_data.sample(num_questions)
    else:
        filtered_data = filtered_data.head(num_questions)
    
    # Display questions
    st.subheader(f"Questions: {selected_topic} ({selected_difficulty})")
    
    for i, (index, row) in enumerate(filtered_data.iterrows(), 1):
        # Question container
        st.markdown(f"### Question {i}")
        st.markdown(f"{row['Question']}")
        
        # Options
        options = row['Options'].split(";")
        for i, option in enumerate(options):
            st.markdown(f"- {option.strip()}")
    
        # Find correct option index
        correct_index = get_correct_option_index(row['Correct Answer'])
        
        # Check if correct_index is valid
        if correct_index >= 0 and correct_index < len(options):
            st.markdown(f"""
            <div class="answer-box">
                ✅ <b>Answer:</b> {options[correct_index].strip()}
            </div>
            """, unsafe_allow_html=True)
            
            # Show explanation if available
            if 'Explanation' in row and pd.notna(row['Explanation']) and row['Explanation'].strip():
                st.markdown(f"""
                <div class="explanation-box">
                    📝 <b>Explanation:</b> {row['Explanation']}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error("❌ Error: Invalid correct answer index.")
        
        st.markdown("<hr>", unsafe_allow_html=True)
