import config
import logging
import time
import telebot
from telebot import types
import dbworker
import GetSchedule

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Поиск по станции', callback_data='Station_Search'))
    keyboard.add(types.InlineKeyboardButton(text='Поиск между станциями', callback_data='Schedule_Search'))
    bot.send_message(message.chat.id, 'Выберите желаемое действие', reply_markup=keyboard)
    dbworker.set_state(message.chat.id, config.States.S_START.value)


@bot.callback_query_handler(func=lambda call: (True and call.data == 'Station_Search'))
def callback_inline(call):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='Back_to_start'))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Ввдите название станции", reply_markup=keyboard)
    dbworker.set_state(call.message.chat.id, config.States.S_STATIONSEARCH.value)


@bot.callback_query_handler(func=lambda call: (True and call.data == 'Schedule_Search'))
def callback_inline(call):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='Back_to_start'))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Вам сюда нельзя", reply_markup=keyboard)
    dbworker.set_state(call.message.chat.id, config.States.S_THROUGHSTATIONS.value)


@bot.callback_query_handler(func=lambda call: (True and call.data == 'Back_to_start'))
def callback_inline(call):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Поиск по станции', callback_data='Station_Search'))
    keyboard.add(types.InlineKeyboardButton(text='Поиск между станциями', callback_data='Schedule_Search'))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Выберите желаемое действие", reply_markup=keyboard)
    dbworker.set_state(call.message.chat.id, config.States.S_START.value)


@bot.callback_query_handler(func=lambda call: (True and call.data.startswith('Some_station ')))
def send_message_with_station(call):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='Back_to_start'))
    station_id = call.data.split(' ')
    result_message = GetSchedule.print_data(station_id[1])
    bot.send_message(call.message.chat.id, result_message, reply_markup=keyboard)
    dbworker.set_state(call.message.chat.id, config.States.S_START.value)


@bot.message_handler(func=lambda message: (message.text and
                                           dbworker.get_state(message.chat.id) == config.States.S_STATIONSEARCH.value))
def station_search(message):
    result = dbworker.fetch_stations(message.text)
    if not result:
        bot.send_message(message.chat.id, 'К сожалению такю станцию найти не удалось')
        dbworker.set_state(message.chat.id, config.States.S_START.value)
    else:
        keyboard = types.InlineKeyboardMarkup()
        result_message = 'Выберите станцию из списка:\n\n'
        # Цикл for для создания колбек клавиш, для переходя по станциям
        # Переход по нужной станции производится нажатием на колбек кнопку с определенной информацией о станции
        for station in result:
            result_message += station[1] + '\n' + station[2] + '\n\n'
            keyboard.add(types.InlineKeyboardButton(text=station[1], callback_data='Some_station ' + str(station[0])))
        keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='Back_to_start'))
        bot.send_message(message.chat.id, result_message, reply_markup=keyboard)


if __name__ == '__main__':
    logging.basicConfig(filename='errors.log', filemode='a', level=logging.INFO)
    log = logging.getLogger('Exception')
    while True:
        try:
            bot.polling()
        except Exception as e:
            log.exception(e)
            time.sleep(5)
            continue
