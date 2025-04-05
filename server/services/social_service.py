from sqlalchemy.orm import Session
from sqlalchemy import desc
from models.models import SocialAccount, SocialPost
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime

def get_social_posts(
    db: Session, 
    section: Optional[str] = None, 
    platform: Optional[str] = None,
    cursor: Optional[str] = None,
    limit: int = 10
):
    """
    Get social media posts from database, optionally filtered by section and platform
    - section: Filter by section (optional)
    - platform: Filter by platform (twitter, facebook, etc.) (optional)
    - cursor: Last post's ID or posted_at timestamp (optional)
    - limit: Maximum number of posts to return
    """
    query = db.query(
        SocialPost,
        SocialAccount.display_name.label("author"),
        SocialAccount.avatar_url.label("author_image_url"),
        SocialAccount.section
    ).join(SocialAccount)
    
    # Apply filters
    if section and section.lower() != "all":
        query = query.filter(SocialAccount.section == section)
    
    if platform:
        query = query.filter(SocialPost.platform == platform)
    
    # Apply cursor pagination if provided
    if cursor:
        try:
            # This is just a simple example - in a real app, you'd need a more robust cursor system
            # Assuming cursor is a timestamp string
            cursor_date = datetime.fromisoformat(cursor)
            query = query.filter(SocialPost.posted_at < cursor_date)
        except ValueError:
            # If cursor isn't a valid date, we'll just ignore it
            pass
    
    # Order by posted date, newest first
    posts_data = query.order_by(desc(SocialPost.posted_at)).limit(limit + 1).all()
    
    # Check if there are more posts
    has_more = len(posts_data) > limit
    result_posts = posts_data[:limit]
    
    # Format the response
    posts = []
    next_cursor = None
    
    for post, author, author_image_url, section in result_posts:
        posts.append({
            "id": post.id,
            "platform": post.platform,
            "content": post.content,
            "postedAt": post.posted_at.isoformat(),
            "url": post.url,
            "mediaUrl": post.media_url,
            "likes": post.likes,
            "shares": post.shares,
            "comments": post.comments,
            "author": author,
            "authorImageUrl": author_image_url,
            "section": section
        })
    
    # Set next cursor to the posted_at of the last post if there are more
    if has_more and result_posts:
        next_cursor = result_posts[-1][0].posted_at.isoformat()
    
    return {
        "posts": posts,
        "nextCursor": next_cursor
    }

def add_social_account(db: Session, account_data: Dict[str, Any]):
    """
    Add a new social media account to the database
    """
    try:
        # Create account ID
        account_id = f"{account_data['platform'].lower()}_{account_data['username']}"
        
        # Check if account already exists
        existing_account = db.query(SocialAccount).filter(SocialAccount.id == account_id).first()
        if existing_account:
            return existing_account
        
        # Create new account
        new_account = SocialAccount(
            id=account_id,
            platform=account_data["platform"],
            username=account_data["username"],
            display_name=account_data.get("display_name", account_data["username"]),
            profile_url=account_data["profile_url"],
            avatar_url=account_data.get("avatar_url", ""),
            section=account_data.get("section", "general"),
            last_updated=datetime.utcnow()
        )
        
        db.add(new_account)
        db.commit()
        db.refresh(new_account)
        
        return new_account
    
    except Exception as e:
        print(f"Error adding social account: {e}")
        db.rollback()
        raise

def add_social_post(db: Session, post_data: Dict[str, Any]):
    """
    Add a new social media post to the database
    """
    try:
        # Generate unique ID if not provided
        post_id = post_data.get("id", str(uuid.uuid4()))
        
        # Check if post already exists
        existing_post = db.query(SocialPost).filter(SocialPost.id == post_id).first()
        if existing_post:
            return existing_post
        
        # Create new post
        new_post = SocialPost(
            id=post_id,
            account_id=post_data["account_id"],
            platform=post_data["platform"],
            content=post_data["content"],
            posted_at=post_data.get("posted_at", datetime.utcnow()),
            url=post_data.get("url", ""),
            media_url=post_data.get("media_url", ""),
            likes=post_data.get("likes", 0),
            shares=post_data.get("shares", 0),
            comments=post_data.get("comments", 0)
        )
        
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        
        return new_post
    
    except Exception as e:
        print(f"Error adding social post: {e}")
        db.rollback()
        raise

async def fetch_social_posts(db: Session, platform_api, account_id: str, limit: int = 20):
    """
    Fetch recent posts from a social media platform API
    This is a placeholder function - you would need to implement platform-specific APIs
    """
    try:
        account = db.query(SocialAccount).filter(SocialAccount.id == account_id).first()
        if not account:
            raise ValueError(f"Account not found: {account_id}")
        
        # This is where you would call the specific platform API
        # For example:
        # if account.platform.lower() == 'twitter':
        #     posts = await fetch_twitter_posts(platform_api, account.username, limit)
        # elif account.platform.lower() == 'facebook':
        #     posts = await fetch_facebook_posts(platform_api, account.username, limit)
        
        # For now, we'll just return a placeholder
        posts = []
        
        # Save posts to database
        for post_data in posts:
            post_data["account_id"] = account_id
            post_data["platform"] = account.platform
            add_social_post(db, post_data)
        
        return posts
    
    except Exception as e:
        print(f"Error fetching social posts for account {account_id}: {e}")
        return []

# Example implementation for Twitter/X API (placeholder)
async def fetch_twitter_posts(api_client, username: str, limit: int = 20):
    """
    Fetch recent tweets from a Twitter/X account
    This is a placeholder - you would need to implement the actual Twitter API
    """
    # This would be replaced with actual Twitter API calls
    # Using a library like tweepy or the Twitter v2 API
    
    # Placeholder data
    return [
        {
            "id": f"tweet_{i}_{username}",
            "content": f"Example tweet {i} from {username}",
            "posted_at": datetime.utcnow(),
            "url": f"https://twitter.com/{username}/status/{i}",
            "likes": i * 10,
            "shares": i * 5,
            "comments": i * 2
        }
        for i in range(1, limit + 1)
    ]

# Example implementation for Mastodon API (placeholder)
async def fetch_mastodon_posts(api_client, username: str, limit: int = 20):
    """
    Fetch recent toots from a Mastodon account
    This is a placeholder - you would need to implement the actual Mastodon API
    """
    # This would be replaced with actual Mastodon API calls
    # Using a library like Mastodon.py
    
    # Placeholder data
    return [
        {
            "id": f"toot_{i}_{username}",
            "content": f"Example toot {i} from {username}",
            "posted_at": datetime.utcnow(),
            "url": f"https://mastodon.social/@{username}/{i}",
            "likes": i * 8,
            "shares": i * 3,
            "comments": i * 1
        }
        for i in range(1, limit + 1)
    ]
    