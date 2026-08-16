import numpy as np


class SignRecognizer:
    """
    Temporal landmark feature extractor.

    The tracker supplies a sequence of face, pose, and hand
    landmarks. This class converts that sequence into a
    normalized feature vector suitable for ASL recognition.
    """

    def __init__(self, sequence_length=30):
        self.sequence_length = sequence_length

    def _hand_features(self, hand):
        if not hand:
            return np.zeros(63, dtype=np.float32)

        wrist = hand[0]

        features = []

        for landmark in hand:
            features.extend([
                landmark["x"] - wrist["x"],
                landmark["y"] - wrist["y"],
                landmark["z"] - wrist["z"],
            ])

        return np.asarray(features, dtype=np.float32)

    def frame_features(self, frame):
        """
        Convert one tracked frame into a fixed-size vector.

        Current representation:
        left hand  = 21 x 3
        right hand = 21 x 3
        pose       = 33 x 3
        """

        left = self._hand_features(frame["left_hand"])
        right = self._hand_features(frame["right_hand"])

        pose = frame["pose"]

        if pose:
            pose_features = []

            for landmark in pose:
                pose_features.extend([
                    landmark["x"],
                    landmark["y"],
                    landmark["z"],
                ])

            pose_features = np.asarray(
                pose_features,
                dtype=np.float32,
            )
        else:
            pose_features = np.zeros(99, dtype=np.float32)

        return np.concatenate([
            left,
            right,
            pose_features,
        ])

    def sequence_features(self, history):
        """
        Convert the recent temporal history into
        a fixed-size sequence.

        Short sequences are padded with zeros.
        Long sequences use the most recent frames.
        """

        frames = list(history)

        if len(frames) > self.sequence_length:
            frames = frames[-self.sequence_length:]

        feature_frames = [
            self.frame_features(frame)
            for frame in frames
        ]

        if not feature_frames:
            return np.zeros(
                (self.sequence_length, 225),
                dtype=np.float32,
            )

        while len(feature_frames) < self.sequence_length:
            feature_frames.insert(
                0,
                np.zeros_like(feature_frames[0]),
            )

        return np.asarray(
            feature_frames,
            dtype=np.float32,
        )

    def motion_features(self, sequence):
        """
        Calculate frame-to-frame movement.

        This is particularly important for motion-based
        signs such as J and Z.
        """

        if len(sequence) < 2:
            return np.zeros_like(sequence)

        return np.diff(
            sequence,
            axis=0,
        )

    def analyze(self, history):
        sequence = self.sequence_features(history)
        motion = self.motion_features(sequence)

        movement_energy = float(
            np.mean(np.abs(motion))
        )

        return {
            "sequence": sequence,
            "motion": motion,
            "movement_energy": movement_energy,
            "frames": len(history),
        }
