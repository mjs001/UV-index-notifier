import os
from dotenv import load_dotenv
load_dotenv()

def determine_env():
  env = os.environ.get('ENVIRONMENT')
  return env
