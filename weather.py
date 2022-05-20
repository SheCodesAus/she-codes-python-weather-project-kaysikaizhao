from audioop import avg
import csv
from datetime import datetime
from ntpath import join
from unittest import result

DEGREE_SYBMOL = u"\N{DEGREE SIGN}C"

def format_temperature(temp):
    """Takes a temperature and returns it in string format with the degrees
        and celcius symbols.

    Args:
        temp: A string representing a temperature.
    Returns:
        A string contain the temperature and "degrees celcius."
    """
    return f"{temp}{DEGREE_SYBMOL}"

def convert_date(iso_string):
    """Converts and ISO formatted date into a human readable format.

    Args:
        iso_string: An ISO date string..
    Returns:
        A date formatted like: Weekday Date Month Year e.g. Tuesday 06 July 2021
    """
    from datetime import datetime
    import calendar

    date = datetime.strptime(iso_string, "%Y-%m-%dT%H:%M:%S%z")
    return " ".join([calendar.day_name[date.weekday()], "{:02d}".format(date.day), calendar.month_name[date.month], str(date.year)])

def convert_f_to_c(temp_in_farenheit):
    """Converts an temperature from farenheit to celcius.

    Args:
        temp_in_farenheit: float representing a temperature.
    Returns:
        A float representing a temperature in degrees celcius, rounded to 1dp.
    """
    temp_in_c = round((float(temp_in_farenheit)-32) * (5/9), 1)
    return temp_in_c

def calculate_mean(weather_data):
    """Calculates the mean value from a list of numbers.

    Args:
        weather_data: a list of numbers.
    Returns:
        A float representing the mean value.
    """
    weather_data = [float(i) for i in weather_data]  
    mean = float(sum(weather_data) / (len(weather_data)))
    return mean 

def load_data_from_csv(csv_file):
    """Reads a csv file and stores the data in a list.

    Args:
        csv_file: a string representing the file path to a csv file.
    Returns:
        A list of lists, where each sublist is a (non-empty) line in the csv file.
    """
    file = []
    csv_result = []
    with open(csv_file, encoding = "utf-8") as csv_data:
        file_reader = csv.reader(csv_data)
        for item in file_reader:
            file.append(item)
        file.pop(0)
        for i in file:
            if i != []:
                csv_result.append([i[0], int(i[1]), int(i[2])])
        # for num in csv_result:
        #     num[1] = int(num[1])
        #     num[2] = int(num[2])
    return(csv_result)

def find_min(weather_data):
    """Calculates the minimum value in a list of numbers.

    Args:
        weather_data: A list of numbers.
    Returns:
        The minium value and it's position in the list.
    """
    weather_data = [float(i) for i in weather_data]
    index_list = []
    num_and_index_list = []
    index_result = []
    i = 0

    if weather_data == []:
        return ()
    else:
        min_value = weather_data[0]
        for num in weather_data:
            if num < min_value:  
                min_value = num

    # solution 1 ----------------------------------------
        # for x in weather_data:                        
        #     if x == min_value:
        #         index_list.append(i)
        #     i += 1
        # return (min_value, index_list[-1])    
    # ---------------------------------------------------         

    # solution 2 ----------------------------------------
        for num in weather_data:                        
            if num < min_value:
                min_value = num
            num_and_index_list.append([num, i])
            i += 1
        for item in num_and_index_list:
            if min_value == item[0]:
                index_result.append(item[1]) 
        return (min_value, index_result[-1])   
    # ---------------------------------------------------  

def find_max(weather_data):
    """Calculates the maximum value in a list of numbers.

    Args:
        weather_data: A list of numbers.
    Returns:
        The maximum value and it's position in the list.
    """
    weather_data = [float(i) for i in weather_data]
    index_list = []
    i = 0

    if weather_data == []:
        return ()
    else:
        max_value = weather_data[0]
        for num in weather_data:
            if num > max_value:  
                max_value = num
        for x in weather_data:                        
            if x == max_value:
                index_list.append(i)
            i += 1
        return (max_value, index_list[-1]) 

