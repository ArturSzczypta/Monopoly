'''
Simulating a monopoly game, to test strategies
''' 

import os
import sys
import numpy as np
import random
import pandas as pd


cycles = 10
#how manu turns there is
turns = 1
players = 5

#Supress scientific notation
np.set_printoptions(suppress=True)


def throw_dice():
    '''
    Return result of throwing dice
    '''
    dice1 = random.randint(1,6)
    dice2 = random.randint(1,6)

    #If duble, return first value as one
    if dice1 == dice2:
        return (1,dice1+dice2)
    else:
        return (0,dice1+dice2)

#dictionary of fields
properties_dict = {'number':None, # From 0 to 39
'owner':None, # player number
'type':None, # street, railroad, utilities
'price':None, # price to buy
'variant':None, # 0 - single, 1 - full set, 0.5 - two railroads, 0.75 - three railroads,
# 1,25 - one house, 1.5 - two houses, 1.75 - three houses, 2 - four houses, 3 - hotel
# -1 - morgage
'bill': None}


class Player:
    def __init__(self,current_loc=0):
        self.current_loc = current_loc
        self.properties = 0
        self.rounds_count = 0
        self.got_double = 0

    def move(val):
        self.current_loc =+ val
        if self.current_loc > 39:
            self.current_loc = 40 - self.current_loc
            self.rounds_count += 1
        elif  self.current_loc < 0:
            self.current_loc = 40 + self.current_loc

    def make_decission(dice_roll):
        self.move(dice_roll[1])









# board single cycle
game_owning = np.zeros((cycles,turns,40)).astype(int)
game_landing = np.zeros((cycles,turns,40)).astype(int)

# change all unbuyable positions to -1, so that they are not buyed
special_ones = [0,2,4,7,10,17,20,22,30,33,36,38]
owned_simple = np.zeros((cycles,40))
game_landing = np.zeros((cycles,turns,40)).astype(int)

# change all unbuyable positions to -1, so that they are not buyed
special_ones = [0,2,4,7,10,17,20,22,30,33,36,38]
for c in range(cycles):
    for i in special_ones:
        # https://stackoverflow.com/a/28952971/5531122
        #game_owning[::,i] = -1
        owned_simple[c][i] = -1
#print(owned_simple)

