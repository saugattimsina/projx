from signalbot.models import TradeSignals, TradeHistory
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
import requests
from user.models import User, UserKey
from celery import shared_task
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
import json
from .trade_set import create_my_trade
import logging
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db import transaction

# import tracemalloc
# tracemalloc.start()
# # from telegram1 import send_telegram_message
# import telegram
# bot = telegram.Bot(token='6167336537:AAGaviat4GGhS8gdTeoA6xHf9YRQ8-_-5QI')
reply_url = f"https://api.telegram.org/bot{settings.TELEGRAM_API_TOKEN}/sendMessage"

# logger = logging.getLogger("django.request")


# Convert the keyboard dictionary to JSON format
# @shared_task
@receiver(post_save, sender=TradeSignals)
def create_default_subscription(sender, instance, created, **kwargs):
    print(instance)
    # if created:
    print("signal recived")
    # logger.info("signal recived")
    users_with_uuid = User.objects.filter(is_client=True)

    keyboard = {
        "inline_keyboard": [
            [{"text": "Follow Signal", "callback_data": instance.id}],
            # [{"text": "Option 2", "callback_data": "option2_data"}],
            [{"text": "Open Google", "url": "https://www.google.com"}],
        ]
    }
    keyboard_json = json.dumps(keyboard)

    message = f"New trade signal created: Symbol - {instance.symbol} \n entryprice :{instance.price} \n stoploss :{instance.stop_amount}"
    print("user with uuid", users_with_uuid)
    data = {}
    for user in users_with_uuid:
        if user.auto_set_trade:
            print("auto set trade", user)

            user_key = UserKey.objects.filter(user=user)
            print("key user ", user_key)
            if user_key:
                print("thau ma aayo")
                x = create_my_trade(instance, user, user_key[0])
                print(x)
                message = "Your Trade has been executed we are updating the message."
                data = {
                    "chat_id": user.telegram_id,
                    "text": message,
                    "reply_markup": keyboard_json,
                }
            else:
                data = {
                    "chat_id": user.telegram_id,
                    "text": "please Setup Your Binance Future Api Key",
                }

        elif user.telegram_id:
            data = {
                "chat_id": user.telegram_id,
                "text": message,
                "reply_markup": keyboard_json,
            }
        else:
            continue

        requests.post(reply_url, data=data)


@receiver(post_save, sender=TradeHistory)
def create_telegram_msg(sender, instance, created, **kwargs):
    if created:
        reply_url = (
            f"https://api.telegram.org/bot{settings.TELEGRAM_API_TOKEN}/sendMessage"
        )
        chat_id = instance.user.telegram_id
        if chat_id:
            reply = "your trade has been created"
            data = {"chat_id": chat_id, "text": reply}
            try:
                requests.post(reply_url, data=data)
            except:
                pass


@receiver(post_save, sender=TradeHistory)
def send_trade_update(sender, instance, created, **kwargs):

    def send_update():
        channel_layer = get_channel_layer()
        group_name = f"user_{instance.user.username}"
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "send_initial_trade_history",
            },
        )

    transaction.on_commit(send_update)
