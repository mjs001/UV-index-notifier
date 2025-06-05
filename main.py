from flask import Flask
import requests
from utilities.determine_env import determine_env
from process_location import process_location


app = Flask(__name__)
@app.route("/location") #make sure matches Next

def get_and_send_data():
  env = determine_env()
  domain = "localhost:3000" if env == "development" else "" #need to fill in
  url = f"{domain}/location" #make sure it matches route in Next
  try:
    res = requests.get(url)
    res.raise_for_status()
    form_data = res.json()
    print("form_data", form_data)
  except requests.exceptions.RequestException as e:
    print("an error has occurred", e)
  processed_data = process_location(form_data) #returns json
  try:
   res = requests.post(f"{domain}/uv_index", json=processed_data) #make sure route matches Next
   res.raise_for_status()
   print("post for uv_index", res.json())
  except requests.exceptions.RequestException as e:
    print("an error has occurred", e)

if __name__ == "__main__":
  app.run()
