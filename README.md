# Marxist School

A one-stop content aggregator dashboard for the Revolutionary Communist International.

## Overview

Marxist School is a web application that aggregates content from various sources into a single dashboard. The application provides a unified interface for accessing educational content including:

- YouTube videos and podcast episodes
- RSS feed articles
- Social media posts
- Reading list recommendations

## Features

- Clean, responsive dashboard layout
- Content organized by sections
- Video player with playlist functionality
- Article feed from various sources
- Curated reading lists with difficulty levels
- Social media integration

## Tech Stack

### Frontend
- React.js
- CSS3 with responsive design

### Backend
- FastAPI (Python)
- SQLAlchemy ORM
- SQLite database

## Getting Started

### Prerequisites
- Node.js (v14 or higher)
- Python (v3.8 or higher)
- YouTube API key

### Installation

1. Clone the repository
   ```
   git clone https://github.com/yourusername/marxist-school.git
   cd marxist-school
   ```

2. Set up the backend
   ```
   cd server
   cp .env.example .env  # Edit this file to add your YouTube API key
   pip install -r requirements.txt
   python main.py
   ```

3. Set up the frontend
   ```
   cd client
   npm install
   npm start
   ```

4. Open your browser and navigate to `http://localhost:3000`

## Configuration

- Add YouTube channels in `channels.json`
- Add RSS feeds in `rss_feeds.json`
- Add social media accounts in `social_accounts.json`
- Add reading materials in `reading_list.json`

## License

This project is licensed under the [GNU Affero General Public License v3 (AGPL-3.0)](https://www.gnu.org/licenses/agpl-3.0.en.html)
