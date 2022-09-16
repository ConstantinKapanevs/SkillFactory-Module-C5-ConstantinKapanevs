from config import keys, TOKEN
from extensions import ConverterException, Converter
import telebot


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def greet_function(message):
    text = "Добро пожаловать в бот пересчета валюты.\n" \
           "Для получения информации о доступных\n" \
           "валютах используйте /info.\n" \
           "Формат ввода для пересчета:\n" \
           "<Базовая валюта> <Валюта, в которую пересчитывать> <Сумма в базовой валюте>."
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['info', ])
def info_function(message):
    text = f"Доступные валюты для пересчета:\n" \
           f"{', '.join(keys.keys())}"
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text', ])
def converter_function(message):
    try:
        text = Converter.calculate_rate(message)
    except ConverterException as e:
        bot.reply_to(message, f'{e}')
    except Exception as e:
        bot.reply_to(message, f'{e}')
    else:
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
