# 🎬 Video Downloader

A modern, full-stack web application that enables users to download videos from popular platforms including YouTube, Instagram, Facebook, and TikTok. Built with React, FastAPI, and yt-dlp for reliable video processing.

![Video Downloader Demo](https://via.placeholder.com/800x400/0066cc/ffffff?text=Video+Downloader+Demo)

## ✨ Features

- 🌐 **Multi-platform support**: YouTube, Instagram, Facebook, TikTok
- 🖼️ **Video preview**: Thumbnail, title, duration, and metadata display
- 📱 **Multiple formats**: Download videos in various qualities and formats
- 🎨 **Modern UI**: Clean, responsive design with Tailwind CSS
- ⚡ **Real-time processing**: Fast video metadata extraction with yt-dlp
- 🛡️ **Error handling**: Graceful handling of private/unavailable videos
- 🧪 **Demo mode**: Test the application without external dependencies
- 🔄 **Auto-refresh**: Real-time updates and format detection

## 🏗️ Architecture

### Frontend Stack
- **React.js 18** with Vite for lightning-fast development
- **Tailwind CSS** for utility-first styling
- **Axios** for HTTP client communication
- **Lucide React** for beautiful icons
- **ESLint** for code quality

### Backend Stack
- **FastAPI** for high-performance async API
- **yt-dlp** (latest) for video metadata extraction
- **Pydantic v2** for robust data validation
- **CORS** middleware for cross-origin requests
- **Python 3.10+** with type hints

## 📁 Project Structure

```
VideoDownloader/
├── 📁 frontend/                 # React frontend application
│   ├── 📁 public/              # Static assets
│   ├── 📁 src/
│   │   ├── 📁 components/      # Reusable React components
│   │   │   ├── VideoDownloader.jsx    # Main downloader interface
│   │   │   └── VideoPreview.jsx       # Video preview component
│   │   ├── 📁 pages/           # Page components
│   │   │   └── Home.jsx        # Home page layout
│   │   ├── App.jsx             # Main app component
│   │   ├── main.jsx            # React entry point
│   │   └── index.css           # Global styles with Tailwind
│   ├── package.json            # Frontend dependencies
│   ├── vite.config.js          # Vite configuration
│   ├── tailwind.config.js      # Tailwind CSS configuration
│   └── .env                    # Environment variables
└── 📁 backend/                 # FastAPI backend application
    ├── 📁 utils/               # Utility modules
    │   └── video_parser.py     # yt-dlp integration and parsing
    ├── main.py                 # FastAPI application entry point
    ├── requirements.txt        # Python dependencies
    ├── test_api.py            # API testing script
    └── .env                    # Backend environment variables
```

## 🚀 Quick Start

### Prerequisites
- **Node.js 18+** and npm/yarn
- **Python 3.10+**
- **Git**

### 🔧 Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env file if needed
   ```

5. **Start the FastAPI server:**
   ```bash
   python main.py
   ```
   
   ✅ **Backend running at:** `http://localhost:8000`

### 🎨 Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env file if needed
   ```

4. **Start the development server:**
   ```bash
   npm run dev
   # or
   yarn dev
   ```
   
   ✅ **Frontend running at:** `http://localhost:5173`

## 🔌 API Documentation

### Core Endpoints

#### `POST /api/download`
Extract video metadata and download links from supported platforms.

**Request Body:**
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

**Success Response (200):**
```json
{
  "title": "Rick Astley - Never Gonna Give You Up",
  "thumbnail": "https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg",
  "duration": 212.0,
  "uploader": "Rick Astley",
  "view_count": 1500000000,
  "formats": [
    {
      "format_id": "22",
      "quality": "720p",
      "ext": "mp4",
      "url": "https://direct-download-url.com/video.mp4",
      "filesize": 50000000,
      "vcodec": "avc1.64001F",
      "acodec": "mp4a.40.2"
    }
  ]
}
```

**Error Responses:**
- `400`: Invalid URL or unsupported platform
- `403`: Private or restricted video
- `404`: Video not found or unavailable
- `451`: Video not available in your region
- `500`: Internal server error

#### `GET /api/health`
Health check endpoint with API status and supported platforms.

**Response:**
```json
{
  "status": "healthy",
  "api_version": "1.0.0",
  "supported_domains": ["youtube.com", "youtu.be", "instagram.com", "facebook.com", "tiktok.com"],
  "cors_origins": ["http://localhost:5173", "http://localhost:3000"]
}
```

#### `GET /`
Basic API information and status.

### Demo Mode
For testing purposes, use `demo` as the URL to get sample data:
```json
{
  "url": "demo"
}
```

## 🎯 Usage Guide

### Basic Usage
1. **Open the application** in your web browser at `http://localhost:5173`
2. **Paste a video URL** from YouTube, Instagram, Facebook, or TikTok
3. **Click "Get Video Info"** to extract metadata and available formats
4. **Choose your preferred format** from the list of available options
5. **Click "Download"** to open the video in a new tab for download

### Supported URL Formats
- **YouTube**: `https://www.youtube.com/watch?v=VIDEO_ID` or `https://youtu.be/VIDEO_ID`
- **Instagram**: `https://www.instagram.com/p/POST_ID/` or `https://www.instagram.com/reel/REEL_ID/`
- **Facebook**: `https://www.facebook.com/watch?v=VIDEO_ID` or `https://fb.watch/VIDEO_ID`
- **TikTok**: `https://www.tiktok.com/@username/video/VIDEO_ID`

### Testing with Demo Mode
Enter `demo` in the URL field to test the application with sample data without making external requests.

## 🛡️ Error Handling & Troubleshooting

### Common Issues

#### Backend Not Starting
```bash
# Check if port 8000 is available
netstat -an | grep 8000

# Install missing dependencies
pip install -r requirements.txt

# Check Python version
python --version  # Should be 3.10+
```

#### Frontend Build Issues
```bash
# Clear node modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Check Node.js version
node --version  # Should be 18+
```

#### CORS Errors
Ensure the backend is running and CORS origins are properly configured in `.env`:
```env
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Error Types Handled

| Error Code | Description | Common Causes |
|------------|-------------|---------------|
| 400 | Bad Request | Invalid URL format, unsupported platform |
| 403 | Forbidden | Private video, authentication required |
| 404 | Not Found | Video deleted, invalid video ID |
| 451 | Unavailable | Region restrictions, copyright blocks |
| 500 | Server Error | yt-dlp issues, network problems |

## 🔒 Limitations & Considerations

### Technical Limitations
- **Public videos only**: Private or restricted content cannot be accessed
- **Platform rate limiting**: Some platforms may limit requests
- **File size constraints**: Very large files may timeout
- **Regional restrictions**: Some content may be geo-blocked

### Legal Considerations
- **Copyright compliance**: Only download content you have permission to use
- **Terms of service**: Respect platform terms and conditions
- **Fair use**: Consider fair use guidelines for downloaded content

## 🧪 Testing

### Manual Testing
```bash
# Test backend health
curl http://localhost:8000/api/health

# Test demo mode
curl -X POST "http://localhost:8000/api/download" \
  -H "Content-Type: application/json" \
  -d '{"url": "demo"}'

# Run backend tests
cd backend
python test_api.py
```

### Frontend Testing
```bash
cd frontend
npm run lint    # Check code quality
npm run build   # Test production build
```

## 🚀 Deployment

### Production Considerations
1. **Environment Variables**: Set production URLs and secrets
2. **HTTPS**: Use SSL certificates for secure connections
3. **Rate Limiting**: Implement API rate limiting
4. **Monitoring**: Add logging and error tracking
5. **Caching**: Consider caching video metadata

### Docker Deployment (Optional)
```dockerfile
# Example Dockerfile for backend
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "main.py"]
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** with proper commit messages
4. **Add tests** if applicable
5. **Submit a pull request** with a clear description

