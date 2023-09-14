TOKEN = "6167336537:AAGaviat4GGhS8gdTeoA6xHf9YRQ8-_-5QI"


api_id =   1437138
api_hash = "b4a91503f2be00dbced4fedeb3364c39"
import django
import os
os.environ["DJANGO_SETTINGS_MODULE"] =  "projx.settings"
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

# ---------------------------------------------------------------------------
# Telegrbotpart
# ---------------------------------------------------------------------------
from telethon import TelegramClient, events
# from asgiref.sync import sync_to_async  # Import async_to_sync
import threading
# from signalbot.views import user_car
from user.models import User
from django.db import connection
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
import queue

result_queue = queue.Queue()
def user_car(user_uuid,id):
    try:
        user = User.objects.get(user_uuid=user_uuid)
        print(user.user_uuid)
        if user:
            if user_uuid == user.user_uuid:
                message = f"Your telegram account has already been linked to your account {user.username}"
            else:    
                user.telegram_id = id
                user.save()
                print(user)
                message = f"Your telegram account has been linked to your account {user.username}"
    except User.DoesNotExist:
        print("User not found")
        message = "Invalid code"
    except Exception as e:
        print("An error occurred:", e)
        message = "An error occurred please retry \n /start <code>"
        
    result_queue.put(message)
    return message



async def handle_start_event(event):
    print(event)
    id = event.peer_id.user_id
    message = event.message.message
    user_code = message.split(' ')[-1]
    
    # Create a thread to run user_car
    user_car_thread = user_car(user_code,id)
    print("user thread",user_car_thread)

    await event.reply(
        user_car_thread,
        link_preview=False
    )


def send_telegram_message(message):
    client.send_message("message")


# Initialize the client and attach the event handler
try:
    with TelegramClient('my_bot_session', api_id=api_id, api_hash=api_hash) as client:
        client.add_event_handler(handle_start_event, events.NewMessage(pattern=r'/start'))
        client.start()
        client.run_until_disconnected()
except Exception as e:
    print(e)


