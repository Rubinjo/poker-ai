import time 
from utils.cards import Deck
from utils.player import Player
from collections import deque
from phevaluator import evaluate_cards

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
        self.playing_players = n_players
        self.blind_values = [10, 20] # for 2 player games
        self.blinds = (n_players - 2) * [0]
        self.blinds.extend(self.blind_values) # for 2 player games
        self.deck = Deck()
        self.players = deque()
        self.board_cards = []
        for i in range(n_players):
            self.players.append(Player(self.deck, f'Player {i}'))
        self.pot = Pot()
        self.winners_lists = []

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

    def getWinners(self, player_scores):
        try:
            while True:
                winners = [key for key, value in player_scores.items() if value == max(player_scores.values())] # get highest score players in the dict

                # if winner was all-in, get runner-up winner(s)
                for winner in winners:
                    if not winner.is_all_in:
                        print('yea')
                        self.winners_lists.append(winners)
                        raise StopIteration 
                # the winners are all all-in, so get the runner-up winner(s)
                # remove winners from player_scores dict

                print(len(player_scores))
                if len(winners) == len(player_scores):
                    print('yes', len(winners))
                    self.winners_lists.append(winners)
                    raise StopIteration

                for winner in winners:
                    player_scores.pop(winner)
                # get the runner-up winner(s)
                self.winners_lists.append(winners)
                self.getWinners(player_scores)
                raise StopIteration
        except StopIteration:
            pass

    def evaluateWinner(self):
        # TODO: fix that if the winner is all-in, other players can win as well from other players
        player_scores = {}
        for player in self.players:
            if player.is_folded: # player is not allowed to be evaluated for the winnings
                continue
            # get the string_form of the cards
            seven_card_hand = [card.string_form for card in player.hand + self.board_cards]
            player_scores[player] = evaluate_cards(*seven_card_hand)

        self.getWinners(player_scores)
        
        
        # print("Winning players:", winners)
        # return winners

    def distribute_winnings(self, winners):
       #TODO: give money 
        pass

    def play_step(self):
        last_player_to_raise = None
        done = False

        while done == False:
            # if only one player remains, end round
            for player in self.players:
                if self.playing_players <= 1: # TODO: why does this work?
                    return 'finished' 
                time.sleep(.5)
                # check if the player to play was the last to raise, then the step is over
                if player.name == last_player_to_raise:
                    done = True
                    break
                # if no player has played yet (last_player_to_raise == None), set it to the current player as they will not be allowed to play anymore
                if last_player_to_raise == None:
                    last_player_to_raise = player.name
                # check if player is folded, or is all-in, then skip or break
                if player.is_folded or player.is_all_in: # if player is not playing, skip
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

                player_total_bet, finished_player = player.evaluate_action(action, self.highest_bet, self.pot) 
                if finished_player:
                    self.playing_players -= 1

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

        # rotate players to make sure the small blind starts the betting
        self.players.rotate(2)

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
        winners = self.evaluateWinner()
        # distribute winnings
        print('distributing winnings')
        self.distribute_winnings(winners) 
        # rotating the blinds
        self.players.rotate(-1)

print('\n')            
poker = Game(n_players=4)
poker.play_round()
# TODO: make more than one round possible

# TODO: if everyone folds, the big blind should win; also happens later when ppl randomly fold
