# routers/maths.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from numpy import median

from database import get_db
from models import Device, DeviceStatsItem
from utils import calculate_median

router = APIRouter()


@router.get("/devices/{device_id}/", response_model=dict)
async def get_device_stats(device_id: int, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.id == device_id).first()
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")

    # Fetch all device stats items
    stats_items = db.query(DeviceStatsItem).filter(DeviceStatsItem.device_id == device_id).all()

    if not stats_items:
        raise HTTPException(status_code=404, detail="No stats available for the device")

    # Find the minimum and maximum x values among the fetched stats items

    x_values = [stats_item.x for stats_item in stats_items]
    y_values = [stats_item.y for stats_item in stats_items]
    z_values = [stats_item.z for stats_item in stats_items]

    x_len = len(x_values)
    y_len = len(y_values)
    z_len = len(z_values)

    # Minimal values for x, y, z
    min_x = min(x_values)
    max_x = max(x_values)

    min_y = min(y_values)
    max_y = max(y_values)

    min_z = min(z_values)
    max_z = max(z_values)

    # Calculate median values for x, y, z
    median_x = median(x_values)
    median_y = median(y_values)
    median_z = median(z_values)

    sum_x = sum(x_values)
    sum_y = sum(y_values)
    sum_z = sum(z_values)

    return {"min_x": min_x, "max_x": max_x, "min_y": min_y, "max_y": max_y, "min_z": min_z, "max_z": max_z,
            "median_x": median_x,
            "median_y": median_y, "median_z": median_z, "x_len": x_len, "y_len": y_len, "z_len": z_len,
            "sum_x": sum_x, "sum_y": sum_y, "sum_z": sum_z}


@router.get("/all_devices_aggregated", response_model=dict)
async def get_all_devices_aggregated_stats(db: Session = Depends(get_db)):
    # Fetch all devices
    devices = db.query(Device).all()

    if not devices:
        raise HTTPException(status_code=404, detail="No devices found")

    total_min_x = float('inf')
    total_max_x = float('-inf')
    total_min_y = float('inf')
    total_max_y = float('-inf')
    total_min_z = float('inf')
    total_max_z = float('-inf')
    total_median_x_values = []
    total_median_y_values = []
    total_median_z_values = []

    for device in devices:
        device_stats = db.query(DeviceStatsItem).filter(DeviceStatsItem.device_id == device.id).all()

        if not device_stats:
            continue  # Skip devices with no stats

        x_values = [stats_item.x for stats_item in device_stats]
        y_values = [stats_item.y for stats_item in device_stats]
        z_values = [stats_item.z for stats_item in device_stats]

        total_min_x = min(total_min_x, min(x_values))
        total_max_x = max(total_max_x, max(x_values))
        total_min_y = min(total_min_y, min(y_values))
        total_max_y = max(total_max_y, max(y_values))
        total_min_z = min(total_min_z, min(z_values))
        total_max_z = max(total_max_z, max(z_values))
        total_median_x_values.extend(x_values)
        total_median_y_values.extend(y_values)
        total_median_z_values.extend(z_values)

    total_median_x = calculate_median(total_median_x_values)
    total_median_y = calculate_median(total_median_y_values)
    total_median_z = calculate_median(total_median_z_values)

    return {
        "total_min_x": total_min_x,
        "total_max_x": total_max_x,
        "total_min_y": total_min_y,
        "total_max_y": total_max_y,
        "total_min_z": total_min_z,
        "total_max_z": total_max_z,
        "total_median_x": total_median_x,
        "total_median_y": total_median_y,
        "total_median_z": total_median_z,
        "len_x": len(total_median_x_values),
        "len_y": len(total_median_y_values),
        "len_z": len(total_median_z_values),

    }
