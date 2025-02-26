import random

class Question:
    def __init__(self, text, level, correct, err1, err2, err3):
        self.text = text
        self.level = int(level)  # Convert to integer
        self.correct = correct
        self.err1 = err1
        self.err2 = err2
        self.err3 = err3

    def get_all_answer(self):
        """Return tutte le risposte in una lista"""
        return [self.correct,self.err1, self.err2, self.err3]

    def get_random_answer(self):
        """Randomizza le risposte """
        answers = self.get_all_answer()
        return random.shuffle(answers)

    def is_correct(self, answer):
        """Verifica se è corretta"""
        return answer == self.correct




class Player:
    def __init__(self, nickname, score=0):
        self.nickname = nickname
        self.score = score


def main():
   pass

if __name__ == "__main__":
    main()