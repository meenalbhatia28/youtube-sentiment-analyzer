import pandas as pd
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from tqdm import tqdm

# Load CSV
df = pd.read_csv("data/comments.csv")

# Enable progress bar
tqdm.pandas()

# Load Hugging Face sentiment analysis pipeline
model_name = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# Map model labels to human-readable sentiment
label_map = {
    "LABEL_0": "NEGATIVE",
    "LABEL_1": "NEUTRAL",
    "LABEL_2": "POSITIVE"
}

# Analyze each comment
df["sentiment"] = df["text"].progress_apply(
    lambda text: label_map[classifier(text[:512])[0]["label"]]
)

# Save results
df.to_csv("data/comments_with_sentiment.csv", index=False)
print("✅ Sentiment analysis complete. Saved to data/comments_with_sentiment.csv")