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
    window.scrollTo({ top: 0, behavior: 'smooth' });
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
    <div className="section-card video-section">
      <h2 className="section-header">Videos</h2>
      <div className="content-container">
        {/* Main column with video player */}
        <div className="main-column">
          <div className="card-container player-container">
            <VideoPlayer video={currentVideo} />
          </div>
        </div>
        
        {/* Video list column */}
        <div className="list-container card-container">
          <VideoList 
            videos={videos}
            currentVideo={currentVideo}
            onSelectVideo={handleVideoSelect}
            onLoadMore={handleLoadMore}
            hasMore={hasMore}
            isLoading={loadingMore}
          />
        </div>
      </div>
    </div>
  );
};

export default VideoSection;
