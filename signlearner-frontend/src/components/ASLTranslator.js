import React, { useState } from "react";
import axios from "axios";

const ASLTranslator = () => {
  const [text, setText] = useState("");
  const [videos, setVideos] = useState([]);
  const [lessonPlan, setLessonPlan] = useState([]);
  const [searchResults, setSearchResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleTranslate = async () => {
    if (!text.trim()) return;
    
    setLoading(true);
    setError("");
    try {
      const response = await axios.post("http://localhost:8000/text-to-asl", {
        text: text,
      });
      setVideos(response.data.video_sequence);
    } catch (error) {
      console.error("Error translating text to ASL:", error);
      setError("Failed to translate text. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleSearchVideos = async () => {
    if (!text.trim()) return;
    
    setLoading(true);
    setError("");
    try {
      const response = await axios.post("http://localhost:8000/search-videos", {
        query: text,
        limit: 6
      });
      setSearchResults(response.data.results);
    } catch (error) {
      console.error("Error searching videos:", error);
      setError("Failed to search videos. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateLesson = async () => {
    if (!text.trim()) return;
    
    setLoading(true);
    setError("");
    try {
      const response = await axios.post("http://localhost:8000/generate-lesson", {
        prompt: text,
        age: 5,
        experience: "beginner"
      });
      setLessonPlan(response.data.lesson_plan);
    } catch (error) {
      console.error("Error generating lesson plan:", error);
      setError("Failed to generate lesson plan. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const containerStyle = {
    padding: "20px",
    fontFamily: "Arial, sans-serif",
    maxWidth: "1200px",
    margin: "0 auto",
    backgroundColor: "#f0f8ff"
  };

  const headerStyle = {
    textAlign: "center",
    color: "#2c3e50",
    fontSize: "2.5em",
    marginBottom: "30px",
    textShadow: "2px 2px 4px rgba(0,0,0,0.1)"
  };

  const inputStyle = {
    padding: "12px",
    fontSize: "16px",
    border: "2px solid #3498db",
    borderRadius: "10px",
    width: "60%",
    marginBottom: "20px",
    outline: "none"
  };

  const buttonStyle = {
    padding: "12px 24px",
    fontSize: "16px",
    backgroundColor: "#3498db",
    color: "white",
    border: "none",
    borderRadius: "10px",
    cursor: "pointer",
    margin: "5px",
    transition: "background-color 0.3s"
  };

  const buttonHoverStyle = {
    backgroundColor: "#2980b9"
  };

  const videoCardStyle = {
    backgroundColor: "white",
    border: "2px solid #e74c3c",
    borderRadius: "15px",
    padding: "20px",
    margin: "15px 0",
    boxShadow: "0 4px 8px rgba(0,0,0,0.1)"
  };

  const videoTitleStyle = {
    color: "#e74c3c",
    fontSize: "1.2em",
    fontWeight: "bold",
    marginBottom: "10px"
  };

  const errorStyle = {
    color: "#e74c3c",
    backgroundColor: "#fadbd8",
    padding: "10px",
    borderRadius: "5px",
    margin: "10px 0"
  };

  const loadingStyle = {
    color: "#3498db",
    fontSize: "1.1em",
    textAlign: "center",
    margin: "20px 0"
  };

  return (
    <div style={containerStyle}>
      <h2 style={headerStyle}>🤟 ASL Learning Assistant for Kids 🤟</h2>
      
      <div style={{textAlign: "center", marginBottom: "30px"}}>
        <input
          type="text"
          value={text}
          placeholder="Type what you want to learn in ASL..."
          onChange={(e) => setText(e.target.value)}
          style={inputStyle}
          onKeyPress={(e) => e.key === 'Enter' && handleTranslate()}
        />
        <br />
        <button 
          onClick={handleTranslate} 
          style={buttonStyle}
          onMouseOver={(e) => e.target.style.backgroundColor = buttonHoverStyle.backgroundColor}
          onMouseOut={(e) => e.target.style.backgroundColor = buttonStyle.backgroundColor}
        >
          🎬 Translate to ASL Videos
        </button>
        <button 
          onClick={handleSearchVideos} 
          style={buttonStyle}
          onMouseOver={(e) => e.target.style.backgroundColor = buttonHoverStyle.backgroundColor}
          onMouseOut={(e) => e.target.style.backgroundColor = buttonStyle.backgroundColor}
        >
          🔍 Search ASL Videos
        </button>
        <button 
          onClick={handleGenerateLesson} 
          style={buttonStyle}
          onMouseOver={(e) => e.target.style.backgroundColor = buttonHoverStyle.backgroundColor}
          onMouseOut={(e) => e.target.style.backgroundColor = buttonStyle.backgroundColor}
        >
          📚 Generate Lesson Plan
        </button>
      </div>

      {loading && <div style={loadingStyle}>🔄 Loading awesome ASL videos for you...</div>}
      {error && <div style={errorStyle}>❌ {error}</div>}

      {/* Text-to-ASL Results */}
      {videos.length > 0 && (
        <div style={{marginTop: "30px"}}>
          <h3 style={{color: "#2c3e50", fontSize: "1.5em"}}>📝 Text Translation Results:</h3>
          {videos.map((item, index) => (
            <div key={index} style={videoCardStyle}>
              <h4 style={videoTitleStyle}>
                Word: "{item.word}" 
                <span style={{fontSize: "0.8em", color: "#7f8c8d", marginLeft: "10px"}}>
                  ({item.source === "hardcoded" ? "📚 Built-in" : item.source === "rag_search" ? "🔍 Found by AI" : "❌ Not found"})
                </span>
              </h4>
              {item.video_url ? (
                <div>
                  {item.video_title && <p style={{color: "#7f8c8d", fontSize: "0.9em"}}>Video: {item.video_title}</p>}
                  <iframe
                    width="500"
                    height="280"
                    src={item.video_url}
                    title={`ASL sign for ${item.word}`}
                    frameBorder="0"
                    allowFullScreen
                    style={{borderRadius: "10px"}}
                  ></iframe>
                </div>
              ) : (
                <p style={{color: "#e74c3c", fontSize: "1.1em"}}>
                  😔 No video available for "{item.word}". Try searching for similar words!
                </p>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Search Results */}
      {searchResults.length > 0 && (
        <div style={{marginTop: "30px"}}>
          <h3 style={{color: "#2c3e50", fontSize: "1.5em"}}>🔍 Search Results:</h3>
          <div style={{display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(400px, 1fr))", gap: "20px"}}>
            {searchResults.map((item, index) => (
              <div key={index} style={videoCardStyle}>
                <h4 style={videoTitleStyle}>{item.title}</h4>
                <p style={{color: "#7f8c8d", fontSize: "0.9em"}}>
                  Duration: {item.duration}s | Similarity: {(item.similarity_score * 100).toFixed(1)}%
                </p>
                <iframe
                  width="100%"
                  height="250"
                  src={item.embed_url}
                  title={`ASL sign: ${item.title}`}
                  frameBorder="0"
                  allowFullScreen
                  style={{borderRadius: "10px"}}
                ></iframe>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Lesson Plan Results */}
      {lessonPlan.length > 0 && (
        <div style={{marginTop: "30px"}}>
          <h3 style={{color: "#2c3e50", fontSize: "1.5em"}}>📚 Your Personalized Lesson Plan:</h3>
          <div style={{display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(400px, 1fr))", gap: "20px"}}>
            {lessonPlan.map((item, index) => (
              <div key={index} style={videoCardStyle}>
                <h4 style={videoTitleStyle}>
                  Lesson {index + 1}: {item.keyword}
                </h4>
                {item.video_id ? (
                  <div>
                    <p style={{color: "#7f8c8d", fontSize: "0.9em"}}>
                      Video: {item.title} | Duration: {item.duration}s
                    </p>
                    <iframe
                      width="100%"
                      height="250"
                      src={item.embed_url}
                      title={`ASL lesson: ${item.keyword}`}
                      frameBorder="0"
                      allowFullScreen
                      style={{borderRadius: "10px"}}
                    ></iframe>
                  </div>
                ) : (
                  <p style={{color: "#e74c3c", fontSize: "1.1em"}}>
                    😔 No video found for "{item.keyword}". Try searching for similar words!
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ASLTranslator;


