import React, { useState } from "react";
import axios from "axios";

const ASLTranslator = () => {
  const [text, setText] = useState("");
  const [videos, setVideos] = useState([]);
  const [lessonPlan, setLessonPlan] = useState([]);

  const handleTranslate = async () => {
    try {
      const response = await axios.post("http://localhost:8000/text-to-asl", {
        text: text,
      });
      setVideos(response.data.video_sequence);
    } catch (error) {
      console.error("Error translating text to ASL:", error);
    }
  };

  const handleGenerateLesson = async () => {
    try {
      const response = await axios.post("http://localhost:8000/generate-lesson", {
        prompt: text,
      });
      setLessonPlan(response.data.lesson_plan);
    } catch (error) {
      console.error("Error generating lesson plan:", error);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>ASL Translator & Lesson Planner</h2>
      <input
        type="text"
        value={text}
        placeholder="Type your lesson request here..."
        onChange={(e) => setText(e.target.value)}
        style={{ padding: "8px", width: "60%" }}
      />
      <button onClick={handleTranslate} style={{ marginLeft: "10px", padding: "8px 16px" }}>
        Translate Text to ASL Videos
      </button>
      <button onClick={handleGenerateLesson} style={{ marginLeft: "10px", padding: "8px 16px" }}>
        Generate Lesson Plan
      </button>

      <div style={{ marginTop: "30px" }}>
        <h3>Video Results:</h3>
        {videos.map((item, index) => (
          <div key={index} style={{ marginBottom: "20px" }}>
            <h4>{item.word}</h4>
            {item.video_url ? (
              <iframe
                width="500"
                height="250"
                src={item.video_url.replace("watch?v=", "embed/")}
                title={`ASL sign ${index}`}
                frameBorder="0"
                allowFullScreen
              ></iframe>
            ) : (
              <p>No video available for this word.</p>
            )}
          </div>
        ))}

        {lessonPlan.length > 0 && (
          <div style={{ marginTop: "30px" }}>
            <h3>Generated Lesson Plan:</h3>
            {lessonPlan.map((item, index) => (
              <div key={index} style={{ marginBottom: "20px" }}>
                <h4>{item.word}</h4>
                {item.video_url ? (
                  <iframe
                    width="500"
                    height="250"
                    src={item.video_url.replace("watch?v=", "embed/")}
                    title={`ASL sign ${item.word}`}
                    frameBorder="0"
                    allowFullScreen
                  ></iframe>
                ) : (
                  <p>No video available for this word.</p>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ASLTranslator;


