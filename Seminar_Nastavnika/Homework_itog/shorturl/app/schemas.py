from pydantic import BaseModel, Field
from datetime import datetime

class URLCreate(BaseModel):
    url: str = Field(example="https://www.hse.ru/ma/data-engineering/")

class URLShortenResponse(BaseModel):
    short_id: str
    short_url: str

class URLStats(BaseModel):
    short_id: str
    full_url: str
    visits: int
    created_at: datetime
    