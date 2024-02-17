from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import database
import models
import schemas

router = APIRouter()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/devices/{device_id}/items/create", response_model=schemas.DeviceStatsItemInDB)
async def create_device_stats_item(device_id: int, stats_item: schemas.DeviceStatsItemCreate,
                                   db: Session = Depends(get_db)):
    device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")

    db_stats_item = models.DeviceStatsItem(device_id=device_id, **stats_item.dict())
    db.add(db_stats_item)
    db.commit()
    db.refresh(db_stats_item)

    return db_stats_item


@router.get("/devices/{device_id}/items/", response_model=List[schemas.DeviceStatsItemInDB])
async def get_device_stats(device_id: int, db: Session = Depends(get_db)):
    device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")

    stats = db.query(models.DeviceStatsItem).filter(models.DeviceStatsItem.device_id == device_id).all()
    if not stats:
        raise HTTPException(status_code=404, detail="Device stats not found")

    return stats


@router.get("/devices/{device_id}/items/{item_id}", response_model=schemas.DeviceStatsItemInDB)
async def get_device_stats_item(device_id: int, item_id: int, db: Session = Depends(get_db)):
    device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")

    stats_item = db.query(models.DeviceStatsItem).filter(models.DeviceStatsItem.device_id == device_id,
                                                         models.DeviceStatsItem.id == item_id).first()
    if stats_item is None:
        raise HTTPException(status_code=404, detail="Device stats item not found")

    return stats_item
