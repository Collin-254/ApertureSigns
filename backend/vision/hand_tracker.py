import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, mode=False, max_hands=2, detection_con=0.5, track_con=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_con = detection_con
        self.track_con = track_con
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=self.mode, max_num_hands=self.max_hands, min_detection_confidence=self.detection_con, min_tracking_confidence=self.track_con)
        self.mp_draw = mp.solutions.drawing_utils

    def process_frame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        extracted_hands = []
        if results.multi_hand_landmarks:
            for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                label = "Unknown"
                if results.multi_handedness:
                    label = results.multi_handedness[hand_idx].classification[0].label
                landmarks = []
                for lm_id, lm in enumerate(hand_landmarks.landmark):
                    landmarks.append({"id": lm_id, "x": round(lm.x, 4), "y": round(lm.y, 4), "z": round(lm.z, 4)})
                extracted_hands.append({"hand": label, "keypoint_count": len(landmarks), "landmarks": landmarks})
        return extracted_hands, results
