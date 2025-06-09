import React from 'react'
import Home from './pages/Home'

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Video Downloader
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Download videos from YouTube, Instagram, Facebook, and TikTok. 
            Simply paste the URL and choose your preferred format.
          </p>
        </header>
        
        <main>
          <Home />
        </main>
        
        <footer className="text-center mt-16 text-gray-500">
          <p>&copy; 2024 Video Downloader. Built with React and FastAPI.</p>
        </footer>
      </div>
    </div>
  )
}

export default App
