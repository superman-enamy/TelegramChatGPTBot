import telebot
from telebot import types

import g4f


api_key_telegram = '6145433381:AAEfS37sKEfLjesp57D9QSdC5F4DXW4ioLM'

bot = telebot.TeleBot(api_key_telegram)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Start")
    markup.add(btn1)
    bot.send_message(message.chat.id, "Hi, I'm the Telegram bot ChatGPT!", reply>


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {'role': 'user', 'content': message.text}
        ],
        'max_tokens': 1000,
        'n': 1,
        'temperature': 0.1
    }

    chat_completion = g4f.ChatCompletion.create(**data)
    response = chat_completion.create()

    bot.send_message(
        message.chat.id,
        response.messages[0].content,
        reply_markup=markup
    )

bot.polling(none_stop=True, interval=1)
