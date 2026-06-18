import cv2
import mediapipe as mp
import pandas as pd
import os

WORD = "SORRY"
SAMPLES = 100

csv_file = "word_data.csv"

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

data = []

count = 0

print(f"Collecting {WORD} samples...")

while True:
    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:

        hand = results.multi_hand_landmarks[0]

        features = []

        for lm in hand.landmark:
            features.extend([
                lm.x,
                lm.y,
                lm.z
            ])

        cv2.putText(
            frame,
            f"{WORD}: {count}/{SAMPLES}",
            (10, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,255,0),
            2
        )

        key = cv2.waitKey(1)

        if key == ord('s'):

            features.append(WORD)
            data.append(features)

            count += 1

            print(f"Saved {count}")

            if count >= SAMPLES:
                break

    cv2.imshow("Collect HELLO", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

df = pd.DataFrame(data)

if os.path.exists(csv_file):
    old = pd.read_csv(csv_file, header=None)
    df = pd.concat([old, df], ignore_index=True)

df.to_csv(csv_file, header=False, index=False)

print("HELLO dataset saved!")