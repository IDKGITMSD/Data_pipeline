import pandas as pd

# Code used to find encoding of News_Articles.csv
# import chardet
# with open('data/News_Articles.csv', 'rb') as f:
#     result = chardet.detect(f.read())
# print(result['encoding'])


# load dataset
df = pd.read_csv("data/News_Articles.csv", encoding='windows-1252')

# inspect first few rows
#df = df.drop('NewsType', axis='columns')
#df.insert(0, 'index', range(0,len(df)))
print(df.columns)
print(df.head())

# Rename columns to match your schema
df.rename(columns={
    'index': 'id',
    'Heading': 'title',
    'Article': 'content',
    'Date': 'timestamp'
}, inplace=True)

# Ensure all fields are in the correct format
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Save the cleaned dataset
df.to_csv('cleaned_news_data.csv', index=False)

print("✅ Dataset cleaned and saved as cleaned_news_data.csv")