class RecommendationService:

    def recommend(self, profile):
        recommendations = []

        mastery = profile["mastery"]
        confidence = profile["average_confidence"]

        for letter in mastery:

            if mastery[letter] < 0:
                recommendations.append({
                    "alphabet": letter,
                    "reason": "Low mastery level"
                })

            elif confidence.get(letter, 1) < 0.70:
                recommendations.append({
                    "alphabet": letter,
                    "reason": "Low confidence"
                })

        return recommendations