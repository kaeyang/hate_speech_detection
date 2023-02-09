import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

from sodapy import Socrata

from reddit_API_scrapper import *


# default setting for now to test if it works
sub = "politics"
num_posts = 5



# Currently creates the folder in the root directory, will change it later
with DAG(dag_id="reddit_post_comment_webscrapping",
         start_date=datetime(2023, 2, 8),
         schedule_interval='@daily') as dag:

    os.environ["no_proxy"] = "*"

    t1 = PythonOperator(task_id="create_datasets",
                        python_callable=whole_process,
                        op_kwargs={"subreddit": sub,
                                   "post_num": num_posts})

    t1
