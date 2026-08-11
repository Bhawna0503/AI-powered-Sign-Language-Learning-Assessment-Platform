from app.learning.assessment_service import AssessmentService
from app.analytics.dashboard import Dashboard

assessment = AssessmentService()

assessment.start_practice()

assessment.process_prediction("A", 99.1, 60)
assessment.process_prediction("B", 83.4, 72)

assessment.next_letter()

assessment.process_prediction("B", 94.8, 61)

assessment.next_letter()

assessment.process_prediction("D", 65.2, 80)

dashboard = Dashboard(assessment.get_attempt_history())

print(dashboard.generate())