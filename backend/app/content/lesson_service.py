class LessonService:
    def __init__(self):
        self.lessons = [
            {
                "id": 1,
                "sign": "A",
                "description": "Closed fist with thumb resting on the side.",
                "meaning": "Represents the alphabet letter A.",
                "image": "assets/asl/A.jpg",
                "difficulty": "Beginner"
            },
            {
                "id": 2,
                "sign": "B",
                "description": "Open hand with fingers together and thumb across the palm.",
                "meaning": "Represents the alphabet letter B.",
                "image": "assets/asl/B.jpg",
                "difficulty": "Beginner"
            },
            {
                "id": 3,
                "sign": "C",
                "description": "Hand curved to form the shape of the letter C.",
                "meaning": "Represents the alphabet letter C.",
                "image": "assets/asl/C.jpg",
                "difficulty": "Beginner"
            },
            {
                "id": 4,
                "sign": "D",
                "description": "Index finger points upward while the thumb touches the middle finger.",
                "meaning": "Represents the alphabet letter D.",
                "image": "assets/asl/D.jpg",
                "difficulty": "Intermediate"
            },
            {
                "id": 5,
                "sign": "E",
                "description": "Fingers curled inward with the thumb tucked underneath.",
                "meaning": "Represents the alphabet letter E.",
                "image": "assets/asl/E.jpg",
                "difficulty": "Intermediate"
            }
        ]

    def get_all_lessons(self):
        return self.lessons

    def get_lesson_by_id(self, lesson_id):
        for lesson in self.lessons:
            if lesson["id"] == lesson_id:
                return lesson
        return None