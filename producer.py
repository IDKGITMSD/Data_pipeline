import boto3
import pandas as pd
from kafka import KafkaProducer
import json

# AWS S3 Config
s3_client = boto3.client('s3', region_name='ap-south-1')
bucket_name = 'news-articles-pipeline'
file_name = 'cleaned_news_data.csv'

# Read dataset from S3
response = s3_client.get_object(Bucket=bucket_name, Key=file_name)
df = pd.read_csv(response['Body'])

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Stream articles with the new schema
for _, row in df.iterrows():
    article = {
        'id': row['id'],
        'content': row['content'],
        'timestamp': str(row['timestamp']),
        'title': row['title']
    }
    producer.send('news-articles', article)
    print(f'Sent: {article}')
