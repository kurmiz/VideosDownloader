from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl, Field
from typing import List, Dict, Any, Optional, Union
import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from utils.video_parser import video_parser

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Video Downloader API",
    description="API for extracting video metadata and download links",
    version="1.0.0"
)

# CORS configuration
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
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
        # Allow extra fields that might come from yt-dlp
        extra = "ignore"


class VideoResponse(BaseModel):
    title: str
    thumbnail: Optional[str] = ""
    duration: Optional[Union[int, float]] = None
    uploader: Optional[str] = None
    view_count: Optional[Union[int, float]] = None
    formats: List[FormatInfo]

    class Config:
        # Allow extra fields that might come from yt-dlp
        extra = "ignore"


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Video Downloader API is running",
        "status": "healthy",
        "supported_platforms": ["YouTube", "Instagram", "Facebook", "TikTok"]
    }


@app.post("/api/download", response_model=VideoResponse)
async def download_video(request: VideoRequest):
    """
    Extract video metadata and download links from supported platforms

    Args:
        request: VideoRequest containing the video URL

    Returns:
        VideoResponse with video metadata and available formats

    Raises:
        HTTPException: For various error conditions
    """
    try:
        logger.info(f"Received request: {request}")
        logger.info(f"URL: {request.url}")

        # Validate URL format
        if not request.url or not request.url.strip():
            logger.error("Error: Empty URL")
            raise HTTPException(
                status_code=400,
                detail="URL is required and cannot be empty"
            )

        url = request.url.strip()
        logger.info(f"Processing URL: {url}")

        # Demo mode for testing - return mock data for specific URLs
        if url in ["https://demo.test", "demo", "test"]:
            logger.info("Demo mode activated")
            return VideoResponse(
                title="Demo Video - Sample Download",
                thumbnail="https://via.placeholder.com/640x360/0066cc/ffffff?text=Demo+Video",
                duration=120,
                uploader="Demo Channel",
                view_count=1000000,
                formats=[
                    FormatInfo(
                        format_id="demo_720p",
                        quality="720p",
                        ext="mp4",
                        url="https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4",
                        filesize=1048576,
                        vcodec="h264",
                        acodec="aac"
                    ),
                    FormatInfo(
                        format_id="demo_480p",
                        quality="480p",
                        ext="mp4",
                        url="https://sample-videos.com/zip/10/mp4/SampleVideo_640x360_1mb.mp4",
                        filesize=524288,
                        vcodec="h264",
                        acodec="aac"
                    )
                ]
            )

        # Check if URL is from supported platform
        logger.info(f"Checking if URL is valid: {url}")
        is_valid = video_parser.is_valid_url(url)
        logger.info(f"URL validation result: {is_valid}")

        if not is_valid:
            logger.error("Error: Unsupported platform")
            raise HTTPException(
                status_code=400,
                detail="Unsupported platform. Supported platforms: YouTube, Instagram, Facebook, TikTok. Use 'demo' for testing."
            )

        # Extract video information
        logger.info("Extracting video information...")
        video_info = video_parser.extract_video_info(url)
        logger.info(f"Video info extracted: {video_info.get('title', 'Unknown')}")
        logger.info(f"Raw video info: {video_info}")

        if not video_info.get('formats'):
            logger.error("Error: No formats found")
            raise HTTPException(
                status_code=404,
                detail="No downloadable formats found for this video"
            )

        # Create response with proper error handling
        try:
            response = VideoResponse(**video_info)
            logger.info("VideoResponse created successfully")
            return response
        except Exception as validation_error:
            logger.error(f"Pydantic validation error: {validation_error}")
            logger.error(f"Video info that failed validation: {video_info}")
            raise HTTPException(
                status_code=500,
                detail=f"Data validation error: {str(validation_error)}"
            )

    except ValueError as e:
        # Handle specific video parsing errors
        error_message = str(e)
        logger.error(f"ValueError: {error_message}")
        if "private" in error_message.lower():
            raise HTTPException(status_code=403, detail="Video is private or restricted")
        elif "unavailable" in error_message.lower():
            raise HTTPException(status_code=404, detail="Video is unavailable or not found")
        elif "region" in error_message.lower():
            raise HTTPException(status_code=451, detail="Video not available in your region")
        elif "no video formats found" in error_message.lower():
            raise HTTPException(status_code=404, detail="No downloadable formats found. Video may be restricted or unavailable.")
        else:
            raise HTTPException(status_code=400, detail=error_message)

    except HTTPException:
        # Re-raise HTTP exceptions
        raise

    except Exception as e:
        # Handle unexpected errors
        logger.error(f"Unexpected error: {str(e)}")
        logger.error(f"Error type: {type(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.get("/api/health")
async def health_check():
    """Detailed health check endpoint"""
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
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
