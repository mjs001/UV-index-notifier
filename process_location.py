from utilities.convert_24hr import convert_24hr

def process_location(form_data):
  #form data is going to be json
  #convert json for form data to dictionary: json.loads(form_data)
  #form data will look something like {"form": {"city": "New%20York", "state": "New%20York", "country": "United%20States%20of%20America"}}
  #will need to create a function in Next that takes form data and adds the %20 for each space in the form data and turns "United States" into "United States of America"
  #will need to construct url by creating a url var that holds all of the apis url for the request except for the actual query and api key. need to create a string for the api key portion of the url and a string called format that holds the &format=json part of the url (after query). Need to retrieve the API key env variable. Create a var called query and set it to an empty string. Then need to loop through form data, if the key is not equal to city add & symbol before following string, so f"&{key}={value}" for a key equaling city write f"{key}={value}". add that string to the query string. Then once looped through all keys and values, construct the full_url with url + query + format + api_key an example of a full url:

  #https://api.geoapify.com/v1/geocode/search?city=New%20York&state=NY&country=United%20States%20of%20America&format=json&apiKey=API_KEY

  #example of another countries url or one that does not have a state:
  #https://api.geoapify.com/v1/geocode/search?city=Tokyo&country=Japan&format=json&apiKey=API_KEY

  #execute get_coordinates save result in var, will be returning a dictionary with lat and lon
  # execute get_uv_index put in get_coordinates var as param save in var
  #return var for results of get_uv_index (can simplify after testing by just returning get_uv_index execution) will return json

#if __name__ == "__main__":
  #process_location() #insert fake form_data for testing
