from sqlalchemy import Column, String, ForeignKey, Text, Integer, DateTime, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from database.db import Base
import datetime

# Existing Models

class Channel(Base):
    __tablename__ = "channels"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    section = Column(String, index=True)
    uploads_playlist_id = Column(String)
    
    videos = relationship("Video", back_populates="channel", cascade="all, delete-orphan")

class Video(Base):
    __tablename__ = "videos"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    channel_id = Column(String, ForeignKey("channels.id"))
    published_at = Column(String, index=True)
    thumbnail_url = Column(String)
    
    channel = relationship("Channel", back_populates="videos")

# New Models for RSS Feeds

class RssFeed(Base):
    __tablename__ = "rss_feeds"
    
    id = Column(String, primary_key=True)
    title = Column(String, index=True)
    url = Column(String, unique=True)
    description = Column(Text)
    section = Column(String, index=True)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)
    
    articles = relationship("RssArticle", back_populates="feed", cascade="all, delete-orphan")

class RssArticle(Base):
    __tablename__ = "rss_articles"
    
    id = Column(String, primary_key=True)
    feed_id = Column(String, ForeignKey("rss_feeds.id"))
    title = Column(String, index=True)
    link = Column(String)
    author = Column(String)
    published_at = Column(DateTime, index=True)
    summary = Column(Text)
    content = Column(Text)
    image_url = Column(String)
    
    feed = relationship("RssFeed", back_populates="articles")

# New Models for Social Media

class SocialAccount(Base):
    __tablename__ = "social_accounts"
    
    id = Column(String, primary_key=True)
    platform = Column(String, index=True)  # twitter, facebook, instagram, etc.
    username = Column(String)
    display_name = Column(String)
    profile_url = Column(String)
    avatar_url = Column(String)
    section = Column(String, index=True)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)
    
    posts = relationship("SocialPost", back_populates="account", cascade="all, delete-orphan")

class SocialPost(Base):
    __tablename__ = "social_posts"
    
    id = Column(String, primary_key=True)
    account_id = Column(String, ForeignKey("social_accounts.id"))
    platform = Column(String, index=True)
    content = Column(Text)
    posted_at = Column(DateTime, index=True)
    url = Column(String)
    media_url = Column(String)
    likes = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    
    account = relationship("SocialAccount", back_populates="posts")

# New Models for Reading List

# Association table for many-to-many relationship between books and tags
book_tags = Table(
    "book_tags",
    Base.metadata,
    Column("book_id", String, ForeignKey("reading_materials.id")),
    Column("tag_id", String, ForeignKey("tags.id"))
)

class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(String, primary_key=True)
    name = Column(String, unique=True, index=True)
    
    # Relationship for many-to-many with books
    books = relationship("ReadingMaterial", secondary=book_tags, back_populates="tags")

class ReadingMaterial(Base):
    __tablename__ = "reading_materials"
    
    id = Column(String, primary_key=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    description = Column(Text)
    difficulty = Column(String, index=True)  # beginner, intermediate, advanced
    section = Column(String, index=True)
    cover_url = Column(String)
    pdf_url = Column(String)
    audio_url = Column(String)
    external_url = Column(String)
    publication_year = Column(String)
    pages = Column(Integer)
    reading_time = Column(Integer)  # in minutes
    
    # Relationship for many-to-many with tags
    tags = relationship("Tag", secondary=book_tags, back_populates="books")
    