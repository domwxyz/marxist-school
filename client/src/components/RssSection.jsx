import React, { useState } from 'react';

const RssSection = ({ articles = [] }) => {
  const [expandedArticle, setExpandedArticle] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleReadMore = (articleId) => {
    // Toggle expanded article
    if (expandedArticle === articleId) {
      setExpandedArticle(null);
    } else {
      setExpandedArticle(articleId);
    }
  };

  const handleLoadMore = async () => {
    setLoading(true);
    try {
      // Simulate loading more articles
      await new Promise(resolve => setTimeout(resolve, 1000));
      setLoading(false);
    } catch (err) {
      console.error('Error loading more articles:', err);
      setLoading(false);
    }
  };

  if (articles.length === 0) {
    return (
      <div className="section-card">
        <h2 className="section-header">Article Feed</h2>
        <div className="section-content">
          <p className="empty-message">No articles available</p>
        </div>
      </div>
    );
  }

  return (
    <div className="section-card">
      <h2 className="section-header">Article Feed</h2>
      <div className="section-content">
        {articles.map((article, index) => (
          <div key={index} className="content-item">
            {article.imageUrl && (
              <div className="content-thumbnail">
                <img src={article.imageUrl} alt={article.title} />
              </div>
            )}
            <div className="content-details">
              <h3 className="content-title">{article.title}</h3>
              <p className="content-source">{article.source}</p>
              <p className="content-date">{new Date(article.publishedAt).toLocaleDateString()}</p>
              <p className="content-description">
                {expandedArticle === index 
                  ? article.summary 
                  : `${article.summary.substring(0, 120)}...`}
              </p>
              <button 
                className="read-more-button"
                onClick={() => handleReadMore(index)}
              >
                {expandedArticle === index ? 'Show Less' : 'Read More'}
              </button>
            </div>
          </div>
        ))}
        
        {articles.length > 0 && (
          <div className="load-more-container">
            <button 
              className="load-more-button" 
              onClick={handleLoadMore}
              disabled={loading}
            >
              {loading ? 'Loading...' : 'Load More Articles'}
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default RssSection;
