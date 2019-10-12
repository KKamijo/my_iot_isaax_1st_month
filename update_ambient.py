#! /usr/bin/env pyhton3

from logging import getLogger
logger = getLogger(__name__)

import envirophat
import ambient
import time
import datetime
import os

AMBIENT_CHANNEL_ID = int(os.environ.get('AMBIENT_CHANNEL_ID'))
AMBIENT_WRITE_KEY = os.environ.get('AMBIENT_WRITE_KEY')

CHECK_SPAN = int(os.environ.get('CHECK_SPAN'))

if __name__ == '__main__':
#    from logging import StreamHandler
#    logger.addHandler(StreamHandler())
    
    # check start script
    print("Script start!")

    # create Ambient Object
    am = ambient.Ambient(AMBIENT_CHANNEL_ID, AMBIENT_WRITE_KEY)

    # main loop
    while True:
        try:
            # check running
            dt_now = datetime.datetime.now()
            print(dt_now.strftime('%Y/%m/%d %H:%M:%S') + " Running!")

            # get acceleromener values
            acc_values = [round(x,2) for x in envirophat.motion.accelerometer()]

            # create send data
            data = {
                'created': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'd1': round(envirophat.weather.temperature(), 1),
                'd2': round(envirophat.weather.altitude(), 1),
                'd3': round(envirophat.weather.pressure(unit='hPa'), 1),
                'd4': envirophat.light.light(),
                'd5': acc_values[0],
                'd6': acc_values[1],
                'd7': acc_values[2]
            }

            # send data
            r = am.send(data)
            print("Status Code:" + str(r.status_code))
            

        except IOError:
            # send error
            print("IOError has occurred!")
            # this is connection erro to enviro phat
            time.sleep(CHECK_SPAN)
            continue

        except Exception as e:
            # send error
            print("Exception has occurred!")
            logger.exception(e)

        # wait time to next send timing
        print("Waiting Start")
        time.sleep(CHECK_SPAN)
        print("Waiting End")