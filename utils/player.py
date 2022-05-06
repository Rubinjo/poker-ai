class Player:
    def __init__(self, deck, name: str):
        self.deck = deck
        self.name = name
        self.is_folded = False
        self.total_bet = 0
        self.balance = 1000
        self.hand = []
        self._get_hand()

    def _get_hand(self):
        for _ in range(2):
            self.hand.append(self.deck.deal())

    def print_hand(self):
        print(f'Hand of {self.name}:', self.hand[0].string_form, self.hand[1].string_form)
    
    def print_status(self):
        self.print_hand()
        print(f'Balance: {self.balance}')

    def print_public(self):
        if self.is_folded:
            print(f'{self.name} folded', end=' '*10)
            print(f'{self.name} has {self.balance}')
        else:
            print(f'{self.name} bet {self.total_bet}', end=' '*10)
            print(f'{self.name} has {self.balance}')

    def get_action(self, possible_actions=['f', 'c', 'r']):
        self.print_status()
        print('\n')
        action = input(f'Action {self.name} (f/c/r(x)): ')
        if action in possible_actions:
            if action == 'r':
                raise_amount = int(input('Raise amount: '))
                print(f'action: {action}{raise_amount}')
                return action + str(raise_amount)
            return action
        print(f'must be one of {possible_actions}')
        self.get_action() 

    def _fold(self):
        self.is_folded = True

    def _call(self, highest_bet: int):
        if highest_bet - self.total_bet > self.balance: # player cannot fully call
            print(f'Player {self.name} is all-in!')
            self.total_bet += self.balance
            self.balance = 0
        else:
            print(f'{highest_bet} - {self.total_bet}')
            self.balance -= highest_bet - self.total_bet
            self.total_bet = highest_bet

    def _raise(self, raise_amount: int):
        if raise_amount > self.balance:
            print(f'Player {self.name} is all-in!')
            self.total_bet += self.balance
            self.balance = 0
        else:
            self.total_bet += raise_amount
            self.balance -= raise_amount

    def evaluate_action(self, action: str, highest_bet: int):
        if action[0] == 'f':
            self._fold() # fold
        elif action[0] == 'c':
            self._call(highest_bet) # call
        elif action[0] == 'r':
            # call, then raise the amount
            self._call(highest_bet)
            self._raise(int(action[1:]))
        return self.total_bet