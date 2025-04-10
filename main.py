import streamlit as st
import gspread
import plotly.express as px
from oauth2client.service_account import ServiceAccountCredentials

# Page config
st.set_page_config(page_title="📚 MCQ Quiz", layout="wide", initial_sidebar_state="expanded")
st.title("📚 MCQ Question Bank")

# Google Sheets authentication
try:
    creds = {
        "type": "service_account",
        "project_id": "gen-lang-client-0825677129",
        "private_key_id": "65f8068623bb08e2a09f82daf250edad3daf20fe",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCtYR/SqwX0Amy7\n0VUaHe0x01B20FPgQQvFTXLxgNdTk6g2wIcj997NQ2I3gboV5htkax18NBQZ6KZy\ng7il4e9oQYa7VBaEXyqgDKrrFlpzt+KHGzQLF0jdRbWJuL5U4hBFpoHIr5vC7Oc6\ny6uKRHRqhGuYWV5BBx4EGtWsFRQ5JXuJDiF64wioh170xAAsEgnKIcpjg3kG1c+n\n3BruIsP0p5hbM5azCTpdVHbBL7F/RCYqULgov6LrrYXsAbgXaISYdbs0msUpp2ze\nFlGqOA5ywHgRDOj/vzf2C1UG0aNODi+gfndxkkTV5+//eq/n5+DZk11hxJ8VuOZp\nNcGReau3AgMBAAECggEAFsfTKZgFETmcVdU8bFEQUGKmiOX4j1ecl1EE0EyQfk/B\nY2hKmWRBJxE6f3aRH717TedxGVeyaHEUJam/AjS8gyNQ854p0zy52guwDXGDcv7v\nSbc+UFK/5Sr6nlzizT5iyvQEy3yfZ64+94+5O1KhRTme9YaQhtTLkdiAyLqATL2z\nnIq2gmKjyCz2KviaaGF5OvyEHOrl38UQMxkBjbE1muxJGPa3CXsbH4JxdSeoljc+\nJFc1LRqFzasdamWxIWL02pGWFWyIZw9iwyKmGD5paB44hS3p5XRhEC3deMiPuLHi\nuSO9XHEgsq48Jv7GolQJaEx1xEs+r1k6O1BUA+ccyQKBgQDd5EqdYwKQLWbgSFU8\nHyYiS2mvYBSFqpE33dpgCkbYigBD/SKHXuHnBd535LYScplYv8EIaUlYN8qICYF5\ngdjibM3LX8l4OlQQKQUp3FUQlYDwyI4WXjxDdAI2YIqq1RFEJ5/GQU/XuN0Q/14J\nmLYIFjrjDDGYAhvmXkMqKXkacwKBgQDIB9AANe3I0Lm9X/m1uKv/Yj70h9kPpJn6\nCj70CfquQl+fISgZo5Yb7/xYAIDxQUsXwI7eUxt4oQLMuhDVKVBNfEx/3rqXqDB+\nrCprLJ6JAwuaFwrgNNAHMO+XsDxP/Qcp/gs93NqbYMw8dn8f3q28sENl1Ar8iOX/\nlKrYNaMErQKBgQCXwYjed1bLcKHJhu70fYFBNz6CuT2P5YYIJW0y/hRSCKAB3+B7\noQLzU+pBKWT03PfP4OWOcSO+d/nGbGnmxk2lHjDphQtvdMUFgGiNpqlu/DEBfMjg\nt3aT04Wn1wM/rxVt/YOivgxzR3W6KE0SVyU4BqwjmLVadybJuXJKJa8zzQKBgQDG\npqOWIfik700W2kLGisEdnjdBZ8xUcbaNEDHW8DYpazdFdIs7cy93TU1BJDbp4Vsv\nGoeIGeb1VInQQZTH7QCYAzKB5vNN+7U1h8uUpjpHfWO/QtUFNs3F5n57GYW8NmAv\n/uCxLi1YE7ig71lukBnggvhcH0pN47LusHk+wX3E/QKBgHQP6jf1iALdJm7fEnPu\nY6BdUP8Sl0Ps/1QN5/9ZyqczCsVLd5G6XXEgDhUESTHsYMIMNfEEfjuaNtKd8d1Q\nVA9ot2yW/IqKGDpdBRWEHmFFJI2c4X812RTFbibS6FjvgLY+CR2ee7uh0WKEGcyf\ntiYUBwODxZRuycZYl3eOICdP\n-----END PRIVATE KEY-----\n",
        "client_email": "data-774@gen-lang-client-0825677129.iam.gserviceaccount.com",
        "client_id": "101552404875723380663",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/data-774%40gen-lang-client-0825677129.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    }
    client = gspread.service_account_from_dict(creds)
    spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1K2HJSL0U0vay4UaW4s3QPAIkQ_noj742ZRQJxbTTbQ0")
    worksheet = spreadsheet.get_worksheet(0)
    raw_records = worksheet.get_all_records()
