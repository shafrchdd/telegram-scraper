from telethon.sync import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest
import time

api_ids = ['your_api_id_1', 'your_api_id_2']  # Add more API IDs as needed
api_hashes = ['your_api_hash_1', 'your_api_hash_2']  # Add more API hashes as needed
phone_numbers = ['your_phone_number_1', 'your_phone_number_2']  # Add more phone numbers as needed

# Load member data from scraped_data.txt file
scraped_data = []
with open('scraped_data.txt', 'r') as file:
    for line in file:
        username, user_id = line.strip().split(',')
        scraped_data.append((username.strip(), int(user_id.strip())))

async def add_members(client_index):
    client = TelegramClient(phone_numbers[client_index], api_ids[client_index], api_hashes[client_index])

    await client.start()

    channel_username = 'your_channel_username'
    for i in range(client_index * 50, min((client_index + 1) * 50, len(scraped_data))):
        username, user_id = scraped_data[i]
        try:
            await client(InviteToChannelRequest(channel_username, [user_id]))
            print(f"Added {username} ({user_id}) from client {client_index + 1} to channel.")
        except Exception as e:
            print(f"Failed to add {username} ({user_id}) from client {client_index + 1}: {e}")

    await client.disconnect()

# Loop through client accounts
for i in range(len(api_ids)):
    asyncio.run(add_members(i))
    time.sleep(60)  # Add delay to avoid rate limiting or blocking by Telegram API
