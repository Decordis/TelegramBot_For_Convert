import telebot
from telebot import types
from info import valut
from extensions import APIException, Conversation
from dotenv import load_dotenv
import os
load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))

@bot.message_handler(commands = ['start',])
def _start_(message):
    markup = types.ReplyKeyboardMarkup()
    bt1 = types.KeyboardButton('/instruction')
    bt2 = types.KeyboardButton('/currency')
    markup.row(bt1, bt2)
    bt3 = types.KeyboardButton('/getcur')
    bt4 = types.KeyboardButton('/help')
    markup.row(bt3,bt4)
    text = (f'Приветствую дорогой {message.chat.username}! 😌 Я здесь для того, чтобы быстро сконвертировать Вам валюту! '
            f'Чтобы узнать, как я работаю, кликайте "instruction". Чтобы получить данные о валютах, кликайте "currency"')

    bot.send_message(message.chat.id, text, reply_markup = markup)

@bot.message_handler(commands = ['instruction',])
def info(message):
    text = ("1) Введите имя валюты из которой вы хотите конвертировать (без запятых с большой буквы)\n"
            "2) введите имя валюты в которую вы хотите конвертировать\n"
            "3) введите число (сумму) для конвертации \n"
            "<b><u>Пример: Рубль Евро 1</u></b>")
    bot.send_message(message.chat.id, text, parse_mode='html')

@bot.message_handler(commands = ['help',])
def info(message):
    text = ('Есть проблема?😵‍💫 \n'
            'Спокойствие и только спокойствие! \n\n'
            
            'Проверьте, правильно ли вы написали: \n'
            '1)<b>Валюты:</b>\n '
            '✅ без запятых, с большой буквы — "Рубль Евро 1"\n\n'
            
            '❌ Большими буквами, неправильное название валюты —  "РУБЛИ евра"\n'
            '❌ С маленькой буквы — "рубль евро"\n '
            '❌ Запятая между словами — "Доллар, Евро"\n\n'
            
            '2)<b>Сумму для конвертации:</b> \n'
            '✅ Число без запятых — "1", "50", "125"\n\n'
            
            ' ❌ Использование букв, знаков — "абс", "1,24", "1абс", "-1"')

    bot.send_message(message.chat.id, text, parse_mode='html')


@bot.message_handler(commands = ['currency',])
def currency(message: telebot.types.Message):
    text = "<b>Доступные валюты:</b>"
    for keys in valut.keys():
        text = '\n'.join((text, keys, ))
    bot.send_message(message.chat.id, text, parse_mode='html')



@bot.message_handler(commands=['getcur'])
def send_go(message):
    bot.reply_to(message, 'oкей, жду! 👌🏻')

    @bot.message_handler(content_types=['text'])
    def convert_func(message):
        try:
            cur = message.text.split(' ')
            if len(cur) != 3:
                raise APIException(f'неправильное введение! 😔')

            quote, base, amount = cur
            result = Conversation.convert(quote, base, amount)

        except APIException as e:
            bot.reply_to(message, f'ошибка пользователя \n{e}')

        except Exception as e:
            bot.reply_to(message, f'ошибка бота\n {e}')
        else:
            text = f' цена {amount} {quote} в {base} - {result}'

            bot.reply_to(message, text)

bot.polling(non_stop=True)




