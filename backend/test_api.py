#!/usr/bin/env python3
"""
Simple test script to verify the video downloader API functionality
"""

import requests
import json

def test_api():
    base_url = "http://localhost:8000"
    
    # Test health endpoint
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"Health check: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
        return
    
    # Test video download endpoint with a simple YouTube video
    print("\nTesting video download endpoint...")
    test_urls = [
        "https://www.youtube.com/watch?v=jNQXAC9IVRw",  # Me at the zoo - first YouTube video
        "https://youtu.be/jNQXAC9IVRw",  # Short YouTube URL
    ]
    
    for url in test_urls:
        print(f"\nTesting URL: {url}")
        try:
            response = requests.post(
                f"{base_url}/api/download",
                json={"url": url},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Success! Title: {data.get('title', 'Unknown')}")
                print(f"   Formats available: {len(data.get('formats', []))}")
                if data.get('formats'):
                    print(f"   First format: {data['formats'][0].get('quality')} {data['formats'][0].get('ext')}")
            else:
                print(f"❌ Error {response.status_code}: {response.text}")
                
        except requests.exceptions.Timeout:
            print("❌ Request timeout")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_api()
