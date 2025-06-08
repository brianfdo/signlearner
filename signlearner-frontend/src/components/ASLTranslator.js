import React, { useState } from "react";
import axios from "axios";

const ASLTranslator = () => {
  const [text, setText] = useState("");
  const [videos, setVideos] = useState([]);

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

  return (
    <div style={{ padding: "20px" }}>
      <h2>ASL Translator</h2>
      <input
        type="text"
        value={text}
        placeholder="Type text here..."
        onChange={(e) => setText(e.target.value)}
        style={{ padding: "8px", width: "60%" }}
      />
      <button onClick={handleTranslate} style={{ marginLeft: "10px", padding: "8px 16px" }}>
        Translate
      </button>

      <div style={{ marginTop: "30px" }}>
        {videos.map((videoUrl, index) => (
          <div key={index} style={{ marginBottom: "20px" }}>
            <iframe
              width="500"
              height="250"
              src={videoUrl.replace("watch?v=", "embed/")}
              title={`ASL sign ${index}`}
              frameBorder="0"
              allowFullScreen
            ></iframe>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ASLTranslator;

