import csv

# Create list of all fields
fields = [None] * 40
fields[0] = 'Start'
fields[10] = 'Jail'
fields[20] = 'Free Parking'
fields[30] = 'Go to Jail'
fields[2] = 'Community Chest'
fields[17] = 'Community Chest'
fields[33] = 'Community Chest'
fields[7] = 'Chance'
fields[22] = 'Chance'
fields[36] = 'Chance'
fields[4] = 'Income Tax'
fields[38] = 'Luxury Tax'

# Save properties.csv content list of dictionaries
with open('properties.csv') as file:
    reader = csv.DictReader(file)
    for row in reader:
        row_dict = {header: value for header, value in row.items()}
        #print(row_dict['number'])
        fields[int(row_dict['number'])] = row_dict

'''
for field in fields:
    print(type(field))
    if isinstance(field, dict):
        print(field['number'])
    else:
        print(field)
    print('-' * 20)
'''

class Property:
    def __init__(self, number, names, set, in_set, price, mortgage, rent, buildinng_cost, house_1, houses_2, houses_3, houses_4, hotel):
        self.number = number
        self.names = names
        self.set = set
        self.in_set = in_set
        self.price = price
        self.mortgage = mortgage
        self.rent = rent
        self.buildinng_cost = buildinng_cost
        self.house_1 = house_1
        self.houses_2 = houses_2
        self.houses_3 = houses_3
        self.houses_4 = houses_4
        self.hotel = hotel
        self.vriant = 1

    def details(self):
        ''' Return all property attributes as a dictionary'''
        return vars(self)
    
    def buy(self, player):
        '''Buy property if player has enough funds'''
        if self.price <= player.funds:
            self.owner = player.number
            player.funds -= self.price
    
    def change_owner(self, player, buyer):
        '''Change property owner'''
        if self.owner == player.number:
            self.owner = buyer.number
            player.properties -= 1
            buyer.properties += 1
        else:
            print('unable to change owner')
    
    def morgage(self, player):
        '''Morgage property if player has enough funds'''
        if self.variant != -1:
            self.variant = -1
            player.funds += self.mortgage
        else:
            player('unable to morgage')
    
    def unmorgage(self, player):
        '''Unmorgage property if player has enough funds'''
        if self.variant == -1 and player.funds >= self.mortgage:
            self.variant = 0
            player.funds -= self.mortgage
        else:
            print('unable to unmorgage')
