from telethon import TelegramClient, events, sync

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
api_id = 12341234
api_hash = '12341234124'

client = TelegramClient('session_name', api_id, api_hash)
client.start()
