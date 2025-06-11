import React, { useState } from 'react'
import axios from 'axios'
import { Download, Link, AlertCircle, Loader2 } from 'lucide-react'
import VideoPreview from './VideoPreview'

const VideoDownloader = () => {
  const [url, setUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [videoData, setVideoData] = useState(null)
  const [error, setError] = useState('')

  const API_BASE_URL = import.meta.env.example.VITE_API_URL || 'https://videosdownloader.onrender.com'

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!url.trim()) {
      setError('Please enter a valid URL')
      return
    }

    setLoading(true)
    setError('')
    setVideoData(null)

    try {
      const response = await axios.post(`${API_BASE_URL}/api/download`, {
        url: url.trim()
      }, {
        headers: {
          'Content-Type': 'application/json',
        },
        timeout: 30000, // 30 second timeout
      })

      setVideoData(response.data)
    } catch (err) {
      console.error('Error fetching video data:', err)
      console.error('Error response:', err.response?.data)

      if (err.code === 'ECONNREFUSED' || err.code === 'ERR_NETWORK') {
        setError('Cannot connect to server. Please make sure the backend is running on port 8000.')
      } else if (err.response?.data?.detail) {
        setError(err.response.data.detail)
      } else if (err.response?.status === 403) {
        setError('Video is private or restricted')
      } else if (err.response?.status === 404) {
        setError('Video not found or unavailable')
      } else if (err.response?.status === 451) {
        setError('Video not available in your region or blocked by platform')
      } else if (err.response?.status === 400) {
        const errorDetail = err.response?.data?.detail || 'Invalid URL or unsupported platform'
        setError(errorDetail)
      } else if (err.code === 'ECONNABORTED') {
        setError('Request timeout. The video might be too large or server is busy.')
      } else {
        setError('Failed to process video. Please check the URL and try again.')
      }
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setUrl('')
    setVideoData(null)
    setError('')
  }

  return (
    <div className="space-y-8">
      {/* URL Input Form */}
      <div className="card p-8">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="url" className="block text-sm font-medium text-gray-700 mb-2">
              Video URL
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Link className="h-5 w-5 text-gray-400" />
              </div>
              <input
                type="url"
                id="url"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="Paste YouTube, Instagram, Facebook, or TikTok URL here..."
                className="input-field pl-10"
                disabled={loading}
              />
            </div>
          </div>

          <div className="flex gap-4">
            <button
              type="submit"
              disabled={loading || !url.trim()}
              className="btn-primary flex items-center gap-2 flex-1 justify-center"
            >
              {loading ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Processing...
                </>
              ) : (
                <>
                  <Download className="h-4 w-4" />
                  Get Video Info
                </>
              )}
            </button>
            
            {(videoData || error) && (
              <button
                type="button"
                onClick={handleReset}
                className="btn-secondary"
              >
                Reset
              </button>
            )}
          </div>
        </form>

        {/* Supported Platforms */}
        <div className="mt-6 pt-6 border-t border-gray-200">
          <p className="text-sm text-gray-600 text-center">
            Supported platforms: 
            <span className="font-medium text-gray-800 ml-1">
              YouTube, Instagram, Facebook, TikTok
            </span>
          </p>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="card p-6 border-red-200 bg-red-50">
          <div className="flex items-center gap-3">
            <AlertCircle className="h-5 w-5 text-red-500 flex-shrink-0" />
            <div>
              <h3 className="text-sm font-medium text-red-800">Error</h3>
              <p className="text-sm text-red-700 mt-1">{error}</p>
            </div>
          </div>
        </div>
      )}

      {/* Video Preview */}
      {videoData && <VideoPreview videoData={videoData} />}
    </div>
  )
}

export default VideoDownloader
