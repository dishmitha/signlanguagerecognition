import { useState, useEffect, useRef } from "react";
import Webcam from "react-webcam";
import axios from "axios";
import { Volume2, Save, Trash2 } from "lucide-react";
import "./App.css";

interface HistoryItem {
  id: string;
  time: string;
  text: string;
}

function App() {
  const webcamRef = useRef<Webcam>(null);

  const [prediction, setPrediction] = useState("Waiting...");
  const [currentWord, setCurrentWord] = useState("");
  const [currentSentence, setCurrentSentence] = useState("");
  const [isActive, setIsActive] = useState(false);

  const [history, setHistory] = useState<HistoryItem[]>([]);

  const captureAndPredict = async () => {
    if (!webcamRef.current) return;

    const imageSrc = webcamRef.current.getScreenshot();

    if (!imageSrc) return;

    const blob = await fetch(imageSrc).then((r) => r.blob());

    const formData = new FormData();
    formData.append("file", blob, "frame.jpg");

    try {
      const response = await axios.post(
  "https://signlanguagerecognition-1cpd.onrender.com/predict",
  formData
);

      const letter = response.data.prediction;

      if (letter) {
        setPrediction(letter);
        setCurrentWord(letter);

        setIsActive(true);

        setTimeout(() => {
          setIsActive(false);
        }, 500);
      }
    } catch (error) {
      console.error("Prediction Error:", error);
    }
  };

  useEffect(() => {
    const interval = setInterval(() => {
      captureAndPredict();
    }, 800);

    return () => clearInterval(interval);
  }, []);

  const handleSpeak = () => {
    if (!currentSentence) return;

    const speech = new SpeechSynthesisUtterance(currentSentence);
    speech.lang = "en-US";
    window.speechSynthesis.speak(speech);
  };

  const handleSave = () => {
    if (!currentSentence) return;

    const newItem: HistoryItem = {
      id: Date.now().toString(),
      time: new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
      text: currentSentence,
    };

    setHistory((prev) => [newItem, ...prev]);
  };

  const handleClear = () => {
    setCurrentWord("");
    setCurrentSentence("");
    setPrediction("Waiting...");
  };
  const handleAddLetter = () => {
  if (prediction && prediction !== "Waiting...") {
    setCurrentSentence((prev) => prev + prediction);
  }
};

const handleSpace = () => {
  setCurrentSentence((prev) => prev + " ");
};

  return (
    <div className="app-wrapper">
      <div className="bg-particles"></div>

      <div className="bubbles">
        {[...Array(15)].map((_, i) => (
          <div
            key={i}
            className="bubble"
            style={{
              left: `${Math.random() * 100}%`,
              width: `${Math.random() * 30 + 10}px`,
              height: `${Math.random() * 30 + 10}px`,
              animationDuration: `${Math.random() * 10 + 5}s`,
              animationDelay: `${Math.random() * 5}s`,
            }}
          />
        ))}
      </div>

      <div className="ocean-waves">
        <div className="wave"></div>
        <div className="wave"></div>
      </div>

      <div className="app-container">

        {/* LEFT SIDE */}
        <div className="webcam-section">

          <div className="webcam-header">
            <h2>🌊 Sign Language Recognition</h2>

            <div className="status-indicator">
              <div className="status-dot"></div>
              <span>Camera Active</span>
            </div>
          </div>

          <div className="webcam-feed">
            <Webcam
              ref={webcamRef}
              audio={false}
              mirrored={true}
              screenshotFormat="image/jpeg"
              videoConstraints={{
                facingMode: "user",
              }}
              style={{
                width: "100%",
                height: "100%",
                objectFit: "cover",
                borderRadius: "20px",
              }}
            />
          </div>

        </div>

        {/* RIGHT SIDE */}
        <div className="side-panel">

          <div
            className={`glass-card prediction-card ${
              isActive ? "active" : ""
            }`}
          >
            <h3 className="card-title">Live Prediction</h3>

            <div className="prediction-text">
              {prediction}
            </div>
          </div>

          <div className="glass-card word-card">
            <h3 className="card-title">Current Word</h3>

            <div className="word-text">
              {currentWord}
            </div>
          </div>

          <div className="glass-card sentence-card">
            <h3 className="card-title">Current Sentence</h3>

            <div className="sentence-text">
              {currentSentence || "No sentence yet"}
            </div>

            <div className="button-group">

  <button
    className="btn btn-save"
    onClick={handleAddLetter}
  >
    Add Letter
  </button>

  <button
    className="btn btn-save"
    onClick={handleSpace}
  >
    Space
  </button>

  <button
    className="btn btn-speak"
    onClick={handleSpeak}
  >
    <Volume2 size={20} />
    Speak
  </button>

  <button
    className="btn btn-save"
    onClick={handleSave}
  >
    <Save size={20} />
    Save
  </button>

  <button
    className="btn btn-clear"
    onClick={handleClear}
  >
    <Trash2 size={20} />
    Clear
  </button>

</div>
</div>

          <div className="glass-card history-panel">
            <h3 className="card-title">
              Translation History
            </h3>

            <div className="history-list">
              {history.map((item) => (
                <div
                  className="history-item"
                  key={item.id}
                >
                  <span className="history-time">
                    {item.time}
                  </span>

                  <span className="history-text">
                    {item.text}
                  </span>
                </div>
              ))}
            </div>
          </div>

        </div>

      </div>
    </div>
  );
}

export default App;