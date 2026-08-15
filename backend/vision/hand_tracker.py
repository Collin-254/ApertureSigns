import cv2
import mediapipe as mp


class HandTracker:
    def __init__(self, mode=False, max_hands=2, detection_con=0.5, track_con=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_con = detection_con
        self.track_con = track_con

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_con,
            min_tracking_confidence=self.track_con,
        )

        self.mp_draw = mp.solutions.drawing_utils

    def process_frame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        extracted_hands = []

        if results.multi_hand_landmarks:
            for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                label = "Unknown"

                if results.multi_handedness:
                    label = results.multi_handedness[
                        hand_idx
                    ].classification[0].label

                landmarks = []

                for lm_id, lm in enumerate(hand_landmarks.landmark):
                    landmarks.append({
                        "id": lm_id,
                        "x": round(lm.x, 4),
                        "y": round(lm.y, 4),
                        "z": round(lm.z, 4),
                    })

                extracted_hands.append({
                    "hand": label,
                    "keypoint_count": len(landmarks),
                    "landmarks": landmarks,
                })

        return extracted_hands, results


if __name__ == "__main__":
    tracker = HandTracker()
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("ERROR: Could not open camera.")
        exit()

    print("Camera started.")
    print("Show your hand to the camera.")
    print("Press Q to quit.")

    while True:
        success, frame = camera.read()

        if not success:
            print("ERROR: Could not read camera frame.")
            break

        detected_hands, results = tracker.process_frame(frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                tracker.mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    tracker.mp_hands.HAND_CONNECTIONS,
                )

        y_position = 30

        for hand in detected_hands:
            text = f"{hand['hand']} hand | {hand['keypoint_count']} points"

            cv2.putText(
                frame,
                text,
                (10, y_position),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2,
            )

            y_position += 30

        cv2.imshow(
            "Aperture Signs - Hand Tracking Test",
            frame,
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()
