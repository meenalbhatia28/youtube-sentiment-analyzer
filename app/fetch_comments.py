import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
import re
import pandas as pd
from googleapiclient.discovery import build
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from tqdm import tqdm
from urllib.parse import urlparse, parse_qs

# Initialize the sentiment analysis pipeline
model_name = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# Label mapping from model output
label_map = {
    "LABEL_0": "NEGATIVE",
    "LABEL_1": "NEUTRAL",
    "LABEL_2": "POSITIVE"
}

def extract_video_id(url):
    """Extract the video ID from a full YouTube URL."""
    parsed_url = urlparse(url)
    query = parse_qs(parsed_url.query)
    return query.get("v", [None])[0]

def fetch_comments_from_video(video_url, output_csv_path):
    video_id = extract_video_id(video_url)
    if not video_id:
        raise ValueError("Invalid YouTube URL")

    api_key = os.getenv("YOUTUBE_API_KEY")
    youtube = build("youtube", "v3", developerKey=api_key)

    comments = []
    next_page_token = None

    print("Fetching comments...")
    while True:
        response = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            pageToken=next_page_token,
            maxResults=100,
            textFormat="plainText"
        ).execute()

        for item in response["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]
            comments.append({
                "author": comment["authorDisplayName"],
                "text": comment["textDisplay"],
                "published_at": comment["publishedAt"]
            })

        next_page_token = response.get("nextPageToken")
        if not next_page_token or len(comments) >= 1000:
            break

    df = pd.DataFrame(comments)

    print("Analyzing sentiment...")
    tqdm.pandas()
    df["sentiment"] = df["text"].progress_apply(
        lambda text: label_map[classifier(text, truncation=True, max_length=512)[0]["label"]]
    )

    df.to_csv(output_csv_path, index=False)
    print(f"✅ Comments + sentiment saved to {output_csv_path}")
