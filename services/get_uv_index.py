
def uv_index_request(coordinates):
  #put actual request here so you can call it multiple times in below function
  #get uv index forecast and do res.json then convert to dictionary and return that

def get_uv_index(coordinates):
  #the coordinates are going to be a dictionary of lat and lon
  #the idea is to make the request with uv_index_request with the coordinates
  #make a while loop with a var called is_not_all_24_hours or something like that that will be true or false depending on if the last elements uv_time has 23 as the hour of the same date or is greater than current dates date.
  #then that data will be json and you will want to loop through it and check if current uv is above or below 1
  #then if it is below 1, save in dictionary with uv_time low_uv see if next val is still below 1 if it is do convert_24hr on the uv_time and add that time and uv to low_uv and continue until hitting above or at 1.
  #once you have that, push that dictionary (low_uv) to low_uv_times which is a list that will hold a dictionary for each block of time the uv index was under 1. then set low_uv to a empty dictionary.
  #if on last element, check if uv_time is same date at 23 hour or the date is greater than current date.
  #if it is then the var is True and you return element
  #if it is False break the loop and you then take the low_uv_times, loop through each one make a list take the time of the first low_uv entry in dictionary then add a dash and then go to last entry. ex: "10 AM - 1 PM" push that to a list called formatted_low_uv_times.
  # If the dictionary only holds one entry, then you need to just push that one entry "10 AM".
  # Then make a dictionary with low_uv_timeblocks as key and formatted_low_uv_times as value.
  #convert low_uv_timeblocks into json with json.dumps(low_uv_timeblocks)
  #return low_uv_timeblocks json

#if __name__ == "__main__":
  #get_uv_index() #insert coordinates for testing
