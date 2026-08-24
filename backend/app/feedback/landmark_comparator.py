import math


class LandmarkComparator:

    def distance(self, landmarks, i1, i2):
        x1, y1, z1 = landmarks[i1*3:i1*3+3]
        x2, y2, z2 = landmarks[i2*3:i2*3+3]

        return math.sqrt(
            (x1-x2)**2 +
            (y1-y2)**2 +
            (z1-z2)**2
        )

    def is_finger_extended(self, landmarks, tip, pip):
        tip_y = landmarks[tip*3 + 1]
        pip_y = landmarks[pip*3 + 1]
        return tip_y < pip_y

    def compare(self, landmarks):
        return {
            "thumb_extended": self.is_finger_extended(landmarks, 4, 3),
            "index_extended": self.is_finger_extended(landmarks, 8, 6),
            "middle_extended": self.is_finger_extended(landmarks, 12, 10),
            "ring_extended": self.is_finger_extended(landmarks, 16, 14),
            "pinky_extended": self.is_finger_extended(landmarks, 20, 18),
            "thumb_index_distance": self.distance(landmarks, 4, 8)
        }