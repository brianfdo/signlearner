import React, { useState } from 'react';
import styles from '../styles/ASLTranslator.styles';
import { formatSimilarityScore, isASLEnhancedStrategy, combineStyles } from '../utils/helpers';

const VideoCard = ({ video, index, isLesson = false }) => {
  const [isHovered, setIsHovered] = useState(false);

  const getSimilarityBadge = () => {
    if (!video.similarity_score) return null;
    
    const badgeStyle = combineStyles(
      styles.badge,
      isASLEnhancedStrategy(video.search_type) ? styles.badgeSuccess : styles.badgeInfo
    );

    return (
      <div style={badgeStyle}>
        {formatSimilarityScore(video.similarity_score)}
      </div>
    );
  };

  const getStepBadge = () => {
    if (!isLesson) return null;
    
    return (
      <div style={styles.lessonStep}>
        Step {index + 1}
      </div>
    );
  };

  const getLinkStyles = () => {
    const baseStyle = isLesson ? styles.lessonLink : styles.videoLink;
    const hoverStyle = isLesson ? styles.lessonLinkHover : styles.videoLinkHover;
    return { baseStyle, hoverStyle };
  };

  const cardStyle = combineStyles(
    styles.videoCard,
    isHovered ? styles.videoCardHover : {}
  );

  const { baseStyle: linkStyle, hoverStyle: linkHoverStyle } = getLinkStyles();

  return (
    <div 
      style={cardStyle}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div style={styles.videoHeader}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          {getStepBadge()}
          <div style={styles.videoTitle}>
            {video.word}
          </div>
        </div>
        {getSimilarityBadge()}
      </div>
      
      <div style={styles.videoDescription}>
        {video.title}
      </div>
      
      <div style={styles.videoWrapper}>
        <iframe
          src={video.embed_url}
          title={video.title}
          style={styles.videoIframe}
          allowFullScreen
        />
      </div>
      
      <div style={styles.videoFooter}>
        <span style={styles.videoDuration}>
          Duration: {video.duration}
        </span>
        <a 
          href={video.url} 
          target="_blank" 
          rel="noopener noreferrer"
          style={linkStyle}
          onMouseOver={(e) => {
            e.target.style.backgroundColor = linkHoverStyle.backgroundColor;
          }}
          onMouseOut={(e) => {
            e.target.style.backgroundColor = linkStyle.backgroundColor;
          }}
        >
          Watch on YouTube →
        </a>
      </div>
    </div>
  );
};

export default VideoCard; 