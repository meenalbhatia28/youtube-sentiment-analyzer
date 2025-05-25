import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Load analyzed comments
df = pd.read_csv("data/comments_with_sentiment.csv")

# --- Sentiment Count Chart ---
sentiment_counts = df["sentiment"].value_counts()

plt.figure(figsize=(6, 4))
sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values)
plt.title("Sentiment Breakdown")
plt.xlabel("Sentiment")
plt.ylabel("Number of Comments")
plt.tight_layout()
plt.show()

# --- Word Cloud of Positive Comments ---
positive_text = " ".join(df[df["sentiment"] == "POSITIVE"]["text"])
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(positive_text)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Positive Comment Word Cloud")
plt.tight_layout()
plt.show()
