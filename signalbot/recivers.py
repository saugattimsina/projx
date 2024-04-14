print("hello world")


from functools import partial

from django.dispatch import receiver
from telethon import events

from django_telethon.signals import telegram_client_registered


async def event_handler(event, client_session):
    print(client_session.name, event.raw_text, sep=" | ")
    # if you need access to telegram client, you can use event.client
    # telegram_client = event.client

    print(event)
    await event.respond("!pong")


@receiver(telegram_client_registered)
def receiver_telegram_registered(telegram_client, client_session, *args, **kwargs):
    print("called")
    handler = partial(event_handler, client_session=client_session)
    telegram_client.add_event_handler(
        handler,
        events.NewMessage(incoming=True, pattern="/ping"),
    )
    print(handler)
