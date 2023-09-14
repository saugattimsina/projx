from signalbot.models import TradeSignals
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
import requests
from user.models import User
from celery import shared_task
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
import json

# import tracemalloc
# tracemalloc.start()
# # from telegram1 import send_telegram_message
# import telegram
# bot = telegram.Bot(token='6167336537:AAGaviat4GGhS8gdTeoA6xHf9YRQ8-_-5QI')
reply_url = f"https://api.telegram.org/bot{settings.TELEGRAM_API_TOKEN}/sendMessage"



# Convert the keyboard dictionary to JSON format
# @shared_task
@receiver(post_save, sender=TradeSignals)
def create_default_subscription(sender, instance, created, **kwargs):
    print(instance)
    # if created:
    users_with_uuid = User.objects.filter(user_uuid__isnull=False)

    keyboard = {
    "inline_keyboard": [
        [{"text": "Follow Signal", "callback_data": instance.id}],
        # [{"text": "Option 2", "callback_data": "option2_data"}],
        [{"text": "Open Google", "url": "https://www.google.com"}],
    ]
    }
    keyboard_json = json.dumps(keyboard)


    message = f"New trade signal created: Symbol - {instance.symbol}, Side - {instance.trade_side}"
    for user in users_with_uuid:
        data = {"chat_id": user.telegram_id, "text": message, "reply_markup": keyboard_json}
        requests.post(reply_url, data=data)

