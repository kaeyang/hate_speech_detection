from datetime import datetime
from google.cloud import storage
from mongodb import *
from pyspark.sql import Row, SparkSession

from user_definition import *


def retreive_reddit(spark, bucket_name, date):
    reddit_comments = (
        spark.read.format("csv")
        .option("header", True)
        .load(f"gs://{bucket_name}/reddit_data/{sub}_comments_{date}.csv")
    )
    reddit_posts = (
        spark.read.format("csv")
        .option("header", True)
        .load(f"gs://{bucket_name}/reddit_data/{sub}_posts_{date}.csv")
    )

    return reddit_posts, reddit_comments


def insert_aggregates_to_mongo():
    spark = SparkSession.builder.getOrCreate()
    conf = spark.sparkContext._jsc.hadoopConfiguration()
    conf.set("google.cloud.auth.service.account.json.keyfile",
             service_account_key_file)
    conf.set("fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")
    conf.set("fs.AbstractFileSystem.gs.impl",
             "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")

    today = datetime.now()

    reddit_posts, reddit_comments = retreive_reddit(
        spark, bucket_name, today.strftime("%Y-%m-%d"))

    # mongoDB comments collection
    mongodb_comments = MongoDBCollection(mongo_username,
                                         mongo_password,
                                         mongo_ip_address,
                                         database_name,
                                         collection_1_name)

    comment_aggregates = reddit_comments.rdd.map(lambda x: x.asDict())

    for aggregate in comment_aggregates.collect():
        print(aggregate)
        mongodb_comments.insert_one(aggregate)

    # mongoDB posts collection
    mongodb_posts = MongoDBCollection(mongo_username,
                                      mongo_password,
                                      mongo_ip_address,
                                      database_name,
                                      collection_2_name)

    posts_aggregates = reddit_posts.rdd.map(lambda x: x.asDict())

    for aggregate in posts_aggregates.collect():
        print(aggregate)
        mongodb_posts.insert_one(aggregate)


if __name__ == "__main__":
    insert_aggregates_to_mongo()
