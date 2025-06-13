from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Union
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from utils.video_parser import video_parser

app = FastAPI(
    title="Video Downloader API",
    description="API for extracting video metadata and download links",
    version="1.0.0"
)

# Enhanced CORS configuration
cors_origins = os.getenv("CORS_ORIGINS", "")
origins = cors_origins.split(",") if cors_origins else [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://videodownloaders.netlify.app/"  # Your Netlify URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VideoRequest(BaseModel):
    url: str

class FormatInfo(BaseModel):
    format_id: str
    quality: str
    ext: str
    url: str
    filesize: Optional[Union[int, float]] = None
    vcodec: Optional[str] = None
    acodec: Optional[str] = None

    class Config:
        extra = "ignore"

class VideoResponse(BaseModel):
    title: str
    thumbnail: Optional[str] = ""
    duration: Optional[Union[int, float]] = None
    uploader: Optional[str] = None
    view_count: Optional[Union[int, float]] = None
    formats: List[FormatInfo]

    class Config:
        extra = "ignore"

@app.get("/")
async def root():
    return {
        "message": "Video Downloader API is running",
        "status": "healthy",
        "supported_platforms": ["YouTube", "Instagram", "Facebook", "TikTok"]
    }

@app.post("/api/download", response_model=VideoResponse)
async def download_video(request: VideoRequest):
    # ... (keep your existing implementation unchanged) ...

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "api_version": "1.0.0",
        "supported_domains": video_parser.SUPPORTED_DOMAINS,
        "cors_origins": origins
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        app,  # Changed from "main:app" to just "app"
        host="0.0.0.0",
        port=port,
        reload=False,  # Disable reload in production
        log_level="info"
    )
