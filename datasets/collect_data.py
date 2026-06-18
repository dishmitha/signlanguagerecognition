import cv2
import mediapipe as mp
import csv

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

# Open Webcam
cap = cv2.VideoCapture(0)

current_label = "A"
sample_count = 0

with open("sign_data.csv", "a", newline="") as file:
    writer = csv.writer(file)

    while True:
        success, frame = cap.read()

        if not success:
            break

        frame = cv2.flip(frame, 1)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        key = cv2.waitKey(1) & 0xFF

        # Change current letter (A-Z)
        if key != 32 and key != 27:  # Ignore SPACE and ESC
            if 65 <= key <= 90:
                current_label = chr(key)

            elif 97 <= key <= 122:
                current_label = chr(key).upper()

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:

                # Draw hand landmarks
                mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )

                # Extract 63 features
                row = []

                for lm in hand_landmarks.landmark:
                    row.extend([lm.x, lm.y, lm.z])

                # Add label
                row.append(current_label)

                # SPACEBAR saves sample
                if key == 32:
                    writer.writerow(row)
                    sample_count += 1
                    print(f"Saved {current_label} sample {sample_count}")

        # Display current letter
        cv2.putText(
            frame,
            f"Letter: {current_label}",
            (10, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        # Display sample count
        cv2.putText(
            frame,
            f"Samples: {sample_count}",
            (10, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 0, 0),
            2
        )

        cv2.imshow("A-Z Data Collector", frame)

        # ESC to exit
        if key == 27:
            break

cap.release()
cv2.destroyAllWindows()