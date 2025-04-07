import streamlit as st
import pandas as pd
import boto3
from io import StringIO
import matplotlib.pyplot as plt
import os

# ✅ AWS S3 Configuration
AWS_ACCESS_KEY = os.environ.get('AWS_DATAPIPE_ACCESS_KEY')
AWS_SECRET_KEY = os.environ.get('AWS_DATAPIPE_SECRET_KEY')
BUCKET_NAME = "news-articles-pipeline"
RESULTS_PATH = "sentiment_results/"

# ✅ Function to Load Data from S3
def load_data_from_s3():
    """Function to load CSV data from S3 into a Pandas DataFrame"""
    
    # Connect to S3
    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )

    # List objects in the sentiment_results folder
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=RESULTS_PATH)

    # Initialize list for DataFrames
    dfs = []

    # Loop through each CSV file
    for obj in response.get('Contents', []):
        if obj['Key'].endswith('.csv'):
            obj_key = obj['Key']
            obj_response = s3.get_object(Bucket=BUCKET_NAME, Key=obj_key)
            
            # Read and load CSV into Pandas DataFrame
            csv_body = obj_response['Body'].read().decode('utf-8')

            # Handle bad lines gracefully
            try:
                df = pd.read_csv(StringIO(csv_body), on_bad_lines='skip')
                dfs.append(df)
            except Exception as e:
                st.error(f"Error loading {obj_key}: {str(e)}")

    # Combine all CSVs into a single DataFrame
    if dfs:
        sentiment_df = pd.concat(dfs, ignore_index=True)
    else:
        sentiment_df = pd.DataFrame()

    return sentiment_df


# ✅ Load the data
st.title("📰 News Article Sentiment Analysis Dashboard")

# Load data from S3
df = load_data_from_s3()

if df.empty:
    st.warning("No data found in S3 bucket. Please check your AWS credentials and data.")
else:
    # ✅ Display raw data
    st.write("### Raw Data Preview")
    st.dataframe(df.head())

    # ✅ Sentiment Distribution
    st.write("### Sentiment Distribution")
    sentiment_counts = df['sentiment'].value_counts()

    fig, ax = plt.subplots(figsize=(10, 5))
    sentiment_counts.plot(kind='bar', color=['green', 'red', 'gray'], ax=ax)
    plt.title('Sentiment Distribution')
    plt.xlabel('Sentiment')
    plt.ylabel('Frequency')
    st.pyplot(fig)

    # ✅ Filter Top Positive and Negative Articles
    st.write("### 🔥 Top Articles by Sentiment")

    # Top 5 Positive Articles
    st.write("🟢 **Top 5 Positive Articles:**")
    top_positive = df[df['sentiment'] == 'positive'].head(5)
    st.dataframe(top_positive[['title', 'content']])

    # Top 5 Negative Articles
    st.write("🔴 **Top 5 Negative Articles:**")
    top_negative = df[df['sentiment'] == 'negative'].head(5)
    st.dataframe(top_negative[['title', 'content']])

    # ✅ Filter by Date Range
    st.write("### 📅 Filter by Date Range")
   # 🚀 Graceful Timestamp Parsing and Filtering

# ✅ Function to handle invalid timestamps safely
def parse_timestamp_safe(ts):
    """Try parsing timestamp safely, return NaT if invalid"""
    try:
        return pd.to_datetime(ts, errors='coerce')  # Assign NaT to invalid timestamps
    except Exception:
        return pd.NaT

# ✅ Apply the parsing function to the `timestamp` column
df['timestamp'] = df['timestamp'].apply(parse_timestamp_safe)

# ✅ Filter out invalid timestamps
df = df[df['timestamp'].notna()]  # Keep only valid timestamps

# 🚀 Date Range Filtering
st.subheader("📅 Filter by Date Range")

# ✅ Date range selector
min_date = df['timestamp'].min()
max_date = df['timestamp'].max()

start_date = st.date_input("Start date", min_date)
end_date = st.date_input("End date", max_date)

# ✅ Filter by date
mask = (df['timestamp'] >= pd.to_datetime(start_date)) & (df['timestamp'] <= pd.to_datetime(end_date))
filtered_df = df[mask]

# ✅ Display filtered articles
st.write(f"✅ Showing articles from {start_date} to {end_date}")
st.dataframe(filtered_df[['title', 'content', 'sentiment', 'timestamp']])

# 🚀 Sentiment Distribution Visualization
st.subheader("📊 Sentiment Distribution")

# ✅ Count sentiment occurrences
sentiment_counts = filtered_df['sentiment'].value_counts()

# ✅ Plotting the distribution
fig, ax = plt.subplots()
ax.bar(sentiment_counts.index, sentiment_counts.values, color=['green', 'red', 'gray'])
ax.set_title('Sentiment Distribution')
ax.set_xlabel('Sentiment')
ax.set_ylabel('Frequency')
st.pyplot(fig)

# 🚀 Word Cloud Visualization
st.subheader("☁️ Most Frequent Words in Articles")

from wordcloud import WordCloud

# ✅ Combine content into a single string
text = " ".join(content for content in filtered_df['content'].dropna())

# ✅ Generate Word Cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

# ✅ Display Word Cloud
fig, ax = plt.subplots(figsize=(12, 6))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis('off')
st.pyplot(fig)

# 🚀 Streamlit App Completion
st.success("✅ App execution complete! 🎯")
