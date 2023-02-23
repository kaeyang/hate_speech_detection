import os

# Reddit API info
client_id= os.environ.get('REDDIT_CLIENT_ID')
client_secret= os.environ.get('REDDIT_CLIENT_SECRET')
user_agent= os.environ.get('USER_AGENT')

# GCP
bucket_name = os.environ.get("GS_BUCKET_NAME")
service_account_key_file = os.environ.get("GS_SERVICE_ACCOUNT_KEY_FILE")

# Data to be collected from Reddit everyday
sub = "all"
num_posts = 25

#MongoDB
mongo_username = os.environ.get("MONGO_USERNAME")
mongo_password =  os.environ.get("MONGO_PASSWORD")
mongo_ip_address = os.environ.get("MONGO_IP")
database_name = os.environ.get("MONGO_DB_NAME")
collection_name = os.environ.get("MONGO_COLLECTION_NAME")