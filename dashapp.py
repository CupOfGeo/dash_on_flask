from app import create_app
import os
from dotenv import load_dotenv
load_dotenv()

key = os.environ['GOOGLE_CRED']
with open('google_key.json', 'w+') as file:
    file.write(key)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google_key.json'

server = create_app()