from kafka import KafkaConsumer
from pyspark.sql import SparkSession
from textblob import TextBlob
import json

# Initialize Spark
spark = SparkSession.builder.appName("NewsPipeline").getOrCreate()

# Kafka Consumer
consumer = KafkaConsumer(
    'news-articles',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Classification and Sentiment Functions
def classify(title):
    """ Classify articles based on title keywords """
    if "stock" in title.lower():
        return "Finance"
    elif "iphone" in title.lower() or "apple" in title.lower():
        return "Tech"
    elif "crash" in title.lower() or "inflation" in title.lower():
        return "Economy"
    else:
        return "General"

def sentiment(text):
    """ Analyze sentiment using TextBlob """
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return "Positive"
    elif analysis.sentiment.polarity < 0:
        return "Negative"
    else:
        return "Neutral"

# Collect and process data
data = []
for message in consumer:
    article = message.value
    category = classify(article['title'])
    sentiment_score = sentiment(article['content'])
    
    data.append((article['id'], article['title'], category, sentiment_score, article['timestamp']))

# Create Spark DataFrame
df = spark.createDataFrame(data, ["id", "title", "category", "sentiment", "timestamp"])

# Save the processed data to S3
output_path = f"s3a://{bucket_name}/processed_news"
df.write.mode("overwrite").csv(output_path)

print("✅ Processed data saved to S3")
