from telethon.sync import TelegramClient
from django_telethon.sessions import DjangoSession
from django_telethon.models import App, ClientSession
from telethon.errors import SessionPasswordNeededError

# Use your own values from my.telegram.org
api_id =   1437138
api_hash = "b4a91503f2be00dbced4fedeb3364c39"

app, is_created = App.objects.update_or_create(
    api_id=api_id,
    api_hash=api_hash,
)
cs, cs_is_created = ClientSession.objects.update_or_create(
    name='default',
)
telegram_client = TelegramClient(DjangoSession(client_session=cs), app.api_id, app.api_hash)
telegram_client.connect()
