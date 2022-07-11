from time import time
import math
from tracemalloc import start
from twilio.rest import Client
from datetime import datetime, timedelta
from delorean import Delorean, epoch
import calendar

def schedule(show):
    account_sid = "ACfe19105a3aa7d11c16d6272a0d3eccda"
    auth_token  = "cfbab195621b28a0753619e06ce95fe4"
    client = Client(account_sid, auth_token)
    station = show[2]

    # get now in the timezone
    # get scheduled show in the timezone
    # convert scheduled show to utc
    show_day = show[3]
    start_time = int(show[4])
    next_show_date = (datetime.utcnow() + timedelta(days=get_day_difference(show_day))).date()
    exact = datetime(year=next_show_date.year, month=next_show_date.month, day=next_show_date.day, hour=start_time)
    print(exact)

    # message = client.messages.create(
    #      messaging_service_sid='MG73e4d89da9b2863a263e62abccc879a1',
    #      body='This is a scheduled message noo noo',
    #      send_at=(time_utc + timedelta(minutes=20)),
    #      schedule_type='fixed',
    #      to='+15127759300'
    #  )

    # print(message.sid)

def now_or_later(show_day, start_time, timezone):
    # the all-important now
    nau = Delorean()
    nau = nau.epoch

    def find_next_day(d, show_day, start_hour, start_minute):
        match show_day:
            case 0:
                return d.next_monday().replace(hour=start_hour, minute=start_minute).truncate('minute')
            case 1:
                return d.next_tuesday().replace(hour=start_hour, minute=start_minute).truncate('minute')
            case 2:
                return d.next_wednesday().replace(hour=start_hour, minute=start_minute).truncate('minute')
            case 3:
                return d.next_thursday().replace(hour=start_hour, minute=start_minute).truncate('minute')
            case 4:
                return d.next_friday().replace(hour=start_hour, minute=start_minute).truncate('minute')
            case 5:
                return d.next_saturday().replace(hour=start_hour, minute=start_minute).truncate('minute')
            case 6:
                return d.next_sunday().replace(hour=start_hour, minute=start_minute).truncate('minute')

            # If an exact match is not confirmed, this last case will be used if provided
            case _:
                return "Something went wrong"

    # when the show will occur
    then = Delorean().shift(timezone)
    print("nau", nau)
    print("then", then)
    start_hour, start_minute = int(math.modf(start_time)[1]), 30 if int(math.modf(start_time)[0]) == 5 else 0
    then = find_next_day(then, show_day, start_hour, start_minute)
    then = then.shift('utc').epoch

    difference = then - nau
    print("difference", difference)
    # if more than 15 mins in future and less than one week
    if(900 < difference < 604800):
        print('schedule regular')
    # if greater than one week, shift back then send
    if(604800 < difference < (604800 * 2)):
        print('shift back a week then schedule')
    # if less than 15 minutes in future, send text now!
    if(difference < 900):
        print('send now!')


def main():
    print(datetime.now() + timedelta(hours=2))

if __name__=="__main__":
    now_or_later(6, 22.5, 'US/Mountain')
    

# def get_day_difference(show_weekday = 3):
#     today_weekday = datetime.utcnow().weekday()
#     print(today_weekday)
#     if(today_weekday == show_weekday):
#         return 0
#     # if later in the week
#     elif(show_weekday > today_weekday):
#         return show_weekday - today_weekday
#     # if earlier in next week
#     elif(show_weekday < today_weekday):
#         return (show_weekday + 1 + (6-today_weekday))

    
#     day = list(calendar.day_name)[show_day]