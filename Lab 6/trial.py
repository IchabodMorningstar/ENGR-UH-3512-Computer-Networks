import datetime

# Convert the 32-bit time value to seconds
time_value = 0x000000f7
time_in_seconds = int(time_value)

# Convert the time in seconds to a datetime object
epoch = datetime.datetime(1970, 1, 1)
resulting_time = epoch + datetime.timedelta(seconds=time_in_seconds)

# Get the current time
current_time = datetime.datetime.now()

# Add the resulting time to the current time
final_time = current_time + (resulting_time - epoch)

# Print the results
print("Resulting Time (from 32-bit value):", resulting_time)
print("Current Time:", current_time)
print("Final Time (Current Time + Resulting Time):", final_time)
