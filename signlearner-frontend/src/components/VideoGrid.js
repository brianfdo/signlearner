import React from 'react';
import VideoCard from './VideoCard';
import styles from '../styles/ASLTranslator.styles';
import { generateVideoKey } from '../utils/helpers';

const VideoGrid = ({ videos, title, isLesson = false }) => {
  if (!videos || videos.length === 0) return null;

  return (
    <div style={styles.card}>
      <h3 style={styles.sectionHeader}>{title}</h3>
      <div style={styles.videoGrid}>
        {videos.map((video, index) => (
          <VideoCard 
            key={generateVideoKey(video, index)}
            video={video}
            index={index}
            isLesson={isLesson}
          />
        ))}
      </div>
    </div>
  );
};

export default VideoGrid; 