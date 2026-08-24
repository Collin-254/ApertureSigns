import cv2
import mediapipe as mp
import numpy as np
import time
from collections import deque


class ApertureTracker:
    def __init__(self):
        self.mp_holistic = mp.solutions.holistic
        self.mp_face_mesh = mp.solutions.face_mesh

        self.history = deque(maxlen=60)

        self.holistic = self.mp_holistic.Holistic(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            refine_face_landmarks=True,
            enable_segmentation=False,
            min_detection_confidence=0.35,
            min_tracking_confidence=0.30,
        )

    def process(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb.flags.writeable = False

        results = self.holistic.process(rgb)

        rgb.flags.writeable = True

        data = {
            "face": [],
            "pose": [],
            "left_hand": [],
            "right_hand": [],
        }

        if results.face_landmarks:
            for i, lm in enumerate(results.face_landmarks.landmark):
                data["face"].append({
                    "id": i,
                    "x": float(lm.x),
                    "y": float(lm.y),
                 
  "z": float(lm.z),
                })

        if results.pose_landmarks:
            for i, lm in enumerate(results.pose_landmarks.landmark):
                data["pose"].append({
                    "id": i,
                    "x": float(lm.x),
                    "y": float(lm.y),
                    "z": float(lm.z),
                    "visibility": float(lm.visibility),
                })

        if
    def.left_hand_landmarks:
            for i, lm in enumerate(results.left_hand_landmarks.landmark):
                data["left_hand"].append({
                    "id": i,
                    "x": float(lm.x),
                    "y": float(lm.y),
                    "z": float(lm.z),
                })

        if results.right_hand_landmarks:
            for i, lm in enumerate(results.right_hand_landmarks.landmark):
                data["right_hand"].append({
                    "id": i,
                    "x": float(lm.x),
                    "y": float(lm.y),
                    "z": float(lm.z),
                })

        self.history.append(data)

        return data, results


def xy(points, index, w, h):
    if not points or index >= len(points):
        return None

    p = points[index]

    x = int(np.clip(p["x"], 0, 1) * w)
    y = int(np.clip(p["y"], 0, 1) * h)

    return x, y


def line(canvas, points, a, b, w, h, thickness=2):
    pa = xy(points, a, w, h)
    pb = xy(points, b, w, h)

    if pa and pb:
        cv2.line(
            canvas,
            pa,
            pb,
            (120, 185, 255),
            thickness,
            cv2.LINE_AA,
        )


def dot(canvas, points, index, w, h, radius=4):
    p = xy(points, index, w, h)

    if p:
        cv2.circle(
            canvas,
            p,
            radius + 2,
                      data["right_hand"].append({
                    "id": i,
       cv2.circle(
            canvas,
            p,
            radius,
            (120, 210, 255),
            -1,
            cv2.LINE_AA,
        )


# ---------------------------------------------------------
# HAND SKELETON
# ---------------------------------------------------------

HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (17, 18), (18, 19), (19, 20),
    (0, 17),
]


def draw_hand(canvas, hand, w, h):
    if not hand:
        return

    for a, b in HAND_CONNECTIONS:
        line(canvas,             w, h, 2)

    for i in range(len(hand)):
        dot(canvas, hand, i, w, h, 3)


# ---------------------------------------------------------
# BODY SKELETON
# ---------------------------------------------------------

POSE_CONNECTIONS = [
    # head
    (0, 1), (1, 2), (2, 3), (3, 7),
    (0, 4), (4, 5), (5, 6), (6, 8),

    # shoulders
    (11, 12),

    # left arm
    (11, 13),
    (13, 15),

    # right arm
    (12, 14),
    (14, 16),

    # torso
    (11, 23),
    (12, 24),
    (23, 24),

    # left leg
    (23, 25),
    (25, 27),
    (27, 29),
    (29, 31),

    # right leg
    (24, 26),
    (26, 28),
    (28, 30),
    (30, 32),
]


def draw_body(canvas, pose, left_hand, right_hand, w, h):
        (5,pose:
        return

    # Main pose structure.
    for a, b in POSE_CONNECTIONS:
        line(canvas, pose, a, b, w, h, 3)

    # Neck.
    left_shoulder = xy(pose, 11, w, h)
    right_shoulder = xy(pose, 12, w, h)
    nose = xy(pose, 0, w, h)

    if left_shoulder and right_shoulder:
        neck = (
            (left_shoulder[0] + right_shoulder[0]) // 2,
            (left_shoulder[1] + right_shoulder[1]) // 2,
        )

        cv2.line(
            canvas
POSE_CONNECTIONS = [
    # head
   k[0], neck[1] - 45),
            (120, 185, 255),
            4,
            cv2.LINE_AA,
        )

        if nose:
            cv2.line(
      
    # lefcanvas,
                (neck[0], neck[1] - 45),
                nose,
                (120, 185, 255),
                3,
                cv2.LINE_AA,
            )

    # Body landmarks.
    for i in range(len(pose)):
        dot(canvas, pose, i, w, h, 5)

    # Explicit wrist -> hand connections.
    left_wrist = xy(pose, 15, w, h)
    right_wrist = xy(pose, 16, w, h)

    if left_hand:
        hand_wrist = xy(left_hand, 0, w, h)

        if left_wrist and hand_wrist:
            cv2.line(
                canvas,
                left_wrist,
                hand_wrist,
                (150, 220, 255),
                5,
                cv2.LINE_AA,
            )

        draw_hand(canvas, left_hand, w, h)

    if right_hand:
        hand_wrist = xy(right_hand, 0, w, h)

        if right_wrist and hand_wrist:
            cv2.line(
                canvas,
                right_wrist,
                hand_wrist,
                (150, 220, 255),
                5,
                cv2.LINE_AA,
            )

        draw_hand(canvas, right_hand, w, h)


# ---------------------------------------------------------
# FACE
# ---------------------------------------------------------

FACE_CONNECTIONS = mp.solutions.face_mesh.FACEMESH_CONTOURS


def draw_face(canvas, face, w, h):
    if not face:
        return

    # Full facial contour structure.
    for a, b in FACE_CONNECTIONS:
        line(canvas, face, a, b, w, h, 1)

    # Additional dense facial landmarks.
    # These make cheeks, eyes, eyebrows, nose and mouth visible.
    important = set()

    regions = [
        range(0, 468),
    ]

    # Sample the full mesh intelligently      for region in regions:
        for i in region:
            if i % 3 == 0:
                important.add(i)

    # Always emphasize expression-critical points.
    important.update([
        10, 152, 1, 4,
        33, 133, 362, 263,
        61, 291, 78, 308,
        13, 14,
        70, 63, 105, 66,
        300, 293, 334, 296,
        234, 454,
    ])

    for i in important:
        if i < len(face):
            dot(canvas, face, i, w, h, 2)


# ---------------------------------------------------------
# CAMERA PREVIEW
# ---------------------------------------------------------

def draw_camera_preview(frame, results):
    preview = frame.copy()

    if results.face_landmarks:
        mp.solutions.drawing_utils.draw_landmarks(
            preview,
            results.face_landmarks,
            mp.solutions.face_mesh.FACEMESH_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp.solutions.drawing_styles
            .get_default_face_mesh_contours_style(),
        )

    if results.pose_landmarks:
            if i % 3 ==awing_utils.draw_landmarks(
            preview,
            results.pose_landmarks,
            mp.solutions.holistic.POSE_CONNECTIONS,
            landmark_drawing_spec=mp.solutions.drawing_styles
            .get_default_pose_landmarks_style(),
        )

    if results.left_hand_landmarks:
        mp.so        if i < len(facdraw_landmarks(
            preview,
            results.left_hand_landmarks,
            mp.solutions.holistic.HAND_CONNECTIONS,
        )

    if results.right_hand_landmarks:
        mp.solutions.drawing_utils.draw_landmarks(
            preview,
            results.right_hand_landmarks,
            mp.solutions.holistic.HAND_CONNECTIONS,
        )

    return preview


# ---------------------------------------------------------
# UI
# ---------------------------------------------------------

def rounded_panel(canvas, x, y, w, h, radius=20):
    overlay = canvas.copy()

    cv2.rectangle(
        overlay,
        (x, y),
        (x + w, y + h),
        (20, 2            preview,
            results.pose_lanerlay, 0.82, canvas, 0.18, 0, canvas)

    cv2.rectangle(
        canvas,
        (x, y),
        (x + w, y + h),
        (65, 90, 115),
        1,
    )


def label(canvas, text, x, y, size=0.6, thickness=1):
    cv2.putText(
        canvas,
        text,
        (x, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        size,
        (205, 220, 235),
        thickness,
        cv2.LINE_AA,
    )


def main():
    tracker = ApertureTracker()

    camera = cv2.VideoCapture(0)

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not camera.isOpened():
        print("ERROR: Could not open camera.")
        return

    print("Aperture Signs investor UI started.")
    print("Press Q to quit.")

    previous = time.time()
    fps = 0.0

    while True:
        ok, frame = camera.read()

        if not ok:
            break

        frame = cv2.flip(frame, 1)

        data, results = tracker.process(frame)

        now = time.time()
        dt = now - previous

        if dt > 0:
            fps = 1.0 / dt

        previous = now

        face = data["face"]
        pose = data["pose"]
        left_hand = data["left_hand"]
        right_hand = data["right_hand"]

        # -------------------------------------------------
        # MAIN CANVAS
        # -------------------------------------------------

        W = 1440
        H = 900

        canvas = np.zeros((H, W, 3), dtype=np.uint8)

        # Deep background.
        canvas[:] = (9, 14, 23)

        # Subtle grid.
        for x in range(0, W, 60):
            cv2.line(
                canvas,
                (x, 0),
                (x, H),
                (16, 26, 39),
                1,
            )

        for y in range(0, H, 60):
            cv2.line(
                canvas,
                (0, y),
                (W, y),
                (16, 26, 39),
                1,
            )

        # -------------------------------------------------
        # HEADER
        # -------------------------------------------------

        label(
            canvas,
            "APERTURE",
            42,
            50,
            0.85,
            2,
        )

        label(
            canvas,
            "SIGNS",
            42,
            80,
            0.55,
            1,
        )

        label(
            canvas,
            "REAL-TIME HUMAN MOTION INTELLIGENCE",
            190,
            64,
            0.45,
            1,
        )

        # Live indicator.
        cv2.circle(
            canvas,
            (1250, 52),
            6,
            (90, 220, 160),
            -1,
        )

        label(
            canvas,
            "LIVE",
            1265,
            58,
            0.48,
            1,
        )

        label(
            canvas,
            f"{fps:04.1f} FPS",
            1335,
            58              0.42,
            1,
        )

        # -------------------------------------------------
        # MAIN SKELETON PANEL
        # -------------------------------------------------

        panel_x = 360
        panel_y = 105
        panel_w = 1035
        panel            0.    rounded_panel(
            canvas,
            panel_x,
            panel_y,
            panel_w,
            panel_h,
        )

        label(
            canvas,
            "LIVE HUMAN SKELETON",
            panel_x + 25,
            panel_y + 35,
            0.48,
            1,
        )

        label(
            canvas,
            "SPATIAL LANDMARK MAP",
            panel_x + panel_w - 190,
            panel_y + 35,
            0.40,
            1,
        )

        # Skeleton region.
        sx = panel_x + 25
        sy = panel_y + 55
        sw = panel_w - 50
        sh = panel_h - 90

        skeleton = np.zeros((sh, sw, 3), dtype=np.uint8)
        skeleton[:] = (12, 18, 28)

        # soft center glow
        cv2.ellipse(
            skeleton,
            (sw // 2, sh // 2),
            (270, 310),
            0,
            0,
            360,
            (18, 30, 45),
            -1,
        )

        draw_body(
            skeleton,
            pose,
            left_hand,
            right_hand,
            sw,
            sh,
        )

        draw_face(
            skeleton,
            face,
            sw,
            sh,
        )

        canvas[
            sy:sy + sh,
            sx:sx + sw,
        ] = skeleton

        # -------------------------------------------------
        # CAMERA CARD
        # -------------------------------------------------

        cam_x = 35
        cam_y = 555
        cam_w = 290
        cam_h = 235

        rounded_panel(
            canvas,
            cam_x,
            cam_y,
            cam_w,
            cam_h,
        )

        label(
            canvas,
            "CAMERA",
            cam_x + 15,
            cam_y + 25,
            0.45,
                        skeleto   preview = draw_camera_preview(frame, results)

        preview = cv2.resize(
            preview,
            (cam_w - 20, cam_h - 55),
        )

        canvas[
            cam_y + 38:cam_y + 38 + preview.shape[0],
            cam_x + 10:cam_x + 10 + preview.shape[1],
        ] = preview

        # -------------------------------------------------
        # SIGN STATUS
        # -------------------------------------------------

        status_x = 35
        status_y = 105

        rounded_panel(
            canvas,
            status_x,
            status_y,
            290,
            200,
        )

        label(
            canvas,
            "RECOGNITION",
            status_x + 15,
            status_y + 30,
            0.45,
            1,
        )

        label(
            canvas,
            "SIGN",
            status_x + 15,
            status_y + 75,
            0.38,
            1,
        )

        label(
            canvas,
            "--",
            status_x + 15,
            status_y + 120,
            1.2,
            2,
        )

        label(
            canvas,
            "TEMPORAL BUFFER",
            status_x + 120,
            status_y + 75,
            0.35,
            1,
        )

        label(
            canvas,
            f"{len(tracker.history):02d} / 60",
            status_x + 120,
            status_y + 105,
            0.55,
            1,
        )

        label(
            canvas,
            "READY",
            status_x + 120,
            status_y + 135,
            0.42,
            1,
        )

        # -------------------------------------------------
        # METRICS
        # -------------------------------------------------

        metric_y = 825

        label(
            canvas,
            f"FACE  {len(face):03d}",
            370,
            metric_y,
            0.42,
            1,
        )

        label(
            canvas,
            f"LEFT HAND  {len(left_hand):02d}",
            510,
            metric_y,
            0.42,
            1,
        )

        label(
            canvas,
            f"RIGHT HAND  {len(right_hand):02d}",
            700,
            metric_y,
            0.42,
            1,
        )

        label(
            canvas,
            f"POSE  {len(pose):02d}",
            920,
            metric_y,
            0.42,
            1,
        )

        label(
            canvas,
            "EDGE VISION",
            1080,
            metric_y,
            0.42,
            1,
        )

        cv2.imshow(
            "Aperture Signs",
            canvas,
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    tracker.holistic.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
