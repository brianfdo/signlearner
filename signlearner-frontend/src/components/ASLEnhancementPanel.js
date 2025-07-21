import React from 'react';
import styles from '../styles/ASLTranslator.styles';
import { formatSimilarityScore } from '../utils/helpers';

const ASLEnhancementPanel = ({ aslEnhancement }) => {
  if (!aslEnhancement) return null;

  const renderVariations = () => {
    if (!aslEnhancement.variations_tried) return null;

    return (
      <div style={styles.variationList}>
        {aslEnhancement.variations_tried.map((variation, idx) => {
          const isBest = aslEnhancement.best_variation === variation;
          const itemStyle = isBest ? styles.variationItemBest : styles.variationItem;
          
          return (
            <div key={idx} style={itemStyle}>
              {isBest && "✓ "}"{variation}"
            </div>
          );
        })}
      </div>
    );
  };

  const formatConfidenceScore = () => {
    return formatSimilarityScore(aslEnhancement.confidence_score, 0);
  };

  return (
    <div style={styles.enhancementPanel}>
      <div style={styles.enhancementHeader}>
        <span style={styles.enhancementTitle}>
          {aslEnhancement.enhancer_type || "LangChain"} ASL Enhancement
        </span>
      </div>
      
      <div style={styles.enhancementGrid}>
        <div>
          <div style={styles.enhancementSection}>
            Grammar Rules Applied:
          </div>
          <div style={styles.enhancementContent}>
            {aslEnhancement.grammar_rules_applied?.join(", ") || "None"}
          </div>
        </div>
        
        <div>
          <div style={styles.enhancementSection}>
            ASL Variations Tried:
          </div>
          {renderVariations()}
        </div>
      </div>
      
      <div style={styles.confidenceBox}>
        <strong>Confidence Score:</strong> {formatConfidenceScore()}
      </div>
    </div>
  );
};

export default ASLEnhancementPanel; 