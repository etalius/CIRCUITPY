import time
import datetime

# Helper function to find the nth weekday of a month (e.g., second Sunday in March)
def get_nth_weekday(year, month, weekday, nth):
    """Find the nth occurrence of weekday in the given month."""
    # Find the first day of the month
    first_day_of_month = time.struct_time((year, month, 1, 0, 0, 0, 0, 0, 0))
    print(first_day_of_month)
    
    # Get the weekday of the first day of the month
    first_weekday = first_day_of_month.tm_wday  # 0=Monday, 6=Sunday
    if first_weekday == weekday:
        first_occurrence =  1
    elif first_weekday < weekday:
        print(first_weekday)
        print(weekday)
        first_occurrence =  weekday - first_weekday + 1
    else:
         # say that we are looking for tuesday = 1
         # and month starts on thurs = 3
         # answer = 6 --> 7 - 3 = 4 + 1
         first_occurrence = 7  - first_weekday + weekday + 1
    
    # Find the first occurrence of the required weekday
    nth_occurrence = first_occurrence + (nth - 1) * 7  # nth occurrence

    return nth_occurrence

# Check if the given timestamp is in DST
def is_dst(utc_time):
    year = utc_time.tm_year
    print(year)
    second_sunday_march = get_nth_weekday(year, 3, 6, 2)
    print(second_sunday_march)
    first_sunday_november = get_nth_weekday(year, 11, 6, 1)
    print(first_sunday_november)
    start_of_dst = time.struct_time((year, 3, second_sunday_march, 2, 0, 0, 0, 0, 0))  # Second Sunday in March, 2:00 AM
    end_of_dst = time.struct_time((year, 11, first_sunday_november, 2, 0, 0, 0, 0, 0))  # First Sunday in November, 2:00 AM
    start_timestamp = time.mktime(start_of_dst)
    end_timestamp = time.mktime(end_of_dst)
    
    current_timestamp = time.mktime(utc_time)
    return start_timestamp <= current_timestamp < end_timestamp

ts = 1741751733
utc_time = time.localtime(ts)
is_dst(utc_time)
