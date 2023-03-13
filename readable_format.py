############################################
# Author: Ondrej Tomasek
# Programmed by: Ondrej Tomasek
# LinkedIn: linkedin.com/in/ondrat
# Date of creation (DD.MM.YYYY): 13.03.2023
############################################
# Please read README.txt before use
############################################

path_history = "data/history.txt"
path_current_data = "data/existing_data.txt"
path_session = "data/session_live_data.txt"

def history_data():
    response_array = []
    with open(path_history, "r") as history_file:
        for line in history_file:
            # Extract the year, month, day, hour, minute, second, and message
            year = line[4:8]
            month = line[10:12]
            day = line[14:16]
            hour = line[21:23]
            minute = line[29:31]
            second = line[37:39]
            message = line[43:-1]
            # Reformat the data according to the desired format
            reformatted_line = f"{day}.{month}.{year} / {hour}:{minute}.{second} - {message}\n"
            response_array.append(reformatted_line)
        response_string = "".join(response_array)
        response = response_string
        return response

def current_data():
    response_array = []
    with open(path_current_data, "r") as current_data_file:
        for line in current_data_file:
            # Extract the year, month, day, hour, minute, second, and message
            year = line[4:8]
            month = line[10:12]
            day = line[14:16]
            hour = line[21:23]
            minute = line[29:31]
            second = line[37:39]
            message = line[43:-1]
            # Reformat the data according to the desired format
            reformatted_line = f"{day}.{month}.{year} / {hour}:{minute}.{second} - {message}\n"
            response_array.append(reformatted_line)
        response_string = "".join(response_array)
        response = response_string
        return response

def session_data():
    response_array = []
    with open(path_session, "r") as session_file:
        for line in session_file:
            # Extract the year, month, day, hour, minute, second, and message
            year = line[4:8]
            month = line[10:12]
            day = line[14:16]
            hour = line[21:23]
            minute = line[29:31]
            second = line[37:39]
            message = line[43:-1]
            # Reformat the data according to the desired format
            reformatted_line = f"{day}.{month}.{year} / {hour}:{minute}.{second} - {message}\n"
            response_array.append(reformatted_line)
        response_string = "".join(response_array)
        response = response_string
        return response
