from datetime import datetime

def convert_24hr(time):
  # 2025-06-01T04:43:54.068Z
  time_formatted = time.split("T")[1]
  time_formatted = time_formatted[:5]
  hour = datetime.strptime(time_formatted[:2], "%H")
  formatted_hour = datetime.strftime(hour, "%I %p")
  if formatted_hour[0] == "0":
    formatted_hour = formatted_hour[1:]

