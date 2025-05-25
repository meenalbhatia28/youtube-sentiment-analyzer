# youtube-sentiment-analyzer
Analyze YouTube comment sentiment using Transformers

## 💡 Motivation

Understanding public sentiment can reveal powerful insights — from brand feedback to social trends. This project uses real-world, user-generated data from YouTube and applies Natural Language Processing (NLP) to classify viewer reactions at scale.

## 🛠 Technologies Used

- **Python**: Core scripting language
- **Streamlit**: Interactive web dashboard
- **YouTube Data API v3**: Comment fetching
- **Transformers (Hugging Face)**: Sentiment classification using `cardiffnlp/twitter-roberta-base-sentiment`
- **Pandas & Matplotlib/Seaborn**: Data wrangling & visualization
- **dotenv**: Secure API key handling
- **WordCloud**: Visualization of common positive phrases

## ✅ Features

- 🔗 Enter any YouTube video link
- 📥 Fetch up to 1000 top-level comments
- 🤖 Analyze sentiment using a pre-trained Transformer model
- 📊 View:
  - Sentiment breakdown
  - Word cloud of positive comments
  - Time-series chart of sentiment trends
- 💬 View top positive/negative comments
- 📁 Download results as a CSV

## 📈 What I Learned / Built

- Developed a fully functional end-to-end machine learning pipeline on real-world data
- Worked with REST APIs and managed secure credentials via environment files
- Built a live dashboard to showcase NLP predictions in an interactive and visual way
- Practiced responsible handling of user-generated content (e.g., comment cleaning, API quota management)
- Improved project structuring for reusability and scalability

## ▶️ How to Run

### 1. Clone repo
```bash
git clone https://github.com/meenalbhatia28/youtube-sentiment-analyzer
cd youtube-sentiment-analyzer
```
### 2.  Create a Virtual Environment (optional but recommended)
```bash
python3 -m venv yt-sentiment-env
source yt-sentiment-env/bin/activate   # On macOS/Linux
# OR
yt-sentiment-env\Scripts\activate      # On Windows
```

### 3. Install the Dependencies
```bash
pip install -r requirements.txt
```

### 4. Add Your YouTube API Key
Create a file called .env in the root of the project with this line:
```bash
YOUTUBE_API_KEY=your_actual_api_key_here
```
**Don't have an API key?**  
- Go to the [Google Cloud Console](https://console.cloud.google.com/)  
- Enable **YouTube Data API v3** for your project  
- Create an API key under **APIs & Services > Credentials**  

### 5. Run the Streamlit App
```bash
streamlit run app/dashboard.py
```
Then open http://localhost:8501 in your browser.

## Project Structure
```bash
youtube-sentiment-analyzer/
│
├── .env.example           # Template for your API key
├── requirements.txt       # Python dependencies
├── data/                  # Output CSVs (ignored from Git)
└── app/
    ├── dashboard.py       # Streamlit UI
    └── fetch_comments.py  # Comment fetching + sentiment logic
```

## Author
## 👤 Author

**Meenal Bhatia**  
🎓 Final-year Computer Science student  
📍 Based in Winnipeg, Canada  
🔗 [LinkedIn](https://www.linkedin.com/in/meenal-bhatia-6b287b198/) • [GitHub](https://github.com/meenalbhatia28)
