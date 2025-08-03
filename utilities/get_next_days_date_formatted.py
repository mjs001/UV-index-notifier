from datetime import datetime, timedelta


# 2025-07-16
def get_next_days_date_formatted(current_date):
    date_obj = datetime.strptime(current_date, "%Y-%m-%d")
    next_day = date_obj + timedelta(days=1)
    return next_day.strftime("%Y-%m-%d")


# print(get_next_days_date_formatted("2025-07-31"))
