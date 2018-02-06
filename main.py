from dateutil.tz import *
from datetime import datetime, timedelta

#from spot_values import get_spot_values
#from database import insert_all_elspot, delete_old_elspot_temp#, select_location_elspot
from config import set_secret_key


def run():
    #get_spot_values()

    #select_location_elspot('Tr.heim')

    #insert_all_elspot('Oslo5', '2018-02-01', '09:00 - 10:00', '40.00')

    #delete_old_elspot_temp('2018-02-02', '10:00 - 11:00')

    
    print(set_secret_key())

    return True

# Define startup functionality
if __name__ == "__main__":
    run()