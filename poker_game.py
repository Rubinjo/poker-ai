import time 
from utils.cards import Deck
from utils.player import Player
from collections import deque
from utils.evaluateWinner import evaluateWinner # TODO: should this be a function or a class?

# TODO: if player is all-in, then make sure that they are not allowed to play again. check if amount of players + folded players is total players -1 (the game is then over), and run to the evaluate winner function.
# TODO: if players are all-in, make sure to save their total bettings somewhere to use it in the winnings distribution
# TODO: check if all players are allowed to play/not allowed to play, when it makes sense
    # folding has been handled
    # this is already wrong when someone is all-in, are there other situtations?
    # first round should start at the player after the big blind (in 2p Poker this is small blind)
        # but after the flop, the player in small blind should start the betting
        # for 3p+ poker, we need to make sure this is fixed. Maybe we can use a queue to keep track of the players that are allowed to play (hier kwam github mee)
        # or we can shift the list of players before/after the flop and at the end of the game 

class Pot:
    def __init__(self):
        self.amount = 0

    def add_to_pot(self, amount):
        self.amount += amount

    def print_status(self):
        print(f'Pot: {self.amount}')
    

class Game:
    def __init__(self, n_players: int):
        self.highest_bet = 0 
        self.n_folded_players = 0
        self.blind_values = [10, 20] # for 2 player games
        self.blinds = (n_players - 2) * [0]
        self.blinds.extend(self.blind_values) # for 2 player games
        self.deck = Deck()
        self.players = deque()
        self.board_cards = []
        for i in range(n_players):
            self.players.append(Player(self.deck, f'Player {i}'))
        self.pot = Pot()

    def deduct_blinds(self):
        for i, player in enumerate(self.players):
            if self.blinds[i] > 0:
                player.evaluate_action('r' + str(self.blinds[i]), 0, self.pot)
            # set the highest bet to the highest blind
        self.highest_bet = max(self.blinds)
            
        
    def print_players(self):
        for player in self.players:
            player.print_hand()
    
    def print_board(self):
        board = ''
        for card in self.board_cards:
            board += card.string_form
        if len(board) == 0:
            board += 'No cards on board'
        print(f'Board: {board}')
        print('-------------')

    def play_step(self):
        last_player_to_raise = None
        done = False

        while done == False:
            for player in self.players:
                # if only one player remains, end round
                if len(self.players) - self.n_folded_players <= 1:
                    return 'finished'
                # if no player has played yet (last_player_to_raise == None), set it to the current player as they will not be allowed to play anymore
                time.sleep(.5)
                # check if player is folded, or was the last person to raise, then skip or break
                if player.name == last_player_to_raise:
                    done = True
                    break
                if last_player_to_raise == None:
                    last_player_to_raise = player.name
                if player.is_folded:
                    continue

                # print game info
                print(f'now evaluating action of {player.name}')
                self.print_board()
                for players in self.players:
                    players.print_public()
                self.pot.print_status()
                print('\n')

                # get action of player and evaluate
                action = player.get_action()
                if action == 'f':
                    # player folded, add to amount of folded players
                    self.n_folded_players += 1
                player_total_bet = player.evaluate_action(action, self.highest_bet, self.pot) 
                # TODO: if save player bets in a list (for giving ppl their right share of the pot)
                # self.pot.raise(player, player_total_bet)

                if player_total_bet > self.highest_bet:
                    # player has raised, so update highest bet and all players get to move again
                    self.highest_bet = player_total_bet
                    last_player_to_raise = player.name

                print('\n'*3) # clear screen

    def play_round(self):
        # deduct the blinds from the (correct) players, and add them to the pot
        self.deduct_blinds()

        # play pre-flop
        self.play_step()
        # deal flop and play another round
        print('dealing flop')
        self.board_cards.append(self.deck.deal())
        self.board_cards.append(self.deck.deal())
        self.board_cards.append(self.deck.deal())
        self.play_step()
        # deal turn and play another round
        print('dealing turn')
        self.board_cards.append(self.deck.deal())
        self.play_step()
        # deal river and play another round
        print('dealing river')
        self.board_cards.append(self.deck.deal())
        self.play_step()
        # determine winner
        print('determining winner')
        # TODO: determine winner
        winner = evaluateWinner(self.players, self.board_cards) 
        # rotating the blinds
        self.players.rotate(1)

print('\n')            
poker = Game(n_players=2)
poker.play_round()