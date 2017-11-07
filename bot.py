import telegram

import sys 
import pprint
import time
import datetime
import dateutil.parser
from pytz import timezone

from parser import parser

# bool variables init 
DONE = {"DH1": False, "DH2": False}

# Parse .config file to obtain TOKEN and CHANNEL NAME
with open('.config', 'r') as f:
    lines = f.readlines()
    # collect token from the config file
    TOKEN = lines[0].split()[2].strip("'")
    CHANNEL_NAME = lines[1].split()[2].strip("'")

# Helpful for debug
def _print(*args):
    time = datetime.datetime.now().time().isoformat()[:8]
    print("[{}]:".format(time) , end=' ')
    print(" ".join(map(str, args)))

def prettify_before_sending(data, mess_name):
    text = ''
    text += '*'+mess_name+' menu for '+data['date'].strftime("%d-%m-%Y")+"*\n"
    
    meal_in_day = ['Breakfast', 'Lunch', 'Dinner'] 
    for meal_name in meal_in_day:
        text += '_'+meal_name+':_ \n '
        for item in data[meal_name]:
            text += '- '+item+'\n '
        text += '\n'

    return text

def send_to_channel(bot, data, mess_name):
    text = prettify_before_sending(data, mess_name)
    
    # send to the channel
    bot.sendMessage(chat_id=CHANNEL_NAME, 
                    text=text, 
                    parse_mode='Markdown')

def main():
    # AUTHETICATION
    try:
        bot = telegram.Bot(token=TOKEN)
    except:
        _print('Invalid Token, update .config and try again')
        exit(1)

    # Sample Message
    # bot.sendMessage(chat_id=CHANNEL_NAME, text="hello")
    _print(TOKEN, CHANNEL_NAME)
    _print(bot.getMe())

    global DONE
    
    # so-called event loop
    while True:
        # get today's datetime, IST timezone 
        ist_timezone = timezone('Asia/Kolkata')
        current_time = datetime.datetime.now(ist_timezone)
        _print("Time in IST: {}".format(current_time))

        # fetch data dict from website
        data = parser() 
        _print("Date fetch complete.")

        for key, val in DONE.items():
            if not DONE[key]:
                _print(data[key]['response'])
                # fetch checking logic 
                if data[key]['response'] is True and current_time.month == data[key]['date'].month and current_time.day == data[key]['date'].day:
                     
                    # send menu through bot
                    _print('Sending {} menu to channel'.format(key))
                    send_to_channel(bot, data[key], key)
                    DONE[key] = True

        # Done for the day?
        if DONE["DH1"] and DONE["DH2"]:
            _print("Ready to sleep now until next day 00:01")

            # now sleep till 12 am of next day
            current_time = datetime.datetime.now(ist_timezone)

            # set date to next day 12:01 am
            wake_up_time = current_time
            wake_up_time += datetime.timedelta(days=1)
            wake_up_time = wake_up_time.replace(hour=0, minute=1)

            # sleep for time delta between these two dates
            time.sleep((wake_up_time - current_time).total_seconds())
            
            # reinit the variables, cuz new day 
            _print("Woke up. Time to get back to work.")
            DONE["DH1"] = DONE["DH2"] = False

        # We will get into this else loop when
        # either one or none of the menu is successfully fetched and posted. 
        # so sleep only for an hour before checking again. 
        # Sleep is for rate limiting the hits to actual mess menu website.
        else:
            # refresh current time
            current_time = datetime.datetime.now(ist_timezone) 
            # sleep for an hour and then try again
            _print('Sleeping for one hour.')
            time.sleep(60 * 60)

            wokeup_time = datetime.datetime.now(ist_timezone)

            # This means you slept on previous day 
            # and woke up on next day, thus, refresh the DONE dict. 
            # Fixes edge case when only one mess menu has been posted. 
            if wokeup_time.date() > current_time.date():
                DONE["DH1"] = DONE["DH2"] = False

            _print('Woke up!')

if __name__ == '__main__':
    # don't publish menu for today if cli arguement exists
    # not specifiying any specific keyword atm 
    if len(sys.argv) > 1: 
        DONE["DH1"] = DONE["DH2"] = True

    main()