### Development Guidelines
- Follow existing code style and conventions
- Add comments for complex logic
- Update documentation for new features
- Test your changes thoroughly

## 📄 License

This project is for **educational purposes**. Please respect platform terms of service and copyright laws.

## ⚠️ Disclaimer

This tool is intended for downloading videos you have permission to download. Users are responsible for:
- Complying with platform terms of service
- Respecting copyright and intellectual property rights
- Following applicable laws and regulations
- Using downloaded content appropriately

## 🆘 Support

If you encounter issues:
1. Check the [troubleshooting section](#-error-handling--troubleshooting)
2. Review the GitHub issues for similar problems
3. Create a new issue with detailed information including:
   - Operating system and version
   - Python/Node.js versions
   - Error messages and logs
   - Steps to reproduce the issue

## 🔄 Recent Updates

### v1.0.0 (Latest)
- ✅ **Fixed Pydantic validation errors** for real-world yt-dlp data
- ✅ **Enhanced error handling** with detailed user feedback
- ✅ **Added demo mode** for testing without external dependencies
- ✅ **Improved data type handling** for duration and filesize fields
- ✅ **Updated yt-dlp** to latest version for better platform support
- ✅ **Added comprehensive logging** for debugging and monitoring

## 🙏 Acknowledgments

- **yt-dlp** team for the excellent video extraction library
- **FastAPI** for the modern Python web framework
- **React** and **Vite** teams for the frontend technologies
- **Tailwind CSS** for the utility-first CSS framework

---

**Made with ❤️ using React, FastAPI, and yt-dlp**

*For educational purposes only. Please respect copyright and platform terms of service.*
