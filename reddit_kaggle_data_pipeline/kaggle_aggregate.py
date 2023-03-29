from google.cloud import storage
from mongodb import *
from pyspark.sql import Row, SparkSession

from user_definition import *


def retreive_kaggle(spark, bucket_name):
    '''Retrieves the kaggle data from GCP'''
    kaggle_data = (
        spark.read.format("csv")
        .option("header", True)
        .load(f"gs://{bucket_name}/kaggle_data.csv")
    )

    return kaggle_data


def insert_aggregates_to_mongo():
    '''Converts csv data from GCP into MongoDB collections and insert them into MongoDB Atlas'''
    spark = SparkSession.builder.getOrCreate()
    conf = spark.sparkContext._jsc.hadoopConfiguration()
    conf.set("google.cloud.auth.service.account.json.keyfile",
             service_account_key_file)
    conf.set("fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")
    conf.set("fs.AbstractFileSystem.gs.impl",
             "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")

    kaggle_data = retreive_kaggle(spark, bucket_name)

    # mongoDB kaggle collection
    mongodb_posts = MongoDBCollection(mongo_username,
                                      mongo_password,
                                      mongo_ip_address,
                                      database_name,
                                      collection_3_name)

    kaggle_aggregates = kaggle_data.rdd.map(lambda x: x.asDict())

    for aggregate in kaggle_aggregates.collect():
        print(aggregate)
        mongodb_posts.insert_one(aggregate)


if __name__ == "__main__":
    insert_aggregates_to_mongo()
