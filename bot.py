import telebot	
from telebot import types 

import requests
import json

api_key_telegram = 'API_TELEGRAM_KEY'
api_key_openai = 'API_OPENAI_KEY'



bot = telebot.TeleBot(api_key_telegram) 

url = 'https://api.openai.com/v1/chat/completions'
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer '+api_key_openai
}

data = {
    'model': 'gpt-3.5-turbo',  # Selected GPT model
    'messages': [
        {'role': 'system','content': 'You are my assistant.'}, # We specify the role of the bot
    ],
    'max_tokens': 1000,  # Maximum number of tokens in the response
    'n': 1,  #  Number of text variants
    'temperature': 0.1  # Temperature (creative component)
}


@bot.message_handler(commands=['start']) # This decorator says that the next function should be called when the bot receives a message with the /start command.
def start(message): # This is the definition of the start function. This function will be called when the bot receives a message with the /start command.
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True) 
    btn1 = types.KeyboardButton("Start")
    markup.add(btn1) 
    bot.send_message(message.from_user.id, "Hi, I'm the Telegram bot ChatGPT!", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    data['messages'].append({"role": "user", "content": message.text}) # Add a new user request to our dialog array, form a request to the server on behalf of the user, with the text received in telegram
    response = requests.post(url, headers=headers, data=json.dumps(data))  # Send a request to the server in json format
    result = response.json() # get the answer in json format and convert to an array
    print(result)
    bot.send_message(message.from_user.id, result['choices'][0]['message']['content'], reply_markup=markup) # Take the text from the array from ChatGPT and send it to Telegram
    data['messages'].append({"role": "assistant", "content": result['choices'][0]['message']['content']}) # Add a new bot response to our dialog array

    # Delete the first element of the array if the array is longer than 40 elements, but leave the first element of the array, which is the initial text of the bot
    while len(data['messages']) > 40:
        data['messages'].pop(1)

bot.polling(none_stop=True, interval=1) # for the bot to start "listening" or "polling" the Telegram server for new messages. "Polling" means regularly receiving data from the Telegram server by the bot to find out if new messages have been received for it.



