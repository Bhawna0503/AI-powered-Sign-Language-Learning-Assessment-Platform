from collections import Counter


class ErrorAnalysisService:
    """
    Analyzes learner mistakes and generates learning insights.
    """

    def __init__(self, progress_service):
        self.progress = progress_service

    def generate_analysis(self):
        report = {
            "most_confused_pairs": self.most_confused_pairs(),
            "low_confidence_letters": self.low_confidence_letters(),
            "needs_revision": self.needs_revision(),
            "performance_trend": self.performance_trend()
        }

        return report

    def most_confused_pairs(self):
        pairs = Counter()

        for item in self.progress.history:
            if not item["correct"]:
                pair = f'{item["expected"]} -> {item["predicted"]}'
                pairs[pair] += 1

        return [
            {"pair": pair, "count": count}
            for pair, count in pairs.most_common(5)
        ]

    def low_confidence_letters(self):
        letters = {}

        for item in self.progress.history:
            expected = item["expected"]

            letters.setdefault(expected, []).append(item["confidence"])

        result = []

        for letter, scores in letters.items():
            avg = sum(scores) / len(scores)

            if avg < 0.60:
                result.append({
                    "letter": letter,
                    "average_confidence": round(avg, 2)
                })

        return result

    def needs_revision(self):
        revision = []

        for item in self.low_confidence_letters():
            revision.append(item["letter"])

        return revision

    def performance_trend(self):
        total = len(self.progress.history)

        if total < 2:
            return {"trend": "Not enough data"}

        half = total // 2

        first_half = self.progress.history[:half]
        second_half = self.progress.history[half:]

        first_accuracy = (
            sum(item["correct"] for item in first_half) / len(first_half)
        ) * 100

        second_accuracy = (
            sum(item["correct"] for item in second_half) / len(second_half)
        ) * 100

        if second_accuracy > first_accuracy:
            trend = "Improving"
        elif second_accuracy < first_accuracy:
            trend = "Declining"
        else:
            trend = "Stable"

        return {
            "trend": trend,
            "first_half_accuracy": round(first_accuracy, 2),
            "second_half_accuracy": round(second_accuracy, 2)
        }