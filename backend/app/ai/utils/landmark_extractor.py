class LandmarkExtractor:
    
    def extract_landmarks(self, results):

        all_hands = []

        if not results.multi_hand_landmarks:
            return all_hands

        for hand_landmarks in results.multi_hand_landmarks:

            hand_points = []

            for landmark in hand_landmarks.landmark:

                hand_points.append({
                    "x": landmark.x,
                    "y": landmark.y,
                    "z": landmark.z
                })

            all_hands.append(hand_points)

        return all_hands