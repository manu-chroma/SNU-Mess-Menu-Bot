import telegram


TOKEN = ''
bot = telegram.Bot(token=TOKEN)

print(bot.getMe())

# sending test message to the channel
bot.sendMessage(chat_id='@snu_mess_menu', text='This is a test message')