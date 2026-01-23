import os
import json
import logging
from datetime import datetime
from telethon import TelegramClient
from dotenv import load_dotenv

# 1. Setup & Credentials
load_dotenv()
api_id = os.getenv('TG_API_ID')
api_hash = os.getenv('TG_API_HASH')
phone = os.getenv('TG_PHONE')

log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
    
# Channels to scrape
channels = [
    'CheMed1',              # CheMed Telegram Channel
    'lobelia4cosmetics',    # Lobelia Cosmetics
    'tikvahpharma',         # Tikvah Pharma
]

# Configure Logging
logging.basicConfig(
    filename='logs/scraping.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

async def scrape_channel(client, channel_username):
    logging.info(f"Starting scrape for {channel_username}...")
    
    # Path for images
    image_dir = f'data/raw/images/{channel_username}'
    os.makedirs(image_dir, exist_ok=True)
    
    # Path for JSON data (Partitioned by date)
    date_str = datetime.now().strftime('%Y-%m-%d')
    json_dir = f'data/raw/telegram_messages/{date_str}'
    os.makedirs(json_dir, exist_ok=True)
    
    messages_data = []

    async for message in client.iter_messages(channel_username, limit=100):
        # Extract metadata
        msg_info = {
            "message_id": message.id,
            "channel_name": channel_username,
            "message_date": str(message.date),
            "message_text": message.text or "",
            "has_media": message.media is not None,
            "views": message.views or 0,
            "forwards": message.forwards or 0,
            "image_path": None
        }

        # Download images if present
        if message.photo:
            file_path = await message.download_media(file=image_dir)
            msg_info["image_path"] = file_path
            logging.info(f"Downloaded image for message {message.id}")

        messages_data.append(msg_info)

    # Save to JSON
    output_file = f"{json_dir}/{channel_username}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(messages_data, f, indent=4, ensure_ascii=False)
    
    logging.info(f"Successfully saved {len(messages_data)} messages for {channel_username}")

async def main():
    async with TelegramClient('kara_session', api_id, api_hash) as client:
        for channel in channels:
            try:
                await scrape_channel(client, channel)
            except Exception as e:
                logging.error(f"Error scraping {channel}: {e}")

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())