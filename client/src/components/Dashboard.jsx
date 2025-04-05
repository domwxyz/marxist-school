import React, { useState, useEffect } from 'react';
import VideoSection from './VideoSection';
import RssSection from './RssSection';
import SocialSection from './SocialSection';
import ReadingListSection from './ReadingListSection';
import SectionSelector from './SectionSelector';
import './Dashboard.css';

const Dashboard = () => {
  const [activeSection, setActiveSection] = useState('all');
  const [sections, setSections] = useState(['all']);
  const [content, setContent] = useState({
    videos: [],
    rssArticles: [],
    socialPosts: [],
    readingList: []
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch all content when component mounts or section changes
  useEffect(() => {
    const fetchContent = async () => {
      try {
        setLoading(true);
        
        // Fetch videos (existing functionality)
        const videosResponse = await fetch(`http://localhost:8000/api/videos?section=${activeSection}`);
        const videosData = await videosResponse.json();
        
        // Fetch RSS articles (new functionality)
        const rssResponse = await fetch(`http://localhost:8000/api/rss?section=${activeSection}`);
        const rssData = await rssResponse.json();
        const rssArticles = rssData.articles || [];
        
        // Fetch social media posts (new functionality)
        const socialResponse = await fetch(`http://localhost:8000/api/social?section=${activeSection}`);
        const socialData = await socialResponse.json();
        const socialPosts = socialData.posts || [];
        
        // Fetch reading list (new functionality)
        const readingListResponse = await fetch(`http://localhost:8000/api/reading-list?section=${activeSection}`);
        const readingListData = await readingListResponse.json();
        const readingMaterials = readingListData.materials || [];
        
        // Extract unique sections from all content
        if (sections.length <= 1) {
          // Use only video data for sections initially since it's the only one fully implemented
          const uniqueSections = ['all', ...new Set(videosData.map(item => item.section))];
          setSections(uniqueSections);
        }
        
        setContent({
          videos: videosData,
          rssArticles: rssArticles,
          socialPosts: socialPosts,
          readingList: readingMaterials
        });
        setLoading(false);
      } catch (err) {
        console.error('Failed to fetch content:', err);
        setError('Failed to load content. Please try again later.');
        setLoading(false);
      }
    };

    fetchContent();
    
    // Set up periodic refreshing (every 5 minutes)
    const intervalId = setInterval(() => fetchContent(), 300000);
    return () => clearInterval(intervalId);
  }, [activeSection]);

  const handleSectionChange = (section) => {
    setActiveSection(section);
    setContent({
      videos: [],
      rssArticles: [],
      socialPosts: [],
      readingList: []
    });
  };

  if (loading && content.videos.length === 0) {
    return (
      <div className="dashboard-container">
        <header className="dashboard-header">
          <div className="header-content">
            <img src="/images/logo.png" alt="Logo" className="logo" />
            <h1>Marxist School</h1>
          </div>
          <SectionSelector 
            sections={sections}
            currentSection={activeSection}
            onSectionChange={handleSectionChange}
          />
        </header>
        <div className="loading">Loading content...</div>
        <footer>
          <a href="https://communistusa.org">Revolutionary Communists of America</a>
        </footer>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-container">
        <header className="dashboard-header">
          <div className="header-content">
            <img src="/images/logo.png" alt="Logo" className="logo" />
            <h1>Marxist School</h1>
          </div>
        </header>
        <div className="error">{error}</div>
        <footer>
          <a href="https://communistusa.org">Revolutionary Communists of America</a>
        </footer>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <div className="header-content">
          <img src="/images/logo.png" alt="Logo" className="logo" />
          <h1>Marxist School</h1>
        </div>
        <SectionSelector 
          sections={sections}
          currentSection={activeSection}
          onSectionChange={handleSectionChange}
        />
      </header>
      
      <div className="dashboard-content">
        <div className="dashboard-grid">
          {/* Video section - upper left */}
          <div className="video-section section-wrapper">
            <VideoSection videos={content.videos} />
          </div>
          
          {/* RSS Feed section - upper right */}
          <div className="rss-section section-wrapper">
            <RssSection articles={content.rssArticles} />
          </div>
          
          {/* Reading List section - lower left */}
          <div className="reading-list-section section-wrapper">
            <ReadingListSection books={content.readingList} />
          </div>
          
          {/* Social Media section - lower right */}
          <div className="social-section section-wrapper">
            <SocialSection posts={content.socialPosts} />
          </div>
        </div>
      </div>
      
      <footer>
        <a href="https://communistusa.org">Revolutionary Communists of America</a>
      </footer>
    </div>
  );
};

export default Dashboard;
