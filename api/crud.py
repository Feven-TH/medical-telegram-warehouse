from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ProductCount(BaseModel):
    object_detected: str
    count: int

class ChannelActivity(BaseModel):
    channel_name: str
    message_count: int
    last_post: datetime

class MessageResult(BaseModel):
    message_id: str
    channel_name: str
    message_text: Optional[str]
    object_detected: Optional[str]
    confidence: Optional[float]

class VisualStats(BaseModel):
    channel_name: str
    total_images_processed: int
    medical_items_found: int