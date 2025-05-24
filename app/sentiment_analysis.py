import pandas as pd
from transformers import pipeline
from tqdm import tqdm

# Load CSV
df = pd.read_csv("data/comments.csv")

# Load Hugging Face sentiment analysis pipeline
classifier = pipeline("sentiment-analysis")

# Analyze each comment
tqdm.pandas()  # adds progress bar
df["sentiment"] = df["text"].progress_apply(lambda text: classifier(text[:512])[0]['label'])

# Save results
df.to_csv("data/comments_with_sentiment.csv", index=False)
print("✅ Sentiment analysis complete. Saved to data/comments_with_sentiment.csv")
