import React from 'react'
import { Download, Clock, Eye, User, FileVideo, Music } from 'lucide-react'

const VideoPreview = ({ videoData }) => {
  const formatFileSize = (bytes) => {
    if (!bytes) return 'Unknown size'
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(1024))
    return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i]
  }

  const formatDuration = (seconds) => {
    if (!seconds) return 'Unknown duration'
    const hours = Math.floor(seconds / 3600)
    const minutes = Math.floor((seconds % 3600) / 60)
    const secs = seconds % 60
    
    if (hours > 0) {
      return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
    }
    return `${minutes}:${secs.toString().padStart(2, '0')}`
  }

  const formatViewCount = (count) => {
    if (!count) return 'Unknown views'
    if (count >= 1000000) {
      return (count / 1000000).toFixed(1) + 'M views'
    }
    if (count >= 1000) {
      return (count / 1000).toFixed(1) + 'K views'
    }
    return count + ' views'
  }

  const getFormatIcon = (format) => {
    if (format.vcodec && format.vcodec !== 'none' && format.vcodec !== 'unknown') {
      return <FileVideo className="h-4 w-4" />
    }
    if (format.acodec && format.acodec !== 'none' && format.acodec !== 'unknown') {
      return <Music className="h-4 w-4" />
    }
    return <FileVideo className="h-4 w-4" />
  }

  const getFormatType = (format) => {
    const hasVideo = format.vcodec && format.vcodec !== 'none' && format.vcodec !== 'unknown'
    const hasAudio = format.acodec && format.acodec !== 'none' && format.acodec !== 'unknown'
    
    if (hasVideo && hasAudio) return 'Video + Audio'
    if (hasVideo) return 'Video Only'
    if (hasAudio) return 'Audio Only'
    return 'Unknown'
  }

  const handleDownload = (format) => {
    // Open download URL in new tab
    window.open(format.url, '_blank')
  }

  return (
    <div className="card p-8">
      <div className="grid md:grid-cols-3 gap-8">
        {/* Video Thumbnail and Basic Info */}
        <div className="md:col-span-1">
          <div className="aspect-video bg-gray-200 rounded-lg overflow-hidden mb-4">
            {videoData.thumbnail ? (
              <img
                src={videoData.thumbnail}
                alt={videoData.title}
                className="w-full h-full object-cover"
                onError={(e) => {
                  e.target.style.display = 'none'
                  e.target.nextSibling.style.display = 'flex'
                }}
              />
            ) : null}
            <div className="w-full h-full flex items-center justify-center text-gray-500">
              <FileVideo className="h-12 w-12" />
            </div>
          </div>
          
          {/* Video Metadata */}
          <div className="space-y-3 text-sm text-gray-600">
            {videoData.duration && (
              <div className="flex items-center gap-2">
                <Clock className="h-4 w-4" />
                <span>{formatDuration(videoData.duration)}</span>
              </div>
            )}
            
            {videoData.view_count && (
              <div className="flex items-center gap-2">
                <Eye className="h-4 w-4" />
                <span>{formatViewCount(videoData.view_count)}</span>
              </div>
            )}
            
            {videoData.uploader && (
              <div className="flex items-center gap-2">
                <User className="h-4 w-4" />
                <span>{videoData.uploader}</span>
              </div>
            )}
          </div>
        </div>

        {/* Video Title and Download Options */}
        <div className="md:col-span-2">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 leading-tight">
            {videoData.title}
          </h2>

          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">
              Available Formats ({videoData.formats.length})
            </h3>

            <div className="grid gap-3 max-h-96 overflow-y-auto">
              {videoData.formats.map((format, index) => (
                <div
                  key={format.format_id || index}
                  className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:border-primary-300 transition-colors"
                >
                  <div className="flex items-center gap-3 flex-1">
                    {getFormatIcon(format)}
                    <div>
                      <div className="font-medium text-gray-900">
                        {format.quality} • {format.ext.toUpperCase()}
                      </div>
                      <div className="text-sm text-gray-600">
                        {getFormatType(format)}
                        {format.filesize && (
                          <span className="ml-2">• {formatFileSize(format.filesize)}</span>
                        )}
                      </div>
                    </div>
                  </div>

                  <button
                    onClick={() => handleDownload(format)}
                    className="btn-primary flex items-center gap-2 ml-4"
                  >
                    <Download className="h-4 w-4" />
                    Download
                  </button>
                </div>
              ))}
            </div>

            {videoData.formats.length === 0 && (
              <div className="text-center py-8 text-gray-500">
                <FileVideo className="h-12 w-12 mx-auto mb-4 opacity-50" />
                <p>No downloadable formats available for this video.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default VideoPreview
