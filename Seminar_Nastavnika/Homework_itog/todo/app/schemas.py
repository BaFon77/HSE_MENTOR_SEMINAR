from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ItemBase(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=255,
        example="Сделать итоговое задание"
    )

    description: Optional[str] = Field(
        max_length=1000,
        example="Задание находиться в ЛМС",
    )

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        example="Сделать итоговое задание"
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,
        example="Задание находиться в ЛМС",
    )
    completed: Optional[bool] = Field(
        None,
        example=True,
        description="Статус задачи"
    )

class ItemOut(ItemBase):
    id: int
    completed: bool = Field(example=False)
    created_at: datetime
