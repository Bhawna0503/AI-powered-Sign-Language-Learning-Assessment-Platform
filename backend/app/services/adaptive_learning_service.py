class AdaptiveLearningService:

    def generate_plan(self, profile):
        plan = {
            "practice_now": [],
            "review_later": [],
            "mastered": []
        }

        mastery = profile["mastery"]

        for letter, score in mastery.items():

            if score < 0:
                plan["practice_now"].append(letter)

            elif score >= 5:
                plan["mastered"].append(letter)

            else:
                plan["review_later"].append(letter)

        return plan