from app.learning.assessment_service import AssessmentService
from app.analytics.statistics import Statistics

assessment = AssessmentService()

assessment.start_practice()

assessment.process_prediction("A", 99.2, 60)
assessment.process_prediction("B", 81.4, 58)
assessment.next_letter()
assessment.process_prediction("B", 95.8, 63)
assessment.next_letter()
assessment.process_prediction("D", 70.5, 72)

attempts = assessment.get_attempt_history()

stats = Statistics(attempts)

print(stats.dashboard())