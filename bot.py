import config
import telebot
import dbworker
from telebot import types
import GetSchedule
from time import sleep

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Поиск по станции', callback_data='Station_Search'))
    keyboard.add(types.InlineKeyboardButton(text='Поиск между станциями', callback_data='Schedule_Search'))
    bot.send_message(message.chat.id, 'Выберите желаемое действие', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: (True and call.data == 'Station_Search'))
def callback_inline(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Введите название станции")
    dbworker.set_state(call.message.chat.id, config.States.S_STATIONSEARCH.value)


@bot.callback_query_handler(func=lambda call: (True and call.data == 'Schedule_Search'))
def callback_inline(call):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='Back_to_start'))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Вам сюда нельзя", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: (True and call.data == 'Back_to_start'))
def callback_inline(call):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Поиск по станции', callback_data='Station_Search'))
    keyboard.add(types.InlineKeyboardButton(text='Поиск между станциями', callback_data='Schedule_Search'))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Выберите желаемое действие", reply_markup=keyboard)


@bot.message_handler(func=lambda message: (message.text and
                                           dbworker.get_state(message.chat.id) == config.States.S_STATIONSEARCH.value))
def station_search(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='Back_to_start'))
    result = GetSchedule.print_data(message.text)  # Цикл for для создания колбек клавиш, для переходя по станциям
    bot.send_message(message.chat.id, result, reply_markup=keyboard)
    dbworker.set_state(message.chat.id, config.States.S_START.value)


if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print('FAIL')
        print(e)
        print('--------')
