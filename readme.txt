📁 Project Structure
Data_pipeline/
├── cleaned_news_data.csv                 # Preprocessed news data
├── consumer.py                           # Kafka consumer (local, receives user input)
├── producer.py                           # Kafka producer (local, pushes data)
├── preprocessing.py                      # Data cleaning and sentiment tagging logic
├── data/
│   └── News_Articles.csv                 # Original dataset
├── Instructions/                         # Screenshot instructions for UI
├── news-sentiment-dashboard/            # Streamlit dashboard
│   ├── app.py                            # Main dashboard app
│   ├── config.toml                       # S3 and app settings
│   ├── requirements.txt                  # Dependencies
│   └── readme.md                         # Internal dashboard readme

⚙️ Key Components
1. Kafka Producer/Consumer (Local)
producer.py: Simulates or sends user-input articles to the Kafka topic.

consumer.py: Reads articles from Kafka and saves them for processing.

🔧 Runs on your local machine.

2. Preprocessing and Sentiment Analysis
preprocessing.py: Cleans the news data and adds a sentiment column using rule-based or ML logic.

Optionally runs on Databricks if needed for large-scale processing.

Saves results to an S3 bucket for access by the dashboard.

3. Streamlit Dashboard
Visualizes sentiment trends.

Includes word clouds, filtering by timestamp, and displays top positive/negative articles.

Loads sentiment data directly from your S3 bucket.

🖥️ Can be run locally with:

streamlit run news-sentiment-dashboard/app.py

🚀 Running the Project
Install requirements (locally):

pip install -r news-sentiment-dashboard/requirements.txt
Start Kafka Producer & Consumer:

python producer.py
python consumer.py
Preprocess data:

python preprocessing.py
Run Streamlit Dashboard:

streamlit run news-sentiment-dashboard/app.py
☁️ Cloud & Integration
Databricks (optional): Used for large-scale sentiment processing.

S3 Bucket: Stores CSV files with sentiment results.

config.toml: Holds bucket name, region, and access configuration.

📊 Dashboard Features
📅 Date range filter for articles
📈 Sentiment distribution (bar chart)
🟢 Top Positive Articles
🔴 Top Negative Articles
☁️ Word Cloud of Frequent Words

🧠 Future Enhancements
✅ Integrate ML model to predict sentiment from user inputs
⏱️ Add real-time updates via Kafka streams
🐳 Dockerize for deployment
Requirements
# Core dependencies
streamlit==1.32.2
pandas==2.2.1
numpy==1.26.4
matplotlib==3.8.3
wordcloud==1.9.3

# Kafka dependencies
kafka-python==2.0.2

# AWS S3 access
boto3==1.34.76
s3fs==2024.3.1
fsspec==2024.3.1

# Secret detection (optional for dev)
detect-secrets==1.4.0

# Spark support (optional for Databricks integration)
pyspark==3.5.1

To install all dependencies 
pip  install -r requirements.txt

get models to predict future unknown data
hinglish language
try to get model to predict on only english data and then try with hinglish data
you could get 100% and <70-80% accuracy\
can generate data by chatgpt

core ranking conference / journal