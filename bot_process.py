TOKEN = "6167336537:AAGaviat4GGhS8gdTeoA6xHf9YRQ8-_-5QI"
import django
import os
os.environ["DJANGO_SETTINGS_MODULE"] =  "projx.settings"
django.setup()

testnet_api_key = "8366bcdb3b876a06242c274783c612ee4a5467a489aeab364ff2455c43328910"
testnet_api_secret = "ff2fbf60ead7192f02ea3df3d1ee134854cdb91f8fbc12816eb5d6b48ab5f897"

import telebot
# from user.models import User
import logging
# from django.core.management.base import BaseCommand
from user.models import User

logger = logging.getLogger(__name__)
bot = telebot.TeleBot(TOKEN, parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN
import pprint
# class Command(BaseCommand):
#     help = 'Run the Telegram bot'
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    x = message
    print(x.json)
    username = x.json['chat']['username']
    user_command = x.json['text']
    user_uuid = user_command.split(' ') 
    try:
        user_uuid_valid =  user_uuid[2]
        try:
            user = User.objects.get(user_uuid=user_uuid_valid)
            print(user)
            if user:
                user.telegram_id = x.json['chat']['id']
                user.save()
                response_message = f"hello {user.username} you are validated"
        except:
            
            response_message = "sorry you are not validated please enter uour correct token"
        

    except IndexError:
        response_message = "please use \start <your token> to start the bot"
        #
    
    bot.reply_to(message, f"{response_message}")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

# def get_keyboard_markup() -> InlineKeyboardMarkup:
#     # Define your clickable options
#     buttons = [
#         [
#             InlineKeyboardButton("Option 1", callback_data="option1"),
#             InlineKeyboardButton("Option 2", callback_data="option2"),
#         ],
#         [InlineKeyboardButton("Option 3", callback_data="option3")],
#     ]
#     return InlineKeyboardMarkup(buttons)


bot.infinity_polling()