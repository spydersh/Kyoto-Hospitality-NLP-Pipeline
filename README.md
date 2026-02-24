# Kyoto Luxury Hospitality: NLP Sentiment & Resilience Analytics

![Dashboard Preview](assets/Visualizing_Business_Intelligence.gif) 

## Executive Summary
As Kyoto faces the "Overtourism-Authenticity Paradox," destination management must transition from volume-based growth to value-based engagement. This project is an end-to-end data engineering and machine learning pipeline designed to decode the structural drivers of guest loyalty in Kyoto's luxury accommodation sector. 

By analyzing user-generated content, this project empirically proves that **Traditional Ryokans generate higher satisfaction and demonstrate greater resilience to seasonal overtourism** compared to Modern Luxury Hotels.

## The Tech Stack
* **Data Extraction:** Go (Concurrent Web Scraper)
* **Data Processing & NLP:** Python (Pandas, Scikit-Learn, Hugging Face Transformers)
* **Machine Learning:** BERT (Context-Aware Sentiment Analysis), Latent Dirichlet Allocation (Topic Modeling)
* **Database Engine:** PostgreSQL (Star Schema Architecture)
* **Business Intelligence:** Power BI, DAX

##  The Computational Pipeline
1. **Extraction:** Harvested a dataset of 6,042 English-language TripAdvisor reviews from Kyoto's Top 10 luxury properties (Ryokans and Hotels) using a high-performance Go scraper.
2. **NLP Pre-processing:** Tokenized and lemmatized unstructured text to prepare for machine learning models.
3. **Structural Analysis (LDA):** Deployed Latent Dirichlet Allocation to uncover 5 dominant thematic factors defining the guest experience, separating "Hardware" (facilities) from "Human-ware" (service hospitableness).
4. **Deep Learning Sentiment (BERT):** Applied a pre-trained BERT model to assign context-aware sentiment polarity scores to each review.
5. **Data Engineering:** Engineered a PostgreSQL relational database utilizing a Star Schema to separate dimensional lookup data (Hotels, Topics) from factual metrics (Reviews, BERT Scores).
6. **BI Visualization:** Connected the SQL database to Power BI to build an interactive dashboard tracking sentiment heatmaps and temporal resilience.

## Key Business Insights

### 1. The "Authenticity Premium"
Traditional Ryokans achieved a significantly higher mean satisfaction rating (4.83/5.0) compared to Modern Luxury Hotels (4.57/5.0). Deep learning sentiment confirms this is driven by "Service Hospitableness" (score: 0.42), which acts as a stronger predictor of 5-star loyalty than "Room Quality" (0.26). 

### 2. Overtourism Resilience
Temporal trend analysis reveals critical dips in "Value for Money" sentiment during peak crowding seasons (April Cherry Blossoms and November Autumn foliage). However, the highly immersive Ryokan model acts as a psychological buffer, demonstrating superior sentiment resilience during these high-stress periods compared to the standardized modern hotel experience. 

##  How to Run the Data Pipeline locally
1. Clone this repository.
2. Ensure PostgreSQL is running on `localhost:5432`.
3. Execute `schema.sql` via pgAdmin or DBeaver to construct the Star Schema.
4. Run `python load_data.py` to ingest the processed CSV data into the relational tables.
5. Open `Kyoto_Luxury_Hospitality.pbix` and refresh the data source to view the interactive visualizations.
