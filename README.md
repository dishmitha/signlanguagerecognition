# 🌊 Sign Language Recognition System

A real-time Sign Language Recognition web application that converts hand gestures into text and speech using Machine Learning, MediaPipe, FastAPI, and React.

## 🚀 Live Demo

### Frontend (Vercel)

https://signlanguagerecognition-l1rc2y74o-dishmithas-projects.vercel.app/

### Backend API (Render)

https://signlanguagerecognition-1cpd.onrender.com/

---

## 📌 Project Overview

This project helps bridge communication gaps by recognizing sign language hand gestures through a webcam and translating them into text in real time.

The system uses MediaPipe for hand landmark detection and a Machine Learning model trained on sign language gesture data. The recognized letters can be combined into words and sentences, spoken aloud using Text-to-Speech, and saved in translation history.

---

## ✨ Features

* Real-time webcam-based sign recognition
* Hand landmark detection using MediaPipe
* Machine Learning-based gesture classification
* Live prediction display
* Add Letter functionality
* Space insertion for sentence formation
* Text-to-Speech conversion
* Save translation history
* Clear sentence functionality
* Responsive and modern UI
* Cloud deployment using Vercel and Render

---

## 🛠️ Technologies Used

### Frontend

* React
* TypeScript
* Vite
* Axios
* React Webcam
* Lucide React
* CSS

### Backend

* FastAPI
* Python
* MediaPipe
* OpenCV
* NumPy
* Scikit-Learn
* Joblib

### Deployment

* Vercel (Frontend)
* Render (Backend)

---

## 🏗️ System Architecture

User Webcam
↓
React Frontend
↓
Axios API Requests
↓
FastAPI Backend
↓
MediaPipe Hand Detection
↓
Machine Learning Model
↓
Predicted Letter
↓
Text / Speech Output

---

## 📂 Project Structure

```text
signlanguagerecognition/
│
├── frontend/
│   ├── src/
│   ├── App.tsx
│   ├── App.css
│   ├── package.json
│   └── ...
│
├── backend/
│   ├── main.py
│   ├── sign_model.pkl
│   ├── label_encoder.pkl
│   ├── requirements.txt
│   └── ...
│
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/dishmitha/signlanguagerecognition.git
```

---

### Backend Setup

```bash
cd backend

pip install -r requirements.txt

uvicorn main:app --reload
```

Backend will run at:

```text
http://127.0.0.1:8000
```

---

### Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend will run at:

```text
http://localhost:5173
```

---

## 🎯 How It Works

1. Webcam captures live hand gestures.
2. Image frames are sent to the FastAPI backend.
3. MediaPipe extracts hand landmarks.
4. The trained ML model predicts the corresponding sign language letter.
5. The predicted letter is displayed on the frontend.
6. Users can:

   * Add letters
   * Insert spaces
   * Form sentences
   * Convert text to speech
   * Save translation history

---

## 📈 Future Enhancements

* Complete ASL word recognition
* Sentence prediction
* Confidence score display
* Multi-hand gesture support
* Local storage for history
* User authentication
* Mobile application version

---

## 👩‍💻 Author

**Dishmitha**



---

## 📜 License

This project is developed for educational and learning purposes.
