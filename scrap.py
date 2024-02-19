from telethon.sync import TelegramClient
from datetime import datetime, timedelta

api_id = 'your_api_id'
api_hash = 'your_api_hash'
phone_number = 'your_phone_number'

client = TelegramClient(phone_number, api_id, api_hash)

async def main():
    await client.start()
    
    # Replace 'your_channel_or_group_username' with the username of your specific group or channel
    target_username = 'your_channel_or_group_username'
    
    # Define the time threshold for activity filtering
    active_time_threshold = datetime.now() - timedelta(days=1)  # Change timedelta according to your preference

    scraped_data = []

    async for dialog in client.iter_dialogs():
        if (dialog.is_channel or dialog.is_group) and dialog.entity.username == target_username:
            async for member in client.iter_participants(dialog):
                last_seen_time = datetime.now() if member.status.last_seen is None else member.status.last_seen
                if last_seen_time >= active_time_threshold:
                    scraped_data.append((member.username, member.id))

    # Writing scraped data to a text file
    with open('scraped_data.txt', 'w') as file:
        for username, user_id in scraped_data:
            file.write(f"{username}, {user_id}\n")

with client:
    client.loop.run_until_complete(main())
