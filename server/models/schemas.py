from pydantic import BaseModel
from typing import List, Optional, Set
from datetime import datetime

# Existing Schemas

class VideoBase(BaseModel):
    id: str
    title: str
    description: str
    published_at: str
    thumbnail_url: str

class Video(VideoBase):
    channel_title: str
    section: str

    class Config:
        orm_mode = True

class ChannelBase(BaseModel):
    id: str
    section: str

class ChannelCreate(ChannelBase):
    pass

class Channel(ChannelBase):
    title: str
    uploads_playlist_id: str

    class Config:
        orm_mode = True

# New Schemas for RSS Feeds

class RssFeedBase(BaseModel):
    title: str
    url: str
    description: Optional[str] = None
    section: str

class RssFeedCreate(RssFeedBase):
    pass

class RssFeed(RssFeedBase):
    id: str
    last_updated: datetime

    class Config:
        orm_mode = True

class RssArticleBase(BaseModel):
    title: str
    link: str
    author: Optional[str] = None
    published_at: datetime
    summary: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[str] = None

class RssArticleCreate(RssArticleBase):
    feed_id: str

class RssArticle(RssArticleBase):
    id: str
    feed_title: str
    section: str

    class Config:
        orm_mode = True

# New Schemas for Social Media

class SocialAccountBase(BaseModel):
    platform: str
    username: str
    display_name: str
    profile_url: str
    avatar_url: Optional[str] = None
    section: str

class SocialAccountCreate(SocialAccountBase):
    pass

class SocialAccount(SocialAccountBase):
    id: str
    last_updated: datetime

    class Config:
        orm_mode = True

class SocialPostBase(BaseModel):
    platform: str
    content: str
    posted_at: datetime
    url: Optional[str] = None
    media_url: Optional[str] = None
    likes: Optional[int] = 0
    shares: Optional[int] = 0
    comments: Optional[int] = 0

class SocialPostCreate(SocialPostBase):
    account_id: str

class SocialPost(SocialPostBase):
    id: str
    author: str  # display_name from account
    author_image_url: Optional[str] = None  # avatar_url from account
    section: str

    class Config:
        orm_mode = True

# New Schemas for Reading List

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: str

    class Config:
        orm_mode = True

class ReadingMaterialBase(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    difficulty: str  # beginner, intermediate, advanced
    section: str
    cover_url: Optional[str] = None
    pdf_url: Optional[str] = None
    audio_url: Optional[str] = None
    external_url: Optional[str] = None
    publication_year: Optional[str] = None
    pages: Optional[int] = None
    reading_time: Optional[int] = None  # in minutes

class ReadingMaterialCreate(ReadingMaterialBase):
    tag_names: Optional[List[str]] = None

class ReadingMaterial(ReadingMaterialBase):
    id: str
    tags: Optional[List[Tag]] = None

    class Config:
        orm_mode = True

# Pagination Schemas

class PaginatedResult(BaseModel):
    items: List
    next_cursor: Optional[str] = None
    total: Optional[int] = None
        