def generate_summary(weather_data):
    """Outputs a summary for the given weather data.

    Args:
        weather_data: A list of lists, where each sublist represents a day of weather data.
    Returns:
        A string containing the summary information.
    """
    total_days = len(weather_data)
    
    avg_low_list = []
    avg_high_list = []

    min_list = []
    max_list = []

    # min_result = []
    # max_result = []

    for num in weather_data:
        avg_low_list.append(num[1])
        avg_high_list.append(num[2])

    avg_low_result_f = calculate_mean(avg_low_list)
    avg_high_result_f = calculate_mean(avg_high_list)

    avg_low_result_c = format_temperature(convert_f_to_c(avg_low_result_f))
    avg_high_result_c = format_temperature(convert_f_to_c(avg_high_result_f))

    for item in weather_data:
        min_list.append(float(item[1]))
        max_list.append(float(item[2])) 

    min_result_f = find_min(min_list)[0]
    max_result_f = find_max(max_list)[0]

    print(min_result_f)

    min_result_c = format_temperature(convert_f_to_c(min_result_f))
    max_result_c = format_temperature(convert_f_to_c(max_result_f))

    for i in weather_data:
        if i[1] == min_result_f or i[2] == min_result_f:
            min_date_data = i[0]
        if i[1] == max_result_f or i[2] == max_result_f:
            max_date_data = i[0]    

    min_date_result = convert_date(min_date_data)
    max_date_result = convert_date(max_date_data)

    # print(total_days, min_result_c, max_result_c, min_date_result, max_date_result, avg_low_result_c, avg_high_result_c)

    result = (f"{total_days} Day Overview\n  The lowest temperature will be {min_result_c}, and will occur on {min_date_result}.\n  The highest temperature will be {max_result_c}, and will occur on {max_date_result}.\n  The average low this week is {avg_low_result_c}.\n  The average high this week is {avg_high_result_c}.\n")
    return result

def generate_daily_summary(weather_data):
    """Outputs a daily summary for the given weather data.

    Args:
        weather_data: A list of lists, where each sublist represents a day of weather data.
    Returns:
        A string containing the summary information.
    """

    daily_sum_data = []
    daily_sum_date = []

    daily_min_temp = []
    daily_max_temp = []

    daily_sum_result = ""
    x = ""
    y = ""
    z = ""

    for sublist in weather_data:
        # x = daily_sum_date.append(convert_date(sublist[0]))                           # solution 1 ----------------------------------------
        # y = daily_min_temp.append(format_temperature(convert_f_to_c(sublist[1])))
        # z = daily_max_temp.append(format_temperature(convert_f_to_c(sublist[2])))     # ---------------------------------------------------
        # x = daily_sum_date.append(convert_date(sublist[0]))                           # solution 2 ----------------------------------------
        x = convert_date(sublist[0])                                                    
        y = format_temperature(convert_f_to_c(sublist[1]))
        z = format_temperature(convert_f_to_c(sublist[2]))
        daily_sum_result += f"---- {x} ----\n"
        daily_sum_result += f"  Minimum Temperature: {y}\n"
        daily_sum_result += f"  Maximum Temperature: {z}\n\n"                                     # ---------------------------------------------------

    # for each_date, min_temp, max_temp in zip(daily_sum_date, daily_min_temp, daily_max_temp):     # solution 1 ----------------------------------------
    #     daily_sum_data.append([each_date, min_temp, max_temp])

    # for sum_result in daily_sum_data:
    #     daily_sum_result += f"---- {sum_result[0]} ----\n"
    #     daily_sum_result += f"  Minimum Temperature: {sum_result[1]}\n"
    #     daily_sum_result += f"  Maximum Temperature: {sum_result[2]}\n\n"                                   # ---------------------------------------------------

    return daily_sum_result