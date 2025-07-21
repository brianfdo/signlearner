import React from 'react';
import ASLEnhancementPanel from './ASLEnhancementPanel';
import styles from '../styles/ASLTranslator.styles';
import { formatSimilarityScore, isASLEnhancedStrategy, combineStyles } from '../utils/helpers';

const SearchInfo = ({ searchInfo }) => {
  if (!searchInfo) return null;

  const getStrategyBadge = () => {
    const isAslPhrase = isASLEnhancedStrategy(searchInfo.strategy);
    const badgeStyle = combineStyles(
      styles.badge,
      isAslPhrase ? styles.badgeSuccess : styles.badgeInfo
    );

    const strategyText = isAslPhrase ? "ASL-Enhanced" : 
                       searchInfo.strategy === "phrase" ? "Phrase Match" : "Word Match";

    return (
      <span style={badgeStyle}>
        {strategyText}
      </span>
    );
  };

  const getSimilarityScore = () => {
    if (isASLEnhancedStrategy(searchInfo.strategy)) {
      return (
        <span style={{color: "#10b981", fontWeight: "bold"}}>
          {formatSimilarityScore(searchInfo.phrase_similarity)} match
        </span>
      );
    }
    
    if (searchInfo.strategy === "words") {
      return (
        <span style={{color: "#3b82f6", fontWeight: "bold"}}>
          {formatSimilarityScore(searchInfo.word_avg_similarity)} avg match
        </span>
      );
    }
    
    return null;
  };

  return (
    <div style={styles.smallCard}>
      <div style={styles.searchInfo}>
        <div style={{
          display: "flex",
          alignItems: "center",
          gap: "8px",
          fontSize: "1.1rem",
          fontWeight: "600",
          color: "#374151",
          flexWrap: "wrap"
        }}>
          {getStrategyBadge()}
          {getSimilarityScore()}
          
          {searchInfo.found_videos !== undefined && (
            <span style={styles.badge}>
              {searchInfo.found_videos}/{searchInfo.total_videos} videos
            </span>
          )}
        </div>
      </div>
      
      <ASLEnhancementPanel aslEnhancement={searchInfo.asl_enhancement} />
    </div>
  );
};

export default SearchInfo; 