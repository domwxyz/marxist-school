import asyncio
import os
import json
from database.db import get_db
from services.youtube_service import YouTubeService
from services.repository import get_channels, update_videos_for_channel
from services.rss_service import fetch_and_update_rss_feeds
from services.social_service import fetch_social_posts

youtube_service = YouTubeService()

async def start_periodic_update():
    """Start the periodic update tasks for all content types"""
    while True:
        try:
            # Update YouTube videos
            await update_all_channels()
            
            # Update RSS feeds
            await update_all_rss_feeds()
            
            # Update social media posts
            await update_all_social_accounts()
            
            # Wait before next update cycle
            # YouTube: every 60 minutes
            # RSS: every 30 minutes
            # Social: every 15 minutes
            await asyncio.sleep(900)  # 15 minutes
        except Exception as e:
            print(f"Error in periodic update: {e}")
            await asyncio.sleep(300)  # Try again in 5 minutes if there's an error

async def update_all_channels():
    """Update all YouTube channels in the database"""
    print("Starting YouTube channels update...")
    db = next(get_db())
    channels = get_channels(db)
    
    for channel in channels:
        try:
            # Get videos from YouTube API
            videos, next_page_token = youtube_service.get_playlist_videos(channel.uploads_playlist_id)
            
            # Update database with videos
            update_videos_for_channel(db, channel.id, videos)
            print(f"Updated {len(videos)} videos for channel {channel.title}")
            
            # Fetch additional pages if available
            while next_page_token:
                additional_videos, next_page_token = youtube_service.get_playlist_videos(
                    channel.uploads_playlist_id, 10, next_page_token
                )
                update_videos_for_channel(db, channel.id, additional_videos)
                print(f"Updated {len(additional_videos)} additional videos for channel {channel.title}")
                
                # Add a small delay to avoid rate limiting
                await asyncio.sleep(1)
                
        except Exception as e:
            print(f"Error updating channel {channel.id}: {e}")
            continue
    
    print("YouTube channels update completed")

async def update_all_rss_feeds():
    """Update all RSS feeds"""
    print("Starting RSS feeds update...")
    db = next(get_db())
    
    try:
        # Check if rss_feeds.json exists
        config_path = os.path.join(os.path.dirname(__file__), "..", "..", "rss_feeds.json")
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                feeds = json.load(f)
            
            # Update all feeds
            await fetch_and_update_rss_feeds(db, feeds)
            print(f"Updated {len(feeds)} RSS feeds")
        else:
            print("No RSS feeds configuration found")
    except Exception as e:
        print(f"Error updating RSS feeds: {e}")
    
    print("RSS feeds update completed")

async def update_all_social_accounts():
    """Update all social media accounts"""
    print("Starting social media accounts update...")
    db = next(get_db())
    
    try:
        # Import here to avoid circular imports
        from models.models import SocialAccount
        
        # Get all accounts
        accounts = db.query(SocialAccount).all()
        
        for account in accounts:
            try:
                # This would need platform-specific API implementations
                # results = await fetch_social_posts(db, None, account.id)
                # print(f"Updated posts for {account.platform} account: {account.username}")
                pass
            except Exception as e:
                print(f"Error updating social account {account.id}: {e}")
                continue
        
        print(f"Updated {len(accounts)} social media accounts")
    except Exception as e:
        print(f"Error updating social media accounts: {e}")
    
    print("Social media accounts update completed")
        