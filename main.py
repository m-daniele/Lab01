import random
from random import shuffle

class Question:
    def __init__(self, text, level, correct, err1, err2, err3):
        self.text = text
        self.level = int(level)  # Convert to integer
        self.correct = correct
        self.err1 = err1
        self.err2 = err2
        self.err3 = err3

    def get_all_answer(self):
        """Return all answer in a list"""
        return [self.correct,self.err1, self.err2, self.err3]

    def get_random_answer(self):
        """randomize answer"""
        answers = self.get_all_answer()
        random.shuffle(answers)
        return answers

    def is_correct(self, answer):
        return answer == self.correct


class Player:
    def __init__(self, nickname, score=0):
        self.nickname = nickname
        self.score = score

class Game:
    def __init__(self, question_file):
        self.questions = []
        self.current_level = 0
        self.max_level = 0
        self.score = 0
        self.load_question(question_file)

    def load_question(self, file_path):
        """Load questions from file and organize them by level."""
        current_lines = []

        with open(file_path, 'r',encoding='utf-8') as file:
            for line in file:
                if line.strip():  # If line is not empty
                    current_lines.append(line.strip())
                else: # line is empty -> end of the current question block
                    if current_lines and len(current_lines)>=6:
                        question = Question(
                            text=current_lines[0],
                            level=current_lines[1],
                            correct=current_lines[2],
                            err1=current_lines[3],
                            err2=current_lines[4],
                            err3=current_lines[5]
                        )
                        self.questions.append(question) # add question to init question list
                        self.max_level=max(self.max_level,self.current_level) # find the max level if needed
                    current_lines=[] #reset lines after question creation

        # Process the last block if file doesn't end with blank line
        if current_lines and len(current_lines) >= 6:
            question = Question(
                text=current_lines[0],
                level=current_lines[1],
                correct=current_lines[2],
                err1=current_lines[3],
                err2=current_lines[4],
                err3=current_lines[5]
            )
            self.questions.append(question)
            self.max_level = max(self.max_level, question.level)

    def get_questions_by_level(self, level):
        """Return all questions of a specific level."""
        return [q for q in self.questions if q.level == level]
        # level_questions=[]  # list comprehension for faster writing
        #for q in self.questions:
        #    if q.level==level:
        #       level_questions.append(q)
        #return level_questions

    def get_random_question(self, level):
        """Return a random question from the specified level."""
        level_questions = self.get_questions_by_level(level)
        if level_questions:
            return random.choice(level_questions)
        return None

    def ask_question(self, question):
        """Present a question to the user and process their answer."""
        print(f"Livello:{question.level}) {question.text}")
        shuffled_answers = question.get_random_answer()
        correct_index = shuffled_answers.index(question.correct) + 1  # +1 for 1-based indexing in file

        # Display answer options
        for i, answer in enumerate(shuffled_answers, 1):
            print(f"\t{i}. {answer}")

        # Get user input
        try:
            user_choice = int(input("Inserisci la risposta: "))
            if 1<=user_choice<=4:
                is_correct = shuffled_answers[user_choice - 1] == question.correct
                if is_correct:
                    print(f"Risposta esatta! \n")
                    self.score+=1
                    self.current_level += 1
                    return True
                else:
                    print(f"Risposta sbagliata! La risposta corretta era: {correct_index}\n")
                    return False
            else:
                print(f"Inserisci un numero tra 0 e 4! \n")
                return self.ask_question(question)
        except ValueError:
            print("Devi inserire un numero!")
            return self.ask_question(question)  # Ask again

    def play(self):
        """Main game loop."""
        game_over = False

        while not game_over:
            question = self.get_random_question(self.current_level)

            result = self.ask_question(question)

            # Check game ending conditions
            if not result:  # Wrong answer
                game_over = True
            elif self.current_level > self.max_level:  # Completed all levels
                print("Complimenti! Hai risposto correttamente a tutte le domande!")
                game_over = True

        print(f"Hai totalizzato {self.score} punti!")
        nickname = input("Inserisci il tuo nickname: ")
        player = Player(nickname, self.score)
        self.save_score(player)

    def save_score(self, player):
        """Save player score to the file."""
        scores = []
        # Read existing scores
        try:
            with open("punti.txt", 'r', encoding='utf-8') as file:
                for line in file:
                    if line.strip():
                        parts = line.strip().split()
                        if len(parts) >= 2:
                            name = " ".join(parts[:-1])  # Handle names with spaces
                            score = int(parts[-1])
                            scores.append((name, score))
        except FileNotFoundError:
            pass  # File doesn't exist yet, we'll create it

        # Add current player's score
        scores.append((player.nickname, player.score))

        def get_score(item):
            return item[1]  # Return the second element (the score)
        # Sort scores using the get_score function, in descending order
        scores.sort(key=get_score, reverse=True)

        # Write scores back to file
        with open("punti.txt", 'w', encoding='utf-8') as file:
            for name, score in scores:
                file.write(f"{name} {score}\n")


def main():
    """Entry point for the trivia game."""
    random.seed()  # Initialize random seed
    game = Game("domande.txt")
    game.play()

if __name__ == "__main__":
    main()