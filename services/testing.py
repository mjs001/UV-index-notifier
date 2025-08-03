from utilities.convert_uv_time_to_hour import convert_uv_time_to_hour

uv_forecast_data = [
    ["2025-07-16T11:00", 0.00],
    ["2025-07-16T12:00", 4.00],
    ["2025-07-16T13:00", 2.00],
    ["2025-07-16T14:00", 1.00],
    ["2025-07-16T15:00", 1.00],
    ["2025-07-16T16:00", 1.00],
    ["2025-07-16T17:00", 8.00],
    ["2025-07-16T18:00", 8.00],
    ["2025-07-16T19:00", 0.00],
    ["2025-07-16T20:00", 6.00],
    ["2025-07-16T21:00", 6.00],
    ["2025-07-16T22:00", 0.00],
    ["2025-07-16T23:00", 0.00],
    ["2025-07-17T00:00", 7.00],
]
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

print(low_uv_time_blocks)
