import os
import json
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        port=os.getenv('DB_PORT')
    )

def load_data():
    conn = get_connection()
    cur = conn.cursor()
    
    # 1. Create Raw Schema and Table
    cur.execute("CREATE SCHEMA IF NOT EXISTS raw;")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS raw.telegram_messages (
            message_id BIGINT,
            channel_name TEXT,
            message_date TIMESTAMP,
            message_text TEXT,
            has_media BOOLEAN,
            image_path TEXT,
            views INT,
            forwards INT
        );
    """)
    
    # 2. Iterate through data/raw/telegram_messages/
    base_path = 'data/raw/telegram_messages'
    for date_folder in os.listdir(base_path):
        folder_path = os.path.join(base_path, date_folder)
        for json_file in os.listdir(folder_path):
            with open(os.path.join(folder_path, json_file), 'r', encoding='utf-8') as f:
                messages = json.load(f)
                for msg in messages:
                    cur.execute("""
                        INSERT INTO raw.telegram_messages 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        msg['message_id'], msg['channel_name'], msg['message_date'],
                        msg['message_text'], msg['has_media'], msg['image_path'],
                        msg['views'], msg['forwards']
                    ))
    
    conn.commit()
    cur.close()
    conn.close()
    print("Data loaded successfully to raw.telegram_messages!")

if __name__ == "__main__":
    load_data()