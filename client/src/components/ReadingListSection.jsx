import React, { useState } from 'react';

const ReadingListSection = ({ books = [] }) => {
  const [expandedBook, setExpandedBook] = useState(null);
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState('all'); // 'all', 'beginner', 'intermediate', 'advanced'

  const handleViewDetails = (bookId) => {
    // Toggle expanded book
    if (expandedBook === bookId) {
      setExpandedBook(null);
    } else {
      setExpandedBook(bookId);
    }
  };

  const handleLoadMore = async () => {
    setLoading(true);
    try {
      // Simulate loading more books
      await new Promise(resolve => setTimeout(resolve, 1000));
      setLoading(false);
    } catch (err) {
      console.error('Error loading more books:', err);
      setLoading(false);
    }
  };

  const handleFilterChange = (newFilter) => {
    setFilter(newFilter);
  };

  // Filter books by difficulty level
  const filteredBooks = filter === 'all' 
    ? books 
    : books.filter(book => book.difficulty === filter);

  if (books.length === 0) {
    return (
      <div className="section-card">
        <h2 className="section-header">Reading List</h2>
        <div className="section-content">
          <p className="empty-message">No reading materials available</p>
        </div>
      </div>
    );
  }

  return (
    <div className="section-card">
      <h2 className="section-header">Reading List</h2>
      
      <div className="filter-buttons">
        <button 
          className={filter === 'all' ? 'active' : ''} 
          onClick={() => handleFilterChange('all')}
        >
          All
        </button>
        <button 
          className={filter === 'beginner' ? 'active' : ''} 
          onClick={() => handleFilterChange('beginner')}
        >
          Beginner
        </button>
        <button 
          className={filter === 'intermediate' ? 'active' : ''} 
          onClick={() => handleFilterChange('intermediate')}
        >
          Intermediate
        </button>
        <button 
          className={filter === 'advanced' ? 'active' : ''} 
          onClick={() => handleFilterChange('advanced')}
        >
          Advanced
        </button>
      </div>
      
      <div className="section-content">
        {filteredBooks.map((book, index) => (
          <div key={index} className="content-item book-item">
            {book.coverUrl && (
              <div className="content-thumbnail book-cover">
                <img src={book.coverUrl} alt={book.title} />
              </div>
            )}
            <div className="content-details">
              <h3 className="content-title">{book.title}</h3>
              <p className="content-source">By {book.author}</p>
              <p className="book-tags">
                <span className={`difficulty-tag ${book.difficulty}`}>
                  {book.difficulty.charAt(0).toUpperCase() + book.difficulty.slice(1)}
                </span>
                {book.tags && book.tags.map((tag, i) => (
                  <span key={i} className="tag">{tag}</span>
                ))}
              </p>
              {expandedBook === index ? (
                <>
                  <p className="book-description">{book.description}</p>
                  <div className="book-links">
                    {book.pdfUrl && (
                      <a href={book.pdfUrl} target="_blank" rel="noopener noreferrer" className="book-link">
                        PDF Download
                      </a>
                    )}
                    {book.audioUrl && (
                      <a href={book.audioUrl} target="_blank" rel="noopener noreferrer" className="book-link">
                        Audio Version
                      </a>
                    )}
                    {book.externalUrl && (
                      <a href={book.externalUrl} target="_blank" rel="noopener noreferrer" className="book-link">
                        External Link
                      </a>
                    )}
                  </div>
                </>
              ) : (
                <p className="content-description">
                  {book.description && `${book.description.substring(0, 100)}...`}
                </p>
              )}
              <button 
                className="details-button"
                onClick={() => handleViewDetails(index)}
              >
                {expandedBook === index ? 'Show Less' : 'View Details'}
              </button>
            </div>
          </div>
        ))}
        
        {filteredBooks.length > 0 && (
          <div className="load-more-container">
            <button 
              className="load-more-button" 
              onClick={handleLoadMore}
              disabled={loading}
            >
              {loading ? 'Loading...' : 'Load More Reading Materials'}
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default ReadingListSection;
