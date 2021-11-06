import telebot
import random

token = ''

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def send_start_message(message):
    bot.send_message(message.chat.id, 'INFO: /get - new image')

@bot.message_handler(commands=['get'])
def send_photo(message):
    base_url = 'https://aws.random.cat/view/'
    number= random.randint(1, 100)
    bot.send_photo(message.chat.id, base_url + str(number))

bot.polling(none_stop=True, interval=0)
