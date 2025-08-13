import logging
import requests
import copy
import os
from time import strptime
from datetime import datetime
from utilities.convert_time_to_12hr import convert_time_to_12hr
from utilities.convert_uv_time_to_hour import convert_uv_time_to_hour
from utilities.get_next_days_date_formatted import get_next_days_date_formatted
from dotenv import load_dotenv
from config import config

load_dotenv()

logger = logging.getLogger(__name__)

env = os.getenv("FLASK_ENV", "development")
app_config = config[env]

REQUEST_TIMEOUT = app_config.REQUEST_TIMEOUT
UV_API_BASE_URL = app_config.UV_API_BASE_URL
TIME_API_BASE_URL = app_config.TIME_API_BASE_URL


def uv_index_forecast_request(lat, lon, timezone):
    """Get UV index forecast data for a location"""
    try:
        time_res = get_current_time_for_uv_index(timezone)
        if time_res is None:
            logger.error(f"Failed to get current time for timezone: {timezone}")
            return None, None, None

        datetime_formatted, human_readable_date, time = time_res

        url = f"{UV_API_BASE_URL}?latitude={lat}&longitude={lon}&hourly=uv_index&timezone=auto"

        logger.info(f"Requesting UV forecast from: {url}")

        res = requests.get(url, timeout=REQUEST_TIMEOUT)
        res.raise_for_status()

        uv_forecast_data = res.json()

        if (
            "hourly" not in uv_forecast_data
            or "time" not in uv_forecast_data["hourly"]
            or "uv_index" not in uv_forecast_data["hourly"]
        ):
            logger.error("Invalid response structure from UV API")
            return None, None, None

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
            if found_current_hour:
                date = h[:10]
                if date_str == date:
                    times.append(h)
            else:
                removed_dates += 1

        del uv_raw_copy[:removed_dates]
        del uv_raw_copy[len(times) :]

        forecast_data_formatted = [
            [individual_time, float(uv_index)]
            for individual_time, uv_index in zip(times, uv_raw_copy)
        ]

        next_day = get_next_days_date_formatted(date_str)
        next_day_formatted = f"{next_day}T00:00"

        if next_day_formatted in hourly_raw:
            next_day_index = hourly_raw.index(next_day_formatted)
            next_day_uv = uv_raw[next_day_index]
            forecast_data_formatted.append([next_day_formatted, float(next_day_uv)])
        else:
            logger.warning(f"Next day data not found for: {next_day_formatted}")

        logger.info(
            f"Successfully processed UV forecast data with {len(forecast_data_formatted)} entries"
        )
        return forecast_data_formatted, human_readable_date, time

    except requests.exceptions.Timeout:
        logger.error(f"Timeout while requesting UV forecast for lat: {lat}, lon: {lon}")
        return None, None, None
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error while retrieving UV index forecast: {e}")
        return None, None, None
    except Exception as e:
        logger.error(f"Unexpected error in uv_index_forecast_request: {e}")
        return None, None, None


def get_current_time_for_uv_index(timezone):
    """Get current time for a specific timezone"""
    try:
        url = f"{TIME_API_BASE_URL}?timeZone={timezone}"

        logger.info(f"Requesting current time from: {url}")

        res = requests.get(url, timeout=REQUEST_TIMEOUT)
        res.raise_for_status()

        data = res.json()

        required_fields = ["date", "dateTime", "time"]
        if not all(field in data for field in required_fields):
            logger.error("Invalid response structure from time API")
            return None

        human_readable_date = data["date"]
        datetime_str = data["dateTime"]
        time_str = data["time"]

        datetime_formatted = datetime_str[:13]
        formatted_time = convert_time_to_12hr(time_str)

        logger.info(f"Successfully retrieved time for timezone: {timezone}")
        return datetime_formatted, human_readable_date, formatted_time

    except requests.exceptions.Timeout:
        logger.error(f"Timeout while requesting current time for timezone: {timezone}")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error while retrieving current time: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error in get_current_time_for_uv_index: {e}")
        return None


def get_uv_index(location_data):
    """Get UV index data for a location"""
    try:
        if not location_data or not isinstance(location_data, dict):
            logger.error("Invalid location_data provided")
            return None

        required_fields = ["lat", "lon", "timezone"]
        if not all(field in location_data for field in required_fields):
            logger.error(
                f"Missing required fields in location_data: {list(location_data.keys())}"
            )
            return None

        lat = location_data["lat"]
        lon = location_data["lon"]
        timezone = location_data["timezone"]

        logger.info(
            f"Processing UV index request for lat: {lat}, lon: {lon}, timezone: {timezone}"
        )

        uv_forecast_data, current_date, current_time = uv_index_forecast_request(
            lat, lon, timezone
        )

        if uv_forecast_data is None or not uv_forecast_data:
            logger.error("Failed to retrieve UV forecast data")
            return None

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

        if low_uv_start_time != "":
            low_uv_time_blocks.append(
                f"{low_uv_start_time} - {convert_uv_time_to_hour(uv_forecast_data[-1][0])}"
            )

        result = {
            "uv_index_forecast": low_uv_time_blocks,
            "current_time": current_time,
            "current_date": current_date,
            "current_uv_index": current_uv_index,
        }

        logger.info(
            f"Successfully processed UV index data. Current UV: {current_uv_index}, Low UV blocks: {len(low_uv_time_blocks)}"
        )
        return result

    except Exception as e:
        logger.error(f"Unexpected error in get_uv_index: {e}")
        return None
