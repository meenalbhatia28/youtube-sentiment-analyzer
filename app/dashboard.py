import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import os
import uuid
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

from fetch_comments import fetch_comments_from_video

st.set_page_config(layout="wide")
st.title("📺 YouTube Sentiment Dashboard")

video_url = st.text_input("Paste YouTube Video URL")

if st.button("Fetch & Analyze"):
    if video_url:
        with st.spinner("Fetching comments and analyzing sentiment..."):
            video_id = str(uuid.uuid4())[:8]
            csv_path = f"data/comments_{video_id}.csv"

            fetch_comments_from_video(video_url, csv_path)

            st.session_state["latest_csv"] = csv_path
            st.success("✅ Comments fetched and saved!")
    else:
        st.warning("⚠️ Please enter a valid YouTube URL.")

existing_csvs = [f for f in os.listdir("data") if f.startswith("comments") and f.endswith(".csv")]
if existing_csvs:
    selected_csv = st.selectbox("Choose a video dataset to analyze:", existing_csvs)
    df = pd.read_csv(os.path.join("data", selected_csv))

    # 📊 Sentiment Summary
    st.subheader("📊 Sentiment Distribution")
    total = len(df)
    st.metric("Total Comments", total)
    for label in ["POSITIVE", "NEUTRAL", "NEGATIVE"]:
        count = df["sentiment"].value_counts().get(label, 0)
        st.metric(label, f"{count} ({(count/total)*100:.1f}%)")

    # 📈 Bar Chart
    sentiment_counts = df["sentiment"].value_counts()
    fig, ax = plt.subplots()
    sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, ax=ax)
    ax.set_ylabel("Number of Comments")
    st.pyplot(fig)

    # ☁️ Word Cloud
    st.subheader("☁️ Word Cloud (Positive Comments)")
    pos_text = " ".join(df[df["sentiment"] == "POSITIVE"]["text"])
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(pos_text)
    fig2, ax2 = plt.subplots()
    ax2.imshow(wordcloud, interpolation="bilinear")
    ax2.axis("off")
    st.pyplot(fig2)

    # 📈 Sentiment Over Time
    st.subheader("📈 Sentiment Over Time")
    df["published_at"] = pd.to_datetime(df["published_at"])
    time_sentiment = df.groupby([df["published_at"].dt.date, "sentiment"]).size().unstack().fillna(0)
    st.line_chart(time_sentiment)

    # 💬 Top Comments
    st.subheader("👍 Top Positive Comments")
    st.dataframe(df[df["sentiment"] == "POSITIVE"].head(5)[["author", "text"]])

    st.subheader("👎 Top Negative Comments")
    st.dataframe(df[df["sentiment"] == "NEGATIVE"].head(5)[["author", "text"]])

    # 📥 CSV Download Link
    def get_csv_download_link(dataframe):
        csv = dataframe.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="sentiment_results.csv">📥 Download CSV</a>'
        return href

    st.markdown(get_csv_download_link(df), unsafe_allow_html=True)

else:
    st.info("ℹ️ No comment datasets available yet. Paste a YouTube URL and click Fetch.")
