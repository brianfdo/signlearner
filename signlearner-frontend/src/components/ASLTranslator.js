import React from 'react';
import Header from './common/Header';
import SearchForm from './SearchForm';
import LoadingSpinner from './common/LoadingSpinner';
import ErrorMessage from './common/ErrorMessage';
import SearchInfo from './SearchInfo';
import VideoGrid from './VideoGrid';
import LessonPlanDisplay from './LessonPlanDisplay';
import useASLApi from '../hooks/useASLApi';
import styles from '../styles/ASLTranslator.styles';

const ASLTranslator = () => {
  const {
    videos,
    searchInfo,
    lessonPlan,
    loading,
    error,
    translateText,
    generateLesson
  } = useASLApi();

  return (
    <div style={styles.container}>
      <div style={styles.innerContainer}>
        <Header 
          title="SignLearner"
          subtitle="Discover American Sign Language through interactive videos"
        />
        
        <SearchForm 
          onTranslate={translateText}
          onGenerateLesson={generateLesson}
          loading={loading}
        />
        
        <ErrorMessage error={error} />
        
        {loading && <LoadingSpinner />}
        
        <SearchInfo searchInfo={searchInfo} />
        

        
        <VideoGrid 
          videos={videos}
          title="ASL Translation Results"
          isLesson={false}
        />
        
        <LessonPlanDisplay 
          lessonPlan={lessonPlan}
        />
      </div>
    </div>
  );
};

export default ASLTranslator;


