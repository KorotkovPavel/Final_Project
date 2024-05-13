import telebot
from config import keys, TOKEN
from extensions import MoneyConverter, ConvertionException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = '''Я Бот-Конвертер валют и я могу вывести конвертацию валюты через команду: 
<Что сконвертировать> <Во что сконвертировать> <количество переводимой валюты>
    Например: "доллар рубль 10" - переведет 10 долларов в рубли
- Показать список доступных валют через команду: /values
- Напомнить, что я могу через команду: /help'''
    bot.reply_to(message, text)
@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = '''- Чтобы сделать конвертацию валют необходимо отправить три параметра в формате: 
<Что сконвертировать> <Во что сконвертировать> <количество переводимой валюты>
    Например: "доллар рубль 10" - переведет 10 долларов в рубли
- Показать список доступных валют через команду: /values'''
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types='text')
def hello(message: telebot.types.Message):
    if message.text.lower() in ['привет', 'хай', 'здарова']:
        bot.send_message(message.chat.id, f'''Приветствую уважаемый пользователь, {message.chat.username}!
К сожалению, я пока не ИИ))), я бот-конвертер валют.
Для начала работы нажми /start
        ''')
    elif message.text.lower() in ['что ты умеешь', 'что ты делаешь']:
        bot.send_message(message.chat.id, 'Для начала работы нажми /start, и все узнаешь!')
    else:
        try:
            value = message.text.lower().split(' ')

            if len(value) > 3:
                raise ConvertionException('''Вы ввели больше трёх параметров для запроса конвертации.
    Необходимо ввести команду в формате: 
    <Что сконвертировать> <Во что сконвертировать> <количество переводимой валюты>
        Например: "доллар рубль 10" - переведет 10 долларов в рубли
    - Показать список доступных валют через команду: /values
    - Напомнить, что я могу через команду: /help''')
            elif len(value) < 3:
                raise ConvertionException('''Вы ввели меньше трёх параметров для запроса конвертации.
    Необходимо ввести команду в формате: 
    <Что сконвертировать> <Во что сконвертировать> <количество переводимой валюты>
        Например: "доллар рубль 10"  - переведет 10 долларов в рубли
    - Показать список доступных валют через команду: /values
    - Напомнить, что я могу через команду: /help''')
            quote, base, amount = value
            total_base = MoneyConverter.convert(quote, base, amount)
        except ConvertionException as e:
            bot.reply_to(message, f'''Ошибка на стороне пользователя:\n{e} ''')
        except Exception as e:
            bot.reply_to(message, f'''Данная команда мне не известна:\n{e}''')
        else:
            text = f'Конвертация {amount} {quote} в {base}: \n{amount} {quote} = \
    {'{0:,}'.format(total_base.__round__(2)).replace(',', ' ')} {base}'
            bot.send_message(message.chat.id, text)



bot.polling()