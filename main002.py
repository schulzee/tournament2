# adding some basic loops to make sure things work


# notes after running this a few times:
# seems like hero buys back in with the starting edge
# --> comment out line 136, uncomment lines 137,138
# --> HERO rebuys for the correct edge, but doesnt get lowered properly

import random
import bisect


## INITIAL SETUP

# setting up base inputs
NUMBER_OF_PLAYERS = 10  # not counting HERO
HERO_STARTING_COIN_WEIGHT = 0.65
DEFAULT_STACK_SIZE = 100
DEFAULT_BUY_IN = 100
DEFAULT_MILESTONES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14, 16, 19, 24, 32, 41] # last milestone is when payouts change to 0
MAX_NUMBER_OF_PLAYERS_FOR_HERO_TO_REBUY = 5  # make sure to pick something here that's outside the payouts
DEFAULT_PAYOUT_RATIOS = [26, 17, 11.25, 6.75, 5.1, 4.2, 3.3, 2.4, 1.8, 1.4, 1.2, 1, .8, .7, .6, .5, 0]
STARTING_PRIZEPOOL = 0

# initialize variables that change over time
hero_coin_weight = HERO_STARTING_COIN_WEIGHT

# create player list and add players to it, as well as hero
PLAYER_LIST = []  # should be lowercase, but too lazy to change this everywhere
for i in range (NUMBER_OF_PLAYERS):
    PLAYER_LIST.append([DEFAULT_STACK_SIZE, i, 0.5])
PLAYER_LIST.append([DEFAULT_STACK_SIZE, "HERO", hero_coin_weight])

# create prize pool and track hero profit
prizepool = len(PLAYER_LIST)*DEFAULT_BUY_IN + STARTING_PRIZEPOOL
hero_profit = -DEFAULT_BUY_IN


## PLAY A HAND
for i in range(0,5000):

    if len(PLAYER_LIST) > 1:
        changed_coin = False

        # pick two players to play a hand against each other
        player_index_1 = random.randint(0, len(PLAYER_LIST)-1)
        player_index_2 = random.randint(0, len(PLAYER_LIST)-1)
        while player_index_2 == player_index_1:
            player_index_2 = random.randint(0, len(PLAYER_LIST)-1)  # added -1 here

        # determine (randomized) pot size, use stacksizes as inputs
        stacksize1 = PLAYER_LIST[player_index_1][0]
        stacksize2 = PLAYER_LIST[player_index_2][0]

        if stacksize1 > stacksize2:
            lowerstack = stacksize2
        elif stacksize2 > stacksize1:
            lowerstack = stacksize1
        else:
            lowerstack = stacksize1

        betsize_rng = random.random()

        if betsize_rng <= 0.2:
            betsize = lowerstack * 0.15

        if 0.2 < betsize_rng <= 0.4:
            betsize = lowerstack * 0.3

        if 0.4 < betsize_rng <= 0.6:
            betsize = lowerstack * 0.45

        if 0.6 < betsize_rng <= 0.8:
            betsize = lowerstack * 0.6

        #if 0.8 < betsize_rng <= 1:
        else:   # changed this to 'else' to get rid of PyCharm warnings
            betsize = lowerstack

        # betsize = lowerstack # trying this out to see if players get properly eliminated

        # figure out who wins the hand. if hero is involved, make sure to use the weighted coin

        if PLAYER_LIST[player_index_1][1] != "HERO" and PLAYER_LIST[player_index_2][1] != "HERO":
            pot_winner = random.sample([player_index_1, player_index_2],1)[0]

        elif PLAYER_LIST[player_index_1][1] == "HERO":
            heroflip = random.random()
            if heroflip <= PLAYER_LIST[player_index_1][2]:
                pot_winner = player_index_1
            else:
                pot_winner = player_index_2

        #elif PLAYER_LIST[player_index_2][1] == "HERO":
        else:  # changed this to 'else' to get rid of PyCharm warnings
            heroflip = random.random()
            if heroflip <= PLAYER_LIST[player_index_2][2]:
                pot_winner = player_index_2
            else:
                pot_winner = player_index_1

        # subtract/add chips for the winner and loser of the hand
        # eliminate players
        if pot_winner == player_index_1:
            PLAYER_LIST[pot_winner][0] = PLAYER_LIST[pot_winner][0] + betsize
            PLAYER_LIST[player_index_2][0] = PLAYER_LIST[player_index_2][0] - betsize
            if PLAYER_LIST[player_index_2][0] == 0:
                del PLAYER_LIST[player_index_2]
                if len(PLAYER_LIST) % (NUMBER_OF_PLAYERS / 10) == 0:
                    hero_coin_weight = hero_coin_weight - 0.015
                    changed_coin = True

        if pot_winner == player_index_2:
            PLAYER_LIST[pot_winner][0] = PLAYER_LIST[pot_winner][0] + betsize
            PLAYER_LIST[player_index_1][0] = PLAYER_LIST[player_index_1][0] - betsize
            if PLAYER_LIST[player_index_1][0] == 0:
                del PLAYER_LIST[player_index_1]
                if len(PLAYER_LIST) % (NUMBER_OF_PLAYERS / 10) == 0:
                    hero_coin_weight = hero_coin_weight - 0.015
                    PLAYER_LIST[-1][2] = hero_coin_weight
                    changed_coin = True

        # check if hero got eliminated, if so see if he can rebuy, payout his price money if not
        if PLAYER_LIST[-1][1] != "HERO":
            if len(PLAYER_LIST) >= MAX_NUMBER_OF_PLAYERS_FOR_HERO_TO_REBUY:
                hero_profit = hero_profit - DEFAULT_BUY_IN
                PLAYER_LIST.append([DEFAULT_STACK_SIZE, "HERO", hero_coin_weight])
                prizepool = prizepool + DEFAULT_BUY_IN
                if changed_coin == True:
                    hero_coin_weight = hero_coin_weight + 0.015
            else:
                pos = bisect.bisect_right(DEFAULT_MILESTONES, len(PLAYER_LIST) + 1) # +1 because hero already got removed from the list
                payout = DEFAULT_PAYOUT_RATIOS[pos - 1]
                hero_profit = hero_profit + payout
                # return hero_profit

        # print(PLAYER_LIST)
        if changed_coin:
            print(i, len(PLAYER_LIST), hero_coin_weight, PLAYER_LIST[-1])

