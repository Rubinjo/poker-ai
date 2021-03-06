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
        self.n_rounds = 0

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
        #TODO: setWinners(self, player_scores)? this function does not give any output, would be weird to get winners
        try:
            while True:
                winners = [key for key, value in player_scores.items() if value == max(player_scores.values())] # get highest score players in the dict

                # if winner was all-in, get runner-up winner(s)
                for winner in winners:
                    if not winner.is_all_in:
                        self.winners_lists.append(winners)
                        raise StopIteration 
                # the winners are all all-in, so get the runner-up winner(s)
                # remove winners from player_scores dict

                print(len(player_scores))
                if len(winners) == len(player_scores):
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

    def distribute_winnings(self):
        for winner_group in self.winners_lists:
            if (self.pot.amount > 0):
                n_winner_group = len(winner_group)
                payout = 0
                winner_group_bet = winner_group[0].total_bet
                for player in self.players:
                    reward = min(winner_group_bet, player.total_bet)
                    payout += reward
                    player.total_bet -= reward
                for winning_player in winner_group:
                    winning_player.balance += payout // n_winner_group
                    self.pot.amount -= payout // n_winner_group

    def play_step(self):
        last_player_to_raise = None
        done = False

        while done == False:
            # if only one player remains, end round
            for player in self.players:
                if self.playing_players <= 1:
                    return 'finished' 
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

    def reset(self):
        self.deck = Deck()
        self.highest_bet = 0
        self.board_cards = []
        self.pot = Pot()
        self.winners_lists = []
        self.playing_players = len(self.players)

        for player in self.players:
            player.reset(self.deck)
            
    def continue_playing(self):
        # check if the game has lost a player, then we stop the game
        for player in self.players:
            if player.balance <= 0:
                print(player.name, 'is skeer')
                return False
        return True

    def play_poker(self):
        #TODO: abstract this further (playing flop, playing river etc)
        #TODO: change play_step() function name to betting_round()
        
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
        self.evaluateWinner()

        # distribute winnings
        print('distributing winnings')
        self.distribute_winnings() 

        # check if continueing play
        if not self.continue_playing():
            print('it is over...')
            return
        
        # reset the game
        self.reset()

        # turn blinds position to the next player
        self.players.rotate(-1)

        # play another round
        self.n_rounds += 1
        print(f'Starting a new round, Round: {self.n_rounds + 1}', '\n'*2)
        self.play_poker()

print('\n')            
poker = Game(n_players=4)

poker.play_poker()

