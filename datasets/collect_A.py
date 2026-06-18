import cv2
import mediapipe as mp
import csv

# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

sample_count = 0

with open("A.csv", "a", newline="") as file:
    writer = csv.writer(file)

    while True:
        success, frame = cap.read()

        if not success:
            break

        frame = cv2.flip(frame, 1)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:

                # Draw landmarks
                mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )

                # Store 63 values (21 landmarks × x,y,z)
                row = []

                for lm in hand_landmarks.landmark:
                    row.extend([lm.x, lm.y, lm.z])

                # Add label
                row.append("A")

                # Press S to save
                key = cv2.waitKey(1)

                if key == ord('s'):
                    writer.writerow(row)
                    sample_count += 1
                    print(f"Saved sample {sample_count}")

        cv2.putText(
            frame,
            f"Samples: {sample_count}",
            (10, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.imshow("Collect A Data", frame)

        if cv2.waitKey(1) & 0xFF == 27:  # ESC
            break

cap.release()
cv2.destroyAllWindows()