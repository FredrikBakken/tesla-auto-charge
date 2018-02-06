import time
import schedule

from dateutil.tz import *
from threading import Thread
from datetime import datetime, timedelta

from spot_values import get_spot_values

start_time = time.time()


# Update elspot with latest data
def update_elspot():
    get_spot_values()


# Store historic data in storage
def add_storage():
    previous_time = datetime.now() + timedelta(hours=-1)
    now_time      = datetime.now()
    previous_date = previous_time.strftime("%Y-%m-%d")
    previous_hour = previous_time.strftime("%H:%M") + ' - ' + now_time.strftime("%H:%M")

    

    return True


def run_every_10_seconds():
    print("Running periodic task!")
    print("Elapsed time: " + str(time.time() - start_time))

def run_schedule():
    while 1:
        schedule.run_pending()
        time.sleep(1)


def scheduler():
    # Scheduled tasks
    schedule.every(120).seconds.do(update_elspot)           # schedule.every().day.at("16.00").do(update_elspot)
    #schedule.every().hour.do()
    
    # Start threading
    t = Thread(target=run_schedule)
    t.start()
    print("Start time: " + str(start_time))
