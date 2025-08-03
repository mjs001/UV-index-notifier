from time import strptime
from utilities.convert_time_to_12hr import convert_time_to_12hr
from utilities.convert_uv_time_to_hour import convert_uv_time_to_hour
from utilities.get_next_days_date_formatted import get_next_days_date_formatted
import requests
import os
import json
import copy
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# use convert_time_To_12hr for current time and use convert_uv_time_to_hour for the uv index hours


def uv_index_forecast_request(lat, lon, timezone):
    time_res = get_current_time_for_uv_index(timezone)
    if time_res != None:
        datetime_formatted, human_readable_date, time = time_res
        current_uv_index = 0

        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=uv_index&timezone=auto"
        try:
            res = requests.get(url)
            res.raise_for_status()
            uv_forecast_data = res.json()
            uv_forecast_data_dict = json.loads(uv_forecast_data)
            uv_forecast_data_dict_copy = copy.deepcopy(uv_forecast_data_dict)
            times = []
            hourly_raw = uv_forecast_data_dict_copy["hourly"]["time"]
            uv_raw = uv_forecast_data_dict_copy["hourly"]["uv_index"]
            uv_raw_copy = copy.deepcopy(uv_raw)
            date_str = datetime_formatted[:10]
            removed_dates = 0
            found_current_hour = False
            for h in hourly_raw:
                if datetime_formatted in h:
                    found_current_hour = True
                if found_current_hour == True:
                    date = h[:10]
                    if date_str == date:
                        times.append(h)
                else:
                    removed_dates += 1
            del uv_raw_copy[:removed_dates]
            del uv_raw_copy[len(times) :]
            print(
                "elements left in uv_raw after removing removed_dates num and num of length of hourly_raw",
                uv_raw_copy,
            )
            forecast_data_formatted = [
                [individual_time, float(uv_index)]
                for individual_time, uv_index in zip(times, uv_raw_copy)
            ]  # [["2025-07-20T11:00", 0.00], ...]

            # get 12am next day
            next_day = get_next_days_date_formatted(date_str)
            next_day_formatted = f"{next_day}T00:00"
            next_day_index = 0
            if next_day_formatted in hourly_raw:
                next_day_index = hourly_raw.index(next_day_formatted)
            else:
                print("Date does not exist in data.")
            next_day_uv = uv_raw[next_day_index]
            forecast_data_formatted.append([next_day_formatted, float(next_day_uv)])
            return forecast_data_formatted, human_readable_date, time
        except requests.exceptions.RequestException as e:
            print("An error occurred while retrieving UV index forecast", e)


def get_current_time_for_uv_index(timezone):
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
        formatted_time = convert_uv_time_to_hour(time)
        return datetime_formatted, human_readable_date, formatted_time
    except requests.exceptions.RequestException as e:
        print("An error occurred while trying to retrieve the current time and date", e)
        return None


def get_uv_index(location_data):
    location_data_dict = json.loads(location_data)
    lat = location_data_dict["lat"]
    lon = location_data_dict["lon"]
    timezone = location_data_dict["timezone"]
    uv_forecast_data, current_date, current_time = uv_index_forecast_request(
        lat, lon, timezone
    )
    current_uv_index = int(uv_forecast_data[0][1])
    low_uv_start_time = ""
    low_uv_time_blocks = []
    for uv_data in uv_forecast_data:
        if uv_data[1] <= 1:
            if low_uv_start_time == "":
                low_uv_start_time = convert_uv_time_to_hour(uv_data[0])
        else:
            if low_uv_start_time != "":
                low_uv_time_blocks.append(
                    f"{low_uv_start_time} - {convert_uv_time_to_hour(uv_data[0])}"
                )
                low_uv_start_time = ""

    return {
        "uv_index_forecast": low_uv_time_blocks,
        "current_time": current_time,
        "current_date": current_date,
    }
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
