"""
landmark_comparator.py

Compares the 21 MediaPipe hand landmarks.

Detects:
- Thumb position
- Finger extension / bending
- Basic finger angles
- Palm orientation

The comparator returns boolean rule results that are
evaluated by RuleEngine.
"""

import math


class LandmarkComparator:

    def __init__(self):
        pass

    # =====================================================
    # DISTANCE
    # =====================================================

    def _distance(self, p1, p2):
        """Calculate 2D distance between two landmarks."""

        return math.sqrt(
            (p1["x"] - p2["x"]) ** 2 +
            (p1["y"] - p2["y"]) ** 2
        )

    # =====================================================
    # ANGLE
    # =====================================================

    def _angle(self, a, b, c):
        """
        Calculate angle ABC using three landmarks.
        """

        ba = (
            a["x"] - b["x"],
            a["y"] - b["y"]
        )

        bc = (
            c["x"] - b["x"],
            c["y"] - b["y"]
        )

        magnitude_ba = math.sqrt(
            ba[0] ** 2 +
            ba[1] ** 2
        )

        magnitude_bc = math.sqrt(
            bc[0] ** 2 +
            bc[1] ** 2
        )

        if magnitude_ba == 0 or magnitude_bc == 0:
            return 0.0

        dot_product = (
            ba[0] * bc[0] +
            ba[1] * bc[1]
        )

        cosine_value = (
            dot_product /
            (magnitude_ba * magnitude_bc)
        )

        # Avoid floating-point errors
        cosine_value = max(
            -1.0,
            min(1.0, cosine_value)
        )

        return math.degrees(
            math.acos(cosine_value)
        )

    # =====================================================
    # FINGER EXTENSION
    # =====================================================

    def _is_finger_extended(
        self,
        landmarks,
        tip,
        pip,
        mcp
    ):
        """
        Determines whether a finger is reasonably extended.

        Uses:
        - tip-to-MCP distance
        - PIP angle
        """

        tip_to_mcp = self._distance(
            landmarks[tip],
            landmarks[mcp]
        )

        pip_angle = self._angle(
            landmarks[mcp],
            landmarks[pip],
            landmarks[tip]
        )

        return (
            tip_to_mcp > 0.12 and
            pip_angle > 150
        )

    # =====================================================
    # COMPARE LANDMARKS
    # =====================================================

    def compare(self, landmarks):

        """
        Compare 21 MediaPipe landmarks.

        Returns a dictionary of rule results.
        """

        if landmarks is None:
            return {}

        if len(landmarks) != 21:
            return {}

        comparison = {}

        # =================================================
        # THUMB
        # =================================================

        thumb_angle = self._angle(
            landmarks[2],
            landmarks[3],
            landmarks[4]
        )

        comparison["thumb"] = (
            thumb_angle > 120
        )

        # =================================================
        # INDEX FINGER
        # =================================================

        index_extended = self._is_finger_extended(
            landmarks,
            tip=8,
            pip=6,
            mcp=5
        )

        comparison["index"] = index_extended

        # =================================================
        # MIDDLE FINGER
        # =================================================

        middle_extended = self._is_finger_extended(
            landmarks,
            tip=12,
            pip=10,
            mcp=9
        )

        comparison["middle"] = middle_extended

        # =================================================
        # RING FINGER
        # =================================================

        ring_extended = self._is_finger_extended(
            landmarks,
            tip=16,
            pip=14,
            mcp=13
        )

        comparison["ring"] = ring_extended

        # =================================================
        # LITTLE FINGER
        # =================================================

        little_extended = self._is_finger_extended(
            landmarks,
            tip=20,
            pip=18,
            mcp=17
        )

        comparison["little"] = little_extended

        # =================================================
        # PALM ORIENTATION
        # =================================================

        palm_width = abs(
            landmarks[5]["x"] -
            landmarks[17]["x"]
        )

        comparison["palm"] = (
            palm_width > 0.05
        )

        # =================================================
        # FINGER ANGLES
        # =================================================

        comparison["index_angle"] = (
            self._angle(
                landmarks[5],
                landmarks[6],
                landmarks[8]
            ) > 150
        )

        comparison["middle_angle"] = (
            self._angle(
                landmarks[9],
                landmarks[10],
                landmarks[12]
            ) > 150
        )

        comparison["ring_angle"] = (
            self._angle(
                landmarks[13],
                landmarks[14],
                landmarks[16]
            ) > 150
        )

        comparison["little_angle"] = (
            self._angle(
                landmarks[17],
                landmarks[18],
                landmarks[20]
            ) > 150
        )

        return comparison