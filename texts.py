import sched
from time import time
import math
from tracemalloc import start
from twilio.rest import Client
from datetime import datetime, timedelta
from delorean import Delorean, epoch
import calendar

def main(phone, show):
    schedule(phone, show)

def schedule(user_number, show):
    account_sid = "ACfe19105a3aa7d11c16d6272a0d3eccda"
    auth_token  = "cfbab195621b28a0753619e06ce95fe4"
    client = Client(account_sid, auth_token)

    show_day, start_time, timezone = show[3], show[4], show[14]
    print("show name", show_day)
    print("start time", start_time)
    print("timezone", timezone)
    now, when = now_or_later(show_day, start_time, timezone)
    print("NOW", "WHEN")
    print(now, when)
    return

    # send now
    if(now):
        body = f"Hi from ephem.fm!  One of the shows you'll receive is scheduled to happen soon! \
            It's called {show.name} on the station {show.station} out of {show.location}. \
            Please go to {show.station_url} and tune in at the next hour mark."

        message = client.messages \
            .create(
            messaging_service_sid='MG73e4d89da9b2863a263e62abccc879a1',
            body=body,
            to=('+1' + user_number)
        )
        print(message.sid)

    # send later
    elif(not now):
        body = f"The stars have aligned and a show matching your preferences is about to start. \
            Tune into {show.station} out of {show.location} at {show.station_url} to listen to {show.name}. \
            Do enjoy."

        message = client.messages \
            .create(
                messaging_service_sid='MG73e4d89da9b2863a263e62abccc879a1',
                body=body,
                send_at=when,
                schedule_type='fixed',
                to=('+1' + user_number)
            )
        print(message.sid)

def now_or_later(show_day, start_time, timezone):
    # the all-important now
    nau = Delorean()
    nau = nau.epoch

    def find_next_day(d, show_day, start_hour, start_minute):
        print("INSIDE FIND NEXT DAY")
        print(d)
        print(show_day)
        print(start_hour)
        print(start_minute)

        match show_day:
            case 0:
                d = d.next_monday().replace(hour=start_hour, minute=start_minute).truncate('minute')
                print("inside find next day")
                print(type(d))
                return d
            case 1:
                d = d.next_tuesday().replace(hour=start_hour, minute=start_minute).truncate('minute')
                print("inside find next day")
                print(type(d))
                return d
            case 2:
                d = d.next_wednesday().replace(hour=start_hour, minute=start_minute).truncate('minute')
                print("inside find next day")
                print(type(d))
                return d
            case 3:
                d = d.next_thursday().replace(hour=start_hour, minute=start_minute).truncate('minute')
                print("inside find next day")
                print(type(d))
                return d
            case 4:
                d = d.next_friday().replace(hour=start_hour, minute=start_minute).truncate('minute')
                print("inside find next day")
                print(type(d))
                return d
            case 5:
                d = d.next_saturday().replace(hour=start_hour, minute=start_minute).truncate('minute')
                print("inside find next day")
                print(type(d))
                return d
            case 6:
                d = d.next_sunday().replace(hour=start_hour, minute=start_minute).truncate('minute')
                print("inside find next day")
                print(type(d))
                return d

            # If an exact match is not confirmed, this last case will be used if provided
            case _:
                return "Something went wrong"

    # when the show will occur
    then = Delorean().shift(timezone)
    print("nau", nau)
    print("then", then)
    start_hour, start_minute = int(math.modf(start_time)[1]), 30 if int(math.modf(start_time)[0]) == 5 else 0
    then = find_next_day(then, show_day, start_hour, start_minute)
    print('returned then')
    print(then)
    then = then.shift('utc').epoch

    difference = then - nau
    print("difference", difference/(3600*24))
    # if more than 15 mins in future and less than one week
    if(900 < difference < 604800):
        return (False, then)
    # if greater than one week, shift back then send
    elif(604800 < difference < (604800 * 2)):
        then = epoch(then).shift('utc') - timedelta(weeks=1)
        return (False, then.epoch)
    # if less than 15 minutes in future, send text now!
    elif(difference < 900):
        return (True, then)
    else:
        print('scheduling failed')

if __name__=="__main__":
    d = Delorean()
    d = d.epoch
    d = (epoch(d).shift('utc') - timedelta(weeks=1)).epoch
    print(d)
    