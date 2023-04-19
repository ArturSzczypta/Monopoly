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
    def __init__(self, player_number, funds, Strategy=None):  
        self.name = 'Player ' + str(player_number)
        self.number = player_number
        self.funds = funds
        self.strategy = Strategy
        self.current_loc = 0
        self.bankrupt = False

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
        # buy = self.strategy.buy_or_not(self.details, player.current_loc)
        buy = True
        # in future checking funds will not be necessary
        if buy and self.funds >= field_list[self.current_loc].price:
            self.funds -= field_list[self.current_loc].price
            self.properties.append(field_list[self.current_loc])
            return True
        else:
            print('auction')
            return False
        
    def auction(self, field_number, current_bid):
        ''' Decide if auction or fold'''
        # decide if auction or fold
        # auction = self.strategy.auction(self.details, field_number, current_bid)
        auction = True
        if auction and self.funds >= current_bid + 10:
            return current_bid + 10
        else:
            print(str(self.name)+' fold')
            return 0

    def pay(self, payment, owner=None):
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
                # If still not enough funds, sell hotels
                for property in self.properties:
                    if property.status == 3 and houses > 3:
                        self.funds += property.buildinng_cost / 2
                        property.status = 2
                        houses -= 4
                        hotels += 1
                        if self.funds >= payment:
                            break
                    # If there are not enough houses, each hotel is worth 5 houses
                    if property.status == 3 and houses < 3:
                        self.funds += 5 * property.buildinng_cost / 2
                        property.status = 1
                        hotels += 1
                        if self.funds >= payment:
                            break

                # If still not enough funds, sell houses, then mortgage
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
                    # If still not enough funds, mortgage
                    for property in given_set:
                        self.funds += property.mortage(self)
                        if self.funds >= payment:
                            break
                if all(property.status == -1 for property in self.properties):
                    break
            # Evaluate if there is enough funds
            if self.funds > payment:
                self.funds -= payment
                if owner:
                    owner.funds += payment
            else:
                # If all properties mortgaged, return 'bancrupt'
                self.bankrupt = True
                print(str(self.name)+' is bancrupt')
                if owner:
                    owner.properties.extend(self.properties)
                    owner.funds += self.funds
                else:
                    for property in self.properties:
                        property.status = 0
                

            

def build_house(self, property):
    ''' Build house if strategy says so and it is possible'''
    # decide if auction or fold
    # auction = self.strategy.build_house(self.details, field_number, current_bid)
    buying = True
    if buying and self.funds >= property.buildinng_cost and houses > 0:
        self.funds -= property.buildinng_cost
        property.status += 0.25
        houses -= 1
        property.calculate_rent()
    
def build_hotel(self, property): 
    ''' Build hotel if strategy says so and it is possible'''
    # decide if auction or fold
    # auction = self.strategy.build_hotel(self.details, field_number, current_bid)
    buying = True
    if buying and self.funds >= property.buildinng_cost and hotels > 0:
        self.funds -= property.buildinng_cost
        property.status += 0.25
        hotels -= 1
        property.calculate_rent()

# Weights for strategy
prop_weights = [1, 1, 1] * 6
prop_auction = [1, 1, 1] * 6
prop_house = [1, 1, 1] * 6
prop_hotel = [1, 1, 1] * 6
prop_bargain = [1, 1, 1] * 6
                    

free_jail_cards = {'chance': True, 'chest': True}
class Game:
    def __init__(self, players_count, start_funds, strategy, prop_weights, prop_auction, prop_house, prop_hotel):
        self.players_count = players_count
        self.start_funds = start_funds
        self.players = [Player(num, start_funds, strategy) for num in range(1, players_count+1)]
        self.prop_weights = prop_weights
        self.prop_auction = prop_auction
        self.prop_house = prop_house
        self.prop_hotel = prop_hotel
        self.turn = 0
        self.players_rent = [] #0 - player, 1 - sum of rent, 2 - highest rent
        for player in self.players:
            sum_rent = sum([prop.rent for prop in player.properties if isinstance(prop, Property) and prop.set != 'Utility'])
            max_rent = max([prop.rent for prop in player.properties if isinstance(prop, Property) and prop.set != 'Utility'])
            self.players_rent.append([player.number, sum_rent, max_rent])
       
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
            self.move(player, throw[1])
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
            player.funds += 200
            player.current_loc = 0
        elif card == 2:
            player.funds += 200
            player.current_loc = 5
        elif card == 3:
            if player.current_loc > 7:
                player.funds += 200
            player.current_loc = 11
        elif card == 4:
            if player.current_loc == 36:
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
            # Move to nearest utility
            if player.current_loc in (7, 36):
                player.current_loc = 12
            else:
                player.current_loc = 28
        elif card == 9:
            # Move to nearest Rail station
            if player.current_loc == 7:
                player.current_loc = 15
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
            player.pay(15)
        elif card == 14:
            #Each player pays 50
            list_temp = [x for x in self.players if x != player]
            for players in list_temp:
                players.pay(50)
                player.funds += 50
        elif card == 15:
            #for each house pay 25, for hotels 100
            payment = 25 * player.house_count + 100 * player.hotels_count
            player.pay(payment)

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
            player.pay(50)
        elif card == 14:
            #Each player pays 50
            list_temp = [x for x in self.players if x != player]
            for players in list_temp:
                players.pay(50)
                player.funds += 50
        elif card == 15:
            #Each player pays 50
            list_temp = [x for x in self.players if x != player]
            for players in list_temp:
                players.pay(10)
                player.funds += 10
        elif card == 16:
            #for each house pay 25, for hotels 100
            payment = 40 * player.house_count + 115 * player.hotels_count
            player.pay(payment)

    def auctioning(self, location):
        ''' Auctioning property'''
        current_bid = 0
        while True:
            bidders = len(self.players)
            for given_player in self.players:
                temp_bid = given_player.auction(player.current_loc, current_bid)
                if temp_bid == 0:
                    bidders -= 1
                else:
                    current_bid = temp_bid
            if bidders == 1:
                break
        for given_player in self.players:
            temp_bid = given_player.auction(player.current_loc, current_bid)
            if temp_bid > 0:
                given_player.pay(current_bid)
                given_player.properties.append(field_list[player.current_loc])
                break
        
    def move(self, player, throw):
        ''' Move player on the board'''
        if player.current_loc + throw > 39:
            player.funds += 200
            player.current_loc = (player.current_loc + throw) - 40
        
        if player.current_loc == 4:
            # Income Tax
            player.pay(200)
        elif player.current_loc == 38:
            # Luxury Tax
            player.pay(100)
        elif player.current_loc == 30:
            # Go to Jail
            player.current_loc = 10
            player.turns_in_jail = 1
        elif player.current_loc in (2, 17, 33):
            # Community Chest
            player.chest_card(player)
            self.move(player, throw)
        elif player.current_loc in (7, 22, 36):
            # Chance
            player.chance_card(player)
            self.move(player, throw)
        elif player.current_loc in (0, 10, 20):
            # Free Parking
            pass
        elif field_list[player.current_loc].owner == 0:
            # Unbought property, buy or auction
            buy = player.buy_or_not()
            if not buy:
                self.auctioning(player.current_loc)
        elif field_list[player.current_loc].owner != player.number:
            # Pay rent
            for given_player in self.players:
                if field_list[player.current_loc].owner == given_player.number:
                    player.pay(field_list[player.current_loc].rent)

            
            

            
        

        