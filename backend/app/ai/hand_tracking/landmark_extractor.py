"""
landmark_extractor.py

Runtime Landmark Extractor

Purpose:
--------
Extracts 21 hand landmarks from MediaPipe detection results.

This file is used during inference by AIEngine.
It DOES NOT process the dataset.
"""

from typing import List, Dict


class LandmarkExtractor:
    """
    Extracts 21 hand landmarks from MediaPipe results.

    Output format:

    [
        [
            {"x": ..., "y": ..., "z": ...},
            ...
            (21 landmarks)
        ]
    ]
    """

    def __init__(self):
        pass

    def extract_landmarks(self, results) -> List[List[Dict[str, float]]]:
        """
        Extract landmarks for every detected hand.

        Parameters
        ----------
        results
            MediaPipe Hands results object.

        Returns
        -------
        list
            List of hands.
            Each hand contains 21 landmarks.
        """

        all_hands = []

        if results is None:
            return all_hands

        if not results.multi_hand_landmarks:
            return all_hands

        for hand_landmarks in results.multi_hand_landmarks:

            hand = []

            for landmark in hand_landmarks.landmark:

                hand.append({
                    "x": float(landmark.x),
                    "y": float(landmark.y),
                    "z": float(landmark.z)
                })

            # Ensure exactly 21 landmarks
            if len(hand) == 21:
                all_hands.append(hand)

        return all_hands

    def landmark_count(self, hand):
        """
        Returns the number of landmarks.

        Parameters
        ----------
        hand : list

        Returns
        -------
        int
        """

        if hand is None:
            return 0

        return len(hand)

    def is_valid(self, hand):
        """
        Validate landmark count.

        Returns
        -------
        bool
        """

        return self.landmark_count(hand) == 21