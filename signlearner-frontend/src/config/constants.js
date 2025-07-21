// API Configuration
export const API_CONFIG = {
  BASE_URL: 'http://localhost:8000',
  ENDPOINTS: {
    TRANSLATE: '/text-to-asl',
    GENERATE_LESSON: '/generate-lesson'
  },
  DEFAULT_LESSON_PARAMS: {
    age: 5,
    experience: 'beginner'
  }
};

// UI Configuration
export const UI_CONFIG = {
  SEARCH_PLACEHOLDER: 'Type what you want to learn in ASL...',
  BUTTON_LABELS: {
    TRANSLATE: 'Translate to ASL',
    GENERATE_LESSON: 'Generate Lesson',
    LOADING_TRANSLATE: 'Searching...',
    LOADING_LESSON: 'Generating...'
  },
  SECTION_TITLES: {
    TRANSLATION_RESULTS: 'ASL Translation Results',
    LESSON_PLAN: 'Your Personalized ASL Lesson'
  },
  HEADER: {
    TITLE: 'SignLearner',
    SUBTITLE: 'Discover American Sign Language through interactive videos'
  }
};

// Search Strategy Configuration
export const SEARCH_STRATEGIES = {
  ASL_PHRASE: 'asl_phrase',
  PHRASE: 'phrase',
  WORDS: 'words'
};

// Badge Configuration
export const BADGE_CONFIG = {
  STRATEGY_LABELS: {
    [SEARCH_STRATEGIES.ASL_PHRASE]: 'ASL-Enhanced',
    [SEARCH_STRATEGIES.PHRASE]: 'Phrase Match',
    [SEARCH_STRATEGIES.WORDS]: 'Word Match'
  }
};

// Error Messages
export const ERROR_MESSAGES = {
  TRANSLATION_FAILED: 'Failed to translate text. Please try again.',
  LESSON_FAILED: 'Failed to generate lesson plan. Please try again.',
  NETWORK_ERROR: 'Network error. Please check your connection and try again.',
  SERVER_ERROR: 'Server error. Please try again later.'
};

// Loading Messages
export const LOADING_MESSAGES = {
  SEARCHING: 'Searching for ASL videos...',
  GENERATING: 'Generating lesson plan...',
  PROCESSING: 'Processing your request...'
};

// Validation Rules
export const VALIDATION = {
  MIN_TEXT_LENGTH: 1,
  MAX_TEXT_LENGTH: 500,
  REQUIRED_FIELDS: ['text']
};

// Animation Configuration
export const ANIMATION = {
  TRANSITION_DURATION: '0.3s',
  HOVER_SCALE: 1.05,
  BUTTON_SCALE_DISABLED: 0.95
};

// Default Values
export const DEFAULTS = {
  SIMILARITY_SCORE_DECIMALS: 1,
  CONFIDENCE_SCORE_DECIMALS: 0,
  TRUNCATE_LENGTH: 100,
  MAX_VIDEOS_PER_GRID: 50
};

export default {
  API_CONFIG,
  UI_CONFIG,
  SEARCH_STRATEGIES,
  BADGE_CONFIG,
  ERROR_MESSAGES,
  LOADING_MESSAGES,
  VALIDATION,
  ANIMATION,
  DEFAULTS
}; 