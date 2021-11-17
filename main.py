import telebot
import random
import sqlite3
import schedule
import time

token = ''

bot = telebot.TeleBot(token)

connection = sqlite3.connect('DataBase.db')
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users(
            userId INT PRIMARY KEY,
            TgName TEXT,
            TgId TEXT,
            RealName TEXT,
            State INT
                )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS subCat(
            userId INT PRIMARY KEY,
            TgName TEXT,
            TgId TEXT
                )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS subDog(
            userId INT PRIMARY KEY,
            TgName TEXT,
            TgId TEXT
                )""")

connection.commit()

state = 0

def get_state(message):
    return state

@bot.message_handler(commands=['start'])
def send_start_message(message):
    bot.send_message(message.chat.id, 'INFO: /get_cat - new cat image \n/get_dog - new dog image \n/subscribe_cats - become cat subscriber \n/subscribe_dogs - become dog subscriber \n/get_cat_subscribers - cat subscribers list \n/get_dog_subscribers - dog subscribers list')
    bot.send_message(message.chat.id, 'What is your name?')
    global state
    state = 1

@bot.message_handler(func= lambda message: get_state(message) == 1)
def ask_preferances(message):
    bot.send_message( message.chat.id, 'Hi, ' + message.text)
    global state
    state = 2
    local_connection = sqlite3.connect('DataBase.db')
    local_cursor = local_connection.cursor()
    local_cursor.execute("INSERT INTO users VALUES(?,?,?,?,?);", (message.chat.id, message.from_user.first_name, message.from_user.username, message.text, state))
    local_connection.commit()

@bot.message_handler(commands=['get_cat'])
def send_cat_photo(message):
    base_url = 'https://aws.random.cat/view/'
    number= random.randint(1, 100)
    bot.send_photo(message.chat.id, base_url + str(number))

@bot.message_handler(commands=['get_dog'])
def send_dog_photo(message):
    base_url = 'https://placedog.net/640/480?random'
    bot.send_photo(message.chat.id, base_url)

@bot.message_handler(commands=['subscribe_cats'])
def subscribe(message):
    local_connection= sqlite3.connect('DataBase.db')
    local_cursor = local_connection.cursor()
    local_cursor.execute("INSERT INTO subCat VALUES(?,?,?);", (message.chat.id, message.from_user.first_name, message.from_user.username))
    local_connection.commit()
    schedule.every(1).minute.do(send_cat_photo, message=message)
    while True:
        schedule.run_pending()

@bot.message_handler(commands=['subscribe_dogs'])
def subscribe(message):
    local_connection= sqlite3.connect('DataBase.db')
    local_cursor = local_connection.cursor()
    local_cursor.execute("INSERT INTO subDog VALUES(?,?,?);", (message.chat.id, message.from_user.first_name, message.from_user.username))
    local_connection.commit()
    schedule.every(1).minute.do(send_dog_photo, message=message)
    while True:
        schedule.run_pending()

@bot.message_handler(commands=['get_cat_subscribers'])
def get_subscriber(message):
    local_connection = sqlite3.connect('DataBase.db')
    local_cursor = local_connection.cursor()
    local_cursor.execute("SELECT * from subCat;")
    all_results = local_cursor.fetchall()
    bot.send_message(message.chat.id, str(message.from_user.first_name))

@bot.message_handler(commands=['get_dog_subscribers'])
def get_subscriber(message):
    local_connection = sqlite3.connect('DataBase.db')
    local_cursor = local_connection.cursor()
    local_cursor.execute("SELECT * from subDog;")
    all_results = local_cursor.fetchall()
    bot.send_message(message.chat.id, str(message.from_user.first_name))

bot.polling(none_stop=True, interval=0)