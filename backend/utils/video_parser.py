import yt_dlp
import re
from typing import Dict, List, Optional, Union
from urllib.parse import urlparse
import logging

# Configure logging for yt-dlp
logging.getLogger('yt_dlp').setLevel(logging.WARNING)


class VideoParser:
    """Utility class for parsing video URLs and extracting metadata using yt-dlp"""
    
    SUPPORTED_DOMAINS = [
        'youtube.com', 'youtu.be', 'instagram.com', 
        'facebook.com', 'tiktok.com', 'fb.watch'
    ]
    
    def __init__(self):
        self.ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'format': 'best[height<=720]/best',
            'no_check_certificate': True,
            'ignoreerrors': False,
            'geo_bypass': True,
            'geo_bypass_country': 'US',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'referer': 'https://www.youtube.com/',
            'extractor_args': {
                'youtube': {
                    'skip': ['hls', 'dash'],
                    'player_skip': ['configs'],
                }
            },
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Accept-Encoding': 'gzip,deflate',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
                'Keep-Alive': '300',
                'Connection': 'keep-alive',
            }
        }
    
    def is_valid_url(self, url: str) -> bool:
        """Check if the URL is valid and from supported platforms"""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            
            # Remove www. prefix if present
            if domain.startswith('www.'):
                domain = domain[4:]
            
            return domain in self.SUPPORTED_DOMAINS
        except Exception:
            return False
    
    def extract_video_info(self, url: str) -> Dict:
        """Extract video metadata using yt-dlp"""
        if not self.is_valid_url(url):
            raise ValueError("Unsupported URL or invalid format")
        
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                if not info:
                    raise ValueError("Could not extract video information")
                
                # Extract formats with download URLs
                formats = []
                if 'formats' in info and info['formats']:
                    for fmt in info['formats']:
                        if fmt.get('url') and fmt.get('ext'):
                            format_info = {
                                'format_id': str(fmt.get('format_id', 'unknown')),
                                'quality': self._get_quality_label(fmt),
                                'ext': str(fmt.get('ext', 'mp4')),
                                'url': str(fmt.get('url')),
                                'filesize': self._safe_int_or_float(fmt.get('filesize')),
                                'vcodec': self._safe_string(fmt.get('vcodec')),
                                'acodec': self._safe_string(fmt.get('acodec'))
                            }
                            formats.append(format_info)
                
                # If no formats found, try to get the direct URL
                if not formats and info.get('url'):
                    formats.append({
                        'format_id': 'default',
                        'quality': 'default',
                        'ext': str(info.get('ext', 'mp4')),
                        'url': str(info.get('url')),
                        'filesize': self._safe_int_or_float(info.get('filesize')),
                        'vcodec': 'unknown',
                        'acodec': 'unknown'
                    })

                return {
                    'title': str(info.get('title', 'Unknown Title')),
                    'thumbnail': str(info.get('thumbnail', '')),
                    'duration': self._safe_int_or_float(info.get('duration')),
                    'uploader': str(info.get('uploader', 'Unknown')),
                    'view_count': self._safe_int_or_float(info.get('view_count')),
                    'formats': formats[:10]  # Limit to first 10 formats
                }
                
        except yt_dlp.DownloadError as e:
            error_str = str(e).lower()
            if 'private video' in error_str or 'unavailable' in error_str:
                raise ValueError("Video is private or unavailable")
            elif 'not available' in error_str or 'blocked' in error_str:
                raise ValueError("Video not available in your region")
            elif 'sign in' in error_str or 'login' in error_str:
                raise ValueError("Video requires authentication")
            elif 'copyright' in error_str:
                raise ValueError("Video blocked due to copyright")
            elif 'age' in error_str and 'restrict' in error_str:
                raise ValueError("Video is age-restricted")
            else:
                raise ValueError(f"Failed to extract video info: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error processing video: {str(e)}")
    
    def _safe_int_or_float(self, value) -> Optional[Union[int, float]]:
        """Safely convert value to int or float, return None if not possible"""
        if value is None:
            return None
        try:
            # Try int first, then float
            if isinstance(value, (int, float)):
                return value
            if isinstance(value, str):
                if '.' in value:
                    return float(value)
                else:
                    return int(value)
            return None
        except (ValueError, TypeError):
            return None

    def _safe_string(self, value) -> Optional[str]:
        """Safely convert value to string, return None for 'none' or empty values"""
        if value is None or value == 'none' or value == '':
            return None
        return str(value)

    def _get_quality_label(self, fmt: Dict) -> str:
        """Generate a human-readable quality label"""
        height = fmt.get('height')
        width = fmt.get('width')
        vbr = fmt.get('vbr')
        abr = fmt.get('abr')

        if height:
            return f"{height}p"
        elif width:
            return f"{width}x{fmt.get('height', '?')}"
        elif vbr:
            return f"{vbr}kbps"
        elif abr:
            return f"Audio {abr}kbps"
        else:
            return fmt.get('format_note', 'Unknown Quality')


# Create a global instance
video_parser = VideoParser()
