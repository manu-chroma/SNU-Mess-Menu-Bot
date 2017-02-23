import telegram

import sys 
import pprint
import time
import datetime
import dateutil.parser
from pytz import timezone

# parser.py
from parser import parser

# INIT Telegram Bot
# parse .config file to obtain token and public channel name
with open('.config', 'r') as f:
    lines = f.readlines()
    # collect token from the config file
    TOKEN = lines[0].split()[2].strip("'")
    BOT_NAME = lines[1].split()[2].strip("'")

# autheticate bot
try:
    bot = telegram.Bot(token=TOKEN)
except:
    print('Invalid Token, update .config and try again')
    exit(1)

# sample message
# bot.sendMessage(chat_id=BOT_NAME, text="hello")

# bool variables init 
DONE, DONE_DH1, DONE_DH2 = (False,) * 3

print(TOKEN, BOT_NAME)
print(bot.getMe())


def prettify_before_sending(data, mess_name):
    text = ''
    text += '*'+mess_name+' menu for '+data['date'].strftime("%d-%m-%Y")+"*\n"
    
    meal_in_day = ['Breakfast', 'Lunch', 'Dinner'] 
    for meal_name in meal_in_day:
        print ('\n')
        text += '_'+meal_name+':_ \n '
        for item in data[meal_name]:
            text += '- '+item+'\n '
        text += '\n'

    # print (text)
    return text


def send_to_channel(data, mess_name):

    text = prettify_before_sending(data, mess_name)
    
    # send to the channel
    bot.sendMessage(chat_id=BOT_NAME, 
                    text=text, 
                    parse_mode='Markdown')


def main():
    
    # use global bools
    global DONE, DONE_DH1, DONE_DH2 
    
    while True:
        # get today's datetime, IST timezone 
        ist_timezone = timezone('Asia/Kolkata')
        current_time = datetime.datetime.now(ist_timezone)
        print("current_time in IST: {}".format(current_time))

        # fetch data dict from website
        data = parser()
        print("fetch data complete..")
        if data['DH1']['response'] is True or data['DH2']['response'] is True:
        	print ('partial/complete menu fetch successful from the website')

        if not DONE_DH1:
            print(data['DH1']['response'])
            # if fetched data actually contains menu
            # and if the date of menu is same as today
            if data['DH1']['response'] is True and current_time.month == data['DH1']['date'].month and current_time.day == data['DH1']['date'].day:
            
                # send message through bot and be done with it
                print ('sending DH1 menu channel')
                send_to_channel(data['DH1'], 'DH1')
                DONE_DH1 = True

        if not DONE_DH2:
            print(data['DH2']['response'])
            if data['DH2']['response'] is True and current_time.month == data['DH2']['date'].month and current_time.day == data['DH2']['date'].day:

                # send message through bot and be done with it
                print ('sending DH2 menu to channel')
                send_to_channel(data['DH2'], 'DH2')
                DONE_DH2 = True

        # if done for the day ?
        if DONE_DH1 and DONE_DH2:

            print("ready to sleep now till next day begins")
            DONE = True

            # now sleep till 12 am of next day
            current_time = datetime.datetime.now(ist_timezone)

            # set date to next day 12:01 am
            wake_up_time = current_time
            wake_up_time += datetime.timedelta(days=1)
            wake_up_time = wake_up_time.replace(hour=0, minute=1)

            # sleep for time delta between these two dates
            time.sleep((wake_up_time - current_time).total_seconds())
            # reinit the variables, cuz new day 
            print("woke back up")
            DONE, DONE_DH1, DONE_DH2 = (False,) * 3

        else:
            # sleep for an hour and then try again
            print('will try to fetch again in an hour')
            time.sleep(60 * 60)
            # sleep for half an hour and then try again to fetch the menu
            print('woke up from 1 hr sleep')

if __name__ == '__main__':
	# don't publish menu for today if cli arguement exists
    # not specifiying any specific keyword atm 
    if len(sys.argv) > 1: 
    	DONE_DH2 = DONE_DH1 = True 

    main()
