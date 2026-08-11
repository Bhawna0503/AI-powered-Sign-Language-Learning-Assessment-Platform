from app.learning.assessment_service import AssessmentService
from app.analytics.progress_service import ProgressService

assessment = AssessmentService()

assessment.start_practice()

assessment.process_prediction("A", 97.5, 63.2)
assessment.process_prediction("B", 80.3, 70.1)

progress = ProgressService(assessment)

print(progress.get_progress())