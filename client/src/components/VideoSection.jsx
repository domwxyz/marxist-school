import React, { useState } from 'react';
import VideoPlayer from './VideoPlayer';
import VideoList from './VideoList';

const VideoSection = ({ videos }) => {
  const [currentVideo, setCurrentVideo] = useState(videos.length > 0 ? videos[0] : null);
  const [loadingMore, setLoadingMore] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const [nextCursor, setNextCursor] = useState(null);

  const handleVideoSelect = (video) => {
    setCurrentVideo(video);
  };

  const handleLoadMore = async () => {
    if (loadingMore || !hasMore || !nextCursor) return;
    
    try {
      setLoadingMore(true);
      
      // Use the existing API endpoint for loading more videos
      const response = await fetch(`http://localhost:8000/api/videos/load-more?cursor=${nextCursor}`);
      const result = await response.json();
      
      if (result.videos && result.videos.length > 0) {
        // Update the videos list by adding the new videos
        // This is just for the skeleton, you'll need to update the parent component's state
        console.log('Loaded more videos:', result.videos);
        
        // Update cursor for next pagination
        setNextCursor(result.nextCursor);
        
        // Determine if there are more videos to load
        setHasMore(!!result.nextCursor);
      } else {
        // No more videos to load
        setHasMore(false);
      }
      
      setLoadingMore(false);
    } catch (err) {
      console.error('Failed to load more videos:', err);
      setLoadingMore(false);
    }
  };

  return (
    <div className="section-card">
      <h2 className="section-header">Videos</h2>
      <div className="section-content">
        {videos.length > 0 ? (
          <>
            <div className="video-container">
              <iframe
                width="100%"
                height="100%"
                src={currentVideo ? `https://www.youtube.com/embed/${currentVideo.id}` : ''}
                title={currentVideo ? currentVideo.title : 'Video player'}
                frameBorder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
              ></iframe>
            </div>
            
            {currentVideo && (
              <div className="video-info">
                <h3>{currentVideo.title}</h3>
                <p className="channel-title">{currentVideo.channel_title}</p>
                <p className="publish-date">
                  {new Date(currentVideo.published_at).toLocaleDateString()}
                </p>
              </div>
            )}
            
            <div className="video-list-compact">
              <h4>More Videos</h4>
              <div className="video-scroll">
                {videos.slice(0, 5).map((video) => (
                  <div
                    key={video.id}
                    className={`video-item ${currentVideo && video.id === currentVideo.id ? 'active' : ''}`}
                    onClick={() => handleVideoSelect(video)}
                  >
                    <div className="thumbnail">
                      <img src={video.thumbnail_url} alt={video.title} />
                    </div>
                    <div className="video-info">
                      <h4>{video.title}</h4>
                      <p className="date">
                        {new Date(video.published_at).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
              
              {hasMore && (
                <div className="load-more-container">
                  <button 
                    className="load-more-button" 
                    onClick={handleLoadMore}
                    disabled={loadingMore}
                  >
                    {loadingMore ? 'Loading...' : 'Load More'}
                  </button>
                </div>
              )}
            </div>
          </>
        ) : (
          <div className="no-content">No videos available</div>
        )}
      </div>
    </div>
  );
};

export default VideoSection;
