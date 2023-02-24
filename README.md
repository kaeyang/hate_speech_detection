# hate_speech_detection


### Data Pipeline
Detailed in this repository is the data pipeline code for scraping posts and comment data from the reddit API and uploading it into a GCP cloud storage bucket. This data is then transformed from a standard .csv file to spark rdd, and finally stored into MongoDB Atlas as a collection. 

The kaggle data follows a similar process as well but in our case, we downloaded it directly instead of accessing through the kaggle API. It is uploaded to the GCP cloud storage bucket manually, and is stored in the MongoDB Atlas as a collection as well.

The whole process is automated through Apache Airflow where the reddit data will be scraped and run each day while the kaggle data is only uploaded once. The yaml file includes the needed libraries in the data pipeline.

**Please put all files in the "reddit_kaggle_data_pipeline" in the airflow/dags file in your local machine**