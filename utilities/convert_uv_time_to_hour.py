from datetime import datetime


def convert_uv_time_to_hour(time):
    # 2025-06-01T04:43:54.068Z
    # "2025-07-14T00:00"
    time_formatted = time.split("T")[1]
    # time_formatted = time_formatted[:5]
    hour = datetime.strptime(time_formatted[:2], "%H")
    formatted_hour = datetime.strftime(hour, "%I %p")
    if formatted_hour[0] == "0":
        formatted_hour = formatted_hour[1:]
    return formatted_hour


# print(convert_uv_time_to_hour("2025-07-14T00:00"))
