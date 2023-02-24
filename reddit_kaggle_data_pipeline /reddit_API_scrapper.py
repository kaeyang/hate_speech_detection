import pandas as pd
from datetime import datetime, date
import praw
from praw.models import MoreComments
from google.cloud import storage

from user_definition import *

# set this for airflow errors. https://github.com/apache/airflow/discussions/24463
os.environ["no_proxy"] = "*"


def create_reddit_instance():
    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret, user_agent=user_agent)
    return reddit


def create_subreddit_df(subreddit, post_num, reddit):
    '''
    Functionality:
        For the given subreddit, create a dataframe with info of the top # of hottest posts in subreddit

    Arguments:
        subreddit = Specific subreddit you want to scrape through.
        post_num = number of top posts you want to grab.

    Output:
        A dataframe that stores the title, score, id, subreddit name, url, number of comments, body, 
        and time it was created of post(s).
    '''
    # Create reddit instance

    posts = []
    ml_subreddit = reddit.subreddit(subreddit)
    for post in ml_subreddit.hot(limit=post_num):
        posts.append([post.title, post.score, post.id, post.subreddit,
                      post.url, post.num_comments, post.selftext, post.created])
    posts = pd.DataFrame(posts, columns=[
                         'title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
    # Convert create time to datetime PST
    posts['created'] = pd.to_datetime(posts['created'], unit='s', utc=True).map(
        lambda x: x.tz_convert('US/Pacific'))
    return posts


def create_comment_df(df, reddit):
    '''
    Functionality:
        From the create_subreddit_df() function, take in the "id" from the post, then extract all comments from post.

    Arguments:
        df = top # of hottest posts in subreddit.

    Output:
        A dataframe that has the post id, and every comment in it. Post_id would be like a primary key in case 
        you want to join the subreddit dataframe.
    '''
    id_list = []
    comment_list = []

    for post_id in df['id']:
        submission = reddit.submission(id=post_id)
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            id_list.append(post_id)
            comment_list.append(comment.body)

    comment_df = pd.DataFrame({"post_id": id_list, "comment": comment_list})
    return comment_df


def write_csv_to_gcs(bucket_name, blob_name, service_account_key_file, df):
    """Write and read a blob from GCS using file-like IO"""
    storage_client = storage.Client.from_service_account_json(
        service_account_key_file)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    with blob.open("w") as f:
        df.to_csv(f, index=False)


def reddit_scrape_upload():
    today = datetime.now()
    reddit = create_reddit_instance()

    posts_df = create_subreddit_df(sub, num_posts, reddit)
    comment_df = create_comment_df(posts_df, reddit)

    posts_blob_name = f'reddit_data/{sub}_posts_{today.strftime("%Y-%m-%d")}.csv'
    comment_blob_name = f'reddit_data/{sub}_comments_{today.strftime("%Y-%m-%d")}.csv'

    write_csv_to_gcs(bucket_name, posts_blob_name,
                     service_account_key_file, posts_df)
    write_csv_to_gcs(bucket_name, comment_blob_name,
                     service_account_key_file, comment_df)
