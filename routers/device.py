# routers/device.py
from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Device
from schemas import DeviceBase, DeviceInDB

router = APIRouter()


@router.post("/create/", response_model=DeviceInDB)
async def create_device(device: DeviceBase, db: Session = Depends(get_db)):
    try:
        db_device = Device(**device.dict())
        db.add(db_device)
        db.commit()
        db.refresh(db_device)
        return db_device
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[DeviceInDB])
async def get_all_devices(db: Session = Depends(get_db)):
    try:
        devices = db.query(Device).all()
        return devices
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{device_id}", response_model=DeviceInDB)
async def get_device(device_id: int, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.id == device_id).first()
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return device
