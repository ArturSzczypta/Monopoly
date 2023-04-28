# Weights for strategy
'''
input:
player
other_players = player_list.pop(player)
property

max_rent = max([oponent.max_rent for oponent in other_players])
sum_rent = sum([oponent.sum_rent for oponent in other_players])
max_funds = max([oponent.funds for oponent in other_players])
min_funds = min([oponent.funds for oponent in other_players])

funds = player.funds
property_current_rent = property.rent
property_possible_rent = calculate_rent(property)

def calculate_rent(self, property):
    assumes itis not railroad or utility
    if property.status == 1:
        property_possible_rent = property.house_1
    elif property.status == 1.25:
        property_possible_rent = property.house_2
    elif property.status == 1.5:
        property_possible_rent = property.house_3
    elif property.status == 1.75:
        property_possible_rent = property.house_4
    elif property.status == 2:
        property_possible_rent = property.hotel
    else:
        property_possible_rent = property.rent

sets = ['Brown', 'Till', 'Pink', 'Orange', 'Red', 'Yellow',
'Green', 'Blue', 'Station', 'Utility']
sets_weight = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

prop_weights = [1, 1, 1] * 6
prop_auction = [1, 1, 1] * 6
prop_house = [1, 1, 1] * 6
prop_hotel = [1, 1, 1] * 6
prop_bargain = [1, 1, 1] * 6
'''