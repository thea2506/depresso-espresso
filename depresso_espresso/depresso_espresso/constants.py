from dotenv import load_dotenv
import os
load_dotenv()

SERVICE = "api/"
MY_NODE_USERNAME = os.environ.get('MY_NODE_USERNAME')
MY_NODE_PASSWORD = os.environ.get('MY_NODE_PASSWORD')
