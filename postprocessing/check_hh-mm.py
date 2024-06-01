def convert_seconds_to_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return hours, minutes


seconds = int(input("Enter the num. seconds: "))
hours, minutes = convert_seconds_to_time(seconds)
print('hh:mm')
print(f"{hours}:{minutes} ")