except Exception as e:
    st.error(f"❌ Error connecting to Google Sheets: {str(e)}")
    st.stop()

# Page selection
page = st.sidebar.selectbox("📑 Select a Page", ["Topic Stats", "Questions"])

# Difficulty map for sorting if needed
diff_map = {'Easy': 1, 'Medium': 2, 'Hard': 3}

if page == "Topic Stats":
    st.subheader("📊 Overview")

    total = len(raw_records)
    st.markdown(f"### ✅ Total Questions: {total}")

    # Count topics and difficulties
    topic_count = {}
    difficulty_count = {}

    for row in raw_records:
        topic = row.get("Topic", "Unknown").strip().title()
        diff = row.get("Difficulty", "Unknown").strip().title()
        topic_count[topic] = topic_count.get(topic, 0) + 1
        difficulty_count[diff] = difficulty_count.get(diff, 0) + 1

    # Number of unique topics
    st.markdown(f"### 📌 Total Topics: {len(topic_count)}")

    # Topic-wise count table
    topic_table = [{"Topic": k, "Questions": v} for k, v in sorted(topic_count.items(), key=lambda x: x[1], reverse=True)]
    st.table(topic_table)

    # Pie chart - top topics
    top_topics = dict(sorted(topic_count.items(), key=lambda x: x[1], reverse=True)[:10])
    fig1 = px.pie(names=list(top_topics.keys()), values=list(top_topics.values()), title="Top 10 Topics")
    st.plotly_chart(fig1, use_container_width=True)

    # Bar chart - difficulty
    fig2 = px.bar(
        x=list(difficulty_count.keys()),
        y=list(difficulty_count.values()),
        labels={'x': 'Difficulty', 'y': 'Questions'},
        title='Difficulty Distribution',
        color=list(difficulty_count.values()),
        color_continuous_scale='Blues'
    )
    fig2.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig2, use_container_width=True)

elif page == "Questions":
    # Get unique topics
    topics = sorted(set(row.get("Topic", "Unknown").strip().title() for row in raw_records))
    selected_topic = st.sidebar.selectbox("📌 Select Topic", topics)

    # Filter by topic
    filtered = [r for r in raw_records if r.get("Topic", "").strip().title() == selected_topic]

    # Get difficulty levels in selected topic
    diff_levels = sorted(set(r.get("Difficulty", "Unknown").strip().title() for r in filtered))
    selected_diff = st.sidebar.selectbox("🎚️ Select Difficulty", ["All"] + diff_levels)

    if selected_diff != "All":
        filtered = [r for r in filtered if r.get("Difficulty", "").strip().title() == selected_diff]

    for idx, row in enumerate(filtered, 1):
        st.markdown(f"### Question {idx}")
        st.write(row.get("Question", "N/A"))

        options = row.get("Options", "").split(";")
        for opt in options:
            st.markdown(f"- {opt.strip()}")

        correct = row.get("Correct Answer", "").strip().upper()
        opt_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
        if correct in opt_map and opt_map[correct] < len(options):
            st.success(f"✅ Answer: {options[opt_map[correct]].strip()}")
        else:
            st.error("❌ Invalid Answer")

        st.markdown("---")
