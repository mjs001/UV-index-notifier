from datetime import datetime


def convert_time_to_12hr(time):
    # "13:40"
    datetime_obj = datetime.strptime(time, "%H:%M")
    formatted_time = datetime_obj.strftime("%I:%M %p")
    return formatted_time


# print(convert_time_to_12hr("13:40"))
