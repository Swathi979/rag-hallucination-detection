"""Health check routes"""
from fastapi import APIRouter
from typing import Dict, Any
import psutil
import platform
from datetime import datetime

router = APIRouter()

@router.get("/health", response_model=Dict[str, Any])
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "system": {
            "platform": platform.system(),
            "python_version": platform.python_version(),
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
        },
    }

@router.get("/stats", response_model=Dict[str, Any])
async def get_stats():
    process = psutil.Process()
    return {
        "uptime_seconds": (datetime.utcnow() - datetime.fromtimestamp(process.create_time())).total_seconds(),
        "memory_mb": process.memory_info().rss / 1024 / 1024,
        "cpu_percent": process.cpu_percent(interval=1),
        "num_threads": process.num_threads(),
    }
