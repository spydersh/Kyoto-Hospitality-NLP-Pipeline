-- 1. Drop existing tables to ensure a clean slate 
DROP TABLE IF EXISTS fact_topic_sentiment;
DROP TABLE IF EXISTS fact_reviews;
DROP TABLE IF EXISTS dim_topics;
DROP TABLE IF EXISTS dim_hotels;

-- 2. Build Table 1: Hotels
CREATE TABLE dim_hotels (
    hotel_id SERIAL PRIMARY KEY,
    hotel_name VARCHAR(255) NOT NULL,
    property_type VARCHAR(50) NOT NULL
);

-- 3. Build Table 2: Topics
CREATE TABLE dim_topics (
    topic_id INT PRIMARY KEY, 
    topic_name VARCHAR(100) NOT NULL,
    keywords TEXT
);

-- 4. Build Table 3: The Core Reviews
CREATE TABLE fact_reviews (
    review_id SERIAL PRIMARY KEY,
    hotel_id INT REFERENCES dim_hotels(hotel_id),
    review_date DATE NOT NULL,
    star_rating INT CHECK (star_rating >= 1 AND star_rating <= 5),
    review_text TEXT
);

-- 5. Build Table 4: The BERT Sentiment Engine
CREATE TABLE fact_topic_sentiment (
    sentiment_id SERIAL PRIMARY KEY,
    review_id INT REFERENCES fact_reviews(review_id),
    topic_id INT REFERENCES dim_topics(topic_id),
    bert_sentiment_score DECIMAL(5,4) NOT NULL, 
    sentiment_polarity VARCHAR(20) 
);