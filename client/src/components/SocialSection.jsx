import React, { useState } from 'react';

const SocialSection = ({ posts = [] }) => {
  const [loading, setLoading] = useState(false);

  const handleLoadMore = async () => {
    setLoading(true);
    try {
      // Simulate loading more posts
      await new Promise(resolve => setTimeout(resolve, 1000));
      setLoading(false);
    } catch (err) {
      console.error('Error loading more posts:', err);
      setLoading(false);
    }
  };

  const getIconForPlatform = (platform) => {
    // This is a placeholder - you would use actual icons
    switch (platform.toLowerCase()) {
      case 'twitter':
      case 'x':
        return '🐦';
      case 'facebook':
        return '📘';
      case 'instagram':
        return '📷';
      case 'mastodon':
        return '🐘';
      default:
        return '💬';
    }
  };

  if (posts.length === 0) {
    return (
      <div className="section-card">
        <h2 className="section-header">Social Media</h2>
        <div className="section-content">
          <p className="empty-message">No social media posts available</p>
        </div>
      </div>
    );
  }

  return (
    <div className="section-card">
      <h2 className="section-header">Social Media</h2>
      <div className="section-content">
        {posts.map((post, index) => (
          <div key={index} className="content-item social-item">
            {post.authorImageUrl && (
              <div className="content-thumbnail author-thumbnail">
                <img src={post.authorImageUrl} alt={post.author} />
              </div>
            )}
            <div className="content-details">
              <div className="social-header">
                <span className="platform-icon">{getIconForPlatform(post.platform)}</span>
                <h3 className="content-title author-name">{post.author}</h3>
                <span className="platform-name">{post.platform}</span>
              </div>
              <p className="content-date">{new Date(post.postedAt).toLocaleDateString()}</p>
              <p className="content-description">{post.content}</p>
              {post.mediaUrl && (
                <div className="social-media">
                  <img src={post.mediaUrl} alt="Social media attachment" />
                </div>
              )}
              <div className="social-stats">
                <span className="likes">❤️ {post.likes || 0}</span>
                <span className="shares">🔄 {post.shares || 0}</span>
                <span className="comments">💬 {post.comments || 0}</span>
              </div>
            </div>
          </div>
        ))}
        
        {posts.length > 0 && (
          <div className="load-more-container">
            <button 
              className="load-more-button" 
              onClick={handleLoadMore}
              disabled={loading}
            >
              {loading ? 'Loading...' : 'Load More Posts'}
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default SocialSection;
