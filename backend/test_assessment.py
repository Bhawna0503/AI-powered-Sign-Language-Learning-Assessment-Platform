from app.learning.assessment_service import AssessmentService

service = AssessmentService()

service.start_practice()

print("Current Letter:", service.get_current_letter())

print()

print(service.process_prediction("A", 98.6, 61.4))

print(service.process_prediction("B", 84.2, 64.8))

print()

print("Next Letter:", service.next_letter())

print()

print(service.process_prediction("B", 97.1, 58.2))

print()

print(service.get_session_statistics())

print()

print(service.get_attempt_history())