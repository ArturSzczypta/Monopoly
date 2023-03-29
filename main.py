'''
Simulating a monopoly game, to test strategies
''' 

import os
import sys
import numpy as np
import random
import pandas as pd


ITERATIONS = 10
#how manu TURNS there is
TURNS = 1
PLAYERS = 5
FUNDS = 2000

#Supress scientific notation
np.set_printoptions(suppress=True)

player_list = []


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
    def __init__(self, player_number, current_loc=0, money=FUNDS):
        
        self.palyer_number = player_number
        self.current_loc = current_loc
        self.money = money

        self.properties = 0

        self.out_of_jail_cards = {'chance': False, 'chest': False}
        self.in_jail = 0

        self.passed_start = 0
        self.in_jail_count = 0

    def move(self,val):
        '''
        Change location based on input (dices or cards)

        '''
        self.current_loc =+ val
        if self.current_loc > 39:
            self.current_loc = 40 - self.current_loc
            self.money += 200

        elif  self.current_loc < 0:
            self.current_loc = 40 + self.current_loc

        # Go to jail field
        if self.current_loc == 30:
            self.current_loc = 10
            self.in_jail = 1
        

    def use_card(self):
        '''
        Use out of jail card if avaliable
        '''
        if self.out_of_jail_cards('chance'):
            self.out_of_jail_cards('chance') = False
            free_jail_cards('chance') = True
            return True
        elif:
            self.out_of_jail_cards('chest') = False
            free_jail_cards('chest') = True
            return True
        return False


def player_throw(player):
    '''
    Deals with player throwing the dice, going to and going out of jail
    '''
    doubles_count = 0
    while doubles_count < 3:
        throw = throw_dice()
        if player.in_jail in range(1,4):
            if not player.use_card:
                throw[0] == False:
                player.in_jail += 1
                break
        player.move(throw[1])
        if throw[0] == True:
            doubles_count += 1
        else:
            break
    if doubles_count == 3:
        player.current_loc = 10
        player.in_jail = 1

# Setting out of jail 
free_jail_cards = {'chance': True, 'chest': True}
#field 7,22,36
def chance_card(has_jail_card=True):
    '''
    Pick chance card
    '''
    if free_jail_cards('chance'):
        card = random.randint(0,16)
    else:
        card = random.randint(1,16)
    if card == 0:
        player.out_of_jail_cards('chance') = True
        free_jail_cards('chance') = False
    elif card == 1:
        player.current_loc = 0
        player.money += 200
    elif card == 2:
        if player.current_loc > 5:
            player.money += 200
        player.current_loc = 5
    elif card == 3:
        if player.current_loc > 11:
            player.money += 200
        player.current_loc = 11
    elif card == 4:
        if player.current_loc > 24:
            player.money += 200
        player.current_loc = 24
    elif card == 5:
        player.current_loc = 39
    elif card == 6:
        player.current_loc = 10
        player.in_jail = 1
    elif card == 7:
        player.current_loc -= 3
    elif card == 8:
        if player.current_loc < 20:
           player.current_loc = 12
           #buy or pay 10 times the dice thrown!!!!!!!!
        else:
           player.current_loc = 28
           #buy or pay 10 times the dice throw!!!!!!!!
    elif card == 9:
        if player.current_loc == 7:
           player.current_loc = 5
           #buy or pay 2 times more!!!!!!!!
        elif player.current_loc == 22:
           player.current_loc = 25
           #buy or pay 2 times more!!!!!!!!
        else:
            player.current_loc = 35
            #buy or pay 2 times more!!!!!!!
    elif card == 10:
        player.money += 150
    elif card == 11:
        player.money += 100
    elif card == 12:
        player.money += 50
    elif card == 13:
        player.money -= 15
    elif card == 14:
        #Each player pays 50
        list_temp = [x for s in player_list if x != player]
        for players in list_temp:
            players.money -= 50
            player.money += 50
    elif card == 15:
        #for each house pay 25, for hotels 100
        house_count = 0
        hotels_count = 0
        players.money -= 25*house_count + 100*hotels_count

#field 17,33
def chest_card(has_jail_card=True):
    '''
    Pick chest card
    '''
    if free_jail_cards('chest'):
        card = random.randint(0,17)
    else:
        card = random.randint(1,17)
    if card == 0:
        player.out_of_jail_cards('chance') = True
        free_jail_cards('chance') = False
    elif card == 1:
        player.current_loc = 0
        player.money += 200
    elif card == 2:
        player.current_loc = 10
        player.in_jail = 1
    elif card == 3:
        player.money += 200
    elif card in range(4,7)
        player.money += 100
    elif card == 7:
        player.money += 50
    elif card == 8:
        player.money += 25
    elif card == 9:
        player.money += 20
    elif card == 10:
        player.money += 10
    elif card in range(11,14)
        player.money -= 50
    elif card == 14:
        #Each player pays 50
        list_temp = [x for s in player_list if x != player]
        for players in list_temp:
            players.money -= 50
            player.money += 50
    elif card == 16:
        #Each player pays 50
        list_temp = [x for s in player_list if x != player]
        for players in list_temp:
            players.money -= 10
            player.money += 10
    elif card == 16:
        #for each house pay 25, for hotels 100
        house_count = 0
        hotels_count = 0
        players.money -= 40*house_count + 115*hotels_count
