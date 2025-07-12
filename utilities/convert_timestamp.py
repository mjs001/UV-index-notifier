from datetime import datetime


def convert_timestamp(time):
    # 2025-06-01T04:43:54.068Z
    datetime_obj = datetime.fromisoformat(time)
    formatted_time = datetime_obj.strftime("%I:%M %p")
    formatted_date = datetime_obj.strftime("%m/%d/%Y")
    return f"{formatted_date} {formatted_time}"
