import feedparser
from typing import List, Dict, Any

async def fetch_rss_feeds(urls: List[str]) -> List[Dict[str, Any]]:
    """Fetch content from RSS feeds."""
    results = []
    
    for url in urls:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]:  # Get latest 5 entries
                results.append({
                    "type": "rss",
                    "source": feed.feed.title,
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.get("published", "Unknown"),
                    "summary": entry.get("summary", "No summary available")
                })
        except Exception as e:
            print(f"Error fetching RSS from {url}: {e}")
    
    return results
    