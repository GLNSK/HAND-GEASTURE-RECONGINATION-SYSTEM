import cv2
import mediapipe as mp

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

tip_ids = [4, 8, 12, 16, 20]


def get_finger_states(hand_landmarks, hand_label):
    fingers = []

    # Thumb
    if hand_label == "Right":
        fingers.append(
            hand_landmarks.landmark[4].x <
            hand_landmarks.landmark[3].x
        )
    else:
        fingers.append(
            hand_landmarks.landmark[4].x >
            hand_landmarks.landmark[3].x
        )

    # Other fingers
    for tip in tip_ids[1:]:
        fingers.append(
            hand_landmarks.landmark[tip].y <
            hand_landmarks.landmark[tip - 2].y
        )

    return fingers


def recognize_gesture(fingers):

    if fingers == [True, True, True, True, True]:
        return "Open Hand"

    elif fingers == [False, False, False, False, False]:
        return "Fist"

    elif fingers == [True, False, False, False, False]:
        return "Thumbs Up"

    elif fingers == [False, True, True, False, False]:
        return "Peace"

    elif fingers == [False, True, False, False, False]:
        return "Pointing"

    elif fingers == [True, True, False, False, False]:
        return "Gun"

    elif fingers == [False, False, False, False, True]:
        return "Pinky"

    elif fingers == [True, False, False, False, True]:
        return "Rock"

    return "Unknown"


cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open webcam")
    exit()

print("Hand Gesture Recognition Started")
print("Press Q to Exit")

while True:

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    gesture = "No Hand"

    if results.multi_hand_landmarks:

        for hand_landmarks, handedness in zip(
                results.multi_hand_landmarks,
                results.multi_handedness):

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_draw.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2),
                mp_draw.DrawingSpec(color=(255,0,0), thickness=2)
            )

            label = handedness.classification[0].label

            fingers = get_finger_states(hand_landmarks, label)

            gesture = recognize_gesture(fingers)

    cv2.rectangle(frame, (0, 0), (380, 70), (0, 0, 0), -1)

    cv2.putText(
        frame,
        "Gesture: " + gesture,
        (10, 45),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow("Hand Gesture Recognition System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

hands.close()
cap.release()
cv2.destroyAllWindows()