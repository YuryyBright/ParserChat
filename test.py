from telethon import TelegramClient, events, sync

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
api_id = 29139837
api_hash = '047d9d5420e85de93a6a4bd829f65a99'

client = TelegramClient('session_name', api_id, api_hash)
client.start()