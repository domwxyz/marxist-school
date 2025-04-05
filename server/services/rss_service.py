from sqlalchemy.orm import Session
from models.models import RssFeed, RssArticle
from typing import List, Optional, Dict, Any
import feedparser
from datetime import datetime
import uuid
import re
from urllib.parse import urlparse

def sanitize_id(text: str) -> str:
    """
    Create a safe ID from text input
    """
    if not text:
        return str(uuid.uuid4())
    
    # Replace special characters and spaces with underscores
    safe_id = re.sub(r'[^\w\s-]', '', text).strip().lower()
    safe_id = re.sub(r'[-\s]+', '_', safe_id)
    
    return safe_id

def get_rss_feeds(db: Session, section: Optional[str] = None, cursor: Optional[str] = None, limit: int = 10):
    """
    Get RSS feeds from database, optionally filtered by section
    """
    query = db.query(RssFeed)
    
    if section and section.lower() != "all":
        query = query.filter(RssFeed.section == section)
    
    feeds = query.order_by(RssFeed.last_updated.desc()).limit(limit).all()
    
    return feeds

def get_rss_articles(db: Session, section: Optional[str] = None, cursor: Optional[str] = None, limit: int = 10):
    """
    Get RSS articles from database, optionally filtered by section
    - section: Filter by section (optional)
    - cursor: Last article's published_at timestamp (optional)
    - limit: Maximum number of articles to return
    """
    query = db.query(
        RssArticle,
        RssFeed.title.label("feed_title"),
        RssFeed.section
    ).join(RssFeed)
    
    if section and section.lower() != "all":
        query = query.filter(RssFeed.section == section)
    
    # Apply cursor pagination if provided
    if cursor:
        # This is just a simple example - in a real app, you'd need to parse the cursor
        # and filter articles accordingly
        query = query.filter(RssArticle.published_at < datetime.fromisoformat(cursor))
    
    # Order by published date, newest first
    articles_data = query.order_by(RssArticle.published_at.desc()).limit(limit + 1).all()
    
    # Check if there are more articles
    has_more = len(articles_data) > limit
    result_articles = articles_data[:limit]
    
    # Format the response
    articles = []
    next_cursor = None
    
    for article, feed_title, section in result_articles:
        articles.append({
            "id": article.id,
            "title": article.title,
            "link": article.link,
            "author": article.author,
            "published_at": article.published_at.isoformat(),
            "summary": article.summary,
            "content": article.content,
            "image_url": article.image_url,
            "source": feed_title,  # Using the feed title as the source
            "section": section
        })
    
    # Set next cursor to the published_at of the last article if there are more
    if has_more and result_articles:
        next_cursor = result_articles[-1][0].published_at.isoformat()
    
    return {
        "articles": articles,
        "next_cursor": next_cursor
    }

async def fetch_and_update_rss_feeds(db: Session, feeds_config: List[Dict[str, Any]]):
    """
    Fetch articles from RSS feeds and update the database
    """
    for feed_config in feeds_config:
        try:
            # Skip if URL is missing
            if "url" not in feed_config:
                print("Missing URL in RSS feed config")
                continue
            
            # Parse the feed
            parsed_feed = feedparser.parse(feed_config["url"])
            
            if not parsed_feed.feed:
                print(f"Failed to parse feed: {feed_config['url']}")
                continue
            
            # Get or create feed in database
            feed_title = feed_config.get("title", parsed_feed.feed.get("title", "Unknown Feed"))
            feed_id = sanitize_id(feed_title)
            
            db_feed = db.query(RssFeed).filter(RssFeed.id == feed_id).first()
            
            if not db_feed:
                # Create new feed
                db_feed = RssFeed(
                    id=feed_id,
                    title=feed_title,
                    url=feed_config["url"],
                    description=parsed_feed.feed.get("description", ""),
                    section=feed_config.get("section", "general"),
                    last_updated=datetime.utcnow()
                )
                db.add(db_feed)
                db.commit()
                db.refresh(db_feed)
            else:
                # Update existing feed
                db_feed.last_updated = datetime.utcnow()
                db.commit()
            
            # Process articles
            for entry in parsed_feed.entries:
                # Create a unique ID for the article
                article_id = sanitize_id(entry.get("id", entry.get("link", "")))
                
                # Check if article already exists
                existing_article = db.query(RssArticle).filter(RssArticle.id == article_id).first()
                
                if not existing_article:
                    # Parse published date
                    published_at = None
                    if "published_parsed" in entry and entry.published_parsed:
                        published_at = datetime(*entry.published_parsed[:6])
                    else:
                        published_at = datetime.utcnow()
                    
                    # Get image URL if available
                    image_url = None
                    if "media_content" in entry and entry.media_content:
                        for media in entry.media_content:
                            if "url" in media and media.get("medium", "") == "image":
                                image_url = media["url"]
                                break
                    
                    # Create new article
                    new_article = RssArticle(
                        id=article_id,
                        feed_id=db_feed.id,
                        title=entry.get("title", "Untitled"),
                        link=entry.get("link", ""),
                        author=entry.get("author", "Unknown"),
                        published_at=published_at,
                        summary=entry.get("summary", ""),
                        content=entry.get("content", [{"value": ""}])[0].get("value", "") if "content" in entry else "",
                        image_url=image_url
                    )
                    
                    db.add(new_article)
            
            db.commit()
            print(f"Updated RSS feed: {feed_title}")
                
        except Exception as e:
            print(f"Error updating RSS feed {feed_config.get('url')}: {e}")
            db.rollback()
            continue

def add_rss_feed(db: Session, feed_data: Dict[str, Any]):
    """
    Add a new RSS feed to the database
    """
    try:
        # Parse the feed to get basic info
        parsed_feed = feedparser.parse(feed_data["url"])
        
        if not parsed_feed.feed:
            raise ValueError(f"Failed to parse feed: {feed_data['url']}")
        
        # Create feed ID
        feed_title = feed_data.get("title", parsed_feed.feed.get("title", "Unknown Feed"))
        feed_id = sanitize_id(feed_title)
        
        # Check if feed already exists
        existing_feed = db.query(RssFeed).filter(RssFeed.id == feed_id).first()
        if existing_feed:
            return existing_feed
        
        # Create new feed
        new_feed = RssFeed(
            id=feed_id,
            title=feed_title,
            url=feed_data["url"],
            description=parsed_feed.feed.get("description", ""),
            section=feed_data.get("section", "general"),
            last_updated=datetime.utcnow()
        )
        
        db.add(new_feed)
        db.commit()
        db.refresh(new_feed)
        
        return new_feed
    
    except Exception as e:
        print(f"Error adding RSS feed: {e}")
        db.rollback()
        raise
    