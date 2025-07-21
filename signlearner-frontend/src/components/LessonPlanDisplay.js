import React from 'react';
import styles from '../styles/ASLTranslator.styles';

const LessonPlanDisplay = ({ lessonPlan }) => {
  if (!lessonPlan) return null;

  const formatDuration = (duration) => {
    if (typeof duration === 'string') return duration;
    return `${duration} minutes`;
  };



  return (
    <div style={styles.card}>
      <div style={styles.lessonHeader}>
        <h2 style={styles.lessonTitle}>{lessonPlan.topic}</h2>
      </div>

      <div style={styles.lessonGrid}>
        {/* Lesson Overview */}
        <div style={styles.lessonSection}>
          <h3 style={styles.sectionTitle}>Lesson Overview</h3>
          <div style={styles.lessonInfo}>
            <div style={styles.infoItem}>
              <span style={styles.infoLabel}>Age Group:</span>
              <span style={styles.infoValue}>{lessonPlan.targetAge}+ years</span>
            </div>
            <div style={styles.infoItem}>
              <span style={styles.infoLabel}>Experience Level:</span>
              <span style={styles.infoValue}>{lessonPlan.experienceLevel}</span>
            </div>
            <div style={styles.infoItem}>
              <span style={styles.infoLabel}>Difficulty:</span>
              <span style={styles.infoValue}>{lessonPlan.difficultyLevel}</span>
            </div>
            <div style={styles.infoItem}>
              <span style={styles.infoLabel}>Duration:</span>
              <span style={styles.infoValue}>{formatDuration(lessonPlan.estimatedDuration)}</span>
            </div>
          </div>
        </div>

        {/* Vocabulary */}
        <div style={styles.lessonSection}>
          <h3 style={styles.sectionTitle}>Vocabulary Words</h3>
          <div style={styles.vocabularyGrid}>
            {lessonPlan.vocabularyWords.map((word, index) => (
              <div key={index} style={styles.vocabularyItem}>
                {word}
              </div>
            ))}
          </div>
          <div style={styles.vocabularyStats}>
            <span style={styles.statBadge}>{lessonPlan.totalVocabulary} words</span>
            <span style={styles.statBadge}>{lessonPlan.videosFound} videos found</span>
          </div>
        </div>

        {/* Objectives */}
        <div style={styles.lessonSection}>
          <h3 style={styles.sectionTitle}>Learning Objectives</h3>
          <ul style={styles.objectiveList}>
            {lessonPlan.objectives.map((objective, index) => (
              <li key={index} style={styles.objectiveItem}>
                {objective}
              </li>
            ))}
          </ul>
        </div>

        {/* Grammar Focus */}
        <div style={styles.lessonSection}>
          <h3 style={styles.sectionTitle}>Grammar Focus</h3>
          <ul style={styles.grammarList}>
            {lessonPlan.grammarFocus.map((grammar, index) => (
              <li key={index} style={styles.grammarItem}>
                {grammar}
              </li>
            ))}
          </ul>
        </div>

        {/* Practice Activities */}
        <div style={styles.lessonSection}>
          <h3 style={styles.sectionTitle}>Practice Activities</h3>
          <ul style={styles.activityList}>
            {lessonPlan.practiceActivities.map((activity, index) => (
              <li key={index} style={styles.activityItem}>
                {activity}
              </li>
            ))}
          </ul>
        </div>

        {/* Cultural Notes */}
        <div style={styles.lessonSection}>
          <h3 style={styles.sectionTitle}>Cultural Notes</h3>
          <div style={styles.culturalNotes}>
            {lessonPlan.culturalNotes}
          </div>
        </div>

        {/* Videos */}
        {lessonPlan.videos && lessonPlan.videos.length > 0 && (
          <div style={styles.lessonSection}>
            <h3 style={styles.sectionTitle}>Learning Videos</h3>
            <div style={styles.videoGrid}>
              {lessonPlan.videos.map((video, index) => (
                <div key={index} style={styles.videoCard}>
                  <div style={styles.videoHeader}>
                    <h4 style={styles.videoTitle}>{video.vocabulary_word}</h4>
                    {video.similarity_score && (
                      <span style={styles.similarityScore}>
                        {(video.similarity_score * 100).toFixed(1)}% match
                      </span>
                    )}
                  </div>
                  
                  {video.embed_url ? (
                    <div style={styles.videoWrapper}>
                      <iframe
                        src={video.embed_url}
                        title={video.title}
                        style={styles.videoIframe}
                        allowFullScreen
                      />
                    </div>
                  ) : (
                    <div style={styles.noVideo}>
                      <span style={styles.noVideoText}>No video available for "{video.vocabulary_word}"</span>
                    </div>
                  )}
                  
                  <div style={styles.videoFooter}>
                    <span style={styles.videoDuration}>
                      {video.duration ? `${video.duration}s` : 'Duration unknown'}
                    </span>
                    {video.url && (
                      <a
                        href={video.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        style={styles.videoLink}
                      >
                        Watch on YouTube
                      </a>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      <div style={styles.lessonFooter}>
        <div style={styles.lessonMeta}>
          <span style={styles.metaItem}>
            Generated with {lessonPlan.langchainUsed ? 'LangChain AI' : 'Rule-based system'}
          </span>
          <span style={styles.metaItem}>
            {new Date(lessonPlan.generatedAt).toLocaleString()}
          </span>
        </div>
      </div>
    </div>
  );
};

export default LessonPlanDisplay; 