import sqlite3
import telebot
from telebot import types

bot = telebot.TeleBot('Your API')


phone_number = ''
description = ''
price = 0


@bot.message_handler(commands=['start'])
def question(message):
    conn = sqlite3.connect('x.sql')
    cur = conn.cursor()

    cur.execute(
        'CREATE TABLE IF NOT EXISTS appartments(id int auto_increment primary key, phone_number varchar(50), description varchar(200), price int )')
    conn.commit()
    cur.close()
    conn.close()

    markup = types.InlineKeyboardMarkup(row_width=1)
    make_advert_btn = types.InlineKeyboardButton('Make advert and pay', callback_data='make_advert')
    watch_advert_btn = types.InlineKeyboardButton('Watch adverts', callback_data='watch_advert')
    markup.add(make_advert_btn, watch_advert_btn)
    bot.send_photo(message.chat.id, open('images/image.jpg', 'rb'), 'Choose what to do:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def get_callback(callback):
    if callback.data == 'make_advert':
        bot.send_message(callback.message.chat.id, 'Please input your phone number')
        bot.register_next_step_handler(callback.message, get_phone_number)
    else:
        conn = sqlite3.connect('x.sql')
        cur = conn.cursor()

        cur.execute('SELECT * FROM appartments')
        appartments = cur.fetchall()

        info = ''

        for appartment in appartments:
            info += f'Phone number: {appartment[1]}\n Description: {appartment[2]} \n Price: {appartment[3]}\n\n'

        cur.close()
        conn.close()

        bot.send_message(callback.message.chat.id, info)


def get_phone_number(message):
    global phone_number
    phone_number = message.text
    bot.send_message(message.chat.id, 'Please input description of appartment')
    bot.register_next_step_handler(message, get_description)


def get_description(message):
    global description
    description = message.text
    bot.send_message(message.chat.id, 'Please input price of appartment')
    bot.register_next_step_handler(message, get_price)


def get_price(message):
    global price
    price = int(message.text)

    conn = sqlite3.connect('x.sql')
    cur = conn.cursor()

    cur.execute("INSERT INTO appartments (phone_number, description, price) VALUES ('%s', '%s', '%s')" % (
        phone_number, description, price))
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Your appartment was publised! Write /start to go in menu')


bot.polling(none_stop=True)
