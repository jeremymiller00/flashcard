import os
import sys
import random


class FlashcardApp(object):
    def __init__(self, filepath) -> None:
        self.filepath = filepath
        self.deck = None

    def setup(self) -> None:
        deck = Deck(self.filepath)
        deck.load_deck()
        self.deck = deck

    def study(self) -> None:
        # repl
        if len(self.deck.unseen_cards) == 0:
            print("Session complete")
            sys.exit(0)
        else:
            os.system('clear')
            print("\n" * 10)
            card = self.deck.draw_card()
            _ = input(card.show_question())
            print("\n" * 5)
            _ = input(card.show_answer())
            self.study()


class Card(object):
    def __init__(self, question, answer) -> None:
        self.question = question
        self.answer = answer

    def show_question(self):
        return self.question

    def show_answer(self):
        return self.answer


class Deck(object):
    def __init__(self, filepath, delimiter='#### ') -> None:
        self.filepath = filepath
        self.unseen_cards = []
        self.seen_cards = []
        self.delimiter = delimiter

    def load_deck(self):
        with open(self.filepath, 'r') as file:
            qstring = file.read()
        questions = qstring.split(self.delimiter)
        for q in questions:
            if q[:3] != '---': # skip header row
                q_and_a = q.split('\n', 1)
                c = Card(q_and_a[0], q_and_a[1])
                self.unseen_cards.append(c)
        print("Deck loaded\n")

    def draw_card(self):
        idx = random.randint(0, len(self.unseen_cards)-1)
        card = self.unseen_cards[idx]
        self.mark_as_seen(card)
        return card
    
    def mark_as_seen(self, card):
        self.seen_cards.append(card)
        try:
            self.unseen_cards.remove(card)
        except ValueError:
            print("Error removing card")

def clean_path(path: list) -> str:
    """
    Accounts for input path which may contain whitespace
    """
    return ' '.join(path)


#####################################

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please provide path to question file")
        print("Usage:")
        print("python flashcard.py pathtofile")
        sys.exit(1)

    # path = clean_path(sys.argv[1:])
    # path = '/Users/Jeremy/Data-Science-Vault/Computers/CS APP/Ch 1 A Tour of Computer Systems.md'
    # path = '/Users/jeremymiller/Data-Science-Vault/Computers/SICP/SICP Flash Cards.md'
    app = FlashcardApp(clean_path(sys.argv[1:]))
    app.setup()
    app.study()


