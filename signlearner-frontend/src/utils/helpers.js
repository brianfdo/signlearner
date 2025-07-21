// Utility functions for common operations

/**
 * Formats similarity score as percentage
 * @param {number} score - Score between 0 and 1
 * @param {number} decimals - Number of decimal places
 * @returns {string} Formatted percentage
 */
export const formatSimilarityScore = (score, decimals = 1) => {
  return `${((score || 0) * 100).toFixed(decimals)}%`;
};

/**
 * Determines if search strategy is ASL-enhanced
 * @param {string} strategy - Search strategy
 * @returns {boolean}
 */
export const isASLEnhancedStrategy = (strategy) => {
  return strategy === 'asl_phrase';
};

/**
 * Gets appropriate badge color based on search strategy
 * @param {string} strategy - Search strategy
 * @returns {string} Color class or style
 */
export const getStrategyBadgeColor = (strategy) => {
  return isASLEnhancedStrategy(strategy) ? 'success' : 'info';
};

/**
 * Combines multiple style objects safely
 * @param {...Object} styles - Style objects to combine
 * @returns {Object} Combined style object
 */
export const combineStyles = (...styles) => {
  return Object.assign({}, ...styles);
};

/**
 * Generates a unique key for video cards
 * @param {Object} video - Video object
 * @param {number} index - Index in array
 * @returns {string} Unique key
 */
export const generateVideoKey = (video, index) => {
  return `${video.video_id || video.url}-${index}`;
};

/**
 * Truncates text to specified length with ellipsis
 * @param {string} text - Text to truncate
 * @param {number} maxLength - Maximum length
 * @returns {string} Truncated text
 */
export const truncateText = (text, maxLength = 100) => {
  if (!text || text.length <= maxLength) return text;
  return `${text.substring(0, maxLength)}...`;
};

/**
 * Validates if text input is valid for API calls
 * @param {string} text - Input text
 * @returns {boolean} Whether text is valid
 */
export const isValidInput = (text) => {
  return text && text.trim().length > 0;
};

/**
 * Formats duration string for display
 * @param {string} duration - Duration string
 * @returns {string} Formatted duration
 */
export const formatDuration = (duration) => {
  if (!duration) return 'Unknown';
  return duration;
};

/**
 * Creates YouTube embed URL from regular YouTube URL
 * @param {string} url - YouTube URL
 * @returns {string} Embed URL
 */
export const getYouTubeEmbedUrl = (url) => {
  if (!url) return '';
  return url.replace('watch?v=', 'embed/');
};

const helpers = {
  formatSimilarityScore,
  isASLEnhancedStrategy,
  getStrategyBadgeColor,
  combineStyles,
  generateVideoKey,
  truncateText,
  isValidInput,
  formatDuration,
  getYouTubeEmbedUrl
};

export default helpers; 