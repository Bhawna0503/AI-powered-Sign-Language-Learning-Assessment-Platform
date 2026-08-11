from app.learning.lesson_manager import LessonManager

lesson = LessonManager()

lesson.start_practice()

print("Current:", lesson.get_current_letter())

print("Next:", lesson.next_letter())

print("Select:", lesson.select_letter("K"))

print("Status:", lesson.get_status())

lesson.restart()

print("Restart:", lesson.get_current_letter())