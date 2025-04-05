import React, { useState, useEffect } from 'react';
import { fetchAllContent } from '../services/api';
import ContentCard from './ContentCard';
import './Dashboard.css';

const Dashboard = () => {
  const [content, setContent] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeFilter, setActiveFilter] = useState('all');

  useEffect(() => {
    const loadContent = async () => {
      try {
        setLoading(true);
        const data = await fetchAllContent();
        setContent(data.content || []);
        setError(null);
      } catch (err) {
        setError('Failed to load content. Please try again later.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    loadContent();
  }, []);

  const filterContent = (type) => {
    setActiveFilter(type);
  };

  const filteredContent = activeFilter === 'all' 
    ? content 
    : content.filter(item => item.type === activeFilter);

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Content Dashboard</h1>
        <div className="filters">
          <button 
            className={activeFilter === 'all' ? 'active' : ''} 
            onClick={() => filterContent('all')}
          >
            All
          </button>
          <button 
            className={activeFilter === 'social' ? 'active' : ''} 
            onClick={() => filterContent('social')}
          >
            Social Media
          </button>
          <button 
            className={activeFilter === 'rss' ? 'active' : ''} 
            onClick={() => filterContent('rss')}
          >
            RSS Feeds
          </button>
          <button 
            className={activeFilter === 'youtube' ? 'active' : ''} 
            onClick={() => filterContent('youtube')}
          >
            YouTube
          </button>
        </div>
      </header>

      <div className="content-grid">
        {loading ? (
          <div className="loading">Loading content...</div>
        ) : error ? (
          <div className="error">{error}</div>
        ) : filteredContent.length === 0 ? (
          <div className="no-content">No content found.</div>
        ) : (
          filteredContent.map((item, index) => (
            <ContentCard key={index} item={item} />
          ))
        )}
      </div>
    </div>
  );
};

export default Dashboard;
