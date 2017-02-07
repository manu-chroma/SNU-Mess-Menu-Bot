import telegram
import time
import datetime
import dateutil

from parser import parser
# from dateutil import parser

# initialise tele bot

# parse .config file to obtain token and public channel name 
with open('.config', 'r') as f:
    lines = f.readlines()
    # collect token from the config file 
    TOKEN = lines[0].split()[2].strip("'")

bot = telegram.Bot(token=TOKEN)


# constants for better code understanding
DH1 = 0
DH2 = 1

# done for the day ?
DONE = False
DONE_DH1 = False
DONE_DH2 = False

def send_to_channel(data):
    print("about to send something")
    text = data
    # data[0]['date'] = dateutil.parser

    del data[0]['date']
    del data[1]['date']
    text = ''
    mess_names = ['DH1', 'DH2']
    bot.sendMessage(chat_id='@snu_mess_menu', text=text)

def main():
    bot.sendMessage(chat_id='@snu_mess_menu', text="hello")

    # declare globals
    global DONE, DONE_DH1, DONE_DH2

    current_time = datetime.datetime.now()

    mess_names = ['DH1', 'DH2']

    while True:
        # fetch data dict from website
        data = parser()
        print("fetch data complete")

        if not DONE:
            if not DONE_DH1:
                print(data[DH1]['response'])
                if data[DH1]['response'] is True: #and current_time._month == data[DH1]['date']._month:
                    print("hello")
                    # send message through bot and be done with it
                    # todo: how to send data in a formatted manner
                    send_to_channel(data)
                    DONE_DH1 = 1


            if not DONE_DH2:
                print(data[DH1]['response'])
                if data[DH2]['response'] is True:
                    print("hello")
                    # send message through bot and be done with it
                    send_to_channel(data)
                    DONE_DH2 = 1

            if DONE_DH1 and DONE_DH2:

                print("ready to sleep now")

                DONE = 1
                # now sleep till 12 am of next day
                current_time = datetime.datetime.now()

                # set date to next day 12:01 am
                wake_up_time = current_time
                wake_up += datetime.timedelta(days=1)
                wake_up_time.replace(hour=0, minute=1)

                # sleep for time delta between these two dates
                time.sleep((wake_up_time-current_time).total_seconds())

            else:
                # sleep for an hour and then try again
                time.sleep(60*60)
        # sleep for half an hour and then try again to fetch the menu

    print(bot.getMe())

    # sending test message to the channel
    # bot.sendMessage(chat_id='@snu_mess_menu', text='This is a test message')

if __name__ == '__main__':
    pass
    # main()
    data = parser()
    send_to_channel(data)