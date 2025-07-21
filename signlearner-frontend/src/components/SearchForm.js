import React, { useState } from 'react';
import styles from '../styles/ASLTranslator.styles';
import { isValidInput, combineStyles } from '../utils/helpers';

const SearchForm = ({ onTranslate, onGenerateLesson, loading }) => {
  const [text, setText] = useState('');
  const [inputFocused, setInputFocused] = useState(false);
  const [showLessonOptions, setShowLessonOptions] = useState(false);
  const [lessonOptions, setLessonOptions] = useState({
    age: 25,
    experience: 'beginner',
    quickMode: false,
    ultraFast: false
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (isValidInput(text)) {
      onTranslate(text);
    }
  };

  const handleGenerateLesson = () => {
    if (isValidInput(text)) {
      onGenerateLesson(text, lessonOptions);
    }
  };

  const handleLessonModeChange = (mode) => {
    setLessonOptions(prev => ({
      ...prev,
      quickMode: mode === 'quick',
      ultraFast: mode === 'ultra-fast'
    }));
  };

  const getButtonStyle = (baseStyle, isDisabled) => {
    return combineStyles(
      styles.button,
      baseStyle,
      isDisabled ? styles.buttonDisabled : {}
    );
  };

  const getInputStyle = () => {
    return combineStyles(
      styles.input,
      inputFocused ? styles.inputFocus : {}
    );
  };

  const handleButtonHover = (e, isDisabled) => {
    if (!isDisabled) {
      e.target.style.transform = styles.buttonHover.transform;
    }
  };

  const handleButtonLeave = (e, isDisabled) => {
    if (!isDisabled) {
      e.target.style.transform = "scale(1)";
    }
  };

  return (
    <div style={styles.card}>
      <form onSubmit={handleSubmit} style={styles.searchForm}>
        <input
          type="text"
          value={text}
          placeholder="Type what you want to learn in ASL..."
          onChange={(e) => setText(e.target.value)}
          style={getInputStyle()}
          onFocus={() => setInputFocused(true)}
          onBlur={() => setInputFocused(false)}
        />
        
        <div style={styles.buttonContainer}>
          <button 
            type="submit"
            disabled={loading}
            style={getButtonStyle(styles.buttonPrimary, loading)}
            onMouseOver={(e) => handleButtonHover(e, loading)}
            onMouseOut={(e) => handleButtonLeave(e, loading)}
          >
            {loading ? "Searching..." : "Translate to ASL"}
          </button>
          
          <button 
            type="button"
            onClick={() => setShowLessonOptions(!showLessonOptions)}
            disabled={loading}
            style={getButtonStyle(styles.buttonSecondary, loading)}
            onMouseOver={(e) => handleButtonHover(e, loading)}
            onMouseOut={(e) => handleButtonLeave(e, loading)}
          >
            {loading ? "Generating..." : "Generate Lesson"}
          </button>
        </div>

        {showLessonOptions && (
          <div style={styles.lessonOptions}>
            <h4 style={styles.lessonOptionsTitle}>Lesson Generation Options</h4>
            
            <div style={styles.optionGroup}>
              <label style={styles.label}>Performance Mode:</label>
              <div style={styles.radioGroup}>
                <label style={styles.radioLabel}>
                  <input
                    type="radio"
                    name="mode"
                    value="full"
                    checked={!lessonOptions.quickMode && !lessonOptions.ultraFast}
                    onChange={() => handleLessonModeChange('full')}
                  />
                  Full Mode (Best Quality)
                </label>
                <label style={styles.radioLabel}>
                  <input
                    type="radio"
                    name="mode"
                    value="quick"
                    checked={lessonOptions.quickMode}
                    onChange={() => handleLessonModeChange('quick')}
                  />
                  Quick Mode (Fast)
                </label>
                <label style={styles.radioLabel}>
                  <input
                    type="radio"
                    name="mode"
                    value="ultra-fast"
                    checked={lessonOptions.ultraFast}
                    onChange={() => handleLessonModeChange('ultra-fast')}
                  />
                  Ultra-Fast Mode (Instant)
                </label>
              </div>
            </div>

            <div style={styles.optionGroup}>
              <label style={styles.label}>Age Group:</label>
              <select
                value={lessonOptions.age}
                onChange={(e) => setLessonOptions(prev => ({ ...prev, age: parseInt(e.target.value) }))}
                style={styles.select}
              >
                <option value={5}>5-10 years</option>
                <option value={15}>11-20 years</option>
                <option value={25}>21-30 years</option>
                <option value={35}>31-40 years</option>
                <option value={45}>41+ years</option>
              </select>
            </div>

            <div style={styles.optionGroup}>
              <label style={styles.label}>Experience Level:</label>
              <select
                value={lessonOptions.experience}
                onChange={(e) => setLessonOptions(prev => ({ ...prev, experience: e.target.value }))}
                style={styles.select}
              >
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
            </div>

            <button 
              type="button"
              onClick={handleGenerateLesson}
              disabled={loading}
              style={getButtonStyle(styles.buttonSuccess, loading)}
              onMouseOver={(e) => handleButtonHover(e, loading)}
              onMouseOut={(e) => handleButtonLeave(e, loading)}
            >
              {loading ? "Generating..." : "Generate Lesson"}
            </button>
          </div>
        )}
      </form>
    </div>
  );
};

export default SearchForm; 