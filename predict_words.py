import cv2
import mediapipe as mp
import joblib
import numpy as np

# Load model and label encoder
model = joblib.load("word_model.pkl")
label_encoder = joblib.load("word_label_encoder.pkl")
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    predicted_letter = ""

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

            # Get probabilities
            probs = model.predict_proba(features)[0]

            # Top 5 predictions
            top5 = np.argsort(probs)[-5:][::-1]

            print("\nTop Predictions:")
            for idx in top5:
                letter = label_encoder.inverse_transform([idx])[0]
                print(f"{letter}: {probs[idx] * 100:.2f}%")

            # Best prediction
            print(features[0][:10])
            pred_num = np.argmax(probs)
            predicted_letter = label_encoder.inverse_transform(
                [pred_num]
            )[0]

    cv2.putText(
        frame,
        f"Prediction: {predicted_letter}",
        (10, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        (0, 255, 0),
        3
    )

    cv2.imshow("Sign Language Recognition", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()