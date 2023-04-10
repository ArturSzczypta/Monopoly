''' Simulating a monopoly game, to test strategies''' 

import numpy as np
import random
from properties import Property, field_list

ITERATIONS = 10
#how manu TURNS there is
TURNS = 1
PLAYERS = 5
FUNDS = 2000
houses = 32
hotels = 12

#Supress scientific notation
np.set_printoptions(suppress=True)

def throw_dice():
    ''' Return result of throwing dice '''
    dice1 = random.randint(1,6)
    dice2 = random.randint(1,6)

    #If duble, return first value as one
    if dice1 == dice2:
        return (1,dice1+dice2)
    else:
        return (0,dice1+dice2)


class Player:
    def __init__(self, player_number, funds):  
        self.name = 'Player ' + str(player_number)
        self.number = player_number
        self.funds = funds
        self.current_loc = 0

        self.properties = []
        self.house_count = 0
        self.hotels_count = 0

        self.out_of_jail_cards = {'chance': False, 'chest': False}
        self.turns_in_jail = 0

        self.passed_start = 0
        self.turns_in_jail_count = 0

    def details(self):
        ''' Return all player attributes as a dictionary'''
        return vars(self)
        
    def use_card(self):
        ''' Use out of jail card if avaliable'''
        if self.out_of_jail_cards['chance']:
            self.out_of_jail_cards['chance'] = False
            free_jail_cards['chance'] = True
            return True
        elif self.out_of_jail_cards['chest']:
            self.out_of_jail_cards['chest'] = False
            free_jail_cards['chest'] = True
            return True
        return False

    def buy_or_not(self):
        ''' Decide if buy or auction'''
        # buy = strategy(self.details, player.current_loc)
        buy = True
        # in future checking funds will not be necessary
        if buy and self.funds >= field_list[self.current_loc].price:
            self.funds -= field_list[self.current_loc].price
            self.append(self.current_loc)
        else:
            return 'auction'
        
    def auction(self, field_number, current_bid):
        ''' Decide if auction or fold'''
        # decide if auction or fold
        # auction = strategy(self.details, field_number, current_bid)
        auction = True
        if auction:
            return current_bid + 1
        else:
            print('fold')

    def pay(self, payment):
        ''' Pay rent if player has enough funds'''
        if self.funds >= payment:
            self.funds -= payment
        else:
            while self.funds < payment:
                # Sort first by rent, acending
                self.properties = sorted(self.properties, key=lambda x: x.rent)
                # mortgage one property at a time, starting from not full sets
                for property in self.properties:
                    if property.status == 0:
                        self.funds += property.mortage(self)
                        if self.funds >= payment:
                            break
                # if still not enough funds, mortgage utilities
                for property in self.properties:
                    if property.set == 'Utility':
                        self.funds += property.mortage(self)
                        if self.funds >= payment:
                            break
                # if still not enough funds, mortgage stations
                for property in self.properties:
                    if property.set == 'Station':
                        self.funds += property.mortage(self)
                        if self.funds >= payment:
                            break
                # if still not enough funds, sell hotels
                for property in self.properties:
                    if property.status == 3 and houses > 3:
                        self.funds += property.buildinng_cost / 2
                        property.status = 2
                        houses -= 4
                        hotels += 1
                        if self.funds >= payment:
                            break
                # if still not enough funds, sell houses, then mortgage
                for property in self.properties:
                    given_set = [prop for prop in self.properties if prop.set == property.set]
                    max_status = 2
                    while any(prop.status > 1 for prop in given_set):
                        for prop in given_set:
                            if prop.status == max_status:
                                self.funds += prop.buildinng_cost / 2
                                prop.status -= 0.25
                                houses += 1
                                if self.funds >= payment:
                                    break
                        max_status -= 0.25
                    # if still not enough funds, mortgage
                    for property in given_set:
                        self.funds += property.mortage(self)
                        if self.funds >= payment:
                            break
                # if all properties mortgaged, return 'bancrupt'
                if self.funds < payment:
                    return 'bancrupt'


                    
