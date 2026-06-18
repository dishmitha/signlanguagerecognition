import cv2
import mediapipe as mp
import joblib
import numpy as np
import pyttsx3

# ==========================
# Text To Speech
# ==========================
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# ==========================
# Load Model
# ==========================
model = joblib.load("sign_model.pkl")
label_encoder = joblib.load("label_encoder.pkl")

# ==========================
# MediaPipe Setup
# ==========================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

# ==========================
# Variables
# ==========================
current_prediction = ""
word = ""
sentence = ""
history = []

# ==========================
# Webcam
# ==========================
cap = cv2.VideoCapture(0)

while True:

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    current_prediction = ""

    # ==========================
    # Hand Detection
    # ==========================
    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            features = []

            for lm in hand_landmarks.landmark:
                features.extend([
                    lm.x,
                    lm.y,
                    lm.z
                ])

            features = np.array(features).reshape(1, -1)

            pred_num = model.predict(features)[0]

            current_prediction = label_encoder.inverse_transform(
                [pred_num]
            )[0]

    # ==========================
    # Keyboard Controls
    # ==========================
    key = cv2.waitKey(1) & 0xFF

    # SPACE -> Add Letter
    if key == 32:

        if current_prediction != "":
            word += current_prediction
            print("Word:", word)

    # ENTER -> Add Word to Sentence + Save History
    elif key == 13:

        if word.strip() != "":

            sentence += word + " "

            history.append(word)

            with open("history.txt", "a") as f:
                f.write(word + "\n")

            print("Sentence:", sentence)

            word = ""

    # BACKSPACE -> Remove Last Letter
    elif key == 8:

        word = word[:-1]

    # C -> Clear Everything
    elif key == ord('c'):

        word = ""
        sentence = ""
        history.clear()

        print("Cleared")

    # S -> Speak Sentence / Word
    elif key == ord('s'):

        text_to_speak = ""

        if sentence.strip() != "":
            text_to_speak = sentence

        elif word.strip() != "":
            text_to_speak = word

        if text_to_speak != "":

            print("Speaking:", text_to_speak)

            engine.stop()
            engine.say(text_to_speak)
            engine.runAndWait()

    # ESC -> Exit
    elif key == 27:
        break

    # ==========================
    # Display Prediction
    # ==========================
    cv2.putText(
        frame,
        f"Prediction: {current_prediction}",
        (10, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    # ==========================
    # Display Current Word
    # ==========================
    cv2.putText(
        frame,
        f"Word: {word}",
        (10, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 0, 0),
        2
    )

    # ==========================
    # Display Sentence
    # ==========================
    cv2.putText(
        frame,
        f"Sentence: {sentence}",
        (10, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 255),
        2
    )

    # ==========================
    # Display History
    # ==========================
    y_pos = 170

    cv2.putText(
        frame,
        "History:",
        (10, y_pos),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 0),
        2
    )

    for item in history[-5:]:

        y_pos += 30

        cv2.putText(
            frame,
            item,
            (10, y_pos),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

    # ==========================
    # Instructions
    # ==========================
    cv2.putText(
        frame,
        "SPACE:Add  ENTER:Save  S:Speak  C:Clear",
        (10, frame.shape[0] - 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (200, 200, 200),
        2
    )

    cv2.imshow(
        "Sign Language Recognition + TTS",
        frame
    )

cap.release()
cv2.destroyAllWindows()