for c in range(cycles):
    
    # For each player: 0 - player number, 1 - position on board, 2 - turns in jail,
    # 3 - free out of jail cards, 4 - passed Start count
    all_players = np.zeros((players,5)).astype(int)

    for i in range(players):
        all_players[i][0] = i+1
    #print(all_players)

    # are out of jail cards avaliable
    aval_chance_card = 1
    aval_chest_card = 1
    card = 0

    # current turn
    c_turn = 0
    thrown_double = 0
    while c_turn < turns:
        for i in range(players):
            #print(all_players[i])
            thrown_double = 0

            while thrown_double < 4:
                move = throw_dice()
                #print(move)
                #not in jail
                if all_players[i][2] == 0:
                    all_players[i][1] += move[1]    

                # in jail
                elif all_players[i][2] > 0:
                    # in jail and thrown double
                    if move[0] == 1:
                        all_players[i][1] += move[1]
                        all_players[i][2] = 0
                        #when going out of jail you don't throw twice although you had double
                        move[0] = 0
                        #print('double - out of jail')
                    else:
                        # in jail, not thrown double, has a card
                        if all_players[i][3] > 0:
                            all_players[i][1] += move[1]
                            all_players[i][3] -= 1
                            all_players[i][2] = 0
                            #print('give card')

                            #getting back cards
                            if aval_chest_card == 0:
                                aval_chest_card = 1
                            else:
                                aval_chance_card = 1
                        # in jail, not thrown double, has no card, less than 3 turns
                        elif all_players[i][3] == 0 and all_players[i][2] < 3:
                            all_players[i][2] += 1
                            #print('stuck in jail')
                        # it's three turns, going out anyway
                        else:
                            all_players[i][1] += move[1]
                            all_players[i][2] = 0
                            #print('out of jail')

                # if thrown double trice you end up in jail
                if move[0] == 0:
                    thrown_double = 4
                else:
                    thrown_double += 1
                    move = throw_dice()
                    if thrown_double == 3:
                        all_players[i][1] = 30
                        all_players[i][2] = 1
                        game_landing[c][c_turn][30] += 1
                        thrown_double = 4
                        #print('three doubles - go to jail')

                if all_players[i][2] == 0:

                    #passing Start
                    if all_players[i][1] > 39:
                        all_players[i][1] = all_players[i][1] - 40
                        all_players[i][4] += 1

                    #print(all_players[i][1])
                    game_landing[c][c_turn][all_players[i][1]] += 1

                    # comunity chests
                    # https://stackoverflow.com/a/15112149/5531122
                    if all_players[i][1] in (2,17,33):
                        #print('chest')
                        if aval_chest_card == 1:
                            card = random.randint(1,17)
                        else:
                            card = random.randint(1,16)

                        # go to start
                        if card == 1:
                            all_players[i][1] = 0
                            all_players[i][4] += 1

                        # go to jail
                        elif card == 2:
                            all_players[i][1] = 30
                            all_players[i][2] = 1
                            game_landing[c][c_turn][30] += 1
                            thrown_double = 4

                        # get out of jail card
                        elif card == 17:
                            all_players[i][3] += 1
                            aval_chest_card = 0
                            #print('chest card')

                    # chance
                    # https://stackoverflow.com/a/15112149/5531122
                    if all_players[i][1] in (7,22,36):
                        #print('chance')
                        if aval_chance_card == 1:
                            card = random.randint(1,16)
                        else:
                            card = random.randint(1,15)

                        # go to start
                        if card == 1:
                            all_players[i][1] = 0
                            all_players[i][4] += 1

                        # go to jail
                        elif card == 2:
                            all_players[i][1] = 30
                            all_players[i][2] = 1
                            game_landing[c][c_turn][30] += 1
                            thrown_double = 4
                        
                        # King's Cross Station
                        elif card == 3:
                            all_players[i][1] = 5
                            game_landing[c][c_turn][5] += 1

                        # Pall Mall (orange)
                        elif card == 4:
                            all_players[i][1] = 11
                            game_landing[c][c_turn][11] += 1

                        # Trafalgar Square (red)
                        elif card == 5:
                            all_players[i][1] = 24
                            game_landing[c][c_turn][24] += 1

                        # Mayfair (cyan)
                        elif card == 6:
                            all_players[i][1] = 39
                            game_landing[c][c_turn][39] += 1

                        # go back 3 places
                        elif card == 7:
                            all_players[i][1] -= 3
                            game_landing[c][c_turn][all_players[i][1]] += 1

                        # Nearest Utility
                        elif card == 8:
                            #print('utility')
                            if all_players[i][1] < 12 and all_players[i][1] > 28:
                                all_players[i][1] = 12
                                game_landing[c][c_turn][12] += 1
                            else:
                                all_players[i][1] = 28
                                game_landing[c][c_turn][28] += 1

                        # Nearest Train station
                        elif card == 9:
                            #print('train')
                            if all_players[i][1] < 5 and all_players[i][1] > 35:
                                all_players[i][1] = 5
                                game_landing[c][c_turn][5] += 1
                            elif all_players[i][1] > 5 and all_players[i][1] < 15:
                                all_players[i][1] = 15
                                game_landing[c][c_turn][15] += 1
                            elif all_players[i][1] > 15 and all_players[i][1] < 25:
                                all_players[i][1] = 25
                                game_landing[c][c_turn][25] += 1
                            else:
                                all_players[i][1] = 35
                                game_landing[c][c_turn][35] += 1

                        # get out of jail card
                        elif card == 16:
                            all_players[i][3] += 1
                            aval_chance_card = 0
                            #print('chance card')

                    # landing on go to jail
                    if all_players[i][1] == 10:
                        all_players[i][1] = 30
                        all_players[i][2] = 1
                        game_landing[c][c_turn][30] += 1
                        thrown_double = 4
                        #print('go to jail')

                    # take if free to buy - first 
                    if owned_simple[c][all_players[i][1]] == 0:
                        owned_simple[c][all_players[i][1]] = i+1
                        game_owning[c][c_turn][all_players[i][1]] = i+1
                #print(all_players[i])
            #print(all_players[i])

            #print('-----------------')
        #print('--------------------------------------------------')
        c_turn += 1
    '''
    print(owned_simple[c])
    print('--------------------------------------------------')
    print(game_owning[c])
    print('--------------------------------------------------')
    print(game_landing[c])
    '''
'''
#print(np.zeros((6,turns,40)).astype(int))
print('--------------------------------------------------')
print('--------------------------------------------------')
print('--------------------------------------------------')
print(owned_simple)
print('--------------------------------------------------')
print(game_owning)
print('--------------------------------------------------')
print(game_landing)


print('--------------------------------------------------')
print('--------------------------------------------------')
print('--------------------------------------------------')
'''
x = 0
landing_simple = np.zeros(40)
#print(landing_simple)
for i in game_landing:
    for j in i:
        #print('----------------')
        #print(j)
        x+= 1
        landing_simple += j
        #print(landing_simple)

print(landing_simple)
print('in %')
tot = np.sum(landing_simple)
print(tot)
landing_simple = landing_simple / tot * 100
print(landing_simple)
aver = np.average(landing_simple)
print(landing_simple - aver)