free_jail_cards = {'chance': True, 'chest': True}
class Game:
    def __init__(self, players_count, start_funds):
        self.players_count = players_count
        self.start_funds = start_funds
        self.players = [Player(num, start_funds) for num in range(1, players_count+1)]
        self.turn = 0

    def turn(self):
        for player in self.players:
            self.player_throws(player)

    def player_throws(self, player):
        ''' Deals with player throwing the dice, going to and going out of jail'''
        doubles_count = 0
        while doubles_count < 3:
            throw = throw_dice()
            if player.turns_in_jail in range(1,4):
                if any(player.out_of_jail_cards.values()):
                    player.use_jail_card()
                    player.turns_in_jail = 0
                elif throw[0] == True:
                    player.turns_in_jail = 0
                else:
                    player.turns_in_jail += 1
                    break
            player.move(throw[1])
            if throw[0] == True:
                doubles_count += 1
            else:
                break
        if doubles_count == 3:
            player.current_loc = 10
            player.turns_in_jail = 1

    def record_turn(self, file_name):
        ''' Saves deteils of the turn to file'''
        turn_details = {'turn': self.turn}
        players = {player.details() for player in self.players}
        turn_details = turn_details.update(players)
        with open(file_name, 'a', encoding='utf-8') as file:
            file.write(turn_details + '\n')

    def bankrupcy(self, player):
        ''' Delete player once bankrupt'''
        self.players.remove(player)
    
    #field 7,22,36
    def chance_card(self, player):
        ''' Pick chance card'''
        if free_jail_cards['chance']:
            card = random.randint(0,16)
        else:
            card = random.randint(1,16)
        if card == 0:
            player.out_of_jail_cards['chance'] = True
            free_jail_cards['chance'] = False
        elif card == 1:
            player.current_loc = 0
            player.funds += 200
        elif card == 2:
            if player.current_loc > 5:
                player.funds += 200
            player.current_loc = 5
        elif card == 3:
            if player.current_loc > 11:
                player.funds += 200
            player.current_loc = 11
        elif card == 4:
            if player.current_loc > 24:
                player.funds += 200
            player.current_loc = 24
        elif card == 5:
            player.current_loc = 39
        elif card == 6:
            player.current_loc = 10
            player.turns_in_jail = 1
        elif card == 7:
            player.current_loc -= 3
        elif card == 8:
            # Utility
            if player.current_loc in (7, 36):
                player.current_loc = 12
            #buy or pay 10 times the dice thrown!!!!!!!!
            else:
                player.current_loc = 28
            #buy or pay 10 times the dice throw!!!!!!!!
        elif card == 9:
            # Rail station
            #nearest rail station
            if player.current_loc == 7:
                player.current_loc = 10
            elif player.current_loc == 22:
                player.current_loc = 25
                #buy or pay 2 times more!!!!!!!!
            else:
                player.current_loc = 5
                #buy or pay 2 times more!!!!!!!
        elif card == 10:
            player.funds += 150
        elif card == 11:
            player.funds += 100
        elif card == 12:
            player.funds += 50
        elif card == 13:
            player.funds -= 15
        elif card == 14:
            #Each player pays 50
            list_temp = [x for x in self.players if x != player]
            for players in list_temp:
                players.funds -= 50
                player.funds += 50
        elif card == 15:
            #for each house pay 25, for hotels 100
            house_count = 0
            hotels_count = 0
            players.funds -= 25*house_count + 100*hotels_count

    #field 2,17,33
    def chest_card(self, player):
        ''' Pick chest card'''
        if free_jail_cards['chest']:
            card = random.randint(0,17)
        else:
            card = random.randint(1,17)
        if card == 0:
            player.out_of_jail_cards['chance'] = True
            free_jail_cards['chance'] = False
        elif card == 1:
            player.current_loc = 0
            player.funds += 200
        elif card == 2:
            player.current_loc = 10
            player.turns_in_jail = 1
        elif card == 3:
            player.funds += 200
        elif card in range(4,7):
            player.funds += 100
        elif card == 7:
            player.funds += 50
        elif card == 8:
            player.funds += 25
        elif card == 9:
            player.funds += 20
        elif card == 10:
            player.funds += 10
        elif card in range(11,14):
            player.funds -= 50
        elif card == 14:
            #Each player pays 50
            list_temp = [x for x in self.players if x != player]
            for players in list_temp:
                players.funds -= 50
                player.funds += 50
        elif card == 15:
            #Each player pays 50
            list_temp = [x for x in self.players if x != player]
            for players in list_temp:
                players.funds -= 10
                player.funds += 10
        elif card == 16:
            #for each house pay 25, for hotels 100
            house_count = 0
            hotels_count = 0
            players.funds -= 40 * house_count + 115 * hotels_count

    def move(player, throw):
        ''' Move player on the board'''
        if player.current_loc + throw > 39:
            player.funds += 200
            player.current_loc = (player.current_loc + throw) - 40
        
        if player.current_loc == 4:
            # Income Tax
            player.funds -= 200
        elif player.current_loc == 38:
            # Luxury Tax
            player.funds -= 100
        elif player.current_loc == 30:
            # Go to Jail
            player.current_loc = 10
            player.turns_in_jail = 1
        elif player.current_loc in (2, 17, 33):
            # Community Chest
            player.chest_card(player)
        elif player.current_loc in (7, 22, 36):
            # Chance
            player.chance_card(player)
        else:
            # Buy or pay rent
            player.buy_or_pay_rent(player)
        

        