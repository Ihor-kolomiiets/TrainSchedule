import config
import telebot
# import dbworker
# from telebot import types
import GetSchedule

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Просто проверка работы\n' + GetSchedule.print_data())


if __name__ == '__main__':
    bot.polling(none_stop=True)
