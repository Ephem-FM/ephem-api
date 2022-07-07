from time import time
from tracemalloc import start
from twilio.rest import Client
from datetime import datetime, timedelta
import pytz

def schedule(show):
    account_sid = "ACfe19105a3aa7d11c16d6272a0d3eccda"
    auth_token  = "cfbab195621b28a0753619e06ce95fe4"
    client = Client(account_sid, auth_token)
    station = show[2]

    # get show datetime
    # convert day to nearest future day with matching weekday
    # enter in time manually
    show_day = show[3]
    start_time = int(show[4])
    next_show_date = (datetime.utcnow() + timedelta(days=get_day_difference(show_day))).date()
    exact = datetime(year=next_show_date.year, month=next_show_date.month, day=next_show_date.day, hour=start_time)
    print(exact)
    
    # convert to UTC


    # time_utc = convert_to_utc('US/Central')
    # print("time utc: ", time_utc)

    # message = client.messages.create(
    #      messaging_service_sid='MG73e4d89da9b2863a263e62abccc879a1',
    #      body='This is a scheduled message noo noo',
    #      send_at=(time_utc + timedelta(minutes=20)),
    #      schedule_type='fixed',
    #      to='+15127759300'
    #  )

    # print(message.sid)

def get_day_difference(show_weekday = 3):
    today_weekday = datetime.utcnow().weekday()
    print(today_weekday)
    if(today_weekday == show_weekday):
        return 0
    # if later in the week
    elif(show_weekday > today_weekday):
        return show_weekday - today_weekday
    # if earlier in next week
    elif(show_weekday < today_weekday):
        return (show_weekday + 1 + (6-today_weekday))

# if today is 2 but show is on 4, return 2
# show is greater than 4 so subtract today from show
# if today is 5 but show is 1, return show_weekday plus 1 plus remaining


def convert_to_utc(show_datetime, show_timezone):
    local = pytz.timezone(timezone)
    local_dt = local.localize(datetime.now(), is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    return utc_dt
    print(local_dt)
    print(utc_dt)

def main():
    print(datetime.now() + timedelta(hours=2))

if __name__=="__main__":
    start_time =  datetime.time(6, 42)
    print(start_time)

