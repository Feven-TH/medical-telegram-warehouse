import os
import psycopg2
from dotenv import load_dotenv
from ultralytics import YOLO

# Load environment variables from .env
load_dotenv()

def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

# 1. Load the YOLO model
model = YOLO('yolov8n.pt') 

# 2. Setup Database Connection
try:
    conn = get_db_connection()
    cur = conn.cursor()
    print("Database connection successful!")
except Exception as e:
    print(f"Error connecting to database: {e}")
    exit()

# 3. Create a table for detections if it doesn't exist
cur.execute("""
    CREATE TABLE IF NOT EXISTS detections (
        id SERIAL PRIMARY KEY,
        message_id TEXT,
        channel_name TEXT,
        object_detected TEXT,
        confidence FLOAT,
        x_min FLOAT, y_min FLOAT, x_max FLOAT, y_max FLOAT
    )
""")

# 4. Iterate through your local images
image_dir = 'data/raw/images/'
for channel in os.listdir(image_dir):
    channel_path = os.path.join(image_dir, channel)
    for img_name in os.listdir(channel_path):
        img_path = os.path.join(channel_path, img_name)
        
        # Run Detection
        results = model(img_path)
        
        for result in results:
            for box in result.boxes:
                # Extract data
                label = result.names[int(box.cls[0])]
                conf = float(box.conf[0])
                coords = box.xyxy[0].tolist() # [xmin, ymin, xmax, ymax]
                
                # Insert into DB
                cur.execute("""
                    INSERT INTO detections (message_id, channel_name, object_detected, confidence, x_min, y_min, x_max, y_max)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (img_name.split('.')[0], channel, label, conf, *coords))

conn.commit()
cur.close()
conn.close()