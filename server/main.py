import json
import os
from fastapi import BackgroundTasks
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from database.db import engine, Base
from routes.api import router as api_router
from services.background import start_periodic_update
from services.repository import get_channel, create_channel
from services.youtube_service import YouTubeService
from services.rss_service import fetch_and_update_rss_feeds, get_rss_feeds
from services.social_service import add_social_account, fetch_social_posts
from services.reading_list_service import import_marxist_classics

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Marxist School API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api")

# Background task for periodic updates
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_periodic_update())

# Load channels from config file
@app.on_event("startup")
async def load_channels_from_config():
    try:
        from database.db import get_db
        
        # Create a YouTube service instance
        youtube_service = YouTubeService()
        
        # Get DB session
        db = next(get_db())
        
        # Check if channels.json exists
        config_path = os.path.join(os.path.dirname(__file__), "..", "channels.json")
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                channels = json.load(f)
            
            print(f"Loading {len(channels)} channels from configuration file...")
            
            # Add each channel
            for channel_data in channels:
                # Skip if channel already exists
                existing = get_channel(db, channel_data.get("channel_id", channel_data.get("id")))
                if existing:
                    print(f"Channel {channel_data.get('channel_id', channel_data.get('id'))} already exists")
                    continue
                
                # Get channel info from YouTube
                channel_id = channel_data.get("channel_id", channel_data.get("id"))
                if not channel_id:
                    print("Missing channel_id in config")
                    continue
                    
                channel_info = youtube_service.get_channel_info(channel_id)
                if not channel_info:
                    print(f"Could not find channel {channel_id}")
                    continue
                
                # Add section from config
                channel_info["section"] = channel_data["section"]
                
                # Create channel in database
                db_channel = create_channel(db, channel_info)
                print(f"Added channel: {db_channel.title}")
                
                # Fetch videos (in the background)
                asyncio.create_task(
                    fetch_and_update_videos(
                        channel_id=db_channel.id,
                        uploads_playlist_id=db_channel.uploads_playlist_id
                    )
                )
    except Exception as e:
        print(f"Error loading channels from config: {e}")

# Load RSS feeds from config
@app.on_event("startup")
async def load_rss_feeds_from_config():
    try:
        from database.db import get_db
        
        # Get DB session
        db = next(get_db())
        
        # Check if rss_feeds.json exists
        config_path = os.path.join(os.path.dirname(__file__), "..", "rss_feeds.json")
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                feeds = json.load(f)
            
            print(f"Loading {len(feeds)} RSS feeds from configuration file...")
            
            # Update feeds in background
            asyncio.create_task(fetch_and_update_rss_feeds(db, feeds))
        else:
            print("No RSS feeds configuration found")
    except Exception as e:
        print(f"Error loading RSS feeds from config: {e}")

# Load social media accounts from config
@app.on_event("startup")
async def load_social_accounts_from_config():
    try:
        from database.db import get_db
        
        # Get DB session
        db = next(get_db())
        
        # Check if social_accounts.json exists
        config_path = os.path.join(os.path.dirname(__file__), "..", "social_accounts.json")
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                accounts = json.load(f)
            
            print(f"Loading {len(accounts)} social media accounts from configuration file...")
            
            # Add each account
            for account_data in accounts:
                try:
                    account = add_social_account(db, account_data)
                    print(f"Added social account: {account.platform} - {account.username}")
                    
                    # Fetch posts in background (this would need platform-specific API implementations)
                    # asyncio.create_task(fetch_social_posts(db, None, account.id))
                except Exception as ae:
                    print(f"Error adding social account: {ae}")
                    continue
        else:
            print("No social accounts configuration found")
    except Exception as e:
        print(f"Error loading social accounts from config: {e}")

# Import initial reading list
@app.on_event("startup")
async def import_initial_reading_list():
    try:
        from database.db import get_db
        
        # Get DB session
        db = next(get_db())
        
        # Check if reading_list.json exists
        config_path = os.path.join(os.path.dirname(__file__), "..", "reading_list.json")
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                materials = json.load(f)
            
            print(f"Loading {len(materials)} reading materials from configuration file...")
            
            # Add each material
            from services.reading_list_service import add_reading_material
            for material_data in materials:
                try:
                    add_reading_material(db, material_data)
                except Exception as me:
                    print(f"Error adding reading material: {me}")
                    continue
        else:
            print("No reading list configuration found, importing classics...")
            # Import classic Marxist texts
            import_marxist_classics(db)
    except Exception as e:
        print(f"Error importing reading list: {e}")

async def fetch_and_update_videos(channel_id: str, uploads_playlist_id: str):
    # Import here to avoid circular imports
    from database.db import get_db
    from services.youtube_service import YouTubeService
    from services.repository import update_videos_for_channel
    
    youtube_service = YouTubeService()
    db = next(get_db())
    
    try:
        # Fetch videos from YouTube - now properly handling tuple return
        videos, next_page_token = youtube_service.get_playlist_videos(uploads_playlist_id)
        
        # Update database
        update_videos_for_channel(db, channel_id, videos)
        
        print(f"Updated {len(videos)} videos for channel {channel_id}")
        
        # Fetch additional pages if available
        while next_page_token:
            additional_videos, next_page_token = youtube_service.get_playlist_videos(
                uploads_playlist_id, 10, next_page_token
            )
            update_videos_for_channel(db, channel_id, additional_videos)
            print(f"Updated {len(additional_videos)} additional videos for channel {channel_id}")
            
            # Add a small delay to avoid rate limiting
            await asyncio.sleep(1)
    except Exception as e:
        print(f"Error fetching videos for channel {channel_id}: {e}")

@app.get("/")
def read_root():
    return {"status": "API is running", "docs": "/docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    