import config
import telebot
# import dbworker
from telebot import types
import GetSchedule

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Півд. Півд-Зах. Дон. зал.', callback_data='South'))
    keyboard.add(types.InlineKeyboardButton(text='Одеська зал.', callback_data='Odesa'))
    keyboard.add(types.InlineKeyboardButton(text='Львівська зал.', callback_data='Lviv'))
    keyboard.add(types.InlineKeyboardButton(text='Дніпропетр. зал.', callback_data='Dnipro'))
    bot.send_message(message.chat.id, 'Оберіть регіон', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: (True and call.data == 'South'))
def callback_inline(call):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Пошук по станції', callback_data='StationSearch'))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Введите номер станции: ", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text)  # Need change to block before choose region
def object_message(message):
    bot.send_message(message.chat.id, "Result:\n" + GetSchedule.print_data(int(message.text)))


if __name__ == '__main__':
    bot.polling(none_stop=True)
