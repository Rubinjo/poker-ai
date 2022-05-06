import time 
from utils.cards import Deck
from utils.player import Player
from collections import deque

class Pot:
    def __init__(self):
        self.amount = 0

class Game:
    def __init__(self, n_players: int, smallBlindPos = 0, BigBlindPos = 1):
        self.highest_bet = 0
        self.n_folded_players = 0
        # self.blinds = [0, 0, 0, 10, 20] # for 5 player games
        self.blinds = [10, 20] # for 2 player games
        self.deck = Deck()
        self.players = []
        self.board_cards = []
        for i in range(n_players):
            self.players.append(Player(self.deck, f'Player {i+1}'))
        self.blind_positions = deque(self.players[smallBlindPos], self.players[BigBlindPos])
        self.pot = Pot()
        
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

        # TODO: deduct blinds

        while done == False:
            for player in self.blind_positions:
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

                # get action of player and evaluate
                action = player.get_action()
                if action == 'f':
                    # player folded, add to amount of folded players
                    self.n_folded_players += 1
                player_total_bet = player.evaluate_action(action, self.highest_bet) 

                self.pot += player_total_bet

                if player_total_bet > self.highest_bet:
                    # player has raised, so update highest bet and all players get to move again
                    self.highest_bet = player_total_bet
                    last_player_to_raise = player.name

                print('\n'*3) # clear screen

    def play_round(self):
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

print('\n')            
poker = Game(n_players=2)
poker.play_round()