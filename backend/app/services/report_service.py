import json


class ReportService:
    def __init__(self, progress_service):
        self.progress = progress_service

    def generate_report(self):
        report = {
            "total_attempts": self.progress.total_attempts(),
            "correct_attempts": self.progress.correct_attempts(),
            "incorrect_attempts": self.progress.incorrect_attempts(),
            "overall_accuracy": round(self.progress.accuracy(), 2),
            "average_confidence": round(
                self.progress.average_confidence(), 2
            ),
            "average_response_time": round(
                self.progress.average_response_time(), 4
            ),
            "strongest_alphabet": self.progress.strongest_alphabet(),
            "weakest_alphabet": self.progress.weakest_alphabet(),
            "most_mistaken": self.progress.most_mistaken()
        }

        return report

    def export_json(self, filename="assessment_report.json"):
        report = self.generate_report()

        with open(filename, "w") as file:
            json.dump(report, file, indent=4)

        print(f"\nReport saved as {filename}")