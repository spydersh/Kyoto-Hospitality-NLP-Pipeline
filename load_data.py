import pandas as pd
from sqlalchemy import create_engine

# 1. Database Connection Engine
db_user = 'XXXXX'
db_password = 'XXXXXX'
db_host = 'localhost'
db_port = '5432'
db_name = 'kyoto_tourism_db'

print("Connecting to the database...")
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

# 2. Read Processed CSV
print("Reading CSV data...")
df = pd.read_csv("processed_reviews_all (2).csv")

# 3. Build & Load: dim_hotels
print("Building Hotel Dimension Table...")
hotels_df = df[['Hotel_Name', 'Type']].drop_duplicates().reset_index(drop=True)
hotels_df.index += 1 # Start ID at 1
hotels_df['hotel_id'] = hotels_df.index
hotels_df = hotels_df.rename(columns={'Hotel_Name': 'hotel_name', 'Type': 'property_type'})

# Push to PostgreSQL
hotels_df[['hotel_id', 'hotel_name', 'property_type']].to_sql('dim_hotels', engine, if_exists='append', index=False)

# 4. Build & Load: dim_topics (Using the exact data from thesis)
print("Building Topic Dimension Table...")
topics_data = {
    'topic_id': [0, 1, 2, 3, 4],
    'topic_name': ['Staff & Service', 'Location & Access', 'Culture', 'Modern Standards', 'Amenities & Bath'],
    'keywords': [
        'hotel, kyoto, staff, stay, service',
        'hotel, kyoto, station, good, great',
        'ryokan, experience, stay, room, dinner',
        'room, hotel, good, service, hyatt',
        'room, japanese, breakfast, tea, bath'
    ]
}
topics_df = pd.DataFrame(topics_data)
topics_df.to_sql('dim_topics', engine, if_exists='append', index=False)

# 5. Map the relational IDs back to main dataset
print("Mapping relational IDs for Fact Tables...")
df = df.merge(hotels_df, left_on='Hotel_Name', right_on='hotel_name', how='left')

# Generate a unique review_id for all 6,042 reviews
df.reset_index(drop=True, inplace=True)
df.index += 1
df['review_id'] = df.index

# 6. Build & Load: fact_reviews
print("Loading Fact Reviews Table...")
fact_reviews_df = df[['review_id', 'hotel_id', 'Date', 'Rating', 'Text']].copy()
fact_reviews_df = fact_reviews_df.rename(columns={
    'Date': 'review_date',
    'Rating': 'star_rating',
    'Text': 'review_text'
})
fact_reviews_df.to_sql('fact_reviews', engine, if_exists='append', index=False)

# 7. Build & Load: fact_topic_sentiment
print("Loading Fact Sentiment Table...")
fact_sentiment_df = df[['review_id', 'Topic', 'Sentiment']].copy()
fact_sentiment_df = fact_sentiment_df.rename(columns={
    'Topic': 'topic_id',
    'Sentiment': 'bert_sentiment_score'
})

# Create a logical polarity column based on float scores
def get_polarity(score):
    if score > 0.05:
        return 'Positive'
    elif score < -0.05:
        return 'Negative'
    else:
        return 'Neutral'

fact_sentiment_df['sentiment_polarity'] = fact_sentiment_df['bert_sentiment_score'].apply(get_polarity)
fact_sentiment_df.to_sql('fact_topic_sentiment', engine, if_exists='append', index=False)

print("SUCCESS! All 6,042 reviews have been engineered into your PostgreSQL database.")