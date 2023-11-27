from datetime import datetime

timestamp = 1
formatted_date = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')

print(formatted_date)