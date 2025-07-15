from utilities.convert_time_to_12hr import convert_time_to_12hr
from utilities.convert_uv_time_to_hour import convert_uv_time_to_hour
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

# NEED TO CHECK HOW MANY TIMESTAMPS WITH UV INDEX ARE RETURNED FROM FORECAST


def uv_index_forecast_request(lat, lon):
    # put actual request here so you can call it multiple times in below function
    # get uv index forecast and do res.json then convert to dictionary and return that
    url = f"https://api.openuv.io/api/v1/forecast?lat={coordinates['lat']}&lng={coordinates['lon']}"
    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        uv_forecast_data = res.json()
        print("uv forecast data", uv_forecast_data)
        uv_forecast_data_dict = json.loads(uv_forecast_data)
        return uv_forecast_data_dict
    except requests.exceptions.RequestException as e:
        print("An error occurred while retrieving UV index forecast", e)


def get_current_time_for_uv_index(timezone):
    # need to make a request to https://timeapi.io/api/time/current/zone?timeZone=America/Chicago
    # return date, time
    url = f"https://timeapi.io/api/time/current/zone?timeZone={timezone}"
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        data_dict = json.loads(data)
        human_readable_date = data_dict["date"]
        datetime = data_dict["dateTime"]
        time = data_dict["time"]
        # 2025-07-15T13:40:56.201195
        datetime_formatted = datetime[:13]
        return datetime_formatted, human_readable_date, time
    except requests.exceptions.RequestException as e:
        print("An error occurred while trying to retrieve the current time and date", e)
        return None


def get_current_uv_index(uv_forecast_data, timezone):
    # need to include time conversion using convert_time_to_12hr
    time_res = get_current_time_for_uv_index(timezone)
    if time_res != None:
        datetime_formatted, human_readable_date, time = time_res
        current_uv_index = 0
        return current_uv_index, human_readable_date, time
    # return human_readable_date, time, uv_index
    # put request for uv index here and then return the uv


def get_uv_index(location_data):
    location_data_dict = json.loads(location_data)
    lat = location_data_dict["lat"]
    lon = location_data_dict["lon"]
    timezone = location_data_dict["timezone"]
    uv_forecast_data = uv_index_forecast_request(lat, lon)
    # human_readable_date, time, uv_index = get_current_uv_index(
    #   uv_forecast_data, timezone
    # )

    # the coordinates are going to be a dictionary of lat and lon
    # the idea is to make the request with uv_index_request with the coordinates
    # make a while loop with a var called is_not_all_24_hours or something like that that will be true or false depending on if the last elements uv_time has 23 as the hour of the same date or is greater than current dates date.
    # then that data will be json and you will want to loop through it and check if current uv is above or below 1
    # then if it is below 1, save in dictionary with uv_time low_uv see if next val is still below 1 if it is do convert_24hr on the uv_time and add that time and uv to low_uv and continue until hitting above or at 1.
    # once you have that, push that dictionary (low_uv) to low_uv_times which is a list that will hold a dictionary for each block of time the uv index was under 1. then set low_uv to a empty dictionary.
    # if on last element, check if uv_time is same date at 23 hour or the date is greater than current date.

    # get date from uv index request, cant see what it is currently due to max requests being made, save that in var, then check if last element has date that is greater than the uv index date var or is 23 hour of same date. If it is neither, make another request with date field filled out, but double check it in Postman and see if this is necessary if it returns the whole days worth then it isnt necessary.

    # if it is then the var is True and you return element
    # if it is False break the loop and you then take the low_uv_times, loop through each one make a list take the time of the first low_uv entry in dictionary then add a dash and then go to last entry. ex: "10 AM - 1 PM" push that to a list called formatted_low_uv_times.
    # If the dictionary only holds one entry, then you need to just push that one entry "10 AM".
    # make dictionary with current_uv as a key and insert current uv
    # Then make a dictionary with low_uv_timeblocks as key and formatted_low_uv_times as value.

    # make sure to convert the date time with convert_timestamp and add that to the raw dict
    # return raw dictionary so it can be converted in main.py

    # convert low_uv_timeblocks into json with json.dumps(low_uv_timeblocks)
    # return low_uv_timeblocks json

    # ex return {date_time: ""}


# if __name__ == "__main__":
# get_uv_index() #insert coordinates for testing
