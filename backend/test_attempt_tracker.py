from app.learning.attempt_tracker import AttemptTracker

tracker = AttemptTracker()

tracker.add_attempt("A", "A", 98.7, 71.2)
tracker.add_attempt("B", "A", 74.5, 69.4)
tracker.add_attempt("C", "C", 95.2, 73.1)

print("Attempts")

for attempt in tracker.get_attempts():
    print(attempt)

print()

print("Total:", tracker.total_attempts())
print("Correct:", tracker.correct_attempts())
print("Incorrect:", tracker.incorrect_attempts())
print("Average Confidence:", tracker.average_confidence())