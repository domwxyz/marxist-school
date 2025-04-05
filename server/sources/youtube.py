from googleapiclient.discovery import build
from typing import List, Dict, Any
import os

async def fetch_youtube_videos(channel_ids: List[str]) -> List[Dict[str, Any]]:
    """Fetch latest videos from YouTube channels."""
    # This is a placeholder - you'll need a YouTube API key
    api_key = os.getenv("YOUTUBE_API_KEY", "")
    if not api_key:
        return []
        
    results = []
    try:
        youtube = build("youtube", "v3", developerKey=api_key)
        
        for channel_id in channel_ids:
            request = youtube.search().list(
                part="snippet",
                channelId=channel_id,
                maxResults=5,
                order="date",
                type="video"
            )
            response = request.execute()
            
            for item in response.get("items", []):
                video_id = item["id"]["videoId"]
                results.append({
                    "type": "youtube",
                    "source": "YouTube",
                    "title": item["snippet"]["title"],
                    "description": item["snippet"]["description"],
                    "published": item["snippet"]["publishedAt"],
                    "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"],
                    "link": f"https://www.youtube.com/watch?v={video_id}"
                })
    except Exception as e:
        print(f"Error fetching YouTube data: {e}")
    
    return results
    