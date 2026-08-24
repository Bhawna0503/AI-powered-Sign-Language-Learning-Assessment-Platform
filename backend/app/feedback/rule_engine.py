class RuleEngine:

    def evaluate(self, expected, predicted, features):
        rules = []

        if expected != predicted:
            rules.append({
                "type": "prediction",
                "message": f"Expected '{expected}' but detected '{predicted}'."
            })

        if not features["index_extended"]:
            rules.append({
                "type": "index",
                "message": "Extend your index finger."
            })

        if not features["middle_extended"]:
            rules.append({
                "type": "middle",
                "message": "Straighten your middle finger."
            })

        if features["thumb_index_distance"] < 0.05:
            rules.append({
                "type": "thumb",
                "message": "Move your thumb slightly away from your index finger."
            })

        return rules