# main.py
from fastapi import FastAPI

from routers import device, stats, maths

app = FastAPI()

if __name__ == "__main__":
    import uvicorn

    # Include routers from the routers module
    app.include_router(device.router, prefix="/devices", tags=["devices"])
    app.include_router(stats.router, prefix="/stats", tags=["stats"])
    app.include_router(maths.router, prefix="/maths", tags=["maths"])

    uvicorn.run(app, host="127.0.0.1", port=8000)
