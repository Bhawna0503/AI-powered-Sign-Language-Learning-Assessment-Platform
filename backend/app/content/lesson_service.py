class LessonService:
    
    def __init__(self):

        self.lessons = [
            {
                "id": 1,
                "sign": "A",
                "description": "Closed fist with thumb resting on the side.",
                "meaning": "Letter A in American Sign Language",
                "image": "assets/asl/A.jpg",
                "difficulty": "Beginner"
            },
            {
                "id": 2,
                "sign": "B",
                "description": "Open hand with fingers together.",
                "meaning": "Letter B in American Sign Language",
                "image": "assets/asl/B.jpg",
                "difficulty": "Beginner"
            },
            {
                "id": 3,
                "sign": "C",
                "description": "Curve your fingers to form the letter C.",
                "meaning": "Letter C in American Sign Language",
                "image": "assets/asl/C.jpg",
                "difficulty": "Beginner"
            },
            {
                "id": 4,
                "sign": "D",
                "description": "Index finger pointing upward.",
                "meaning": "Letter D in American Sign Language",
                "image": "assets/asl/D.jpg",
                "difficulty": "Beginner"
            },
            {
                "id": 5,
                "sign": "E",
                "description": "Fingers folded over the thumb.",
                "meaning": "Letter E in American Sign Language",
                "image": "assets/asl/E.jpg",
                "difficulty": "Beginner"
            }
        ]

    def get_all_lessons(self):
        return self.lessons

    def get_lesson_by_id(self, lesson_id: int):

        for lesson in self.lessons:
            if lesson["id"] == lesson_id:
                return lesson

        return None