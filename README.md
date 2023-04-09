# hate_speech_detection


### Data Pipeline
Detailed in this repository is the data pipeline code for scraping posts and comment data from the reddit API and uploading it into a GCP cloud storage bucket. This data is then transformed from a standard .csv file to spark rdd, and finally stored into MongoDB Atlas as a collection. 

The kaggle data follows a similar process as well but in our case, we downloaded it directly instead of accessing through the kaggle API. It is uploaded to the GCP cloud storage bucket manually, and is stored in the MongoDB Atlas as a collection as well.

The whole process is automated through Apache Airflow where the reddit data will be scraped and run each day while the kaggle data is only uploaded once. The yaml file includes the needed libraries in the data pipeline.

**Please put all files in the "reddit_kaggle_data_pipeline" in the airflow/dags file in your local machine**

### Model training and text classification
We utilized the Databricks cluster and pyspark.sql and pyspark.ml libraries to prepreprocess the dataset and apply a Naive Bayes Classifier to do hate speech detection and offensive language detection.

### Data Preprocessing
The primary goal of data preprocessing is to make the dataset compatible with a Naive Bayes Classifier. To achieve this goal, we need to tokenize the tweets and embed words in each tweet into a vector of word counts. First we remove all null values from the tweets. For each tweet, we keep only English characters and numbers, and then split the string into words by space. Lastly, we remove the stop words and create word embeddings. 

We do some further data engineering on the label column. In general, modeling for binary classification yields a better performance than a multiclass classification. Therefore, we split the multiclass label column into two binary-class columns. We create two new columns: one called "hate speech" which is labeled 1 if the original label is "hate speech" and 0 otherwise, while the other called "offensive language" which is labeled 1 if the original label is "offensive language" and 0 otherwise. With these two new label columns, we are able to train two separate binary classification models against them respectively.

### Model Training and Evaluation
In this section we use our data to train two Naive Bayes Classifiers, one for each label column, and evaluate their performance by f1 score on the test data. We first split the preprocessed data into training and test set. For each of the "hate speech" and "offensive language" label columns, we fit a multinormial Naive Bayes Classifier on training data against the labels, and then compute the f1 score between predicted and true labels on the test set. The Naive Bayes Classifier produces an f1 score of 0.8707 when detecting hate speech and an f1 score of 0.9165 when detecting offensive language. Training the Naive Bayes Classifier and computing f1 score on test data for hate speech detection takes 4.13 seconds; training the Naive Bayes Classifier and computing f1 score on test data for offensive language detection takes 6.15 seconds.

### Conclusion
We notice that the model performance of Naive Bayes Classifier is in general good. An f1 score of 0.8707 for hate speech detection and 0.9165 for offensive language detection is more than acceptable for a text classification model. This reflects the fact that even though Naive Bayes classifiers
initializes with some assumptions, it performs well for text classification tasks and is a fast and efficient algorithm in practice.

This project of building a hate speech detection model on texts from social media enriches our experience in building an end-to-end machine learning pipeline. First of all we implemented a scalable and efficient pipeline architecture that can handle large volumes of data and complex multi-step processing tasks. We also learned the importance of data preprocessing and feature engineering in a machine learning project. The next step may be trying out different language models such as BERT and see how the Naive Bayes Classifier would perform on the Reddit comment data.
