from reddit_API_scrapper import *
import sys

'''
can run this directly from command line:
$python run_script.py <subreddit> <num_posts>
'''

subreddit = str(sys.argv[1])
num_posts = int(sys.argv[2])

dir_path = create_reddit_day_data_dirs()
posts_df = create_subreddit_df(subreddit, num_posts)
comment_df = create_comment_df(posts_df)

export_df_to_csv(subreddit, posts_df, comment_df, dir_path)
