import pandas as pd
import os
from datetime import datetime, date
import praw
from praw.models import MoreComments

# Reddit Instance for authentication
reddit = praw.Reddit(client_id='vutUqpaYhLKZn9bvQLfQfQ',
                     client_secret='D5PL7150dMuIOOmBH_Urn3GTJJaU3g', user_agent='WebScrapping')

# default folder, change this to save in a different place
folder_path = "/Users/"


def create_reddit_day_data_dirs(folder_path):
    '''
    Functionality:
        Creates a folder of folders with years and months for each entry

    Output:
        Returns the base path of the dirs to be used later to store the .csv files
    '''
    try:
        today = datetime.now()
        os.makedirs(f'{folder_path}/reddit_{today.strftime("%Y/%m")}')
    except:
        pass

    return os.path.abspath(f'{folder_path}/reddit_{today.strftime("%Y/%m")}')


def create_subreddit_df(subreddit, post_num):
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


def create_comment_df(df):
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


def export_df_to_csv(subreddit, posts_df, comments_df, dir_path):
    '''
    Functionality:
        convert the comments and posts dataframes to csv

    Arguments:
        subreddit = subreddit that we scraped from.
        posts_df =  output of create_subreddit_df()
        comments_df = output of create_comment_df()
        dir_path = folder where csv will be stored
    '''
    today = datetime.now()
    # Will replace csv if existing
    posts_df.to_csv(dir_path + '/' +
                    f'{subreddit}_posts_{today.strftime("%Y-%m-%d")}.csv')
    comments_df.to_csv(
        dir_path + '/' + f'{subreddit}_comments_{today.strftime("%Y-%m-%d")}.csv')


def whole_process(subreddit, post_num):
    dir_path = create_reddit_day_data_dirs(folder_path)
    posts_df = create_subreddit_df(subreddit, post_num)
    comment_df = create_comment_df(posts_df)
    export_df_to_csv(subreddit, posts_df, comment_df, dir_path)
