import React from 'react';
import './ContentCard.css';

const ContentCard = ({ item }) => {
  const renderCardContent = () => {
    switch(item.type) {
      case 'social':
        return (
          <div className="social-content">
            <div className="source">{item.source}</div>
            <p>{item.content}</p>
          </div>
        );
      
      case 'rss':
        return (
          <div className="rss-content">
            <div className="source">{item.source}</div>
            <h3>{item.title}</h3>
            <div className="published">{item.published}</div>
            <p>{item.summary}</p>
            <a href={item.link} target="_blank" rel="noopener noreferrer">Read more</a>
          </div>
        );
      
      case 'youtube':
        return (
          <div className="youtube-content">
            <div className="source">{item.source}</div>
            <h3>{item.title}</h3>
            {item.thumbnail && (
              <div className="thumbnail">
                <img src={item.thumbnail} alt={item.title} />
              </div>
            )}
            <p>{item.description}</p>
            <a href={item.link} target="_blank" rel="noopener noreferrer">Watch video</a>
          </div>
        );
      
      default:
        return (
          <div className="unknown-content">
            <div className="source">{item.source}</div>
            <p>{item.content}</p>
          </div>
        );
    }
  };

  return (
    <div className={`content-card ${item.type}`}>
      {renderCardContent()}
    </div>
  );
};

export default ContentCard;
