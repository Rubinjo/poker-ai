import random

class Deck:
    def __init__(self):
        self.cards = []
        for card_idx in range(52):
            self.cards.append(Card(card_idx))
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()
    
    def print_deck(self):
        for card in self.cards:
            pass
            print(card.string_form, card.card_no)


class Card():
    def __init__(self, card_idx: int):
        self.suit, self.rank, self.card_no, self.string_form = self._generate_card(card_idx)
    
    def _generate_card(self, card_idx):
        suits = ["C", "D", "H", "S"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        suit = card_idx % 4
        rank = card_idx // 4
        string_form = suits[suit] + ranks[rank]
        return (suits[suit], ranks[rank], card_idx, string_form)
