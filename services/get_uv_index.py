from time import strptime
from utilities.convert_time_to_12hr import convert_time_to_12hr
from utilities.convert_uv_time_to_hour import convert_uv_time_to_hour
from utilities.get_next_days_date_formatted import get_next_days_date_formatted
import requests
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
            uv_forecast_data_dict_copy = copy.deepcopy(uv_forecast_data)
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
            # print(
            #     "elements left in uv_raw after removing removed_dates num and num of length of hourly_raw",
            #     uv_raw_copy,
            # )
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
        human_readable_date = data["date"]
        datetime = data["dateTime"]
        time = data["time"]
        # 2025-07-15T13:40:56.201195
        datetime_formatted = datetime[:13]
        formatted_time = convert_time_to_12hr(time)
        return datetime_formatted, human_readable_date, formatted_time
    except requests.exceptions.RequestException as e:
        print("An error occurred while trying to retrieve the current time and date", e)
        return None


def get_uv_index(location_data):
    location_data_dict = location_data
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

    # Ensure the last block is appended if it runs to the end
    if low_uv_start_time != "":
        low_uv_time_blocks.append(
            f"{low_uv_start_time} - {convert_uv_time_to_hour(uv_forecast_data[-1][0])}"
        )

    return {
        "uv_index_forecast": low_uv_time_blocks,
        "current_time": current_time,
        "current_date": current_date,
        "current_uv_index": current_uv_index,
    }


# if __name__ == "__main__":
# get_uv_index() #insert coordinates for testing
