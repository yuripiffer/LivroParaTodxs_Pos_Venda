import datetime

today = datetime.date.today()
yesterday = datetime.datetime.strptime(str(today - datetime.timedelta(days=1)), '%Y-%m-%d')
date = {"initial_date": yesterday, "final_date": yesterday}

print("today", today)
print("yesterday", yesterday)
print("date", date)