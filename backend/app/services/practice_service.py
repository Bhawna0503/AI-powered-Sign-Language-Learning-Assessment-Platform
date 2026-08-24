from app.content.alphabet import ALPHABETS


class PracticeService:
    def __init__(self):
        self.current_index = 0
        self.attempts = 0
        self.correct = 0

    def current_letter(self):
        return ALPHABETS[self.current_index]

    def next_letter(self):
        if self.current_index < len(ALPHABETS) - 1:
            self.current_index += 1

    def record_attempt(self, is_correct):
        self.attempts += 1
        if is_correct:
            self.correct += 1

    def accuracy(self):
        if self.attempts == 0:
            return 0
        return (self.correct / self.attempts) * 100