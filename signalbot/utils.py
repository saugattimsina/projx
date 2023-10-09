import requests

from django.conf import settings
from celery import shared_task
from user.models import User,UserKey
from .models import TradeSignals

import uuid


from .trade_set import create_my_trade

def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False

reply_url = f"https://api.telegram.org/bot{settings.TELEGRAM_API_TOKEN}/sendMessage"
def commands_handlers(message_text,user_telegram):
    if message_text.startswith("/"):
        reply = f"you typed {message_text}"
        if message_text.startswith("/start"):
            uuid = message_text.split(' ')[-1]
            print("uuid is ",uuid)
            if is_valid_uuid(uuid):
                user = User.objects.filter(user_uuid=uuid,telegram_id=user_telegram).first()
                if user:
                    reply = f"Hi {user.username} you were already registered"
                else:
                    print("the user is",user)
                    user = User.objects.filter(user_uuid=uuid).first()
                    if user:
                        user.telegram_id = user_telegram
                        user.save()
                        reply = f"Hi {user.username} you were registered"
                    else:
                        reply = f"invalid key please recheck \n use /start <your_token> to setup your account" 
            else:
                reply = f"invalid key (non uuid) please recheck \n use /start <your_token> to setup your account"
                
    
    else:
        reply = f"Hi"
    
    return reply



def new_message(message):
    chat_id = message["message"]["chat"]["id"]
    message_text = message["message"]["text"]
    user_telegram = message["message"]["from"]["id"]
    print(message_text)
    return message_text,chat_id,user_telegram

@shared_task
def process_telegram_message(message):
    print(message)
    my_message = message.get('edited_message',None)
    print(my_message)
    
    if not my_message:
        my_message = message.get('message',None)
        if my_message:
            reply,chat_id,user_telegram = new_message(message)
            if reply.startswith("/"):
                reply = commands_handlers(reply,user_telegram)
        else:
            my_message = message.get('callback_query',None)
            if my_message:

                reply,chat_id,user_telegram = new_message(my_message)
                click_data = my_message["data"]
                print(reply,chat_id,user_telegram)
                signal= TradeSignals.objects.get(id=click_data)
                user = User.objects.filter(telegram_id=chat_id).first()
                print(user)
                userkey = UserKey.objects.filter(user=user).first()
                print(userkey)
                trade_data = create_my_trade(signal,user,userkey)
                print(signal)
                print("the data is",click_data)
                reply = f"your trade has been placed we will let you know once it is executed"
        data = {"chat_id": chat_id, "text": reply}

        requests.post(reply_url, data=data)



