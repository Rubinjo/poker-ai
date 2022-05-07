
class Player():
    def __init__(self, all_in):
        self.is_all_in = all_in
    
a = Player(True)
b = Player(True)
c = Player(True)
d = Player(False)
e = Player(True)

winners = {a: 4, b: 3, c: 4, d: 2, e: 3}


list_of_winners_nice = []
def getWinners(player_scores):
    try:
        while True:
            winners = [key for key, value in player_scores.items() if value == max(player_scores.values())] # get highest score players in the dict

            # if winner was all-in, get runner-up winner(s)
            for winner in winners:
                if not winner.is_all_in:
                    print('yea')
                    list_of_winners_nice.append(winners)
                    raise StopIteration 
            # the winners are all all-in, so get the runner-up winner(s)
            # remove winners from player_scores dict

            print(len(player_scores))
            if len(winners) == len(player_scores):
                print('yes', len(winners))
                list_of_winners_nice.append(winners)
                raise StopIteration

            for winner in winners:
                player_scores.pop(winner)
            # get the runner-up winner(s)
            list_of_winners_nice.append(winners)
            getWinners(player_scores)
            raise StopIteration
    except StopIteration:
        pass

    
getWinners(winners)
print(list_of_winners_nice)

