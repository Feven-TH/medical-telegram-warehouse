from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from . import schemas
from .database import SessionLocal  # Assume standard SQLAlchemy setup here

app = FastAPI(title="Kara Solutions Medical API", version="1.0.0")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/reports/top-products", response_model=List[schemas.ProductCount])
def get_top_products(limit: int = 10, db: Session = Depends(get_db)):
    """Endpoint 1: Returns the most frequently detected medical objects."""
    query = text("""
        SELECT object_detected, COUNT(*) as count 
        FROM fct_medical_inventory 
        GROUP BY object_detected 
        ORDER BY count DESC 
        LIMIT :limit
    """)
    return db.execute(query, {"limit": limit}).mappings().all()

@app.get("/api/channels/{channel_name}/activity", response_model=schemas.ChannelActivity)
def get_channel_activity(channel_name: str, db: Session = Depends(get_db)):
    """Endpoint 2: Activity trends for a specific channel."""
    query = text("""
        SELECT channel_name, COUNT(*) as message_count, MAX(message_timestamp) as last_post
        FROM fct_messages
        WHERE channel_name = :channel
        GROUP BY channel_name
    """)
    result = db.execute(query, {"channel": channel_name}).mappings().first()
    if not result:
        raise HTTPException(status_code=404, detail="Channel not found")
    return result

@app.get("/api/search/messages", response_model=List[schemas.MessageResult])
def search_messages(query: str, limit: int = 20, db: Session = Depends(get_db)):
    """Endpoint 3: Search for specific keywords in medical messages."""
    sql = text("""
        SELECT message_id, channel_name, message_text, object_detected, confidence
        FROM fct_medical_inventory
        WHERE message_text ILIKE :search
        LIMIT :limit
    """)
    return db.execute(sql, {"search": f"%{query}%", "limit": limit}).mappings().all()

@app.get("/api/reports/visual-content", response_model=List[schemas.VisualStats])
def get_visual_stats(db: Session = Depends(get_db)):
    """Endpoint 4: Stats about image usage and YOLO detections."""
    query = text("""
        SELECT channel_name, COUNT(DISTINCT message_id) as total_images_processed, COUNT(*) as medical_items_found
        FROM fct_medical_inventory
        GROUP BY channel_name
    """)
    return db.execute(query).mappings().all()