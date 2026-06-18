from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import cv2
import mediapipe as mp
import numpy as np
import joblib

# Load model
model = joblib.load("sign_model.pkl")
label_encoder = joblib.load("label_encoder.pkl")

# MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    min_detection_confidence=0.7
)

app = FastAPI()

# Allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Sign Language API Running"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    image_bytes = await file.read()

    npimg = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    if not results.multi_hand_landmarks:
        return {"prediction": ""}

    hand_landmarks = results.multi_hand_landmarks[0]

    features = []

    for lm in hand_landmarks.landmark:
        features.extend([
            lm.x,
            lm.y,
            lm.z
        ])

    features = np.array(features).reshape(1, -1)

    pred_num = model.predict(features)[0]

    prediction = label_encoder.inverse_transform(
        [pred_num]
    )[0]

    return {
        "prediction": prediction
    }