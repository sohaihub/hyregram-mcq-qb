import streamlit as st
import gspread
import plotly.express as px
from oauth2client.service_account import ServiceAccountCredentials

# Page config
st.set_page_config(page_title="📚 MCQ Quiz", layout="wide", initial_sidebar_state="expanded")
st.title("📚 MCQ Question Bank")

# Google Sheets authentication
try:
    creds ={
  "type": "service_account",
  "project_id": "gen-lang-client-0825677129",
  "private_key_id": "6b650cb37df5576f8cb5c1f8f528c3211e3b6bf2",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDDWosoEheFQ1Mq\nS7BLwR9SZI5AMh7RzbjNUURI/xtzWO+CkPCpV146GjXfAIm3FBqbeyCIwCvVET6q\nts8TxhPrp9jBQGtepJt1sAwmlD1tqnvwT6bOvvPt9Zmc1/y9MhSSId6h+GaP14Bw\n4Uu8ilOqWw5KolsUd9+wExSxRunGwoR9lcsnEzdC3KOpIrxVXImZkq63fcvXN15u\nj92ihjP8jH4tU45csEPVMjruPkgnYnq6le2CVDKh+rtV3MMHqg5hedS/1T4U8OiN\n6daTmk95SUC3xmYgOzEsG+gk/HvpS84H1Mm4F+ZSDcY82adX0kPDupvyFCu8VzNy\nTXQwR5hvAgMBAAECggEAQUW8EE/3Nuo3W/79MVqeRg/eLdnxTUWxFT0tlTxT5jcV\nk+ks2FAeZkiCrnfGC/t2JnQ9+yNGogMIjs7VIvTAjDFBbdTB61YRsYF4ld1bJwzb\nK4DZqePIqj4xLORICMk2cVtKwZC3aCFnw4+rmBwZ92ZEQLC9wPmKrpC5jcA1dVjM\nlUpEYku1P0VCs50E9gqm3AnZGiFZn2gQffSOQ5DAA5cr+MHAlcjYLV/7rti11frV\nYOGc0QTvjpVJYz/tdY9MF7XrS0P2nyroU+ifuW1l/ojWVkjvojusazyBZyThGQXL\nyFGFIGsWVCjtZGdqRfYF4JCUheiLU+t35QXT++JjKQKBgQDnwf7c53+OKE1DWTXI\n10zX/sKKrWgfTDLM82y+aVY2AJv4ddKwC4BVr/mkBFpiO1Fzm6+XJq4UbysJ03ji\njA1vfvtvJAdpI54/1PB9U956ZDTH+aV90nSMf5FPQEqjFKkg3BUukDgm/jfAJJBP\nflA6kzRIQxrSyBfQJolcrr+iVwKBgQDXybg93LfR3rPyCjdnQRwdzphct4BNmUpI\nKuWIN6NlsgQoBv4aO3LuTPfPV2fEwkUSOva1Qb0zW9GX72pH8Ocl3fOja/ZOiZh7\njSPKZ2e2PiJhIDMiZ7/X4ALb9L+vpRuM3KgMuKIcREdENdHd23T0q84XDJNsjd+V\na6ZuniPbqQKBgFSJ3U/zWgIfDV/90LK8Zpl7orc3Xf3cq8M7IHWssvfr7PkK8Zmp\n+FxJXsTHmbivbpy/M6PtRh7KFmb1LulksRn0tf7qo5FknrsmD7uHtmXq253+oLFu\n7Xi6p+TCzPcD+FW2MjvT+8etf+Sk8cctilJzk+SwJb6xoo4ZII4gaGLtAoGBAJLj\n2esiiG7wroWgtr4u8DjKHaVftJMeOhaOPNlRJoVffLzSpb6toTreYgJeeWDS7bnP\nMYmJSoXfhvlqHGsEbhS01dj08SHdQFM6bJandU31VenPxX8yKMGG1+tq2+Fw/yQQ\nQMUIGjIruGeSS14+uYqkORIvmVtX6E8KjKzYMYihAoGBAJuD4B/Xa+KBftwAtzTt\n/yknB04zJqsxzkIgR4M9beVZQYV6WWEl52kv+eI6xgO0LiV41CAGhwQXg0wf/48F\nu70MiG40Lg9NVUQWQnxEdHw7VINu4jdEDbBaN+0fV4CNIZjc1ALWI/jUMMu4mExl\nTggZc56ircRw+JTT++KgNCg+\n-----END PRIVATE KEY-----\n",
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

    # Count topics
    topic_count = {}
    difficulty_count = {}

    for row in raw_records:
        topic = row.get("Topic", "Unknown").strip().title()
        diff = row.get("Difficulty", "Unknown").strip().title()

        topic_count[topic] = topic_count.get(topic, 0) + 1
        difficulty_count[diff] = difficulty_count.get(diff, 0) + 1

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
