import telebot
from telebot import types

bot = telebot.TeleBot('your api')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Go to website')
    markup.row(btn1)
    btn2 = types.KeyboardButton('Delete text')
    btn3 = types.KeyboardButton('Change text')
    markup.row(btn2, btn3)
    file = open('images/image.jpg', 'rb')
    bot.send_photo(message.chat.id, file)
    # bot.send_message(message.chat.id, 'Hi', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)

def on_click(message):
    if message.text == 'Go to website':
        bot.send_message(message.chat.id, 'Website is open')

    elif message.text == 'Delete text':
        bot.send_message(message.chat.id, 'Deleted')


# @bot.message_handler(content_types=['text'])
# def get_text(message):
#     markup = types.InlineKeyboardMarkup()
#     btn1 = types.InlineKeyboardButton('Go to website', url='https://google.com')
#     markup.row(btn1)
#     btn2 = types.InlineKeyboardButton('Delete text', callback_data='delete')
#     btn3 = types.InlineKeyboardButton('Change text', callback_data='edit')
#     markup.row(btn2, btn3)
#     bot.reply_to(message, 'Such a nice text!', reply_markup=markup)
#

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == 'edit':
        bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id - 1)


bot.polling(none_stop=True)
