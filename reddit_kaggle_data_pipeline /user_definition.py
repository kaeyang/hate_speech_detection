import os

# Reddit API info, you can set one up through your reddit account
client_id = os.environ.get('REDDIT_CLIENT_ID')
client_secret = os.environ.get('REDDIT_CLIENT_SECRET')
user_agent = os.environ.get('USER_AGENT')

# GCP, you would need to create a GCP project and storage bucket first
bucket_name = os.environ.get("GS_BUCKET_NAME")
service_account_key_file = os.environ.get("GS_SERVICE_ACCOUNT_KEY_FILE")

# Data to be collected from Reddit everyday, can be changed to your interests
sub = "all"
num_posts = 25

# MongoDB Atlas,
mongo_username = os.environ.get("MONGO_USERNAME")
mongo_password = os.environ.get("MONGO_PASSWORD")
mongo_ip_address = os.environ.get("MONGO_IP")
database_name = os.environ.get("MONGO_DB_NAME")

# hardcoded
collection_1_name = 'comments'
collection_2_name = 'posts'
collection_3_name = 'kaggle'

# Please change this to where your airflow/dags file is located
dag_folder = "..."
