import { useState } from 'react';
import axios from 'axios';
import { isValidInput } from '../utils/helpers';

const API_BASE_URL = 'http://localhost:8000';

const useASLApi = () => {
  const [videos, setVideos] = useState([]);
  const [searchInfo, setSearchInfo] = useState(null);
  const [lessonPlan, setLessonPlan] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');


  const resetState = () => {
    setVideos([]);
    setLessonPlan(null);
    setSearchInfo(null);
    setError('');

  };

  const handleApiError = (error, defaultMessage) => {
    console.error('API Error:', error);
    setError(error.response?.data?.message || defaultMessage);
  };

  const translateText = async (text, options = {}) => {
    if (!isValidInput(text)) return;
    
    setLoading(true);
    resetState();
    
    try {
      const startTime = Date.now();
      const response = await axios.post(`${API_BASE_URL}/text-to-asl`, {
        text: text.trim(),
        fast_mode: true  // Use fast mode for better performance
      });
      const endTime = Date.now();
      
      const { 
        video_sequence, 
        search_strategy, 
        phrase_similarity, 
        word_avg_similarity, 
        asl_enhancement,
        response_time_ms,
        found_videos,
        total_videos
      } = response.data;
      
      setVideos(video_sequence);
      setSearchInfo({
        strategy: search_strategy,
        phrase_similarity,
        word_avg_similarity,
        asl_enhancement: asl_enhancement || null,
        found_videos,
        total_videos
      });
      

    } catch (error) {
      handleApiError(error, 'Failed to translate text. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const generateLesson = async (text, options = {}) => {
    if (!isValidInput(text)) return;
    
    setLoading(true);
    resetState();
    
    try {
      const startTime = Date.now();
      const response = await axios.post(`${API_BASE_URL}/generate-lesson`, {
        prompt: text.trim(),
        age: options.age || 25,
        experience: options.experience || 'beginner',
        quick_mode: options.quickMode || false,
        ultra_fast: options.ultraFast || false
      });
      const endTime = Date.now();
      
      const {
        lesson_topic,
        target_age,
        experience_level,
        vocabulary_words,
        lesson_objectives,
        grammar_focus,
        practice_activities,
        cultural_notes,
        difficulty_level,
        estimated_duration,
        lesson_videos,
        total_vocabulary,
        videos_found,
        generated_at,
        langchain_used,
        response_time_ms
      } = response.data;
      
      setLessonPlan({
        topic: lesson_topic,
        targetAge: target_age,
        experienceLevel: experience_level,
        vocabularyWords: vocabulary_words,
        objectives: lesson_objectives,
        grammarFocus: grammar_focus,
        practiceActivities: practice_activities,
        culturalNotes: cultural_notes,
        difficultyLevel: difficulty_level,
        estimatedDuration: estimated_duration,
        videos: lesson_videos,
        totalVocabulary: total_vocabulary,
        videosFound: videos_found,
        generatedAt: generated_at,
        langchainUsed: langchain_used
      });
      

    } catch (error) {
      handleApiError(error, 'Failed to generate lesson plan. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return {
    videos,
    searchInfo,
    lessonPlan,
    loading,
    error,
    translateText,
    generateLesson
  };
};

export default useASLApi; 