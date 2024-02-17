# schemas.py
from pydantic import BaseModel
from datetime import datetime

class DeviceBase(BaseModel):
    name: str

class DeviceInDB(DeviceBase):
    id: int
    created_at: datetime

class DeviceStatsItemCreate(BaseModel):
    x: float
    y: float
    z: float

class DeviceStatsItemInDB(DeviceStatsItemCreate):
    id: int
    created_at: datetime
    device_id: int
